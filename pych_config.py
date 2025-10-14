import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QStyle
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, Qt, QThread, QProcess, QTimer
from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QLineEdit, QFileDialog

import json

import qdarktheme

import subprocess
import subprocess, os
from PySide6.QtCore import QTimer
import threading


CFG_PATH = os.path.join(os.path.dirname(__file__), "config/pych-gui.cfg")
with open(CFG_PATH, "r") as f:
    CFG = json.load(f)


def load_ui(path: str):
    ui_file = QFile(path)
    if not ui_file.open(QIODevice.ReadOnly):
        raise FileNotFoundError(f"No se puede abrir el archivo .ui: {path}")
    loader = QUiLoader()
    widget = loader.load(ui_file)
    ui_file.close()
    if widget is None:
        raise RuntimeError(f"No se pudo cargar la interfaz desde: {path}")
    return widget


class UIConfigWindow:

    def __init__(self, ui_path: str | None = None, stylesheet: str = "light"):
        self.ui_path = ui_path 

        self.app = QApplication(sys.argv)

        try:
            self.app.setStyleSheet(qdarktheme.load_stylesheet(stylesheet))
        except Exception:
            pass

        self.window = None

    def load(self):
        """Carga el archivo .ui y guarda el widget en self.window."""
        widget = load_ui(self.ui_path)
        print(type(widget))

        # Si el .ui define un QMainWindow, úsalo tal cual para evitar anidar ventanas.
        if isinstance(widget, QMainWindow):
            self.window = widget
        else:
            # Si el .ui devuelve otro tipo de widget (QWidget), lo colocamos
            # como central widget dentro de un QMainWindow.
            main = QMainWindow()
            main.setCentralWidget(widget)
            self.window = main

        self.J = {}
        self.reloadTimes = 0

        self.add_ui_controls(None)

        return self.window

    def show(self):
        """Muestra la ventana (la carga antes si no está cargada)."""
        if self.window is None:
            self.load()
        self.window.show()

    def run(self):
        self.show()
        return self.app.exec()
    
    def add_ui_controls(self, controller):
            
        if self.window is None:
            self.load()
        
        if self.window.btn_apply is not None:
            self.window.btn_apply.clicked.connect(self.btn_apply_clicked)
        
        json_file = CFG.get("LAST_CONFIG_FILE", "config/activate.json")
        with open(json_file,'r') as f:
            self.J = json.load(f)

        s = self.app.style()
        self.ico = s.standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder)

        for i in range(1,2):
            obj = getattr(self.window, f"ed_CONFIG_FILE", None)
            if obj is not None:
                obj.setText(json_file)
                action_buscar = QAction(self.ico, "Buscar", self.window)
                obj.addAction(action_buscar,QLineEdit.ActionPosition.TrailingPosition)
                action_buscar.triggered.connect(lambda checked, key="#CONFIG_FILE", obj=obj: self.on_browse(key, obj, type="file", opts="JSON Files (*.json)"))

                def on_text_changed(text):
                    CFG["LAST_CONFIG_FILE"] = text
                    with open(CFG_PATH, "w") as f:
                        json.dump(CFG, f, indent=4)
                    self.log(f"Configuration file changed to {text}")
                    
                    try:
                        with open(text,'r') as f:
                            self.J.clear()
                            self.J.update(json.load(f))
                            self.J["#CONFIG_FILE"] = text

                        for key in self.J:
                            obj = getattr(self.window, f"ed_{key}", None)
                            if obj is not None:
                                obj.setText(self.J[key])
                    except Exception as e:
                        self.log(f"Error loading configuration file: {e}")


                obj.returnPressed.connect(lambda obj=obj: on_text_changed(obj.text()))
                action_buscar.triggered.connect(lambda checked, obj=obj: on_text_changed(obj.text()))
                break

        for key in self.J.get("_IS_FOLDER", []):
            obj = getattr(self.window, f"ed_{key}", None)
            if obj is not None:
                action_buscar = QAction(self.ico, "Buscar", self.window)
                obj.addAction(action_buscar,QLineEdit.ActionPosition.TrailingPosition)
                action_buscar.triggered.connect(lambda checked, key=key, obj=obj: self.on_browse(key, obj, type="folder",opts="*.*"))

        for key in self.J.get("_IS_FILE", []):
            obj = getattr(self.window, f"ed_{key}", None)
            if obj is not None:
                action_buscar = QAction(self.ico, "Buscar", self.window)
                obj.addAction(action_buscar,QLineEdit.ActionPosition.TrailingPosition)
                action_buscar.triggered.connect(lambda checked, key=key, obj=obj: self.on_browse(key, obj, type="file"))


        for key in self.J:
            obj = getattr(self.window, f"ed_{key}", None)
            if obj is not None:
                obj.setText(self.J[key])
                obj.textChanged.connect(lambda text, k=key: self.J.update({k: text}))

        if self.window.btn_ping is not None:
            self.window.btn_ping.clicked.connect(self.btn_ping_clicked)
        
        if self.window.btn_mount is not None:
            self.window.btn_mount.clicked.connect(self.btn_mount_clicked)

        self.mount_timer = QTimer(self.window)
        self.mount_timer.timeout.connect(self.check_mount_status)
        self.mount_timer.setSingleShot(False)
        self.mount_timer.singleShot(1000, self.check_mount_status)
        self.mount_timer.start(10000)

        self.ping_timer = QTimer(self.window)
        self.ping_timer.timeout.connect(self.check_ping_status)
        self.ping_timer.setSingleShot(False)
        self.ping_timer.singleShot(2000, self.check_ping_status)
        self.ping_timer.start(10000)

        self.window.btn_remote_build.clicked.connect(self.btn_remote_build_clicked)
        self.window.btn_remote_build_plugins.clicked.connect(self.btn_remote_build_plugins_clicked)

        self.window.btn_remote_update_files.clicked.connect(self.btn_remote_update_files_clicked)

        self.window.btn_stop.clicked.connect(self.btn_stop_clicked)
        self.window.btn_start.clicked.connect(self.btn_start_clicked)

        pass

    def btn_start_clicked(self):
        if self.window is None:
            self.load()

        if getattr(self.window, "led_running", None) is not None:
            self.window.led_running.setStyleSheet("color: green;")

        program = "bash"
        arguments = [
            "-c",
            f"source {self.get_activate_sh_path()} && cd {self.J['PYCH_CORE_WORK']} && ./scripts/remote.sh start"
        ]

        self.log("Remote start command started.")
        print("Executing:", program, " ".join(arguments))

        self.start_process = QProcess(self.window)
        self.start_process.start(program, arguments)
        self.start_process.finished.connect(self.on_start_finished)
        # self.start_process.waitForFinished(5000)
        self.log("Remote start command finished.")

    def on_start_finished(self):
        print("Remote start finished. Exit code:", self.start_process.exitCode())
        if getattr(self.window, "led_running", None) is not None:
            if self.start_process.exitCode() == 0:
                self.window.led_running.setStyleSheet("color: orange;")
                res = self.start_process.readAllStandardOutput().data().decode()
                self.log("Remote start succeeded.")
                print(res)  
            else:
                self.window.led_running.setStyleSheet("color: red;")
                self.log("Remote start failed.")
                if self.start_process.readAllStandardOutput().data().decode().strip()!="":
                    self.log(self.start_process.readAllStandardOutput().data().decode())
                if self.start_process.readAllStandardError().data().decode().strip()!="":
                    self.log(self.start_process.readAllStandardError().data().decode())

    def btn_stop_clicked(self):
        if self.window is None:
            self.load()

        program = "bash"
        arguments = [
            "-c",
            f"source {self.get_activate_sh_path()} && cd {self.J['PYCH_CORE_WORK']} && ./scripts/remote.sh stop"
        ]

        self.log("Remote stop command started.")
        print("Executing:", program, " ".join(arguments))

        self.stop_process = QProcess(self.window)
        self.stop_process.start(program, arguments)
        self.stop_process.waitForFinished(5000)
        self.log("Remote stop command finished.")

            

    def btn_remote_update_files_clicked(self):
        if self.window is None:
            self.load()
    
        program = "bash"
        arguments = [
            "-c",
            f"source {self.get_activate_sh_path()} && cd {self.J['PYCH_CORE_WORK']} && ./scripts/remote.sh copy"
        ]

        print("Executing:", program, " ".join(arguments))
        self.log("Remote update files started.")
        # return

        self.update_files_process = QProcess(self.window)
        self.update_files_process.start(program, arguments)
        self.update_files_process.waitForFinished(5000)
        self.log("Remote update files finished.")
        res = self.update_files_process.readAllStandardOutput().data().decode()
        self.log(res)
        err = self.update_files_process.readAllStandardError().data().decode()
        if err.strip()!="":
            self.log(err)

    def btn_remote_build_plugins_clicked(self):
        if self.window is None:
            self.load()
        
        if getattr(self.window, "led_remote_build_plugins", None) is not None:
            self.window.led_remote_build_plugins.setStyleSheet("color: orange;")

        if self.J.get("EXTERNAL_PLUGIN_PATH", [])==[]:
            self.log("No EXTERNAL_PLUGIN_PATH defined in config/activate.json")
            if getattr(self.window, "led_remote_build_plugins", None) is not None:
                self.window.led_remote_build_plugins.setStyleSheet("color: red;")
            return
        

        self.plugins_build_process = []
        for p in self.J["EXTERNAL_PLUGIN_PATH"]:
            pass

            program = "bash"
            arguments = [
                "-c",
                f"source {self.get_activate_sh_path()} && cd {p} && ./build.sh {self.J.get('REMOTE_ARCH','aarch64-unknown-linux-gnu')}"
            ]
            print("Executing:", program, " ".join(arguments))
            self.log(f"Remote build plugins started. {p}")

            self.plugins_build_process.append(QProcess(self.window))
            self.plugins_build_process[-1].finished.connect(lambda exitCode, exitStatus, p_path=p: self.on_remote_build_plugins_finished(self.plugins_build_process[-1], p_path))
            self.plugins_build_process[-1].start(program, arguments)

    def on_remote_build_plugins_finished(self,my_process=None,p_path=None):
        print("Remote build plugins finished. Exit code:", my_process.exitCode())
        if getattr(self.window, "led_remote_build_plugins", None) is not None:
            if my_process.exitCode() == 0:
                self.window.led_remote_build_plugins.setStyleSheet("color: green;")
                res = my_process.readAllStandardOutput().data().decode()
                self.log(f"Remote build plugins succeeded. {p_path}")
                print(res)

            else:
                self.window.led_remote_build_plugins.setStyleSheet("color: red;")
                self.log(my_process.readAllStandardOutput().data().decode())
                self.log(my_process.readAllStandardError().data().decode())
                self.log(f"Remote build plugins failed. {p_path}")

    def btn_remote_build_clicked(self):
        if self.window is None:
            self.load()
        
        if getattr(self.window, "led_remote_build", None) is not None:
            self.window.led_remote_build.setStyleSheet("color: orange;")

        program = "bash"
        arguments = [
            "-c",
            f"source {self.get_activate_sh_path()} && cd {self.J['PYCH_CORE_WORK']} && {self.J['PYCH_CORE_WORK']}/scripts/remote.sh build {self.J.get('REMOTE_ARCH','aarch64-unknown-linux-gnu')}"
        ]

        print("Executing:", program, " ".join(arguments))
        self.log("Remote Core build started.")
        # return

        self.build_process = QProcess(self.window)
        self.build_process.finished.connect(self.on_remote_build_finished)
        self.build_process.start(program, arguments)

    def on_remote_build_finished(self):
        print("Remote build finished. Exit code:", self.build_process.exitCode())
        if getattr(self.window, "led_remote_build", None) is not None:
            if self.build_process.exitCode() == 0:
                self.window.led_remote_build.setStyleSheet("color: green;")
                res = self.build_process.readAllStandardOutput().data().decode()
                print(res)  
                self.log("Remote Core build succeeded.")

            else:
                self.window.led_remote_build.setStyleSheet("color: red;")
                self.log("Remote build failed.")
                self.log(self.build_process.readAllStandardOutput().data().decode())
                self.log(self.build_process.readAllStandardError().data().decode())

    def check_ping_status(self):
        if self.window is None:
            self.load()
        
        if getattr(self.window, "led_ping", None) is not None:
            self.btn_ping_clicked()
        
        return True

    def check_mount_status(self):
        if self.window is None:
            self.load()
        
        if getattr(self.window, "led_mount", None) is not None:
            if self.remote_is_mounted():
                self.window.led_mount.setStyleSheet("color: green;")
            else:
                self.window.led_mount.setStyleSheet("color: red;")
        
        return True

    def remote_is_mounted(self):
        cmd = ["bash" , "-c" , f"source {self.get_activate_sh_path()} &&  {self.J['PYCH_CORE_WORK']}/scripts/remote.sh ismnt"]
        sp = QProcess(self.window)
        sp.start(cmd[0], cmd[1:])
        sp.waitForFinished(5000)
        output = sp.readAllStandardOutput().data().decode().strip()
        error = sp.readAllStandardError().data().decode().strip()
        sp.exitCode()
        print("Command:", " ".join(cmd))
        print("Output:", output)
        print("Error:", error)
        print("Exit Code:", sp.exitCode())
        return sp.exitCode()==0

    def btn_mount_clicked(self):

        if self.window is None:
            self.load()
        
        if getattr(self.window, "led_mount", None) is not None:
            self.window.led_mount.setStyleSheet("color: orange;")

        if self.remote_is_mounted():
            if getattr(self.window, "led_mount", None) is not None:
                self.window.led_mount.setStyleSheet("color: green;")
            print("Already mounted.")
            self.remote_umount()
            return

        program = "sshfs"
        arguments = [
            "-o","ConnectTimeout=5",
            f"{self.J.get('REMOTE_USER', 'pi')}@{self.J.get('REMOTE_ADDR', 'raspberrypi.local')}:{self.J.get('REMOTE_WORK', '/home/pi/core')}",
            self.J.get('REMOTE_LOCAL', './remote')
        ]

        print("Executing:", program, " ".join(arguments))
        # return

        self.mount_process = QProcess(self.window)
        self.mount_process.finished.connect(self.on_mount_finished)
        self.mount_process.start(program, arguments)

    def remote_umount(self):
        cmd = ["bash" , "-c" , f"source {self.get_activate_sh_path()} &&  {self.J['PYCH_CORE_WORK']}/scripts/remote.sh umount"]
        sp = QProcess(self.window)
        sp.start(cmd[0], cmd[1:])
        sp.waitForFinished(5000)
        print("Command:", " ".join(cmd))
        self.window.led_mount.setStyleSheet("color: red;")

    def on_mount_finished(self):
        if getattr(self.window, "led_mount", None) is not None:
            if self.mount_process.exitCode() == 0:
                self.window.led_mount.setStyleSheet("color: green;")
            else:
                self.window.led_mount.setStyleSheet("color: red;")

    def btn_ping_clicked(self):
        if self.window is None:
            self.load()

        if getattr(self.window, "led_ping", None) is not None:
            self.window.led_ping.setStyleSheet("color: orange;")

        class WorkerThread(QThread):
            def __init__(self, parent=None,app=None):
                super().__init__(parent)
                self.res_local = False
                self.app = app

            def run(self):
                param = "-n" if os.name == "nt" else "-c"
                comando = ["ping", param, "1", self.app.J.get("REMOTE_ADDR", "127.0.0.1")]
                try:
                    resultado = subprocess.run(
                        comando,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    self.res_local = (resultado.returncode == 0)
                except subprocess.TimeoutExpired:
                    self.res_local = False

        def update_ui(res_local):
            if getattr(self.window, "led_ping", None) is not None:
                if res_local:
                    self.window.led_ping.setStyleSheet("color: green;")
                else:
                    self.window.led_ping.setStyleSheet("color: red;")

        worker_thread = WorkerThread(self.window,self)
        worker_thread.finished.connect(lambda: update_ui(worker_thread.res_local))
        worker_thread.start()     
        

        return True

    def get_activate_sh_path(self):
        return f"{CFG.get('LAST_CONFIG_FILE', 'config').split('.')[0]}.sh"

    def btn_apply_clicked(self):
        print("Apply clicked")

        Jaux = self.J.copy()
        for key in list(Jaux.keys()):
            if key.startswith("#"):
                Jaux.pop(key)

        with open(os.path.join(os.path.dirname(__file__), CFG["LAST_CONFIG_FILE"]), "w") as f:
            json.dump(Jaux, f, indent=4)
        print("Configuration saved.")

        to_save = self.get_activate_sh_path()
        with open(os.path.join(os.path.dirname(__file__), to_save), "w") as f:
            f.write("#!/bin/bash\n")
            f.write("# Generated by pych-gui\n")
            f.write("\n")
            f.write(f"export PYCH_ACTIVATE_SH='{self.get_activate_sh_path()}'\n")

            f.write("\n")
            for key in self.J:
                if not key.startswith("#") and not key.startswith("_"):
                    f.write(f"export {key}='{self.J[key]}'\n")

    
            f.write("\n")
            f.write('export REMOTE_SSH_ARGS="-i ${REMOTE_SSH_KEY} "\n')
            f.write('export REMOTE_SSH="${REMOTE_USER}@${REMOTE_ADDR}" \n')
            f.write('export REMOTE_TTY="ssh $REMOTE_SSH_ARGS $REMOTE_SSH" \n')

            f.write("\n")
            f.write(f"export PROJECT_NAME='{self.J['PROJECT_PATH'].split('/')[-1]}'\n")

            f.write("\n")
            f.write('export LD_LIBRARY_PATH=lib/:${LD_LIBRARY_PATH} \n')

            f.write("\n")
            f.write("export PYCH_CORE_ACTIVATED=\"1\" \n")
            f.write('export PYCH_NAME="core"\n')
            f.write(r"""export PS1='($(echo $PYCH_NAME))\[\e[1;32m\]\u@\h:\[\e[1;34m\]\w\[\e[0m\]\$ ' """)
            
            f.write("\n\n")
            f.write('echo "PYCH (Activated)"\n')

        
        self.log("Configuration applied.")
        self.log("Shell script saved in " + to_save)


    def on_browse(self,key, obj, type="folder", opts="All Files (*)"):
        print(f"Browse for {key}")
        if self.window is None:
            self.load()
        if type == "folder":
            selected_dir = self.open_dialog_get_folder()
            if selected_dir:
                obj.setText(selected_dir)
                self.J[key] = selected_dir
                print(f"Directorio seleccionado: {selected_dir}")
        elif type == "file":
            selected_file = self.open_dialog_get_file(opts=opts)
            if selected_file:
                obj.setText(selected_file)
                self.J[key] = selected_file
                print(f"Archivo seleccionado: {selected_file}")
        

    def open_dialog_get_folder(self):
        if self.window is None:
            self.load()
        
        current_dir = self.window.ed_PYCH_CORE_WORK.text() or os.getcwd()
        selected_dir = QFileDialog.getExistingDirectory(
            self.window,
            "Select Directory",
            current_dir,
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        return selected_dir

    def open_dialog_get_file(self, opts="All Files (*)"):
        if self.window is None:
            self.load()
        
        current_dir = self.window.ed_PYCH_CORE_WORK.text() or os.getcwd()
        selected_file, _ = QFileDialog.getOpenFileName(
            self.window,
            "Select File",
            current_dir,
            opts
        )
        return selected_file

    def log(self, message):
        print(f"{message}")
        self.window.txt_log.append(message)
        self.window.txt_log.ensureCursorVisible()


def main():
    base_dir = os.path.dirname(__file__) or os.getcwd()
    default_ui = os.path.join(base_dir, "ui_files/activate_editor.ui")

    ui_path = sys.argv[1] if len(sys.argv) > 1 else default_ui

    ui = UIConfigWindow(ui_path)
    sys.exit(ui.run())


if __name__ == "__main__":
    main()
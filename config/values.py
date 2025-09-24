from PySide6.QtCore import Qt

TEST_FILE = "/home/inception/git/pych/gui/robot.json"

KEY_WIDGET = {
    "plugins":{
        "path":None
    }
}


DATA_KEYS = Qt.UserRole+100

from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLineEdit, QCheckBox,QTextEdit,
    QPushButton, QSizePolicy, QWidget, QListWidgetItem, QStyleOptionButton, QStyle)


def match_pattern(pattern: str, candidate: str) -> bool:
    pat_tokens = pattern.split()
    cand_tokens = candidate.split()
    if len(pat_tokens) != len(cand_tokens):
        return False
    return all(p == c or p == '*' for p, c in zip(pat_tokens, cand_tokens))



GLOBAL_VARS={
    "commIO_plugins":[ "commIO_plugins_0" , "commIO_plugins_1", "commIO_plugins_2" ],
    "deviceIO_plugins":[ "deviceIO_plugins_0" , "deviceIO_plugins_1", "deviceIO_plugins_2" ],
    "controlIO_plugins":[ "controlIO_plugins_0" , "controlIO_plugins_1", "controlIO_plugins_2" ],
    "commIO_nodes":[ "commIO_nodes_0" , "commIO_nodes_1", "commIO_nodes_2" ],
    "deviceIO_nodes":[ "deviceIO_nodes_0" , "deviceIO_nodes_1", "deviceIO_nodes_2" ],
    "controlIO_nodes":[ "controlIO_nodes_0" , "controlIO_nodes_1", "controlIO_nodes_2" ]
}
EDIT_TYPES = {}

for key in ["plugins",
            "plugins path",
            "plugins commIO",
            "plugins deviceIO",
            "plugins controlIO"]:
    EDIT_TYPES[key] = {
        "#obj": None
    }

EDIT_TYPES=EDIT_TYPES | {
    "plugins commIO *": {
        "#obj": QComboBox,
        "#value": QLineEdit,
        "#values": GLOBAL_VARS["commIO_plugins"]
    },
    "plugins deviceIO *": {
        "#obj": QComboBox,
        "#value": QLineEdit,
        "#values": GLOBAL_VARS["deviceIO_plugins"]
    },
    "plugins controlIO *": {
        "#obj": QComboBox,
        "#value": QLineEdit,
        "#values": GLOBAL_VARS["controlIO_plugins"]
    },

    "deviceIO ref_pos config source calibrate":{
        "#value": QCheckBox
    },

    "controlIO * type":{
        "#value": QComboBox,
        "#values": GLOBAL_VARS["controlIO_plugins"]
    }


}

DEFAULT_TYPES={
    bool: QCheckBox,
    int: QLineEdit,
    float: QLineEdit,   
    str: QLineEdit,
    list: QTextEdit,
    "*": QLineEdit
}

def get_matching_rule(key: str, rules: dict = EDIT_TYPES) -> dict:
    for pattern, rule in rules.items():
        if match_pattern(pattern, key):
            return rule
    return {}
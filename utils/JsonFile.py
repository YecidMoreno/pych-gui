import json

class JsonFile():
    
    def __init__(self, path=None):
        
        self.path = path

        if path is not None:
            with open(path) as f:
                self.j = json.load(f)           
        else:
            self.j = {}

        # self.j.setdefault("plugins", {}).setdefault("path", [])
        # self.j.setdefault("plugins", {}).setdefault("commIO", [])
        # self.j.setdefault("plugins", {}).setdefault("deviceIO", [])
        # self.j.setdefault("plugins", {}).setdefault("controlIO", [])

        pass

    def save_to_file(self, output=None):
        if not output:
            output = self.path

        if output is not None:
            with open(output,'w') as f:
                json.dump(self.j,f,indent=4)

        pass

    def __del__(self):
        pass

    def setFromKeys(self,keys,val,create_if_not_exist=False):
        j_aux = self.j
        for key in keys[:-1]:
            if create_if_not_exist:
                if key not in j_aux:
                    j_aux[key] = {}

            j_aux = j_aux[key]
        
        
        j_aux[keys[-1]] = val

    def getFromKeys(self,keys):
        value = self.j
        for key in keys:
            value = value[key]
        
        return value

    def delete_key(self,keys):
        j_aux = self.j
        for key in keys[:-1]:
            j_aux = j_aux[key]
        
        del j_aux[keys[-1]]
    

    def move_key(self, new_key, old_key):
        # self.setFromKeys(new_key,self.getFromKeys(old_key))
        # self.delete_key(old_key)
        
        j_aux = self.j
        for key in old_key[:-1]:
            j_aux = j_aux[key]

        last_key = old_key[-1]

        if last_key not in j_aux:
            raise KeyError(f"La clave '{last_key}' no existe.")

        old_value = j_aux[last_key]
        
        nuevo = {}
        for k, v in j_aux.items():
            if k == last_key:
                nuevo[new_key[-1]] = old_value
            else:
                nuevo[k] = v

        j_aux.clear()
        j_aux.update(nuevo)

    @staticmethod
    def dfs(d, ruta=[]):
        for k, v in d.items():
            clave_actual = ruta + [k]
            yield clave_actual
            if isinstance(v, dict):
                yield from JsonFile.dfs(v, clave_actual)
    @staticmethod
    def keys2str(keys):
        return " ".join(keys)

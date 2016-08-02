_settings = {
}

default_settings = {

}

class settings(object):
    def __init__(self,scope):
        self._scope = scope

    def default(self, keys):
        update_default(self._scope,keys)

    def __getattr__(self, name):
        return get_key(self._scope,name)

    def __setattr__(self, name, value):
        if name == '_scope':
            super().__setattr__(name,value)
        else:
            set_key(self._scope,name,value)



def update_default(scope,keys):
    if scope not in default_settings:
        default_settings[scope]={}
    default_settings[scope].update(keys)

def set_default(scope,key,val):
    if scope not in default_settings:
        default_settings[scope]={}
    default_settings[scope][key]=val

def get_default(scope,key):
    scope = default_settings.get(scope,{})
    return scope.get(key,None)

def get_key(scope,key):
    s = _settings.get(scope,None)
    if s is None:
        return get_default(scope,key)
    else:
        ret = s.get(key,None)
        if ret is None:
            return get_default(scope,key)
        else:
            return ret

def set_key(scope,key,value):
    if scope not in default_settings:
        default_settings[scope]={}
    default_settings[scope][key]=value

def update_settings(keys,scope=None):
    if scope is None:
        _settings.update(keys)
    else:
        if scope not in _settings:
            _settings[scope]={}
        _settings[scope].update(keys)


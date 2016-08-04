from lib.events import EventMixin, add_event_mixin


def extend_instance(obj, cls):
    """
        Apply mixins to a class instance after creation
        (thanks http://stackoverflow.com/questions/8544983/dynamically-mixin-a-base-class-to-an-instance-in-python)
    """

    base_cls = obj.__class__
    base_cls_name = obj.__class__.__name__
    obj.__class__ = type(base_cls_name, (cls,base_cls),{})


class ObjMixin(object):
    def _create_observer(self):
        if not hasattr(self,'_obs____'):
            self._obs____ = EventMixin()

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            change_event = {
                'type':'__setattr__',
                'key':name,
                'value':value,
                'observed_obj':self,
            }
            if hasattr(self,name):
                change_event['old'] = getattr(self,name)
            super().__setattr__(name,value)
            self._obs____.emit('change',change_event)
        else:
            super().__setattr__(name,value)


class ArrayMixin(object):
    def _create_observer(self):
        if not hasattr(self,'_obs____'):
            self._obs____ = EventMixin()

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            change_event = {
                'type':'__setattr__',
                'key':name,
                'value':value
            }
            if hasattr(self,name):
                change_event['old'] = getattr(self,name)
            super().__setattr__(name,value)
            self._obs____.emit('change',change_event)
        else:
            super().__setattr__(name,value)

    def __setitem__(self, key, value):
        change_event = {
            'observed_obj':self,
            'type':'__setitem__',
            'key':key,
            'value':value
        }
        try:
            change_event['old']=self[key]
        except:
            pass
        super().__setitem__(key,value)
        self._obs____.emit('change',change_event)

    def __delitem__(self, key):
        change_event = {
            'observed_obj':self,
            'type':'__delitem__',
            'key':key,
        }
        try:
            change_event['old']=self[key]
        except:
            pass
        super().__delitem__(key)
        self._obs____.emit('change',change_event)

    def pop(self,*args):
        if len(args) > 0:
            index = args[0]
        else:
            index = len(self)-1
        change_event = {
            'observed_obj':self,
            'type':'__delitem__',
            'key':index,
        }
        change_event['old']=super().pop(*args)
        self._obs____.emit('change',change_event)
        return change_event['old']

    def sort(self,*args,**kwargs):
        super().sort(*args,**kwargs)
        self._obs____.emit('change',{'type':'change'})

class ListProxy(list):
    def __init__(self, lst):
        me=[]
        for i in lst:
            if type(i) == list:
                me.append(ListProxy(i))
            elif type(i) == dict:
                me.append(DictProxy(i))
            else:
                me.append(i)
        super().__init__(me)

class DictProxy(dict):
    def __init__(self, dct):
        me={}
        for k,v in dct.items():
            if type(v) == list:
                me[k]=ListProxy(v)
            elif type(v) == dict:
                me[k]=DictProxy(v)
            else:
                me[k]=v
        super().__init__(me)

def observe(obj,observer=None):
    if not hasattr(obj,'_obs____'):
        if hasattr(obj,'__setitem__'):
            extend_instance(obj,ArrayMixin)
        else:
            extend_instance(obj,ObjMixin)
        obj._create_observer()
    if observer is not None:
        obj._obs____.bind('change',observer,'change')
    return obj._obs____
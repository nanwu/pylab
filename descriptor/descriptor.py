
class p(object):
    
    def __init__(self, fget=None, fset=None, fdel=None):
        self._fget = fget
        self._fset = fset
        self._fdel = fdel

    def __get__(self, obj, obj_type):
        if self._fget is None:
            raise AttributeError("Attribute not found")
        return self._fget(obj)

    def __set__(self, obj, val):
        if self._fset is None:
            raise AttributeError("Can't set the attribute")
        self._fset(obj, val)

    def __delete__(self, obj):
        if self._fdel is None:
            raise AttributeError("Can't delete the attribute")
        self._fdel(obj)
    
    def getter(self, fget):
        return type(self)(fget, self._fset, self._fdel)
    
    def setter(self, fset):
        return type(self)(self._fget, fset, self._fdel)

    def deleter(self, fdel):
        return type(self)(self._fget, self._fset, fdel)

class A(object):

    @p
    def attr1(self):
        print "attr1 getter invoked"

    @attr1.setter
    def attr1(self, val):
        print "attr1 setter invoked"

    @attr1.deleter
    def attr1(self):
        print "attr1 deleter invoked"

a = A()
a.attr1
a.attr1 = 1
del a.attr1

class Property(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value    

    def __eq__(self, p2):
        if isinstance(p2, self.__class__):
            return self.value == p2.value and self.key == p2.key

def find_property(name, ps):    
    for p in ps:
        if p.key == name:
            return p.value
    
    return None

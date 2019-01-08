class Property(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value    

def find_property(name, ps):    
    for p in ps:
        if ps.name == name:
            return ps.value
    
    return None
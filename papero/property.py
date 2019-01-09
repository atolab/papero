class Property(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value    

def find_property(name, ps):    
    for p in ps:
        if p.key == name:
            return p.value
    
    return None
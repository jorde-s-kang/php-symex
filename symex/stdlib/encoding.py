class EscapedValue:
    def __init__(self, value):
        self.value = value

def phpEncodeString(string, env):
    return EscapedValue(string)

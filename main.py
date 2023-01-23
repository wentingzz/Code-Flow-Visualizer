import copy
# import graphviz
ARRAY_SIZE = 4      #element size in an array
class IR:
    def __init__(self, opcode, val1=None, val2=None, ir=-1):
        if ir == -1:
            global ir_num
            self.ir = ir_num
            ir_num += 1
        else:
            self.ir = ir
        self.op = opcode
        self.val1 = val1
        self.val2 = val2
    def __eq__(self, other):
        if self and not other or other  and not self:
            return False
        if isinstance(self, IR) and isinstance(other, IR) and self.op == other.op and (self.ir == other.ir or -1 in [self.ir, other.ir]) and self.val1 == other.val1 and self.val2 == other.val2:
            return True
        return False
    def __repr__(self):
        return f"{self.ir}: {self.op}{self.getVarStr(self.val1)}{self.getVarStr(self.val2)}"
    def __hash__(self):
        return hash(tuple([self.ir, self.op]))
    def getVarStr(self, v):
        if v != None:
            if isinstance(v, IR):
                return f" ({v.ir})"
            elif isinstance(v, int):
                return f" #{v}"
            else:
                return f" {v}"
        return ""
    def set(self, opcode, val1, val2):
        self.op = opcode
        self.val1 = val1
        self.val2 = val2

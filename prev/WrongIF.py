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
        if self.op == other.op and self.val1 == other.val1 and self.val2 == other.val2:
            return True
        return False
    def __repr__(self):
        res = f"{self.ir}: {self.op}"
        if self.val1 != None:
            if isinstance(self.val1, IR):
                res += f" ({self.val1.ir})"
            else:
                res += f" #{self.val1}"
        if self.val2 != None:
            if isinstance(self.val2, IR):
                res += f" ({self.val2.ir})"
            else:
                res += f" {self.val2}"
        return res
    def __hash__(self):
        return hash(tuple([self.ir, self.op]))
    def set(self, opcode, val1, val2):
        self.op = opcode
        self.val1 = val1
        self.val2 = val2

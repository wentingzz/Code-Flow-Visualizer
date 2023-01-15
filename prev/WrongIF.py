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
class B:
    def __init__(self, bb_num, dom = None, left = None):
        self.dom = dom
        self.var = {}
        if dom != None:
            self.var = dict(dom.var)
        self.irs = []
        self.num = bb_num
        self.left = left
        self.join = None
        self.loop = -1
    def __repr__(self):
        res = f"BB{self.num}| {{"
        for ir in self.irs:
            res += f" {ir} |"
        return res[:-1]+"}}"
    def setNum(self, num):
        self.num = num
    def addToBBs(self):
        print(f"Check BB Var: {bbs[-2].var}\n{bbs[-1].var}\n{self.var}")
        if self.num == -1:
            self.num = len(bbs)
        bbs.append(self)
    def phiPush(self):
        for key in self.var.keys():
            if self.var[key].op == "phiTBD":
                self.var[key].op = "phi"
                if self.join:
                    self.updatePhi(key, self.var[key])
    def updatePhi(self, d, e):
        if not self.join:
            return
        # print(f"Phi: {d}, {e}, BB{self.join.num}, {self.join.var}")
        if self.left:
            if self.join.var[d].op == "phiTBD":
                self.join.var[d].val1 = e
            else:
                ir = self.join.addIR("phiTBD", e, self.join.var[d])
                self.join.var[d] = ir
                self.join.updatePhi(d, ir)
        else:
            if self.join.var[d].op == "phiTBD":
                self.join.var[d].val2 = e
            else:
                ir = self.join.addIR("phiTBD", self.join.var[d], e)
                self.join.var[d] = ir
                self.join.updatePhi(d, ir)
        # print(f"After Phi: {d}, {e}, {self.join.var}")
    def addIR(self, opcode, val1=None, val2=None):
        if len(self.irs) == 1 and self.irs[0].op == "" and opcode != "const":
            self.irs[0].set(opcode, val1, val2)
            return self.irs[0]
        if opcode.startswith("b"):
            tmp = IR(opcode, val1, val2)
            self.irs.append(tmp)
            return tmp
        elif opcode.startswith("phi"):
            tmp = IR(opcode, val1, val2)
            if self.loop > -1:
                self.irs.insert(self.loop, tmp)
                self.loop += 1
            else:
                self.irs.append(tmp)
            return tmp
        if opcode == "const":
            for x in bbs[0].irs:
                if x.op == opcode and x.val1 == val1:
                    return x
            else:
                tmp = IR(opcode, val1, val2)
                bbs[0].irs.append(tmp)
                return tmp
        else:
            for x in self.irs:
                if x.op == opcode and x.val1 == val1 and x.val2 == val2:
                    return x
            else:
                tmp = IR(opcode, val1, val2)
                self.irs.append(tmp)
                return tmp
class B:
    def __init__(self, prev, nxt=None):
        self.num = -1
        self.prev = pre
        self.next = nxt
    def active(self):
        if self.num == -1:
            self.num = len(bbs)
        bbs.append(self)
class IfB(B):
    def __init__(self, prev, nxt=None):
        B.__init__(self, prev, nxt):
        self.left = B()
        self.right = B()
        self.join = B()

class WhileB(B):
    def __init__(self, prev, nxt=None):
        B.__init__(self, prev, nxt):
        self.header = B()
        self.body = B()
        self.end = B()


ir_num = 1
bbs = [BB(0), BB(1)]
flow = ["BB0:s -> BB1:n"]

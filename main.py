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
bbs = []
class ArrayVar:
    def __init__(self, names=[], size=None):
        self.a = {}
        if len(bbs) > 0:
            self.size = size
            for n in names:
                self.a[n[0]] = [bbs[0].addIR("const", f"{n[0]}_adr"), None, n[1], {}]
    def getCap(self, name):
        return self.a[name][2]
    def copy(self):
        res = ArrayVar()
        res.a = copy.deepcopy(self.a)
        res.size = self.size
        return res
    def __repr__(self):
        res = "Array:\n"
        for name, v in self.a.items():
            res += f"\t{name} at {v[1]} has {v[-1]}\n"
        return res + "\n"
    def get(self, name, idx):
        if name in self.a and idx in self.a[name][-1]:
            return self.a[name][-1][idx]
        return None
    def reset(self, name, idx = None):
        if name in self.a:
            if idx and idx in self.a[name][-1]:
                tmp = self.a[name][-1][idx]
                self.a[name][-1] = {}
                self.a[name][-1][idx] = tmp
            else:
                self.a[name][-1] = {}
    def getBase(self, name, bb):
        if self.a[name][1] == None:
            self.a[name][1] = bb.addIR("add", "#BASE", self.a[name][0])
        return self.a[name][1]
    def set(self, name, idx, val):
        if name in self.a:
            self.a[name][-1][idx] = val
            # print(f"Set:\n\t{idx}\n\t{self.a[name][-1]}")
            return val
    def remove(self, name, idx):
        if name in self.a:
            self.a[name][-1][idx] = None
flow = ["BB0:s -> BB1:n"]
class GeneralBB:
    def __init__(self, bb_num, dom = None, left = None):
        self.dom = dom
        self.var = {}
        if dom != None:
            self.var = dict(dom.var)
            self.a = dom.a.copy()
        else:
            self.a = ArrayVar()
        self.irs = []
        self.num = bb_num
        self.left = left
        self.join = None
    def __repr__(self):
        res = f"BB{self.num}| {{"
        for ir in self.irs:
            res += f" {ir} |"
        return res[:-1]+"}}"
    def setNum(self, num):
        self.num = num
    def addToBBs(self):
        # print(f"Check BB Var: {bbs[-2].var}\n{bbs[-1].var}\n{self.var}")
        if self.num == -1:
            self.num = len(bbs)
        bbs.append(self)
        if self.dom:
            flow.append(f"BB{self.dom.num}:b -> BB{self.num}:n [color=blue,style=dotted,label=\"dom\"]")
    def addIR(self, opcode, val1=None, val2=None):
        if len(self.irs) == 1 and opcode != "const" and self.irs[0].op == "":
            self.irs[0].set(opcode, val1, val2)
            return self.irs[0]
        if opcode.startswith("b"):
            tmp = IR(opcode, val1, val2)
            self.irs.append(tmp)
            return tmp
        # elif opcode.startswith("phi"):
        #     tmp = IR(opcode, val1, val2)
        #     self.irs.append(tmp)
        #     return tmp
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
    def computeIdx(self, name, idx):
        res, cap = None, self.a.getCap(name)
        if len(cap) > 1:
            for i in range(len(idx)):
                if isinstance(cap[i], int) and cap[i] != 1:
                    cap[i] = bbs[0].addIR("const", cap[i])
                if res != None:
                    if isinstance(cap[i], IR):
                        res = self.addIR("add", res, self.addIR("mul", cap[i], idx[i]))
                    else:
                        res = self.addIR("add", res, idx[i])
                else:
                    res = self.addIR("mul", cap[i], idx[i])
            return res
        return idx[0]

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
class BB(GeneralBB):
    def __init__(self, bb_num, dom = None, left = None):
        GeneralBB.__init__(self, bb_num, dom, left)
        self.rec = True
    def setRec(self, isRec):
        self.rec = isRec
    def setA(self, d, idx, val):
        tIdx = tuple(idx)
        self.resetA(d, tIdx)
        res = self.a.get(d, tIdx)
        if res:
            location = res.val1
        else:
            idx = self.computeIdx(d, idx)
            offset = self.addIR("mul", idx, self.a.size)
            base = self.a.getBase(d, self)

            location = self.addIR("adda", offset, base)
            # print(f"SetA:{d} at {idx} \n\t{base} \n\t{location}\n\t{val}")
        return self.a.set(d, tIdx, self.addIR("store", location, val))
    def getA(self, name, idx):
        tidx = tuple(idx)
        res = self.a.get(name, tidx)
        if not res:
            idx = self.computeIdx(name, idx)
            offset = self.addIR("mul", idx, self.a.size)
            base = self.a.getBase(name, self)
            location = self.addIR("adda", offset, base)
            res = self.a.set(name, tidx, self.addIR("load", location))
            # print(f"GetA: \n\t{base} \n\t{location}\n\t{res}")
        return res
    def resetA(self, name, idx=[]):     #reset self.a[name] except key = idx and reset all its join BB recursively
        self.a.reset(name, tuple(idx))
        if self.join and self.rec:
            self.join.addIR("kill", name)
            self.join.resetA(name)
            # print(self.num, self.join.a)
    # def removeA(self, name, idx):       #remove self.a[name][idx]
    #     # idx = self.computeIdx(name,idx)
    #     self.a.remove(name, tuple(idx))
    #     if self.join and self.rec:
    #         self.join.a.remove(name, idx)
    def phiPush(self, phis = None):
        #set instructions with "phiTBD" to "phi" and update its join BB
        for key in self.var.keys():
            if self.var[key] and self.var[key].op == f"phiTBD{self.num}":
                if self.rec and self.join:
                    self.updatePhi(key, self.var[key])
                self.var[key].op = "phi"
        #add additional phis to the join BB if there exists any
        if self.rec and phis:
            for k, v in phis.items():
                self.updatePhi(k,v)
    def updatePhi(self, d, e):
        if not self.join:
            return
        # print(f"Phi: {d}, {e}, BB{self.join.num}, {self.join.var}")
        if self.left:
            #add/update instruction "phiTBD" to its join BB with val1
            if self.join.var[d].op == f"phiTBD{self.join.num}":
                self.join.var[d].val1 = e
            else:
                ir = self.join.addIR(f"phiTBD{self.join.num}", e, self.join.var[d])
                self.join.var[d] = ir
                if self.rec:    #update phi recursively
                    self.join.updatePhi(d, ir)
        else:
            #add/update instruction "phiTBD" to its join BB with val2
            if self.join.var[d].op == f"phiTBD{self.join.num}":
                self.join.var[d].val2 = e
                ir = self.join.var[d]
            else:
                ir = self.join.addIR(f"phiTBD{self.join.num}", self.join.var[d], e)
                self.join.var[d] = ir
                if self.rec:    #update phi recursively
                    self.join.updatePhi(d, ir)
        # print(f"After Phi: {d}, {e}, {self.join.var}")
    def addPhis(self, phis):    #used in while loop to add "phiTBD" to current BB
        for d in phis.keys():
            ir = self.addIR(f"phiTBD{self.num}", self.var[d], ir_num)
            phis[d] = ir
            self.var[d] = ir
        return phis

ir_num = 0
bbs += [BB(0), BB(1)]
class regularTok:
    def __init__(self, s, idx = 0):
        self.s = s
        self.idx = idx
    def skip(self):
        while self.s[self.idx] == " ":
            self.idx += 1
    def skipTo(self, c):
        self.idx = self.s.index(c, self.idx) + len(c)
    def ident(self):
        self.skip()
        # print("Id",self.s[self.idx:])
        if self.s[self.idx].isalpha():
            res = self.idx
            while self.idx < len(self.s) and self.s[self.idx].isalnum():
                self.idx += 1
            v = self.s[res:self.idx]
            return v
    def number(self, bb, add=True):
        self.skip()
        # print("Number",self.s[self.idx:])
        if self.s[self.idx].isdigit():
            res = self.idx
            while self.idx < len(self.s) and self.s[self.idx].isdigit():
                self.idx += 1
            res = int(self.s[res:self.idx])
            if add:
                res = bb.addIR("const", res)
            return res

    def D(self, bb):
        self.skip()
        # print("D", self.s[self.idx:])
        res, idx = self.ident(), []
        self.skip()
        while self.s[self.idx] == "[":
            self.idx += 1
            idx.append(self.E(bb))
            self.skipTo("]")
            self.skip()
        return (res, idx)
    def F(self, bb):
        self.skip()
        res = 0
        # print("F", self.s[self.idx:])
        if self.s[self.idx] == "(":
            self.idx += 1
            res = self.E(bb)
            self.skipTo(")")
        elif self.s[self.idx].isdigit():
            res = self.number(bb)
            #TODO const
        elif self.s[self.idx].isalpha():
            if self.s[self.idx:].startswith("call "):
                res = self.FC(bb)
            else:
                res,idx = self.D(bb)
                if idx:
                    return bb.getA(res, idx)
                elif res in bb.var:
                    return bb.var[res]
                # res = lookup[self.ident()]
        return res
    def T(self, bb):
        # print("T", self.s[self.idx:])
        res = self.F(bb)
        self.skip()
        while self.idx < len(self.s) and self.s[self.idx] in ["*", "/"]:
            mul = self.s[self.idx] == "*"
            self.idx += 1
            if mul:
                res = bb.addIR("mul", res, self.F(bb))
            else:
                res = bb.addIR("div", res, self.F(bb))
        return res
    def E(self, bb):
        # print("E", self.s[self.idx:])
        self.skip()
        res = self.T(bb)
        self.skip()
        while self.idx < len(self.s) and self.s[self.idx] in ["+", "-"]:
            plus = self.s[self.idx] == "+"
            self.idx += 1
            if plus:
                res = bb.addIR("add", res, self.T(bb))
            else:
                res = bb.addIR("sub", res, self.T(bb))
        return res
    def R(self, bb):
        # print("\nR", self.s[self.idx:])
        self.skip()
        res = self.E(bb)
        # print("R", res, bb.irs)
        op = ""
        self.skip()
        if self.s[self.idx:].startswith("=="):
            op = "bne"
            self.idx += 2
        elif self.s[self.idx:].startswith("!="):
            op = "beq"
            self.idx += 2
        elif self.s[self.idx:].startswith("<="):
            op = "bgt"
            self.idx += 2
        elif self.s[self.idx:].startswith(">="):
            op = "blt"
            self.idx += 2
        elif self.s[self.idx:].startswith("<"):
            op = "bge"
            self.idx += 1
        elif self.s[self.idx:].startswith(">"):
            op = "ble"
            self.idx += 1
        self.skip()
        res = bb.addIR("cmp", res, self.E(bb))
        return bb.addIR(op, res, -1)
class tokenizer(regularTok):
    def A(self, bb):
        self.skipTo("let ")
        d, idx = self.D(bb)
        self.skipTo("<-")
        e = self.E(bb)
        if idx:
            bb.setA(d, idx, e)
        else:
            bb.updatePhi(d,e)
            bb.var[d] = e
        return e
    def FC(self, bb):
        # print("FC", self.s[self.idx])
        self.skipTo("call ")
        name = self.ident()
        if name == "InputNum":
            res = bb.addIR("read")
        elif name == "OutputNum":
            self.skipTo("(")
            self.skip()
            res = bb.addIR("write", self.E(bb))
        elif name == "OutputNewLine":
            res = bb.addIR("writeNL")
        else:
            print("No user defined function")
            exit(0)
        self.skipTo(")")
        return res
    def IS(self, bb):
        self.skipTo("if")
        braIR = self.R(bb)

        self.skipTo("then")
        left, right, join = BB(-1, bb, True), BB(-1, bb, False), BB(-1, bb)
        if bb.join:
            join.join, join.left = bb.join, bb.left
        left.join, right.join = join, join
        left.addToBBs()
        flow.append(f"BB{bb.num}:s -> BB{left.num}:n [label=\"fall-through\"]")
        left = self.SS(left)

        left.addIR("bra", -1)
        if len(join.irs) == 0:
            join.addIR("")
        self.skip()
        if self.s[self.idx:].startswith("else "):
            self.idx += 5
            right.addToBBs()
            flow.append(f"BB{bb.num}:s -> BB{right.num}:n [label=\"branch\"]")
            tmp = self.SS(right)
            if len(right.irs) == 0:
                right.addIR("")
            braIR.val2 = right.irs[0]
            right = tmp
        else:
            braIR.val2 = join.irs[0]
        left.irs[-1].val1 = join.irs[0]

        join.phiPush()
        join.addToBBs()
        flow.append(f"BB{left.num}:s -> BB{join.num}:n [label=\"branch\"]")
        if right.num > 0:
            flow.append(f"BB{right.num}:s -> BB{join.num}:n [label=\"fall-through\"]")
        else:
            flow.append(f"BB{bb.num}:s -> BB{join.num}:n [label=\"branch\"]")
        self.skipTo("fi")
        return join
    def preprocess(self, bb):
        start = self.idx
        stack = ["od"]
        var, a = {}, []
        while stack:
            if self.s[self.idx:].startswith("let "):
                self.idx += 4
                d, idx = self.D(bb)
                if not idx:
                    var[d] = None
                else:
                    a.append([d,idx])
            elif self.s[self.idx:].startswith("while "):
                self.idx += 6
                stack.append("od")
            elif self.s[self.idx:].startswith(" od"):
                stack.pop()
            self.idx += 1
        self.idx = start
        return (var, a)
    def WS(self, bb):
        self.skipTo("while ")
        phis, arrays = self.preprocess(bb)

        join = BB(-1, bb)
        join.addToBBs()
        phis = join.addPhis(phis)
        # kill array if it's assigned in the while loop
        for a in arrays:
            join.addIR("kill", a[0])
            join.resetA(a[0])
        flow.append(f"BB{bb.num}:s -> BB{join.num}:n")
        # print(join.var)
        bra = self.R(join)
        # print(join.var)
        # print(f"Join:{join.a}")
        loop = BB(-1, join, False)
        loop.join = join
        loop.addToBBs()
        loop.setRec(False)  #preprocessed. No need to recursively update phis

        flow.append(f"BB{join.num}:s -> BB{loop.num}:n [label=\"fall-through\"]")


        # print(f"\nThis Initial join {join.num}: {join.var}")
        # print(f"\nThis Initial loop {loop.num}: {loop.a}")
        self.skipTo("do ")
        loop = self.SS(loop)
        flow.append(f"BB{loop.num}:s -> BB{join.num}:n [label=\"fall-through\"]")

        end = BB(-1, join)
        # print(f"End:\n\t{arrays}\n\t{end.a}")
        # print(f"End:\n\t{end.a}")
        end.addToBBs()
        flow.append(f"BB{join.num}:s -> BB{end.num}:n [label=\"follow\"]")

        join.phiPush()
        self.skipTo("od")
        # end.var = join.var
        # print(join.var, loop.var)
        if len(end.irs) == 0:
            ir = end.addIR("")
        else:
            ir = end.irs[0]
        bra.val2 = ir

        if bb.join:
            end.join, end.left = bb.join, bb.left
        end.phiPush(phis)   # update phi with additional phis from preprocessed step

        return end
    # def RS(self, lookup):
    #     self.skipTo("return ")
    #     self.skip()
    #     if not self.s[self.idx:].startswith(("let", "call", "if", "then", "else", "fi", "while","do", "od", "return")):
    #         self.E(lookup)

    def S(self, l):
        self.skip()
        # print("S", self.s[self.idx:])
        if self.s[self.idx:].startswith("let "):
            self.A(l)
        elif self.s[self.idx:].startswith("call "):
            self.FC(l)
        elif self.s[self.idx:].startswith("if "):
            l = self.IS(l)
        elif self.s[self.idx:].startswith("while "):
            l = self.WS(l)
        # elif self.s[self.idx:].startswith("return"):
        #     self.RS(l)
        return l
    def SS(self, bb):
        self.S(bb)
        while self.s[self.idx] == ";":
            self.idx += 1
            bb = self.S(bb)
        return bb

    def TD(self, s):
        if s.startswith("var"):
            self.skipTo("var ")
            return (True, None)
        else:
            self.skipTo("[")
            cap = []
            self.number(None, False)
            self.skipTo("]")
            self.skip()
            while self.s[self.idx] == "[":
                self.idx += 1
                n = self.number(None, False)
                cap = [x * n for x in cap]
                cap.append(n)
                self.skipTo("]")
                self.skip()
            cap.append(1)
            return (False, cap)
    def VD(self):
        s = self.s[self.idx:].lstrip()
        var = {}
        name, size = [], None
        while(s.startswith("var ") or s.startswith("array")):
            isVar, cap = self.TD(s)
            if isVar:
                var[self.ident()] = None
                while self.s[self.idx] == ",":
                    self.idx += 1
                    var[self.ident()] = None
                    self.skip()
            else:
                name.append((self.ident(), cap))
                size = bbs[0].addIR("const", ARRAY_SIZE)
                while self.s[self.idx] == ",":
                    self.idx += 1
                    name.append((self.ident(), cap))
                    self.skip()
            self.skipTo(";")
            s = self.s[self.idx:].lstrip()
        bbs[-1].var = var
        bbs[-1].a = ArrayVar(name, size)
        return var


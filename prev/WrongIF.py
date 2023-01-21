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
class regularTok:
    def __init__(self, s, idx = 0):
        self.s = s
        self.idx = idx
    def skip(self):
        while self.s[self.idx] == " ":
            self.idx += 1
    def ident(self):
        self.skip()
        # print("Id",self.s[self.idx:])
        if self.s[self.idx].isalpha():
            res = self.idx
            while self.idx < len(self.s) and self.s[self.idx].isalnum():
                self.idx += 1
            v = self.s[res:self.idx]
            return v
    def number(self, bb):
        self.skip()
        # print("Number",self.s[self.idx:])
        if self.s[self.idx].isdigit():
            res = self.idx
            while self.idx < len(self.s) and self.s[self.idx].isdigit():
                self.idx += 1
            res = int(self.s[res:self.idx])
            res = bb.addIR("const", res)
            return res

    def D(self, bb):
        self.skip()
        # print("D", self.s[self.idx:])
        res = self.ident()
        while self.s[self.idx] == "[":
            self.idx += 1
            self.E(bb)
            self.idx += 1
        return res
    def F(self, bb):
        self.skip()
        res = 0
        # print("F", self.s[self.idx:])
        if self.s[self.idx] == "(":
            self.idx += 1
            res = self.E(bb)
            self.idx += 1
        elif self.s[self.idx].isdigit():
            res = self.number(bb)
            #TODO const
        elif self.s[self.idx].isalpha():
            if self.s[self.idx:].startswith("call "):
                res = self.FC(bb)
            else:
                res = self.D(bb)
                # print(res, bb)
                if res in bb.var:
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
        # print("R", self.s[self.idx:])
        self.skip()
        res = self.E(bb)
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
        self.idx = self.s.index("let ", self.idx) + 4
        d = self.D(bb)
        self.idx = self.s.index("<-", self.idx) + 2
        e = self.E(bb)
        bb.updatePhi(d,e)
        bb.var[d] = e
        return e
    def FC(self, bb):
        # print("FC", self.s[self.idx])
        self.idx = self.s.index("call ", self.idx) + 5
        name = self.ident()
        if name == "InputNum":
            res = bb.addIR("read")
        self.idx = self.s.index("(", self.idx) + 1
        self.skip()
        if self.s[self.idx] != ")":
            if name == "OutputNum":
                res = bb.addIR("write", self.E(bb))
            else:
                self.E(bb)
                self.skip()
                while self.s[self.idx] == ",":
                    self.idx += 1
                    self.E(bb)
                    self.skip()
        self.idx = self.s.index(")", self.idx) + 1
        return res
    def IS(self, bb):
        # print("IS", self.s[self.idx:])

        self.idx = self.s.index("if ", self.idx) + 3
        braIR = self.R(bb)
        self.idx = self.s.index("then ", self.idx) + 5
        left, right, join = BB(-1, bb, True), BB(-1, bb, False), BB(-1, bb)
        if bb.join:
            join.join, join.left = bb.join, bb.left
        left.join, right.join = join, join
        left.addToBBs()
        flow.append(f"BB{bb.num}:s -> BB{left.num}:n [label=\"fall-through\"]")
        left = self.SS(left)
        left.addIR("bra", -1)
        # print(f"Left: {left}\n{left.var}\nJoin: {join}\n{join.var}\n")

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
            # print(f"Right: {right}\n{right.var}\nJoin: {join}\n{join.var}\n")
        else:
            if len(join.irs) == 0:
                join.addIR("")
            braIR.val2 = join.irs[0]
        left.irs[-1].val1 = join.irs[0]
        join.phiPush()
        join.addToBBs()
        flow.append(f"BB{left.num}:s -> BB{join.num}:n [label=\"branch\"]")
        if right.num > 0:
            flow.append(f"BB{right.num}:s -> BB{join.num}:n [label=\"fall-through\"]")
        else:
            flow.append(f"BB{bb.num}:s -> BB{join.num}:n [label=\"fall-through\"]")
        self.idx = self.s.index("fi", self.idx) + 2
        return join
    def loop(self, join, loop, idx):
        jl, ll, maxI = 0, 0, 4
        # tmp = join.var
        while maxI and jl != len(join.irs) and ll != len(loop.irs):
            jl, ll, loop.var = len(join.irs), len(loop.irs), dict(join.var)
            # loop.join, join.loop = join, 0
            print(f"\nThis {maxI} join {join.num}: {join.var}")
            self.idx = idx
            self.idx = self.s.index("do ", self.idx) + 3
            self.SS(loop)
            print(f"\nThis {maxI} loop {loop.num}: {loop.var}")
            self.idx = self.s.index("od", self.idx) + 2
            maxI -= 1
            # print(jl, join, join.var)
        # join.var = tmp
        # join.phiPush()
        return

    def WS(self, bb):
        # print("WS", self.s[self.idx:])
        self.idx = self.s.index("while ", self.idx) + 6
        startIdx = self.idx
        join, loop, end = BB(-1, bb), BB(-1, bb, False), BB(-1, bb)
        loop.join, join.loop = join, 0
        join.addToBBs()
        flow.append(f"BB{bb.num}:s -> BB{join.num}:n")
        bra = self.R(join)
        loop.addToBBs()
        end.addToBBs()
        flow.append(f"BB{join.num}:s -> BB{loop.num}:n [label=\"fall-through\"]")
        flow.append(f"BB{loop.num}:s -> BB{join.num}:n [label=\"fall-through\"]")
        flow.append(f"BB{join.num}:e -> BB{end.num}:n [label=\"follow\"]")
        self.idx = self.s.index("do ", self.idx) + 3
        print(f"\nThis Initial join {join.num}: {join.var}")
        print(f"\nThis Initial loop {loop.num}: {loop.var}")
        self.SS(loop)

        self.idx = self.s.index("od", self.idx) + 2
        self.loop(join, loop, startIdx)
        end.var = join.var
        # print(join.var, loop.var)
        ir = end.addIR("")
        bra.val2 = ir
        if bb.join:
            end.join = bb.join
        return end
    def RS(self, lookup):
        self.idx = self.s.index("return ", self.idx) + 7
        self.skip()
        if not self.s[self.idx:].startswith(("let", "call", "if", "then", "else", "fi", "while","do", "od", "return")):
            self.E(lookup)

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
        elif self.s[self.idx:].startswith("return"):
            self.RS(l)
        return l
    def SS(self, bb):
        # print("SS", self.s[self.idx:])
        # tmp = len(irs)
        self.S(bb)
        while self.s[self.idx] == ";":
            self.idx += 1
            bb = self.S(bb)
        # if len(irs) == tmp:
        #     irs.append(IR(""))
        return bb

    def TD(self, s):
        if s.startswith("var"):
            self.idx = self.s.index("var ", self.idx) + 4
        else:
            self.idx = self.s.index("array ", self.idx) + 6
            #TODO more
    def VD(self):
        s = self.s[self.idx:].lstrip()
        var = {}
        while(s.startswith("var ") or s.startswith("array ")):
            self.TD(s)
            var[self.ident()] = None
            while self.s[self.idx] == ",":
                self.idx += 1
                var[self.ident()] = None
                self.skip()
            self.idx = self.s.index(";", self.idx) + 1

            s = self.s[self.idx:].lstrip()
        return var

# //     def FP(self):
# //         start = self.s.index("(", self.idx) + 1
# //         end = self.s.index(")", self.idx)
# //         idList = self.s[start:end].split(",")
# //         self.idx = end + 1

# //     def FB(self):
# //         self.VD()
# //         self.idx = self.s.index("{", self.idx) + 1
# //         self.SS()
# //         self.idx = self.s.index("}", self.idx) + 1

# //     def FD(self):
# //         s = self.s[self.idx:].lstrip()
# //         while s.startswith("void") or s.startswith("function"):
# //             self.idx = self.s.index("function ", self.idx) + 9
# //             self.ident()
# //             self.FP()
# //             self.idx += 1
# //             self.FB()
# //             self.idx += 1

    def process(self):
        bbs[-1].var = self.VD()
        # self.FD()
        self.skip()
        if self.s[self.idx] == "{":
            self.idx += 1
            self.SS(bbs[-1])
            self.idx = self.s.index("}", self.idx) + 1
def printGraph():
    print("digraph G{")
    for bb in bbs:
        print(f"BB{bb.num} [shape=record, label=\"<b>{bb}\"];")
    for f in flow:
        print(f"{f};")
    print("}")
class parser:
    def __init__(self, s):
        if s.startswith("main"):
            s = s[4:]
        self.s = s

    def computation(self):
        t = tokenizer(self.s)
        t.process()
        # getIR("end")
        printGraph()
        for bb in bbs:
            print(f"BB{bb.num}:{bb.var}")
        # print(bbs[0])
        # for bb in bbs[1:]:
        #     print(bb)
        # print(bbs[-1].var)
        # print(flow)
# s = input("Enter your input")
# s = "main  var a, b  , c ;  var  n,  x,  j   ;  {let  a  <-  3  +   2;       if 1<= 2   then   let a <- a + 3 fi}"
# s = ("main var a, b, c, d, e;  {let a <- call InputNum ( ); let b<- a ;"
#      "let c   <- b; let d<-b+c; let e<- a+b;  "
#      "if a < 0 then "
#      "  let d <- d+e;   if d != 0  then let a <- d fi;"
#      "  else   let d<-a; if e >= 1 then let e <- a else let e<-1 fi; let a <- c"
#      "  fi;"
#      "call OutputNum  ( a ) }"
#     )
# s = ("main var a,b,c,d,e; {let a<-call InputNum(); "
#      "let b<-a; let c<-b; let d<- b+ c; let e <-a+b;"
#      "if a<0 then let d<-d+e; let a<- d else let d<- e  fi;"
#      " call OutputNum(a)}"
# )
s = ("main var x,y,i,j; {let i<-call InputNum(); "
     "let x<-0; let y<-0; let j<- i; while x<10 do "
     " let x <- i + 1; if x < 0 then let y <- j + 1 fi; let i <-i + 1 "
     "od; call OutputNum(x)}"
)

# s = ("main var x,y,i,j; {let i<-call InputNum(); "
#      "let x<-0; let y<-0; let j<- i; while x<10 do "
#      " let x <- i + 1; let y <- j + 1; while j<10 do "
#      " let x <- j + 1; let y <- i + 1; let j <-j + 1 "
#      "od; let i <-i + 1 "
#      "od; call OutputNum(x)}"
# )

p = parser(s)
p.computation()
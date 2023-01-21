lookup = {}
class tokenizer:
    def __init__(self, s, idx = 0):
        self.s = s
        self.idx = idx

    def F(self):
        res = 0
        if self.s[self.idx] == "(":
            self.idx += 1
            res = self.E()
            self.idx += 1
        elif self.s[self.idx].isdigit():
            res = self.idx
            while self.idx < len(self.s) and self.s[self.idx].isdigit():
                self.idx += 1
            res = int(self.s[res:self.idx])
        elif self.s[self.idx].isalpha():
            res = self.idx
            while self.idx < len(self.s) and self.s[self.idx].isalnum():
                self.idx += 1
            res = lookup[self.s[res:self.idx]]
        return res
    
    def T(self):
        res = self.F()
        while self.idx < len(self.s) and self.s[self.idx] in ["*", "/"]:
            mul = self.s[self.idx] == "*"
            self.idx += 1
            if mul:
                res *= self.F()
            else:
                res /= self.F()
        return res
    
    def E(self):
        res = self.T()
        while self.idx < len(self.s) and self.s[self.idx] in ["+", "-"]:
            plus = self.s[self.idx] == "+"
            self.idx += 1
            if plus:
                res += self.T()
            else:
                res -= self.T()
        return res
    
    def process(self):
        while self.idx < len(self.s) and self.s[self.idx] == " ":
            self.idx += 1
        s = self.s[self.idx:]
        if s.startswith("var"):
            s = s[3:].split("<-")
            global lookup
            self.s = s[1].replace(" ", "")
            self.idx = 0
            lookup[s[0].replace(" ", "")] = self.E()
        else:
            self.s, self.idx = self.s.replace(" ", ""), 0
            print(self.E())
        
class parser:
    def __init__(self, s):
        if s.startswith("computation "):
            s = s[12:]
        self.list = s.split(";")
        self.list[-1] = self.list[-1].split(".")[0]
        self.lidx = 0
    
    def computation(self):
        while self.lidx < len(self.list):
            t = tokenizer(self.list[self.lidx])
            t.process()
            self.lidx += 1
s = input("Enter your input")
# s = "computation var i <- 2 * 3; var abracadabra <- 7; i - 5 - 1 ; (((abracadabra * i))) . "
p = parser(s)
p.computation()
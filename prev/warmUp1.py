s = input("Enter your input: ")
# s = "1   +2    *(3+4) . 7 * 6 ."
s = s.replace(" ", "")
idx = 0

def factor():
    global idx
    res = 0
    if s[idx] == "(":
        idx += 1
        res = expression()
    elif s[idx].isdigit():
        res = idx
        while(s[idx].isdigit()):
            idx += 1
        res = int(s[res:idx])
    return res
        
def term():
    global idx
    res = factor()
    while(s[idx] == "*" or s[idx]=="/"):
        mul = (s[idx] == "*")
        idx += 1
        
        if mul:
            res *= factor()
        else:
            res /= factor()
    return res

def expression():
    global idx
    res = term()
    while(s[idx] == '+' or s[idx] == "-"):
        plus = (s[idx] == "+")
        idx += 1
        if plus:
            res += term()
        else:
            res -= term()
    return res

def computation():
    global idx
    while idx < len(s):
        print(expression())
        idx += 2
    
computation()
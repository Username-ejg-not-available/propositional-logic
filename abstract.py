from console import Console as c

props = {}

class Logic:
    def __init__(self): pass
    def asStr(self,top: bool=True) -> str: pass
    def solve(self, ps) -> bool: pass
    def isSame(self,other) -> bool: pass
    def size(self) -> int: pass

class And(Logic):
    def __init__(self,o1: Logic,o2: Logic):
        self.op1 = o1
        self.op2 = o2
    def asStr(self,top: bool=True) -> str:
        if top: return self.op1.asStr(False) + "&" + self.op2.asStr(False)
        else: return "(" + self.op1.asStr(False) + "&" + self.op2.asStr(False) + ")"
    def solve(self, ps) -> bool: 
        s1 = self.op1.solve(ps)
        s2 = self.op2.solve(ps)
        return s1 and s2
    def isSame(self,other: Logic) -> bool:
        return isinstance(other,And) and self.op1.isSame(other.op1) and self.op2.isSame(other.op2)
    def size(self) -> int: 
        return 1 + self.op1.size() + self.op2.size()

class Or(Logic):
    def __init__(self,o1: Logic,o2: Logic):
        self.op1 = o1
        self.op2 = o2
    def asStr(self,top: bool=True) -> str:
        if top: return self.op1.asStr(False) + "|" + self.op2.asStr(False)
        else: return "(" + self.op1.asStr(False) + "|" + self.op2.asStr(False) + ")"
    def solve(self, ps) -> bool: 
        s1 = self.op1.solve(ps)
        s2 = self.op2.solve(ps)
        return s1 or s2
    def isSame(self,other) -> bool:
        return isinstance(other,Or) and self.op1.isSame(other.op1) and self.op2.isSame(other.op2)
    def size(self) -> int: 
        return 1 + self.op1.size() + self.op2.size()

class Xor(Logic):
    def __init__(self,o1: Logic,o2: Logic):
        self.op1 = o1
        self.op2 = o2
    def asStr(self,top: bool=True) -> str:
        if top: return self.op1.asStr(False) + "^" + self.op2.asStr(False)
        else: return "(" + self.op1.asStr(False) + "^" + self.op2.asStr(False) + ")"
    def solve(self, ps) -> bool: 
        s1 = self.op1.solve(ps)
        s2 = self.op2.solve(ps)
        return (s1 and not s2) or (not s1 and s2)
    def isSame(self,other) -> bool:
        return isinstance(other,Xor) and self.op1.isSame(other.op1) and self.op2.isSame(other.op2)
    def size(self) -> int: 
        return 1 + self.op1.size() + self.op2.size()

class Not(Logic):
    def __init__(self,o1: Logic):
        self.op = o1
    def asStr(self,top:bool=True)->str:
        if top: return "~"+self.op.asStr(False)
        return "(~" + self.op.asStr(False) + ")"
    def solve(self, ps) -> bool: 
        s = self.op.solve(ps)
        return not s
    def isSame(self,other) -> bool:
        return isinstance(other,Not) and self.op.isSame(other.op)
    def size(self) -> int: 
        return 1 + self.op.size()

class If(Logic):
    def __init__(self,o1: Logic,o2: Logic):
        self.op1 = o1
        self.op2 = o2
    def asStr(self,top: bool=True) -> str:
        if top: return self.op1.asStr(False) + "->" + self.op2.asStr(False)
        else: return "(" + self.op1.asStr(False) + "->" + self.op2.asStr(False) + ")"
    def solve(self, ps) -> bool: 
        s1 = self.op1.solve(ps)
        s2 = self.op2.solve(ps)
        return (not s1) or s2
    def isSame(self,other) -> bool:
        return isinstance(other,If) and self.op1.isSame(other.op1) and self.op2.isSame(other.op2)
    def size(self) -> int: 
        return 1 + self.op1.size() + self.op2.size()

class Iff(Logic):
    def __init__(self,o1: Logic,o2: Logic):
        self.op1 = o1
        self.op2 = o2
    def asStr(self,top: bool=True) -> str:
        if top: return self.op1.asStr(False) + "<->" + self.op2.asStr(False)
        else: return "(" + self.op1.asStr(False) + "<->" + self.op2.asStr(False) + ")"
    def solve(self, ps) -> bool: 
        s1 = self.op1.solve(ps)
        s2 = self.op2.solve(ps)
        return (not s1 or s2) and (s1 or not s2)
    def isSame(self,other) -> bool:
        return isinstance(other,Iff) and self.op1.isSame(other.op1) and self.op2.isSame(other.op2)
    def size(self) -> int: 
        return 1 + self.op1.size() + self.op2.size()

class Prop(Logic):
    def __init__(self, letter):
        self.l = letter
    def asStr(self,top:bool=True) -> str:
        return self.l
    def solve(self,ps) -> bool:
        return ps[self.l] == 'T'
    def isSame(self,other) -> bool:
        return other == self
    def size(self) -> int: 
        return 1

class Bool(Logic):
    def __init__(self, b: bool):
        self.b = b
    def asStr(self,top:bool=True) -> str:
        if self.b: return "_T"
        return "_F"
    def solve(self,ps) -> bool:
        return self.b
    def isSame(self,other) -> bool:
        return isinstance(other,Bool) and self.b == other.b
    def size(self) -> int: 
        return 1

def makeProp(letter: str) -> Logic:
    if letter not in props: props[letter] = Prop(letter)
    return props[letter]

def copytree(tree: Logic) -> Logic:
    match tree:
        case Prop(l=x): return makeProp(x)
        case Bool(): return Bool(tree.b)
        case Not(op=x): return Not(copytree(x))
        case _: 
            return tree.__class__(copytree(tree.op1),copytree(tree.op2))

def getProps(tree: Logic):
    match tree:
        case Prop(l=x): return [x]
        case Bool(): return []
        case Not(op=x): return getProps(tree.op)
        case _: return list(set(getProps(tree.op1) + getProps(tree.op2)))

class ForAll(Logic):
    def __init__(self,p: Logic,o: Logic):
        self.op1 = p
        self.op2 = o
    def asStr(self) -> str:
        return "_A"+self.op1.asStr()+"(" + self.op2.asStr() + ")"
    def solve(self,ps) -> bool:
        return False
    def isSame(self,other) -> bool:
        return isinstance(other,ForAll) and self.op1.isSame(other.op1) and self.op2.isSame(other.op2)
    def size(self) -> int: 
        return 1 + self.op2.size()

class Exists(Logic):
    def __init__(self,p: Logic,o: Logic):
        self.op1 = p
        self.op2 = o
    def asStr(self) -> str:
        return "_E"+self.op1.asStr()+"(" + self.op2.asStr() + ")"
    def solve(self,ps) -> bool:
        return True
    def isSame(self,other) -> bool:
        return isinstance(other,Exists) and self.op1.isSame(other.op1) and self.op2.isSame(other.op2)
    def size(self) -> int: 
        return 1 + self.op2.size()
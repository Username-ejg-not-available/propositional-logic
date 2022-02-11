import abstract as ab
import truthtable as tt

def reduce(treestr: str, show: bool) -> ab.Logic:
    table = tt.Table(treestr)
    treecopy = None
    while treecopy == None or not table.tree.isSame(treecopy):
        treecopy = ab.copytree(table.tree)
        table.tree = _rTrueFalse(table.tree, show)
        table.tree = _SimpleMatch(table.tree,show,table.props)
        table.tree = _rMatch(table.tree, show)
    return table.tree

def rec(table: tt.Table,show: bool,func) -> ab.Logic:
    match table.tree:
        case ab.Prop(): pass
        case ab.Bool(): pass
        case ab.Not():
            table.tree.op = func(table.tree.op,show)
        case _:
            table.tree.op1 = func(table.tree.op1,show)
            table.tree.op2 = func(table.tree.op2,show)
    return table.tree

def _rTrueFalse(tree: ab.Logic, show: bool) -> ab.Logic:
    if isinstance(tree,ab.Bool): return ab.Bool(tree.asStr() == '_T')
    table = tt.Table(tree)
    if not (False in table.table): 
        if show: print("Reduced",tree.asStr(),"to TRUE")
        return ab.Bool(True)
    elif not (True in table.table): 
        if show: print("Reduced",tree.asStr(),"to FALSE")
        return ab.Bool(False)
    else: 
        return rec(table,show,_rTrueFalse)

def _rMatch(tree: ab.Logic, show: bool) -> ab.Logic:
    table = tt.Table(tree)
    treestr = tree.asStr()
    match tree:
        case ab.Or(op1=x,op2=ab.And(op1=y,op2=z)) if x.isSame(y) or x.isSame(z):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Absorption Law: p|(p&q) == p")
            return x
        case ab.Or(op2=x,op1=ab.And(op1=y,op2=z)) if x.isSame(y) or x.isSame(z):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Absorption Law: (p&q)|p == p")
            return x
        case ab.And(op1=x,op2=ab.Or(op1=y,op2=z)) if x.isSame(y) or x.isSame(z):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Absorption Law: p&(p|q) == p")
            return x
        case ab.And(op2=x,op1=ab.Or(op1=y,op2=z)) if x.isSame(y) or x.isSame(z):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Absorption Law: p&(p|q) == p")
            return x
        case ab.And(op1=x,op2=y) if x.isSame(y):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Idempotent Law: p&p == p")
            return x
        case ab.Or(op1=x,op2=y) if x.isSame(y):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Idempotent Law: p|p == p")
            return x
        case ab.And(op1=x,op2=ab.Bool(b=True)):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Identity Law: p&_T == p")
            return x
        case ab.Or(op1=x,op2=ab.Bool(b=False)):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Domination Law: p|_F = p")
            return x
        case ab.And(op2=x,op1=ab.Bool(b=True)):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Identity Law: _T&p == p")
            return x
        case ab.Or(op2=x,op1=ab.Bool(b=False)):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Domination Law: _F|p = p")
            return x
        case ab.Not(op=ab.Not(op=x)):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Double Negation Law: ~(~p) == p")
            return x
        case ab.Xor(op1=ab.Bool(b=True),op2=x):
            ch = ab.Not(x)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: _T^p == ~p")
            return ch
        case ab.Xor(op2=ab.Bool(b=True),op1=x):
            ch = ab.Not(x)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: p^_T == ~p")
            return ch
        case ab.Xor(op1=ab.Bool(b=False),op2=x):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Domination Law: _F^p == p")
            return x
        case ab.Xor(op1=ab.Bool(b=False),op2=x):
            if show: print("Reduced",treestr,"to",x.asStr(),"by Domination Law: p^_F == p")
            return x
        case ab.Iff(op1=x,op2=ab.Bool(b=False)):
            ch = ab.Not(x)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: p<->_F == ~p")
            return ch
        case ab.Iff(op2=x,op1=ab.Bool(b=False)):
            ch = ab.Not(x)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: _F<->p == ~p")
            return ch
        case ab.Iff(op1=x,op2=ab.Bool(b=True)):
            if show: print("Reduced",treestr,"to",x.asStr(),"by ??? Law: p<->_T == p")
            return x
        case ab.Iff(op2=x,op1=ab.Bool(b=True)):
            if show: print("Reduced",treestr,"to",x.asStr(),"by ??? Law: _T<->p == p")
            return x
        case ab.If(op1=x,op2=ab.Bool(b=False)):
            ch = ab.Not(x)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: p->_F == ~p")
            return ch
        case ab.If(op2=x,op1=ab.Bool(b=True)):
            if show: print("Reduced",treestr,"to",x.asStr(),"by ??? Law: _T->p == p")
            return x
        case ab.Not(op=ab.Iff(op1=x,op2=y)):
            ch = ab.Xor(x,y)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: ~(p<->q) == p^q")
            return ch
        case ab.If(op1=ab.Not(op=x),op2=y):
            ch = ab.Or(x,y)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (~p)->q == p|q")
            return ch
        case ab.Iff(op1=x,op2=ab.If(op1=y,op2=z)) if x.isSame(y):
            ch = ab.And(y,z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: p<->(p->q) == p&q")
            return ch
        case ab.Iff(op2=x,op1=ab.If(op1=y,op2=z)) if x.isSame(y):
            ch = ab.And(y,z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (p->q)<->p == p&q")
            return ch
        case ab.Xor(op1=x,op2=ab.Iff(op1=y,op2=z)) if x.isSame(y):
            ch = ab.Not(z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: p^(p<->q) == ~q")
            return ch
        case ab.Xor(op1=x,op2=ab.Iff(op1=z,op2=y)) if x.isSame(y):
            ch = ab.Not(z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: p^(q<->p) == ~q")
            return ch
        case ab.Xor(op2=x,op1=ab.Iff(op1=z,op2=y)) if x.isSame(y):
            ch = ab.Not(z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (q<->p)^p == ~q")
            return ch
        case ab.Xor(op2=x,op1=ab.Iff(op1=y,op2=z)) if x.isSame(y):
            ch = ab.Not(z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (p<->q)^p == ~q")
            return ch
        case ab.And(op1=x,op2=ab.Iff(op1=y,op2=z)) if x.isSame(y):
            ch = ab.And(y,z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: p&(p<->q) == p&q")
            return ch
        case ab.And(op1=x,op2=ab.Iff(op1=z,op2=y)) if x.isSame(y):
            ch = ab.And(y,z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: p&(q<->p) == p&q")
            return ch
        case ab.And(op2=x,op1=ab.Iff(op1=z,op2=y)) if x.isSame(y):
            ch = ab.And(y,z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (q<->p)&p == p&q")
            return ch
        case ab.And(op2=x,op1=ab.Iff(op1=y,op2=z)) if x.isSame(y):
            ch = ab.And(y,z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (p<->q)&p == p&q")
            return ch
        case ab.Iff(op1=ab.Not(op=x),op2=ab.Not(op=y)):
            ch = ab.Iff(x,y)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (~p)<->(~q) == p<->q")
            return ch
        case ab.And(op1=ab.And(op1=w,op2=x),op2=ab.And(op1=y,op2=z)) if w.isSame(y) or x.isSame(y):
            ch = ab.And(ab.And(w,x),z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (p&q)&(p&r) == (p&q)&r")
            return ch
        case ab.And(op1=ab.And(op1=w,op2=x),op2=ab.And(op1=y,op2=z)) if w.isSame(z) or x.isSame(z):
            ch = ab.And(ab.And(w,x),y)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (p&q)&(r&p) == (p&q)&r")
            return ch
        case ab.Or(op1=ab.Or(op1=w,op2=x),op2=ab.Or(op1=y,op2=z)) if w.isSame(y) or x.isSame(y):
            ch = ab.Or(ab.Or(w,x),z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (p&q)&(p&r) == (p&q)&r")
            return ch
        case ab.Or(op1=ab.Or(op1=w,op2=x),op2=ab.Or(op1=y,op2=z)) if w.isSame(z) or x.isSame(z):
            ch = ab.Or(ab.Or(w,x),y)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (p|q)|(r|p) == (p|q)|r")
            return ch
        case ab.If(op1=ab.And(op1=w,op2=x),op2=ab.And(op1=y,op2=z)) if w.isSame(z) or x.isSame(z):
            ch = ab.If(ab.And(w,x),y)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (p&q)->(p&r) == (p&q)->r")
            return ch
        case ab.If(op1=ab.And(op1=w,op2=x),op2=ab.And(op1=y,op2=z)) if w.isSame(y) or x.isSame(y):
            ch = ab.If(ab.And(w,x),z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (p&q)->(p&r) == (p&q)->r")
            return ch
        case ab.If(op1=ab.Or(op1=w,op2=x),op2=ab.Or(op1=y,op2=z)) if y.isSame(x) or z.isSame(x):
            ch = ab.If(w,ab.Or(y,z))
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (p|q)->(p|r) == q->(p|r)")
            return ch
        case ab.If(op1=ab.And(op1=w,op2=x),op2=ab.And(op1=y,op2=z)) if w.isSame(y) or z.isSame(w):
            ch = ab.If(x,ab.Or(y,z))
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (p|q)->(p|r) == q->(p|r)")
            return ch
        case ab.Xor(op1=ab.Xor(op1=w,op2=x),op2=ab.Xor(op1=y,op2=z)) if w.isSame(y):
            ch = ab.Xor(x,z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (a^b)^(a^c) == b^c")
            return ch
        case ab.Xor(op1=ab.Xor(op1=w,op2=x),op2=ab.Xor(op1=y,op2=z)) if w.isSame(z):
            ch = ab.Xor(x,y)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (a^b)^(a^c) == b^c")
            return ch
        case ab.Xor(op1=ab.Xor(op1=w,op2=x),op2=ab.Xor(op1=y,op2=z)) if x.isSame(y):
            ch = ab.Xor(w,z)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (a^b)^(a^c) == b^c")
            return ch
        case ab.Xor(op1=ab.Xor(op1=w,op2=x),op2=ab.Xor(op1=y,op2=z)) if x.isSame(z):
            ch = ab.Xor(w,y)
            if show: print("Reduced",treestr,"to",ch.asStr(),"by ??? Law: (a^b)^(a^c) == b^c")
            return ch
        case ab.Xor(op1=x,op2=ab.Xor(op1=y,op2=z)) if x.isSame(y):
            if show: print("Reduced",treestr,"to",z.asStr(),"by ??? Law: p^(p^q) == q")
            return z
        case ab.Xor(op1=x,op2=ab.Xor(op1=y,op2=z)) if x.isSame(z):
            if show: print("Reduced",treestr,"to",y.asStr(),"by ??? Law: p^(q^p) == q")
            return y
        case ab.Xor(op2=x,op1=ab.Xor(op1=y,op2=z)) if x.isSame(y):
            if show: print("Reduced",treestr,"to",z.asStr(),"by ??? Law: (p^q)^p == q")
            return z
        case ab.Xor(op2=x,op1=ab.Xor(op1=y,op2=z)) if x.isSame(z):
            if show: print("Reduced",treestr,"to",y.asStr(),"by ??? Law: (q^p)^p == q")
            return y
        case _: 
            return rec(table,show,_rMatch)

def _SimpleMatch(tree: ab.Logic, show: bool, props) -> ab.Logic:
    table = tt.Table(tree,props)
    treestr = tree.asStr()
    # generate permutations of all expressions using all props, attempt equiv, recurse
    # make sure to use .isSame to make sure you dont reduce simple to simple
    match tree:
        case ab.Prop(): return tree
        case ab.Bool(): return tree
        case _:
            ch = None
            for p in props:
                ch = ab.makeProp(p)
                if not ch.isSame(tree) and tt.equiv(p, treestr): break
                ch = ab.Not(ch)
                if not ch.isSame(tree) and tt.equiv("~"+p,treestr): break
                f = False
                for q in props:
                    if p == q: continue
                    ch = ab.And(ab.makeProp(p),ab.makeProp(q))
                    ch2 = ab.And(ab.makeProp(q),ab.makeProp(p))
                    if not (ch.isSame(tree) or ch2.isSame(tree)) and tt.equiv(p+"&"+q,treestr): 
                        f = True
                        break
                    ch = ab.Or(ab.makeProp(p),ab.makeProp(q))
                    ch2 = ab.Or(ab.makeProp(q),ab.makeProp(p))
                    if not (ch.isSame(table.tree) or ch2.isSame(table.tree)) and tt.equiv(p+"|"+q,treestr): 
                        f = True
                        break
                    ch = ab.Xor(ab.makeProp(p),ab.makeProp(q))
                    ch2 = ab.Xor(ab.makeProp(q),ab.makeProp(p))
                    if not (ch.isSame(table.tree) or ch2.isSame(table.tree)) and tt.equiv(p+"^"+q,treestr): 
                        f = True
                        break
                    ch = ab.If(ab.makeProp(p),ab.makeProp(q))
                    if not ch.isSame(table.tree) and tt.equiv(p+"->"+q,treestr): 
                        f = True
                        break
                    ch = ab.Iff(ab.makeProp(p),ab.makeProp(q))
                    ch2 = ab.Iff(ab.makeProp(q),ab.makeProp(p))
                    if not (ch.isSame(table.tree) or ch2.isSame(table.tree)) and tt.equiv(p+"<->"+q,treestr): 
                        f = True
                        break
                if f: break
            else:
                return rec(table,show,lambda x, y: _SimpleMatch(x,y,props))
            if show: print("Reduced",treestr,"to",ch.asStr(),"by Logical Equivalence")
            return ch
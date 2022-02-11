import reduce as r
import random

def genTree(max=5, props=['p','q','r']) -> r.ab.Logic:
    if max==0: 
        return random.choice([r.ab.makeProp(random.choice(props))])
    choices = [r.ab.Prop,r.ab.And,r.ab.Or,
                r.ab.Xor,r.ab.Not,r.ab.If,r.ab.Iff]
    muhtree = random.choice(choices)
    match muhtree:
        case r.ab.Prop: return r.ab.makeProp(random.choice(props))
        case r.ab.Bool: return r.ab.Bool(random.choice([True,False]))
        case r.ab.Not: return r.ab.Not(genTree(max-1,props))
        case _: pass
    return muhtree(genTree(max-1,props),genTree(max-1,props))

#tree = genTree(3,['a','b','c','d'])
tree = r.tt.lp.parse.Parser("((b<->b)->c)|((d->a)^(c&b))").parse()
print("Original Exp:",tree.asStr(),"\n\nOriginal Table:")
r.tt.Table(tree).printTable(True)
print("")
reducedTree = r.reduce(tree, True)
print("\nReduced Exp:",reducedTree.asStr(),"\n\nReduced Table:")
r.tt.Table(reducedTree).printTable(True)
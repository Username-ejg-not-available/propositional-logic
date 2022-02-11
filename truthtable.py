import logicparser as lp
import abstract as ab
from console import Console

class Table:
    def __init__(self,tree: str,altProps = []):
        if isinstance(tree,str): self.tree = lp.parse.Parser(tree).parse()
        else: self.tree = tree
        if altProps != []: self.props = sorted(altProps)
        else: self.props = sorted(ab.getProps(self.tree))
        self.combs = [{pr:"F" for pr in self.props}]
        self.table = [self.tree.solve(self.combs[0])]
        for x in range(1,2**len(self.combs[0])):
            temp = x
            self.combs.append({})
            for pr in self.props:
                if temp % 2 == 1: self.combs[-1][pr] = "T"
                else: self.combs[-1][pr] = "F"
                temp = int(temp / 2)
            self.table.append(self.tree.solve(self.combs[-1]))

    def printTable(self, verbose: bool):
        grid = [self.props] + [list(c.values()) for c in self.combs]
        def rec(t: ab.Logic,p) -> dict:
            match t:
                case ab.Prop(): return {}
                case ab.Bool(): return {}
                case ab.Not(op=x): 
                    r = rec(x,p)
                    r.update({
                        t.hwOut():list(map(lambda y: str(y),Table(t,p).table))
                    })
                    return r
                case _: 
                    r = rec(t.op1,p)
                    r.update(rec(t.op2,p))
                    r.update({
                        t.hwOut():list(map(lambda y: str(y),Table(t,p).table))
                    })
                    return r

        if verbose:
            r = rec(self.tree,self.props)
            for x in r:
                grid[0] += [x]
                for y in range(len(r[x])):
                    grid[y+1] += [r[x][y]]
        else:
            grid[0] += [self.tree.hwOut()]
            for x in range(len(self.table)):
                grid[x+1] += [str(self.table[x])]
        c = Console()
        c.grid(grid, True)

def equiv(inp1, inp2):
    return not (False in Table("("+inp1+")<->("+inp2+")").table)

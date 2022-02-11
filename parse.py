import lexer
import abstract as ab

STARTNONTERM = "\31"
start = ""
table = {}

class Parser:
    def __init__(self,tks: str):
        self.stack = [start]
        self.semstack = []
        self.lookahead = 0
        self.tkstream = lexer.lex.start(tks)

    def parse(self) -> ab.Logic:
        while len(self.stack) != 0:
            next = table[self.stack[0]][self.tkstream[self.lookahead]['symbol']]
            #accept
            if next == "accept":
                if len(self.semstack)>0: return self.semstack[0]
                else: 
                    print("CRINGE! Parse error: empty sem stack")
                    exit(1)
            #failure
            elif next == None:
                print("Parse error: cringe token " + str(self.tkstream[self.lookahead]))
                exit(1)
            #shift/goto
            elif isinstance(next,str):
                self.attemptSem()
                self.stack = [next] + self.stack
                self.lookahead += 1
            #reduce
            else:
                self.attemptSem()
                self.stack = [table[self.stack[next[1]]][next[0]]] + self.stack[next[1]:]
        print("Parse Error: unexpected EOF")
        exit(1)
    
    def attemptSem(self) -> None:
        if self.stack[0] == 'term ::= PROP ● ': 
            self.semstack = [ab.makeProp(self.tkstream[self.lookahead-1]["lexeme"])] + self.semstack
        elif self.stack[0] == 'term ::= BOOL ● ':
            self.semstack = [ab.Bool(self.tkstream[self.lookahead-1]["lexeme"]=='_T')] + self.semstack
        elif self.stack[0] == 'd ::= term AND e ● ':
            exp = self.semstack[0]
            term = self.semstack[1]
            self.semstack = [ab.And(term,exp)] + self.semstack[2:]
        elif self.stack[0] == 'b ::= term OR c ● ':
            exp = self.semstack[0]
            term = self.semstack[1]
            self.semstack = [ab.Or(term,exp)] + self.semstack[2:]
        elif self.stack[0] == 'c ::= term XOR d ● ':
            exp = self.semstack[0]
            term = self.semstack[1]
            self.semstack = [ab.Xor(term,exp)] + self.semstack[2:]
        elif self.stack[0] == 'e ::= NOT f ● ':
            term = self.semstack[0]
            self.semstack = [ab.Not(term)] + self.semstack[1:]
        elif self.stack[0] == 'a ::= term IF b ● ':
            exp = self.semstack[0]
            term = self.semstack[1]
            self.semstack = [ab.If(term,exp)] + self.semstack[2:]
        elif self.stack[0] == 'exp ::= term IFF a ● ':
            exp = self.semstack[0]
            term = self.semstack[1]
            self.semstack = [ab.Iff(term,exp)] + self.semstack[2:]
        elif self.stack[0] == 'f ::= FORALL PROP ● term':
            self.semstack = [ab.makeProp(self.tkstream[self.lookahead-1]["lexeme"])] + self.semstack
        elif self.stack[0] == 'f ::= EXISTS PROP ● term':
            self.semstack = [ab.makeProp(self.tkstream[self.lookahead-1]["lexeme"])] + self.semstack
        elif self.stack[0] == 'f ::= FORALL PROP term ● ':
            term = self.semstack[0]
            prop = self.semstack[1]
            self.semstack = [ab.ForAll(prop,term)] + self.semstack[2:]
        elif self.stack[0] == 'f ::= EXISTS PROP term ● ':
            term = self.semstack[0]
            prop = self.semstack[1]
            self.semstack = [ab.Exists(prop,term)] + self.semstack[2:]
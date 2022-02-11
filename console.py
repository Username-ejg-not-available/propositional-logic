import shutil

class Console:
    # ANSI CODES
    ANSI_RESET_ALL = "\033[0m"
    ANSI_CLEAR_ALL = "\x1b[2J\x1b[1;1H"

    # ANSI Formatting Characters
    Format = {
        "BOLD": "\033[1m",
        "FAINT": "\033[2m",
        "RESET_WEIGHT": "\033[22m",
        "UNDERLINE": "\033[4m",
        "DOUBLE_UNDERLINE": "\033[21m",
        "RESET_UNDERLINE": "\033[24m",
        "INVERSE": "\033[7m",
        "RESET_INVERSE": "\033[27m",
        "OVERLINE": "\033[53m",
        "RESET_OVERLINE": "\033[55m",
        "ITALIC": "\033[3m",
        "CONCEAL": "\033[8m",
        "RESET_CONCEAL": "\033[28m",
        "STRIKE": "\033[9m",
    }

    # what the fuck
    ANSI_SLOW_BLINK = "\033[5m"
    ANSI_RESET_BLINK = "\033[25m"

    # ANSI Foreground Colors
    ForegroundColor = {
        "BLACK": "\033[30m",
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[33m",
        "BLUE": "\033[34m",
        "MAGENTA": "\033[35m",
        "CYAN": "\033[36m",
        "WHITE": "\033[37m",
        "RESET": "\033[39m",
    }

    # ANSI Background Colors
    BackgroundColor = {
        "BLACK": "\033[40m",
        "RED": "\033[41m",
        "GREEN": "\033[42m",
        "YELLOW": "\033[43m",
        "BLUE": "\033[44m",
        "MAGENTA": "\033[45m",
        "CYAN": "\033[46m",
        "WHITE": "\033[47m",
        "RESET": "\033[49m",
    }

    # Unicode Bars
    Bars = {
        "VERT": "│",
        "HORIZ": "─",
        "TOP_LEFT": "┌",
        "TOP_RIGHT": "┐",
        "BOTTOM_LEFT": "└",
        "BOTTOM_RIGHT": "┘",
        "LEFT_ROW_JOIN": "├",
        "RIGHT_ROW_JOIN": "┤",
        "TOP_COL_JOIN": "┬",
        "BOTTOM_COL_JOIN": "┴",
        "CENTER_JOIN": "┼",
        "BLOCK_FULL": "█",
    }
    def __init__(self) -> None: 
        self.fit_terminal()

    def fit_terminal(self) -> None:
        temp = shutil.get_terminal_size()
        self._vp_width = temp.columns
        self._vp_height = temp.lines

    def setBackgroundColor(self,color: str):
        if color in Console.BackgroundColor.keys(): print(Console.BackgroundColor[color])
        return self

    def setForegroundColor(self,color: str):
        if color in Console.ForegroundColor.keys(): print(Console.ForegroundColor[color])
        return self

    def addFormats(self,f):
        match f:
            case [_]:
                for x in f: 
                    if x in Console.Format.keys(): print(Console.Format[x])
            case _:
                if f in Console.Format.keys(): print(Console.Format[f])
        return self

    def reset(self):
        print(Console.ANSI_RESET_ALL)
        return self

    def pad_right(self,text: str, width: int, padding: str) -> str:
        pad_diff = width - len(text)
        if pad_diff < 1: return text
        temp = text
        for _ in range(int(pad_diff / len(padding))):
            temp += padding
        return temp

    def pad_left(self,text: str, width: int, padding: str) -> str:
        pad_diff = width - len(text)
        if pad_diff < 1: return text
        temp = text
        for _ in range(int(pad_diff / len(padding))):
            temp = padding + temp
        return temp

    def pad_center(self,text: str, width: int, padding: str) -> str:
        lw = int((width-len(text))/2) + len(text)
        return self.pad_right(self.pad_left(text,lw,padding),width,padding)

    def grid(self,gridvals,dynamic_width: bool = False):
        if gridvals == []: return
        numcols = max(map(lambda x: len(x),gridvals))
        if dynamic_width:
            colwidths = [0 for _ in range(numcols)]
            for y in range(numcols):
                for x in gridvals:
                    if len(x) <= y: continue
                    if len(x[y])+1 > colwidths[y]: colwidths[y] = len(x[y])+1
        else: colwidths = [(self._vp_width - numcols -1) / numcols for _ in range(numcols)]
        if colwidths == 0: return

        head = Console.Bars["TOP_LEFT"]
        for x in range(numcols):
            head += self.pad_right("",colwidths[x]-1,Console.Bars["HORIZ"])
            if x == numcols-1: head += Console.Bars["TOP_RIGHT"]
            else: head += Console.Bars["TOP_COL_JOIN"]
        print(head)
        for x in gridvals:
            row = ""
            for y in range(len(x)):
                row += Console.Bars["VERT"] + self.pad_center(x[y],colwidths[y]-1," ")
            if len(x) < numcols:
                for y in range(numcols - len(x)):
                    row += self.pad_right(Console.Bars["VERT"],colwidths[y+len(x)]," ")
            print(row + Console.Bars["VERT"])
        tail = Console.Bars["BOTTOM_LEFT"]
        for x in range(numcols):
            tail += self.pad_right("",colwidths[x]-1,Console.Bars["HORIZ"])
            if x == numcols-1: tail += Console.Bars["BOTTOM_RIGHT"]
            else: tail += Console.Bars["BOTTOM_COL_JOIN"]
        print(tail)
        return self

#c = Console()
#c.grid([["q","r","titty"],["zoinks"],["Jinkies","t"]], True)
import sys

TABSTOP = 8

class Line:
    def __init__(self, line):
        l = line.rstrip(" \t\r\n").expandtabs(TABSTOP)
        self.text = l.lstrip(" \t")
        self.tab = len(l) - len(self.text)
        self.sub = None
    def __str__(self):
        return " " * self.tab + self.text
    def __repr__(self):
        s = ":" + repr(self.sub) if self.sub is not None else ""
        return "<{tab}>'{text}'".format(tab = self.tab, text = self.text) + s

class TabException(Exception):
    def __init__(self, line, tab):
        Exception.__init__(self)
        self.line = line
        self.tab = tab
    def __str__(self):
        return "'" + str(self.line) + "'"
    def perror(self, file = sys.stderr):
        print(str(self.line), file = file)
        print(" " * self.tab + "^", file = file)
        print("Invalid indent", file = file, flush = True)

class Block:
    class _Source:
        def __init__(self, strings):
            self._iter = iter(strings)
            self.next()
        def peek(self):
            return self._line
        def next(self):
            while True:
                l = next(self._iter, None)
                self._line = Line(l) if l is not None else None
                if self._line is None or len(self._line.text) > 0: break
    def __init__(self, strings):
        root = type(strings) is not Block._Source
        if root:
            strings = Block._Source(strings)
        self.data = list()
        tab = strings.peek().tab
        while strings.peek() is not None:
            line = strings.peek()
            if line.tab < tab:
                break
            elif line.tab > tab:
                self.data[-1].sub = Block(strings)
                if strings.peek() is not None and strings.peek().tab > tab:
                    raise TabException(strings.peek(), tab)
            else:
                self.data.append(line)
                strings.next()
        if root and strings.peek() is not None:
            raise TabException(strings.peek(), tab)
    def __repr__(self):
        return "{" + ",".join([repr(x) for x in self.data]) + "}"


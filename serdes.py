#!/usr/bin/python

TAB = " "*4

TYPES = {
    "u8"    : "uint_fast8_t",
    "u16le" : "uint_fast16_t",
    "u16be" : "uint_fast16_t",
    "u32le" : "uint_fast32_t",
    "u32be" : "uint_fast32_t",
}

class Item:
    def __init__(self, name):
        self.name = name
        self.data = [ ]
    def write(self, out):
        # write struct
        out.write("\nstruct {name} {{\n".format(name = self.name))
        for n, t in self.data:
            ct = TYPES[t]
            out.write(TAB + "{type} {fld};\n".format(type = ct, fld = n))
        out.write("};\n")
        # write introspection
        out.write("\nconst struct _serdes {name} = {{\n".format(name = self.name))
        for n, t in self.data:
            fmt = { "name" : self.name, "fld" : n, "type" : t }
            out.write(TAB + "{{ _serdes_{type}, offsetof(struct {name}, {fld}) }},\n".format(**fmt))
        out.write("};\n");

def serdes(inp, out):
    item = None
    for line in inp:
        line = line.rstrip()
        if line == "": continue
        if line[0] not in (' ','\t'):
            if item is not None:
                item.write(out)
            item = Item(line)
        else:
            n, t = [ x.strip() for x in line.split(":") ]
            item.data.append((n, t))
    if item is not None:
        item.write(out)

if __name__ == "__main__":
    import sys
    serdes(sys.stdin, sys.stdout)


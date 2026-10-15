import re

def parse_moiety(m):
    """Return list of (mult, {el: n}, charge) for each moiety component."""
    res = []
    for part in re.split(r",(?![^()]*\))", m):
        part = part.strip()
        if not part:
            continue
        mult = 1.0
        mm = re.match(r"^([\d.]+)\((.*)\)n?$", part)
        if mm:
            mult = float(mm.group(1)); part = mm.group(2)
        part = re.sub(r"^\((.*)\)n$", r"\1", part)
        ch = 0
        cm = re.search(r"(\d*)([+-])$", part)
        if cm:
            ch = int(cm.group(1) or 1) * (1 if cm.group(2) == "+" else -1)
            part = part[:cm.start()].strip()
        comp = {}
        for e, n in re.findall(r"([A-Z][a-z]?)([\d.]+)", part):
            comp[e] = comp.get(e, 0) + float(n)
        res.append((mult, comp, ch))
    return res



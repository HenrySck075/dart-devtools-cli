from textual.widgets import Tree

def dicttree(d:dict):
    t = Tree("JSON data")
    t.root.expand()

    q = [(t.root, d)]

    while len(q)!=0:
        i = q[0]

        n = i[0]
        c = i[1]
        for k,v in c.items():
            if type(v) not in [dict, list]: n.add_leaf(f"[b]{k}[/b]: {str(v)}")
            if type(v) == list:
                v = dict(enumerate(v))
            if type(v) == dict:
                q.append((n.add(f"[b]{k}[/b]: {str(v)}"),v))

        q.pop(0)
    
    return t

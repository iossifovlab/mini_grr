import gzip
from collections import defaultdict


data = defaultdict(list)
F = gzip.open("/mnt/wigtop1/data/unsafe/iossifov/sfari_grr/dbNSFPv4.4a/dbNSFP4.4a.gz", "rt")
hcs = F.readline().strip("\n\r").split("\t")
for li,l in enumerate(F):
    cs = l.strip("\n\r").split("\t")
    assert len(cs) == len(hcs)

    for c,v in zip(hcs, cs):
        data[c].append(v)
    if li > 100:
        break
F.close()


def infer_type(values):
    ## consider int
    give_up_ints = False
    n_int = 0
    for v in values:
        if give_up_ints:
            break
        try:
            vi = int(v)
            n_int += 1
        except ValueError:
            try:
                vf = float(v)
                give_up_ints = True
            except ValueError:
                pass
    if not give_up_ints:
        if n_int/len(values) > 0.95:
            return "int"
        else:
            return "str"

    n_floats = 0
    for v in values:
        try:
            vf = int(v)
            n_floats += 1
        except ValueError:
            pass
    if n_floats/len(values) > 0.95:
            return "float"
        else:
            return "str"
# python tools/generate_chebyshev_tables.py ~/_code/pytrt/tools/python/qs/cgvalues.json
import json
from itertools import izip

def print_values( filename ):
    with open(filename, 'rU') as f:
        data = json.load(f)

    vals = data['contents']
    ordinates = data['ordinates']

    titles = []
    contents = []
    for n in vals[:-1]:
        titles.append( r"\multicolumn{2}{c}{$N=%d$, $w=\pi / %d$ }" % (
            n, n / 2) )
        lines = []
        for (i, omega) in enumerate(ordinates[str(n)]):
            lines.append( r"$\omega_{%d}$ & ${}=%.16f$" % (i, omega) )
        contents.append( lines )

    filename = "cheby.tex"
    with open("cheby.tex", 'w') as f:
        f.write( r"\begin{tabular}{l@{}l}" )
        for (t,c) in izip(titles, contents):
            f.write( " \\toprule\n" + t)
            f.write( " \\\\ \\midrule\n")
            f.write( " \\\\\n".join(c) )
            f.write( " \\\\" )
        f.write( " \\bottomrule\n\\end{tabular}\n")

    print "Wrote table:"
    print "\\input{" + filename + "}"

#******************************************************************************#
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "syntax: %s cgvalues.json" % sys.argv[0]
        sys.exit(1)

    print_values( sys.argv[1])



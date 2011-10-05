#! /usr/bin/env python

# update_gnuplot_loc.py
# Seth R. Johnson
#
# Modify gnuplot output, relinking symbolic links and changing the absolute path
# in the .tex files.
import os
import re
from glob import glob

_tex_include_command = r'\includegraphics{%s}'
_re_includepath = re.compile( _tex_include_command.replace('\\', r'\\')
        % "(.*?)" )


def recursive_stuff( base ):
    for (root, dirs, files) in os.walk( base ):
        for filename in files:
            filename = os.path.join(root, filename)
            if os.path.islink( filename ):
                print "Modifying symlink:", filename
                #rewrite_symlink( filename )
            elif is_gnuplot_output( filename ):
                print "Modifying TeX file:", filename
                rewrite_tex( filename)

def is_gnuplot_output( filename ):
    with open(filename, 'r') as f:
        line = next(iter(f))
        return line.startswith("% GNUPLOT: LaTeX picture")

def rewrite_symlink( filename ):
    (dirname, texname) = os.path.split( os.readlink( filename ) )
    src = os.path.abspath(
            os.path.join( os.path.split( filename )[0], texname ) )
    print "Relinking %s to %s" % (filename, src)

    new_filename = filename + "~"

    os.symlink( src, new_filename)
    os.remove(filename)
    os.rename(new_filename, filename)

def rewrite_tex( filename ):
    picname = os.path.splitext(filename)[0]
    (root, picname) = os.path.split(picname)

    if picname == "plot":
        picname = glob( os.path.join( root, "*.pdf") )[0]
        picname = os.path.splitext(picname)[0]
    else:
        picname = os.path.join(root, picname)

    picname = os.path.abspath( picname )
    print picname

    new_filename = filename + "~"

    with open(filename, "r") as old:
        with open(new_filename, "w") as new:
            for line in old:
                m = _re_includepath.search( line )
                if m:
                    line = (line[:m.start()]
                            + _tex_include_command % picname
                            + line[m.end():] )
                new.write(line)

    os.remove(filename)
    os.rename(new_filename, filename)

################################################################################
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "%s BASE_DIR" % sys.argv[0]
        sys.exit(1)

    base = sys.argv[1]
    recursive_stuff( base)

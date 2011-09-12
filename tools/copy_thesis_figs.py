import os
import shutil
import re

_tex_include_command = r'\includegraphics{%s}'
_re_includepath = re.compile( _tex_include_command.replace('\\', r'\\')
        % "(.*?)" )

class ResearchCopier( object):
    def __init__(self, oldroot, newroot):
        """ Init with _research/figures, _thesis/figures"""
        self.oldroot = os.path.abspath( oldroot )
        self.newroot = os.path.abspath( newroot )

    def run(self):
        for (root, dirs, files) in os.walk( self.oldroot ):
            for filename in files:
                if os.path.islink( os.path.join(root, filename) ):
                    self.handle_symlink( root, filename, isdir=False)
            for filename in dirs:
                if os.path.islink( os.path.join(root, filename) ):
                    self.handle_symlink( root, filename, isdir=True )

    def handle_symlink(self, root, filename, isdir=False):
        old_path = os.path.join(root, filename)
        new_path = old_path.replace( self.oldroot, self.newroot)

        original = os.path.abspath( os.path.join( root,
                            os.readlink( old_path ) ) )
        #print "symlink at", old_path
        #print "corresponds to", new_path
        #print "original link:", original
        if isdir:
            # assume it's a gnuplot thing:
            # - replace symlink with folder
            # - copy original enclosed pdf and tex to the new folder
            # - rename the tex file to plot.tex
            # - rewrite the tex file to have the correct PDF pointer
            moved_folder = False
            try:
                os.rename(new_path, new_path + "~")
                moved_folder = True
            except OSError, e:
                pass
            os.mkdir(new_path)
            if moved_folder:
                shutil.rmtree(new_path + "~" )

            texname = os.path.split( original )[1]

            # COPY PDF AS-IS
            new_pdf_name = os.path.join( new_path, texname + ".pdf")
            shutil.copy2(
                    os.path.join( original, texname + ".pdf"),
                    new_pdf_name,
                    )

            # RENAME TEX FILE
            new_tex_name = os.path.join( new_path, "plot.tex")
            shutil.copy2(
                    os.path.join( original, texname + ".tex"),
                    new_tex_name,
                    )
            print "new tex file:", new_tex_name
            rewrite_tex( new_tex_name, new_pdf_name)

        else:
            # it's an image, etc.
            # - replace the symlink with a copy of the orginal file
            try:
                os.remove( new_path )
            except OSError, e:
                print e
            shutil.copy2( original, new_path )

def rewrite_tex( filename, pdf_path ):
    new_filename = filename + "~"

    with open(filename, "r") as old:
        with open(new_filename, "w") as new:
            for line in old:
                m = _re_includepath.search( line )
                if m:
                    line = (line[:m.start()]
                            + _tex_include_command % pdf_path
                            + line[m.end():] )
                new.write(line)

    os.remove(filename)
    os.rename(new_filename, filename)

################################################################################
if __name__ == "__main__":
    oldroot = "/Users/seth/_research/figures"
    newroot = "/Users/seth/_thesis/figures"

#    import sys
#    if len(sys.argv) != 3:
#        print "%s oldroot newroot" % sys.argv[0]
#        sys.exit(1)
#
#    (oldroot, newroot) = sys.argv[1:]
    rc = ResearchCopier(oldroot, newroot)
    rc.run()


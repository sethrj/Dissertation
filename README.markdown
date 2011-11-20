Compiling the thesis
--------------------

There are several support files necessary to compile the thesis, and a number
of paths are hardcoded. You will need to edit some text files to get this to
work.

First, open `texmf/tex/latex/srj/SRJinclude.tex` and scroll down to where it
defines the command `\setSRJthesisfigurepaths`. Change these hardcoded paths to
the path of *your* figures directory. Save and exit.

Next, in the Terminal, go to the root directory. Run the following command:

    python tools/update_gnuplot_loc.py figures

This updates the Gnuplot paths stored in the figures directory.

Finally, add the bibliography and style files in the `texmf` folder to your
`texmf` folder. On a Mac, if you haven't got one set up already, and you're using the standard MacTeX distribution, just run the following command:

    ln -s $(pwd)/texmf ~/Library/texmf

Now go to the thesis directory, type `make` (if you're on a Mac), and hopefully
it will work! (It actually probably won't, because you don't have
[Skim](http://skim-app.sourceforge.net/) installed.)

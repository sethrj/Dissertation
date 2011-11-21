# Plot thesis lengths from your advisor
# Seth R Johnson
import matplotlib.pyplot as plt
from itertools import izip
zip = izip

data = """
Paul Nowak 1988 191 *
Tareq Aboalfaraj 1989 133 -
Kassem Khattab 1989 160 -
Robert Rulko 1991 153 -
Todd Wareing 1991 222 -
Kasem Abotel 1993 169 -
Todd Palmer 1993 270 -
Moaied Miften 1994 147 -
Todd Urbatsch 1995 157 -
Bob Grove 1996 138 -
Scott Turner 1996 110 -
Patrick Brantley 1998 249 -
Brian Franke 1999 175 -
Carla Barrett 1999 183 -
Danny Tolar 1999 209 -
Marc Cooper 1999 202 -
Christopher Leakeas 1999 233 -
Jeff Densmore 2002 173 -
Heath Hanshaw 2005 188 -
Allan Wollaber 2008 273 *
Troy Becker 2009 247 *
Gregory Davidson 2010 319 *
Emily Wolters 2011.1 218 *
Jinan Yang 2011.3 238 -
Seth Johnson 2011.95 208 -
"""[1:-1].split('\n')
#Radiation therapy-type stuff:
# Philip Tchou 2007 160 *
#Non-NERS students:
# Richard Vasques 2009 123 -

data = [ line.split() for line in data]
data = sorted(data, key=lambda x: x[2])
print "\n".join( " ".join(items) for items in data)

names = []
years = []
pages = []
onehalfed = []

for (first, last, year, page, double) in data:
    names.append( last )
    years.append( float(year) )

    onehalf = (double == "*")
    onehalfed.append( onehalf)

    page = int(page)
    if onehalf:
        # convert one-and-a-half spaced to double spaced equivalent
        # based on my dissertation
        page = int( page * float(208) / 170 )
    pages.append( page )

fig = plt.figure(figsize=(8,6), dpi=150)
ax = fig.add_axes( [.1,.1,.8,.8] )
(x,y) = zip( *((x,y) for (x,y,z) in zip(years, pages, onehalfed) if z))
ax.plot( x, y, 'ro', mfc='none', mec='r', label="1.5-spaced")
(x,y) = zip( *((x,y) for (x,y,z) in zip(years, pages, onehalfed) if not z))
ax.plot( x, y, 'kx', label="double-spaced")
ax.legend(loc="best")

for (year, page, last) in zip(years, pages, names):
    ax.text( year, page, last, ha='left', va='top')

ax.set_xlabel('Year')
ax.set_title('Larsen NERS student dissertation lengths')
ax.set_ylabel('Double-spaced page equivalent')
ax.set_ylim(0,None)
plt.draw()
raw_input('press enter to exit')

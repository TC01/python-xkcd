xkcd v2.0 - A Python interface to xkcd.com
By Ben Rosser
Released under MIT License (see LICENSE.txt)

This is a Python library for accessing and retrieving links to comics from the
xkcd webcomic by Randall Munroe. It is NOT endorsed or made by him, it's an
entirely independent project.

It makes use of the JSON interface to Randall's site to retrieve comic data.
One can create comic objects manually using Comic(number), or can use the helper
functions provided- getLatestComic(), getRandomComic(), and getComic()- to do
this. Once you have a Comic object, you can access data from it using various
provided methods.

-------------------------------------------------------------------------------

Documentation:

I will eventually get around to generating some proper HTML docs for the module,
but in the mean time here's the output of "pydoc xkcd":

-------------------------------------------------------------------------------

NAME
    xkcd - Python library for accessing xkcd.com

FILE
    /usr/lib/python2.7/site-packages/xkcd.py

DESCRIPTION
    This is a Python library for accessing and retrieving links to comics from
    the xkcd webcomic by Randall Munroe. It is NOT endorsed or made by him, it's
    an entirely independent project.
    
    It makes use of the JSON interface to Randall's site to retrieve comic data.
    
    One can create comic objects manually using Comic(number), or can use the 
    helper functions provided- getLatestComic(), getRandomComic(), and 
    getComic()- to do this. Once you have a Comic object, you can access data
    from it using various provided methods.

CLASSES
    Comic
    
    class Comic
     |  Methods defined here:
     |  
     |  __init__(self, number)
     |  
     |  __repr__(self)
     |  
     |  __str__(self)
     |  
     |  download(self, path='')
     |      Download the image of the comic, returns the name of the output file
     |  
     |  getAltText(self)
     |      Returns the alt text of the comic
     |  
     |  getImageLink(self)
     |      Returns a URL link to the comic's image
     |  
     |  getImageName(self)
     |      Returns the name of the comic's image
     |  
     |  getTitle(self)
     |      Returns the title of the comic
     |  
     |  show(self)
     |      Uses the webbrowser module to open the comic

FUNCTIONS
    getComic(number)
        Function to return a Comic object for a given comic number
    
    getLatestComic()
        Function to return a Comic object for the latest comic number
    
    getLatestComicNum()
        Function to return the number of the latest comic.
    
    getRandomComic()
        Function to return a Comic object for a random comic number

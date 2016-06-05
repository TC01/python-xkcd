# xkcd v2.3.2 - A Python interface to xkcd.com

By Ben Rosser, released under MIT License (see LICENSE.txt)

This is a Python library for accessing and retrieving links to comics from the
xkcd webcomic by Randall Munroe. It is NOT endorsed or made by him, it's an
entirely independent project.

It makes use of the JSON interface to Randall's site to retrieve comic data.
One can create comic objects manually using Comic(number), or can use the helper
functions provided- getLatestComic(), getRandomComic(), and getComic()- to do
this. Once you have a Comic object, you can access data from it using various
provided methods.

Documentation is available [here](https://pythonhosted.org/xkcd/).

## Changelog:

### Version 2.3.3:
* Made pypandoc conversion optional; long_description will be MD formatted if it
cannot be imported (and rST-formatted if it can).

### Version 2.3.2:
* Fixed distutils URL to point at TC01/python-xkcd, not TC01/xkcd.
* Started using pypandoc to dynamically turn README.md into a RST long-description.

### Version 2.3:
* Fixed ASCII bug in Python 2.x
* Created Sphinx documentation and uploaded it to pythonhosted.org

### Version 2.2:
* Fixed very silly bug with xkcd.getComic()
* Added a getExplanation() which returns an explainxkcd link for a Comic().
* Added support for Python 3!

### Version 2.1:
* Fixed bugs with Comic.download() function
* Added optional parameter to Comic.download() to change name of output file
* Added more information to long_description text

## Credits:

* Ben Rosser <rosser.bjr@gmail.com>: Developer

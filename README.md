xkcd v2.2 - A Python interface to xkcd.com
------------------------------------------

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

Documentation is available [here](https://pythonhosted.org/xkcd/).

Note that PyPI currently doesn't support Markdown formatting for long_description,
hence the ugly rendering here.

## Changelog:

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

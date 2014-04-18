#!/usr/bin/env python

from distutils.core import setup

long_description = """This is a Python library for accessing and retrieving links to comics from the
xkcd webcomic by Randall Munroe. It is NOT endorsed or made by him, it's an
entirely independent project.

It makes use of the JSON interface to Randall's site to retrieve comic data.
One can create comic objects manually using Comic(number), or can use the helper
functions provided- getLatestComic(), getRandomComic(), and getComic()- to do
this. Once you have a Comic object, you can access data from it using various
provided methods."""

setup(name='xkcd',
	version='2.1',
	description='Library to access xkcd.com',
	long_description=long_description,
	author='Ben Rosser',
	license="MIT",
	author_email='rosser.bjr@gmail.com',
	url="http://venus.arosser.com/projects/xkcd",
	py_modules=['xkcd'])


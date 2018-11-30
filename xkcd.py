"""Python library for accessing xkcd.com.

This is a Python library for accessing and retrieving links to comics from
the xkcd webcomic by Randall Munroe. It is NOT endorsed or made by him, it's
an entirely independent project.

It makes use of the JSON interface to Randall's site to retrieve comic data.
Both Python 2 and Python 3 are supported, and there are no dependencies beyond
the Python standard library, so xkcd's footprint should be very light.

There is support for accessing specific comics, the latest comic, or a
random comic. Comic metadata can be queried and the comics themselves can be
downloaded onto your local system. The goal is simply to provide a relatively
Pythonic wrapper around the xkcd API for any Python program or library that
wants to access information about xkcd comics, for one reason or another.

The xkcd module, as of version 2.4.0, also supports getting information on
What If articles from whatif.xkcd.com. This information is generated by
scraping the What If archive page with a HTML parser."""

import copy
import json
import os
import random
import sys
import webbrowser

# Python 3 support!
if sys.version_info[0] <= 2:
	import urllib2 as urllib
	import HTMLParser
else:
	# This is kind of broken but I'm not sure of a better way.
	import urllib.request as urllib
	import html.parser as HTMLParser

# Define the URLs as globals.
xkcdUrl = "https://www.xkcd.com/"			# The URL for xkcd.
imageUrl = "https://imgs.xkcd.com/comics/"	# The root URL for image retrieval.
explanationUrl = "https://explainxkcd.com/"	# The URL of the explanation.
archiveUrl = "https://what-if.xkcd.com/archive/"	# The What If Archive URL.

# Functions that work on What Ifs.

def getWhatIfArchive():
	"""	Parses the xkcd What If archive. getWhatIfArchive passes the HTML text of
		the archive page into a :class:`WhatIfArchiveParser` and then calls
		the parser's :func:`WhatIfArchiveParser.getWhatIfs` method and returns the dictionary produced.

		This function returns a dictionary mapping article numbers to :class:`WhatIf`
		objects for every What If article published thus far. If the parsing fails,
		for whatever reason, the dictionary will be empty."""
	archive = urllib.urlopen(archiveUrl)
	text = archive.read()
	if sys.version_info[0] >= 3:
		text = text.decode('utf-8')
	archive.close()

	parser = WhatIfArchiveParser()
	parser.feed(text)
	return parser.getWhatIfs()

def getLatestWhatIfNum(archive=None):
	"""	Returns an integer representing the number of the latest What If article
		published. This is done by calling :class:`getLatestWhatIf` and returning
		the number of that method's result.

		Takes an optional "archive" argument. If this argument is None, the
		:func:`getWhatIfArchive` routine is first called to populate the archive
		of published What If articles. If it is not, however, "archive" is assumed
		to be a dictionary and used as the set of articles to chooose from.
	"""

	latestWhatIf = getLatestWhatIf(archive)
	return latestWhatIf.number

def getLatestWhatIf(archive=None):
	"""	Returns a :class:`WhatIf` object representing the latest What If article.

		Takes an optional "archive" argument. If this argument is None, the
		:func:`getWhatIfArchive` routine is first called to populate the archive
		of published What If articles. If it is not, however, "archive" is assumed
		to be a dictionary and used as the set of articles to chooose from.
	"""

	if archive is None:
		archive = getWhatIfArchive()

	# Get the archive keys as a list and sort them by ascending order.
	# The last entry in keys will be the latest What if.
	keys = list(archive.keys())
	keys.sort()
	return archive[keys[-1]]

def getRandomWhatIf():
	"""	Returns a randomly generated :class:`WhatIf` object, using the Python standard library
		random number generator to select the object. The object is returned
		from the dictionary produced by :func:`getWhatIfArchive`; like the other What If
		routines, this function is called first in order to get a list of all previously
		published What Ifs."""

	random.seed()
	archive = getWhatIfArchive()
	latest = getLatestWhatIfNum(archive)
	number = random.randint(1, latest)
	return archive[number]

def getWhatIf(number):
	"""	Returns a :class:`WhatIf` object corresponding to the What If article of
		index passed to the function. If the index is less than zero or
		greater than the maximum number of articles published thus far,
		None is returned instead.

		Like all the routines for handling What If articles, :func:`getWhatIfArchive`
		is called first in order to establish a list of all previously published
		What Ifs.

		Arguments:

			number: an integer or string that represents a number, this is the index of article to retrieve.

		Returns the resulting :class:`WhatIf` object."""
	archive = getWhatIfArchive()
	latest = getLatestWhatIfNum(archive)
	
	if type(number) is str and number.isdigit():
		number = int(number)
	if number > latest or latest <= 0:
		return None
	return archive[number]

class WhatIf:

	"""
		Class representing an xkcd What If article.

		The WhatIf class is somewhat simpler than the :class:`Comic` class.
		It simply provides functions for querying information about the link
		to, title of, and index of a What If article.

		Unlike the :class:`Comic` class, you are not meant to construct them
		directly. Instead, call :func:`getWhatIfArchive` to produce a dictionary
		mapping numbers to WhatIf objects and then select the one(s) you are
		interested in.
	"""

	def __init__(self):
		self.number = -1
		self.title = ''
		self.link = ''

	def __str__(self):
		return "What If object for " + self.link

	def __repr__(self):
		return self.__str__()

	def getTitle(self):
		"""Returns the title of the What If article."""
		return self.title

	def getNumber(self):
		"""Returns the number of the What If article."""
		return self.number

	def getLink(self):
		"""Returns a link to the What If article."""
		return self.link

# Utility functions

def convertToAscii(string, error="?"):
	"""	Utility function that converts a unicode string to ASCII. This
		exists so the :class:`Comic` class can be compatible with Python 2
		libraries that expect ASCII strings, such as Twisted (as of this writing,
		anyway). It is unlikely something you will need directly, and its
		use is discouraged.

		Arguments:

			string: the string to attempt to convert.

			error: a string that will be substituted into 'string' wherever Python is unable
			to automatically do the conversion.

		convertToAscii returns the converted string."""

	running = True
	asciiString = string
	while running:
		try:
			asciiString = asciiString.encode('ascii')
		except UnicodeError as unicode:
			start = unicode.start
			end = unicode.end
			asciiString = asciiString[:start] + "?" + asciiString[end:]
		else:
			running = False
	return asciiString

# Possibly, BeautifulSoup or MechanicalSoup or something would be nicer
# But xkcd currently has no external dependencies and I'd like to keep it that way.
class WhatIfArchiveParser(HTMLParser.HTMLParser):

	"""
		The WhatIfArchiveParser is a subclass of the Python standard library
		HTML parser. It is invoked by :func:`getWhatIfArchive` to parse
		the xkcd What If archive page, and automatically populate :class:`WhatIf`
		objects

		As there is not a JSON API for the What If blog (or at least, the author
		was unable to find one), this seemed the simplest way to implement fetching
		of information about them.

		This class is designed for internal usage only; there should be no reason
		for you to use it directly outside of the xkcd module.
	"""

	def __init__(self):
		# Ugh, this is an "old style class"
		if sys.version_info[0] <= 2:
			HTMLParser.HTMLParser.__init__(self)
		else:
			# Keep python 3.3 compatibility
			if sys.version_info[1] <= 3:
				super().__init__()
			else:
				super().__init__(convert_charrefs=False)

		# Create a dictionary of what-ifs, indexed by number.
		self.whatifs = {}
		self.currentWhatIf = None

		# Parsing metadata
		self.parsingWhatIf = False
		self.seenATag = 0

	def handle_starttag(self, tag, attrs):
		# Check if this is an archive entry.
		if tag == "div" and ("class", "archive-entry") in attrs:
			self.parsingWhatIf = True
			self.currentWhatIf = WhatIf()

		# If we're parsing an archive entry:
		if self.parsingWhatIf:
			if tag == "a":
				# <a> tags occur twice in an archive entry, this value influences the result of
				# the data parsed; is it an image or is it the title?
				self.seenATag += 1

				# Only do this once.
				if self.currentWhatIf.number == -1:
					link = ""
					for pair in attrs:
						if pair[0] == "href":
							link = pair[1]
					# If we fail to find a link for whatever reason or if the parsing fails,
					# fail to generate a comic.
					try:
						num = link[len("//what-if.xkcd.com/"):-1]
						num = int(num)
					except:
						num = -1
					self.currentWhatIf.number = num
					self.currentWhatIf.link = "https:" + link

	def handle_data(self, data):
		# Some cruder parsing to pick out the data.
		if self.parsingWhatIf:
			if self.seenATag == 2:
				self.currentWhatIf.title = data

	def handle_endtag(self, tag):
		# When we encounter the final </div>, stop parsing these.
		if tag == "div" and self.parsingWhatIf:
			self.parsingWhatIf = False
			if self.currentWhatIf.number != -1:
				self.whatifs[self.currentWhatIf.number] = copy.copy(self.currentWhatIf)

		# When we encounter the final </a>, reset seen counter to make handle_data
		# not do anything.
		if self.parsingWhatIf and tag == "a" and self.seenATag == 2:
			self.seenATag = 0

	def getWhatIfs(self):
		"""	Returns a dictionary of :class:`WhatIf` objects, indexed into by
			their number. This function must be invoked after the HTML parsing has
			finished, i.e. after calling self.feed.

			If for some reason the parsing has failed, the dictionary will be empty."""
		return self.whatifs

# Functions that work on Comics.

def getLatestComicNum():
	"""	Uses the xkcd JSON API to look up the number of the latest xkcd comic.

		Returns that number as an integer."""
	xkcd = urllib.urlopen("https://xkcd.com/info.0.json").read()
	xkcdJSON = json.loads(xkcd.decode())
	number = xkcdJSON['num']
	return number

def getLatestComic():
	"""	Produces a :class:`Comic` object for the latest xkcd comic. This function
		is just a wrapper around a call to :func:`getLatestComicNum`, and then
		constructs a :class:`Comic` object on its return value.

		Returns the resulting comic object."""
	number = getLatestComicNum()
	return Comic(number)

def getRandomComic():
	"""	Produces a :class:`Comic` object for a random xkcd comic. Uses the
		Python standard library random number generator in order to select
		a comic.

		Returns the resulting comic object."""
	random.seed()
	numComics = getLatestComicNum()
	number = random.randint(1, numComics)
	return Comic(number)

def getComic(number, silent=True):
	"""	Produces a :class:`Comic` object with index equal to the provided argument.
		Prints an error in the event of a failure (i.e. the number is less than zero
		or greater than the latest comic number) and returns an empty Comic object.

		Arguments:
			an integer or string that represents a number, "number", that is the index of the comic in question.

			silent: boolean, defaults to True. If set to False, an error will be printed
			to standard output should the provided integer argument not be valid.

		Returns the resulting Comic object for the provided index if successful,
		or a Comic object with -1 as the index if not."""
	numComics = getLatestComicNum()
	
	if type(number) is str and number.isdigit():
		number = int(number)
	if number > numComics or number <= 0:
		if not silent:
			print("Error: You have requested an invalid comic.")
		return Comic(-1)
	return Comic(number)

class Comic:

	"""	Class representing a single xkcd comic. These can be produced via number of
		ways; if you know the number of the comic you want to query, you can just
		construct them yourself (e.g. Comic(integer)), but the recommended way is to
		use the :func:`getComic` function.

		There are also helper functions available to get the latest comic (:func:`getLatestComic`)
		and a random comic(:func:`getRandomComic`) as comic objects.
	"""

	def __init__(self, number):
		global xkcdUrl, imageUrl
		if type(number) is str and number.isdigit():
			number = int(number)
		self.number = number
		if number <= 0:
			self.link = "Invalid comic"
			return

		"""	The link to the comic on the xkcd website."""
		self.link = xkcdUrl + str(number)

		#Get data from the JSON interface
		jsonString = self.link + "/info.0.json"
		xkcd = urllib.urlopen(jsonString).read()
		xkcdData = json.loads(xkcd.decode())
		self.title = xkcdData['safe_title']
		self.altText = xkcdData['alt']
		self.imageLink = xkcdData['img']
		self.imageNum = xkcdData['num']
		self.day = xkcdData['day']
		self.month = xkcdData['month']
		self.year = xkcdData['year']

		# This may no longer be necessary.
#		if sys.version_info[0] >= 3:
#			self.title = str(self.title, encoding='UTF-8')
#			self.altText = str(self.altText, encoding='UTF-8')
#			self.imageLink = str(self.imageLink, encoding='UTF-8')

		#Get the image filename
		offset = len(imageUrl)
		index = self.imageLink.find(imageUrl)
		self.imageName = self.imageLink[index + offset:]

	def __str__(self):
		return "Comic object for " + self.link

	def __repr__(self):
		return "Comic object for " + self.link

	def getTitle(self):
		"""	Returns the title of the comic, as a UTF-8 formatted Unicode string."""
		return self.title

	def getAsciiTitle(self):
		"""	Returns the ASCII-formatted version of the title.

		This function, and the other ASCII getters in the Comic class, exists so that
		code which depends on some legacy Python 2 component, like Twisted (which as
		of this writing does not support Unicode terribly well) can retrieve a version
		of comic metadata that they can use. It uses the :func:`convertToAscii` helper
		function to replace characters Python cannot automatically convert with a "?".

		You should do your best to not need to use this routine and prefer :func:`getTitle`
		wherever possible.
		"""
		asciiTitle = convertToAscii(self.title)
		return asciiTitle

	def getAsciiAltText(self):
		"""	Returns the ASCII-formatted version of the comic's alt-text. See
		:func:`getAsciiTitle` and :func:`getAltText` for more information."""
		asciiAltText = convertToAscii(self.altText)
		return asciiAltText

	def getAsciiImageLink(self):
		"""	Returns the ASCII-formatted version of the link to the comic's
			image. See :func:`getAsciiTitle` and :func:`getImageLink` for more information."""
		asciiImageLink = convertToAscii(self.imageLink)
		return asciiImageLink

	def getAltText(self):
		"""	Returns the alt-text of the comic (the text that appears when one places
			their cursor over the image in a web browser) as a UTF-8 formatted Unicode string."""
		return self.altText

	def getImageLink(self):
		"""	Returns a URL linking to the comic's image as a UTF-8 formatted Unicode string."""
		return self.imageLink

	def getImageName(self):
		"""	Returns the filename of the comic's image as a UTF-8 formatted Unicode string."""
		return self.imageName

	def getExplanation(self):
		"""	Returns an explainxkcd link for the comic. explainxkcd is a wiki with community
			contributed explanations for xkcd comics; this function produces the URL for
			a given comic and returns that URL."""
		global explanationUrl
		return explanationUrl + str(self.number)
	
	def getNumber(self):
		""" Returns the Comic number."""
		return self.imageNum

	# Possible date formats:
	# YMD: year, month, day
	# DMY: day, month, year
	# MDY: month, day, year
	def getDate(self, dateType="MDY"):
		""" Returns Comic date."""
		if dateType == "MYD":
			return "{}/{}/{}".format(self.month, self.year, self.day)
		elif dateType == "DMY":
			return "{}/{}/{}".format(self.day, self.month, self.year)
		elif dateType == "MDY":
			return "{}/{}/{}".format(self.month, self.day, self.year)
		else:
			return "{}/{}/{}".format(self.month, self.day, self.year)

	def show(self):
		"""	Uses the Python webbrowser module to open the comic in your system's
			web browser."""
		webbrowser.open_new_tab(self.link)

	def download(self, output="", outputFile="", silent=True):
		"""	Downloads the image of the comic onto your computer.

			Arguments:
				output: the output directory where comics will be downloaded to. The
				default argument for 'output is the empty string; if the empty
				string is passed, it defaults to a "Downloads" directory in your home folder
				(this directory will be created if it does not exist).

				outputFile: the filename that will be written. If the empty string
				is passed, outputFile will default to a string of the form xkcd-(comic number)-(image filename),
				so for example, xkcd-1691-optimization.png.

				silent: boolean, defaults to True. If set to False, an error will be printed
				to standard output should the provided integer argument not be valid.

			Returns the path to the downloaded file, or an empty string in the event
			of failure."""
		image = urllib.urlopen(self.imageLink).read()

		#Process optional input to work out where the dowload will go and what it'll be called
		if output != "":
			output = os.path.abspath(os.path.expanduser(output))
		if output == "" or not os.path.exists(output):
			output = os.path.expanduser(os.path.join("~", "Downloads"))
			# Create ~/Downloads if it doesn't exist, since this is the default path.
			if not os.path.exists(output):
				os.mkdir(output)
		if outputFile == "":
			outputFile = "xkcd-" + str(self.number) + "-" + self.imageName

		output = os.path.join(output, outputFile)
		try:
			download = open(output, 'wb')
		except:
			if not silent:
				print("Unable to make file " + output)
			return ""
		download.write(image)
		download.close()
		return output

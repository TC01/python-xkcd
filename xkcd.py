"""Python library for accessing xkcd.com.

This is a Python library for accessing and retrieving links to comics from
the xkcd webcomic by Randall Munroe. It is NOT endorsed or made by him, it's
an entirely independent project.

It makes use of the JSON interface to Randall's site to retrieve comic data.

One can create comic objects manually using Comic(number), or can use the
helper functions provided- getLatestComic(), getRandomComic(), and
getComic()- to do this. Once you have a Comic object, you can access data
from it using various provided methods.

This documentation is not that great, but it should be getting better Soon."""

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
xkcdUrl = "http://www.xkcd.com/"			# The URL for xkcd.
imageUrl = "http://imgs.xkcd.com/comics/"	# The root URL for image retrieval.
explanationUrl = "http://explainxkcd.com/"	# The URL of the explanation.
archiveUrl = "https://what-if.xkcd.com/archive/"	# The What If Archive URL.

class WhatIf:

	def __init__(self):
		self.number = -1
		self.title = ''
		self.link = ''

	def __str__(self):
		return "What If object for " + self.link

	def __repr__(self):
		return self.__str__()

	def getTitle(self):
		"""Returns the title of the What If."""
		return self.title

	def getNumber(self):
		"""Returns the number of the What If."""
		return self.number

	def getLink(self):
		"""Returns a link to the What If."""
		return self.link

# Possibly, BeautifulSoup or MechanicalSoup or something would be nicer
# But xkcd currently has no external dependencies and I'd like to keep it that way.
class WhatIfArchiveParser(HTMLParser.HTMLParser):

	def __init__(self):
		# Ugh, this is an "old style class"
		if sys.version_info[0] <= 2:
			HTMLParser.HTMLParser.__init__(self)
		else:
			super().__init__()

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
					self.currentWhatIf.link = "http:" + link

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
		return self.whatifs

class Comic:

	def __init__(self, number):
		global xkcdUrl, imageUrl
		self.number = number
		if number <= 0:
			self.link = "Invalid comic"
			return
		self.link = xkcdUrl + str(number)

		#Get data from the JSON interface
		jsonString = self.link + "/info.0.json"
		xkcd = urllib.urlopen(jsonString).read()
		xkcdData = json.loads(xkcd.decode())
		self.title = xkcdData['safe_title']
		self.altText = xkcdData['alt']
		self.imageLink = xkcdData['img']

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
		"""Returns the title of the comic"""
		return self.title

	def getAsciiTitle(self):
		"""Returns the ASCII version of a title, with appropriate try/except."""
		asciiTitle = convertToAscii(self.title)
		return asciiTitle

	def getAsciiAltText(self):
		"""Returns the ASCII version of alt text, with appropriate try/except."""
		asciiAltText = convertToAscii(self.altText)
		return asciiAltText

	def getAsciiImageLink(self):
		"""Returns the ASCII version of image link, with appropriate try/except."""
		asciiImageLink = convertToAscii(self.imageLink)
		return asciiImageLink

	def getAltText(self):
		"""Returns the alt text of the comic"""
		return self.altText

	def getImageLink(self):
		"""Returns a URL link to the comic's image"""
		return self.imageLink

	def getImageName(self):
		"""Returns the name of the comic's image"""
		return self.imageName

	def getExplanation(self):
		"""Returns an explain xkcd link for the comic."""
		global explanationUrl
		return explanationUrl + str(self.number)

	def show(self):
		"""Uses the webbrowser module to open the comic"""
		webbrowser.open_new_tab(self.link)

	def download(self, output="", outputFile=""):
		"""Download the image of the comic, returns the name of the output file"""
		image = urllib.urlopen(self.imageLink).read()

		#Process optional input to work out where the dowload will go and what it'll be called
		if output != "":
			output = os.path.abspath(os.path.expanduser(output))
		if output == "" or not os.path.exists(output):
			output = os.path.expanduser(os.path.join("~", "Downloads"))
		if outputFile == "":
			outputFile = "xkcd-" + str(self.number) + "-" + self.imageName

		output = os.path.join(output, outputFile)
		try:
			download = open(output, 'wb')
		except:
			print("Unable to make file " + output)
			return ""
		download.write(image)
		download.close()
		return output

# Functions that work on Comics.

def getLatestComicNum():
	"""Function to return the number of the latest comic."""
	xkcd = urllib.urlopen("http://xkcd.com/info.0.json").read()
	xkcdJSON = json.loads(xkcd.decode())
	number = xkcdJSON['num']
	return number

def getLatestComic():
	"""Function to return a Comic object for the latest comic number"""
	number = getLatestComicNum()
	return Comic(number)

def getRandomComic():
	"""Function to return a Comic object for a random comic number"""
	random.seed()
	numComics = getLatestComicNum()
	number = random.randint(1, numComics)
	return Comic(number)

def getComic(number):
	"""Function to return a Comic object for a given comic number"""
	numComics = getLatestComicNum()
	if number > numComics or number <= 0:
		print("Error: You have requested an invalid comic.")
		return Comic(-1)
	return Comic(number)

# Functions that work on What Ifs.

def getWhatIfArchive():
	"""	Function to return a dictionary of all published What If objects,
		indexed into by their number."""
	archive = urllib.urlopen(archiveUrl)
	text = archive.read()
	if sys.version_info[0] >= 3:
		text = text.decode('utf-8')
	archive.close()

	parser = WhatIfArchiveParser()
	parser.feed(text)
	return parser.getWhatIfs()

def getLatestWhatIfNum(archive=None):
	"""	Returns the number of the latest What If. Takes optional "archive" argument, if this is not
		None (default value) it will be used as the dictionary what if archive."""
	latestWhatIf = getLatestWhatIf(archive)
	return latestWhatIf.number

def getLatestWhatIf(archive=None):
	"""	Function to return a What If object for the latest What If. Takes optional "archive" argument,
		this is not None(default value) it will be used as the dictionary what if archive."""
	if archive is None:
		archive = getWhatIfArchive()

	# Get the archive keys as a list and sort them by ascending order.
	# The last entry in keys will be the latest What if.
	keys = list(archive.keys())
	keys.sort()
	return archive[keys[-1]]

def getRandomWhatIf():
	"""	Function that returns a random What If object."""
	random.seed()
	archive = getWhatIfArchive()
	latest = getLatestWhatIfNum(archive)
	number = random.randint(1, latest)
	return archive[number]

def getWhatIf(number):
	"""	Function that returns a specified What If object. Returns
		None if the specified What If is out of range."""
	archive = getWhatIfArchive()
	latest = getLatestWhatIfNum(archive)
	if number > latest or latest <= 0:
		return None
	return archive[number]

# Utility functions

def convertToAscii(string, error="?"):
	"""Utility function that converts unicode 'string' to ASCII, replacing all unparseable characters with 'error'.
		This exists for compatibilty with e.g. python2 and twisted."""
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

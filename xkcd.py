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

import json
import os
import random
import sys
import webbrowser

# Python 3 support!
if sys.version_info[0] <= 2:
	import urllib2 as urllib
else:
	# This is kind of broken but I'm not sure of a better way.
	import urllib.request as urllib

# Define the URLs as globals.
xkcdUrl = "http://www.xkcd.com/"			# The URL for xkcd.
imageUrl = "http://imgs.xkcd.com/comics/"	# The root URL for image retrieval.
explanationUrl = "http://explainxkcd.com/"	# The URL of the explanation.

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

def convertToAscii(string, error="?"):
	"""Utility function that converts unicode 'string' to ASCII, replacing all unparseable characters with 'error'."""
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

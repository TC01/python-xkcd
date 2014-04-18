"""Python library for accessing xkcd.com

This is a Python library for accessing and retrieving links to comics from
the xkcd webcomic by Randall Munroe. It is NOT endorsed or made by him, it's
an entirely independent project.

It makes use of the JSON interface to Randall's site to retrieve comic data.

One can create comic objects manually using Comic(number), or can use the 
helper functions provided- getLatestComic(), getRandomComic(), and
getComic()- to do this. Once you have a Comic object, you can access data
from it using various provided methods."""

import json
import os
import random
import urllib2 as urllib
import webbrowser

class Comic:
	
	def __init__(self, number):
		self.number = number
		if number <= 0:
			self.link = "Invalid comic"
			return
		self.link = "http://www.xkcd.com/" + str(number)
		
		#Get data from the JSON interface
		jsonString = self.link + "/info.0.json"
		xkcd = urllib.urlopen(jsonString).read()
		xkcdData = json.loads(xkcd)
		self.title = xkcdData['safe_title'].encode('ascii')
		self.altText = xkcdData['alt'].encode('ascii')
		self.imageLink = xkcdData['img'].encode('ascii')
		
		#Get the image filename
		offset = len('http://imgs.xkcd.com/comics/')
		index = self.imageLink.find('http://imgs.xkcd.com/comics/')
		self.imageName = self.imageLink[index + offset:]
		
	def __str__(self):
		return "Comic object for " + self.link
		
	def __repr__(self):
		return "Comic object for " + self.link
	
	def getTitle(self):
		"""Returns the title of the comic"""
		return self.title
	
	def getAltText(self):
		"""Returns the alt text of the comic"""
		return self.altText
		
	def getImageLink(self):
		"""Returns a URL link to the comic's image"""
		return self.imageLink
		
	def getImageName(self):
		"""Returns the name of the comic's image"""
		return self.imageName
	
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
			print "Unable to make file " + output
			return ""
		download.write(image)
		download.close()
		return output
	
def getLatestComicNum():
	"""Function to return the number of the latest comic."""
	xkcd = urllib.urlopen("http://xkcd.com/info.0.json").read()
	xkcdJSON = json.loads(xkcd)
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
		print "Error: You have requested an invalid comic."
		return Comic(-1)
	return ComiC(number)

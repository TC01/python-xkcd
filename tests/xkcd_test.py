# unit test suite for python-xkcd

import os
import unittest

import xkcd

class TestXkcd(unittest.TestCase):

	def test_no_such_comic(self):
		bad = xkcd.getComic(-100)
		self.assertEqual(bad.number, -1)

	def test_comic(self):
		# Get a comic to test.
		test = xkcd.getComic(869)
		self.assertEqual(test.number, 869)
		self.assertEqual(test.title, "Server Attention Span")
		self.assertEqual(test.imageName, "server_attention_span.png")

	def test_download_comic(self):
		# Try to download a comic.
		dlname = "xkcd-unittestserver_attention_span.png"
		test = xkcd.getComic(869)
		test.download(outputFile=dlname)

		path = os.path.join(os.path.expanduser("~"), "Downloads", dlname)
		self.assertTrue(os.path.exists(path))

		# Delete the downloaded file
		os.remove(path)

	def test_download_comic_2x(self):
		# Try to download a 2x comic
		dlname = "xkcd-unittestpython_environment_2x.png"
		test = xkcd.getComic(1987)
		test.download(outputFile=dlname, x2=True)

		path = os.path.join(os.path.expanduser("~"), "Downloads", dlname)
		self.assertTrue(os.path.exists(path))

		# Delete the downloaded file
		os.remove(path)

	def test_whatif(self):
		# Get a What If to test.
		test = xkcd.getWhatIf(3)
		self.assertEqual(test.number, 3)
		self.assertEqual(test.title, "Yoda")

if __name__ == '__main__':
	unittest.main()

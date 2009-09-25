#!/usr/bin/python
import sgmllib
import sys

class MyParser(sgmllib.SGMLParser):
    "A simple parser class."

    def parse(self, s):
        "Parse the given string 's'."
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        "Initialise an object, passing 'verbose' to the superclass."

        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = []

    def start_a(self, attributes):
        "Process a hyperlink and its 'attributes'."

        for name, value in attributes:
            if name == "href":
		if value.startswith("/watch?v="):
			self.hyperlinks.append("youtube-dl -t http://youtube.com"+value)

    def get_hyperlinks(self):
        "Return the list of hyperlinks."

        return self.hyperlinks

def f2(seq): 
   # order preserving
   checked = []
   for e in seq:
       if e not in checked:
           checked.append(e)
   return checked

import urllib, sgmllib

# Get something to work with.
f = urllib.urlopen(sys.argv[1])
s = f.read()

# Try and process the page.
# The class should have been defined first, remember.
myparser = MyParser()
myparser.parse(s)

# Get the hyperlinks.
print f2(myparser.get_hyperlinks())
yt = open("youtube_links","w")

for link in f2(myparser.get_hyperlinks()):
	yt.write(link)
	yt.write("\n")

print "\nYouTube Batch Download Script \"youtube_links\" has been generated. Execute it !"
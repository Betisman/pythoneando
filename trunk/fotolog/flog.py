import httplib2, urllib, getpass, sgmllib
httplib2.debuglevel = 1
headers = {'Content-type': 'application/x-www-form-urlencoded'}
http = httplib2.Http()

def getAmigos(user):
	url = 'http://ff.fotolog.com/all.html?u=' + user + '&ip=0'
	headers['Content-type'] = 'text/html'
	response, content = http.request(url, 'POST', headers=headers)
	#parseHtml(content)
	myparser = MyParser()
	print 'myparser'
	myparser.parse(content)
	print 'parse'
	print myparser.get_trs()

# class AmigosHtmlParser(sgmllib.SGMLParser):
	# def reset(self):
        # SGMLParser.reset(self)
        # self.urls = []
	
	# def start_tr(self, attrs):
        # tr = [v for k, v in attrs if k=='href']
        # if href:
            # self.urls.extend(href)

class MyParser(sgmllib.SGMLParser):
    def parse(self, s):
        self.feed(s)
        self.close()
	
	def __init__(self, verbose=0):
		sgmllib.SGMLParser.__init__(self, verbose)
		self.hyperlinks = []
	
	def start_tr(self, attrs):
		self.trs.append('tr')
	
	def get_trs():
		return self.trs




getAmigos('betisman')
	
	
# for cons in consultar:
	# cont = 0
	# html = urlopen('http://www.fotolog.com/'+cons).read()
	# indexend = html.find('</h1>', html.find('<h1 id="phototitle">'))
	# indexst = html.rfind('>', 0, indexend)
	# title = html[indexst+1:indexend]
	# enc = html.find('<div class="comment"')
	# guests = []
	# while (enc != -1):
		# divend = html.find('</div>', enc)
		# guestend = html.find('</a>', enc, divend)
		# guestst = html.rfind('>', 0, guestend)
		# if guestst > -1:
			# guest = html[guestst+1:guestend]
			# if len(guest) > 0:
				# guests.append(guest)
		# enc = html.find('<div class="comment"', enc+1)
		# cont = cont + 1
	
	# print cons + ': (%s) "%s"\n\t%s' %(cont,title,guests)
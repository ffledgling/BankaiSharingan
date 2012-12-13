from BeautifulSoup import BeautifulSoup
import urllib,urllib2
import os

def install_proxy(proxy={'http':'your.proxy.com:portNumber'}):
	urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler(proxy)))
	return

def sanitize(string):
	temp=''
	illegal_chars=['/','\\','*','&','|','*','>','<','"',':']
	for ch in string:
		if ch not in illegal_chars:
			temp=temp+ch
	return str(temp)

def fetch(url,add_base=True):
	Base_url='http://www.mangareader.net'
	if add_base is True:
		url=Base_url+url
	page_request = urllib2.Request(url)
	return urllib2.urlopen(page_request).read()


def extract(doc):
	soup=BeautifulSoup(doc)
	#print bs.prettify()

	#print soup.title

	#print div
	#print div.contents
	page = soup.find('div',{'id':'selectpage'})
	#print page
	info = soup.find('div',{'id':'mangainfo'})
	chap_name = info.find('h1').string			#CHAPTER NAME
	#print "Path name: ",path_chap
	div = soup.find('div',{'id':'imgholder'})		#GETS DIV CONTAINING IMG/END OF MANGA INFO
	end = div.find('div',{'id':'recom_info'})		#TEXT FROM END OF MANGA
	img = div.find('img',{'id':'img'})			#IMAGE TO DOWNLOAD




	if end is not None:
		print soup.find('h2',{'class':'c2'}).text,end.contents[1]
		return False
	elif img is not None:
	
	#GETS PAGE NUMBER 
		page_num = page.find('option',{'selected':'selected'}).string
	
	#PRINT INFO
		print chap_name,",Page "+page_num," ...",

	#"Create Path and folder and file"
		
		print "Creating File and Folder... ",
		path_chap = sanitize(chap_name)
		if os.path.exists(path_chap) is not True:
			os.mkdir(path_chap)
		temp = open(os.path.join(path_chap,page_num+'.jpg'),'wb')
		print "Done. ",
		
	#"Download image"
		print "Downloading image... ",
		temp.write(fetch(img.get('src'),False))
		temp.close()
		print "Done."
	#Get link to next page
		nxt = div.find('a').get('href')
		return nxt
	else:
		print "Some strange error occured... Exiting"
		return False

def control(url,apply_proxy=False):
	
	first=True
	if apply_proxy is True:
		install_proxy()
	
	while url is not False:
		if first is True:
			url = extract(fetch(url,False))
			first=False
		else:
			url = extract(fetch(url))
	return
#want_proxy = raw_input("Do you wish to use a proxy?[y/n] : ")
url=raw_input('URL: ')
control(url)

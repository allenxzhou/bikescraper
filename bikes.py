import re
import mechanize
import urllib
import urllib2

"""
DEBUG ISSUES:

- For the following url: "http://sfbay.craigslist.org/nby/bik/3947827531.html",
mechanize.urlopen has issues, whereas urllib.urlopen does not. As a result,
using the latter for now.

- Abnormality in the quotations around hyperlink references: for the references
to the actual post links, uses double quotations; for the references to next/prev
page, uses single quotation.

----------------------------

Brief info: search through bicycle listings on Craigslist

How-to: Mechanize - 
1. Create url to be accessed
2. Create a request (mechanize.Request)
3. Open the url for that request (mechanize.urlopen)
4. Gain the parsed response for the form (mechanize.ParseResponse)
5. Apply your changes to the form's elements (print form to see the controls)
   *Similar to a dictionary style of setting values*
6. Use the click() function on the form (parsed response) to create a
   second request
7. Send that second request through a urlopen to get the resulting website
"""

brands = ["cannondale", "felt", "fuji", "giant", "specialized", "trek"]
keywords = ["52", "53", "54", "shimano", "sora", "tiagra", "105", "ultegra", \
			"road", "allez", "defy"]
avoid = ["bmx", "mountain", "kids", "fixie", "jacket", "clothing", "fixed gear", \
		 "hybrid", "mtb"]

def openLink(text):
	text = text.lower()
	open = False
	for word in avoid:
		if word in text:
			return False
	
	for word in keywords:
		if word in text:
			open = True
	
	return open

def scourPage(text, fileRead, fileWrite):

	# Double quotations work fine for the posting listings
	links = re.findall(r'class="row".+?href="(.+?)"', text)

	for link in links:

		if "http:" in link:
			url = link
		else:
			url = homePage + link

		# Line 1 of 2 (below) that replaces mechanize with urllib
		page = urllib.urlopen(url)
		pageText = page.read()
		title = re.search(r'"postingtitle">.{0,10}<span.+?>[\s\'"]+(.+?)[\s\'"]{0,10}</h2>', \
						  pageText, re.DOTALL)
		body = re.search(r'"postingbody">(.+?)</section>', pageText, re.DOTALL)
		openBody = False
		openTitle = False

		if body != None:
			body = body.group(1)
			openBody = openLink(body)

		if title != None:
			title = title.group(1)
			openTitle = openLink(title)

		if (openTitle and openBody) and (url not in fileRead) and (title not in fileRead):
			fileWrite.write(title + "\n" + url + "\n")

	fileWrite.close()

print "start"
homePage = "http://sfbay.craigslist.org"
request = mechanize.Request(homePage)
response = mechanize.urlopen(request)
print "first forms call"
forms = mechanize.ParseResponse(response, backwards_compat=False)
form = forms[0]

request = form.click()
response = mechanize.urlopen(request)
emptySearch = response.geturl()
request = mechanize.Request(emptySearch)
response = mechanize.urlopen(request)
print "second forms call"
forms = mechanize.ParseResponse(response, backwards_compat=False)
form = forms[0]

form["catAbb"] = ["bik"]
form["maxAsk"] = "500"
form.find_control("hasPic").items[0].selected = True

print "start of for loop"
for brand in brands:
	print "inside for loop"
	form["query"] = brand
	
	request = form.click()
	response = mechanize.urlopen(request)
	text = response.read()

	fileR = open('bikes.txt', 'r').read()
	fileA = open('bikes.txt', 'a')

	scourPage(text, fileR, fileA)

	fileA.close()

	# Single quotation used for next page link wrapper around the hyperlink reference
	# Also hacky means of making sure that when there is no next link, that it avoids
	# finding the "first" link; more sound method would be to use the "npcontrols" division
	next = re.findall(r'class="nplink next".{0,50}<a href=\'(.+?)\'>', text, re.DOTALL)
	print next

	print "start of while loop"
	while len(next) != 0:
		print "inside while loop"
		# Line 2 of 2 (below) that replaces mechanize with urllib
		text = urllib.urlopen(next[0]).read()
		print "fuckers"
		
		fileR = open('bikes.txt', 'r').read()
		fileA = open('bikes.txt', 'a')

		scourPage(text, fileR, fileA)

		fileA.close()

		next = re.findall(r'class="nplink next".{0,50}<a href=\'(.+?)\'>', text, re.DOTALL)
		print next


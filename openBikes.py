import sys
import re
import webbrowser

# Number passed in from command line; sys.argv is a list
if len(sys.argv) == 3:
	number = int(sys.argv[1])
	side = sys.argv[2]
elif len(sys.argv) != 1:
	print "Enter arguments in the following format: [number] [head/tail]"
	print "Leave blank for default (open all links)"
	sys.exit()

file = open('bikes.txt', 'r')
text = file.read()
		
links = re.findall(r'http://.+?.html', text)

try:
	if side == "head":
		for i in range(0, number):
			webbrowser.open(links[i])
	elif side == "tail":
		for i in range(1, number + 1):
			webbrowser.open(links[len(links) - i])
except:
	for link in links:
		webbrowser.open(link)

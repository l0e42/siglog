import dateparser
import re
import pickle
document = pickle.load( open( "save.p", "rb" ) )
print(document)

import sys

if len(sys.argv) > 1:
	email = sys.argv[1] == 'email'
else: 
	email = False

def process(item):

	if item['type'] == 'title':
		return title(item)
	if item['type'] == 'ul':
		return ul(item)
	if item['type'] == 'li':
		return li(item)
	if item['type'] =='text':
		return text(item)
	if item['type'] =='tag':
		return tag(item)
	if item['type'] =='miniul':
		return miniul(item)

	if item['type'] =='info':
		return info(item)

	if item['type'] =='meta':
		return meta(item)

	if item['type'] =='dates':
		return dates(item)

	if item['type'] =='date':
		return date(item)

	return "don't know "+ item['type']

def simplify(item):
	return item.replace("&","")

def format(item):
	return item.replace("&","\\&")

def repl(match):
	obj = match.group(0)
	urlify = obj.replace("_","\\_")
	return  "\\href{" + obj+ "}{" + urlify+ "}"

def text(item):
	txt =  item['text']
	txt = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+([a-zA-Z]|[0-9]|\/)+", repl,txt)	
	txt = re.sub(r"\"(.*?)\"","``\\g<1>''",txt)
	return format(txt)

def info(item):
	return item['text'] + " \n\n"

def meta(item):
	return  text(item) + "\\\\ \n"
	# return "<p class=\"meta\">" + text(item) + "</p>"

def dates(item):

	if len(item['text']) == 1:
		return item['text'][0]['name'] + ": " + item['text'][0]['date'] + " \n"
	else:
		txt = ""
		txt += "\\rowcolors{1}{white}{gray!25}\\begin{tabulary}{\\linewidth}{LL}"
		for y,x in enumerate(item['text']):
			# if y %2 == 0:
			txt += "" + process(x) +  " \\\\\n"
			# else:
				# txt += "<tr class=\"odd\">" + process(x) +  " </tr>"
		txt += "\\end{tabulary}\n"
	return txt

def date(item):
	txt = ""
	txt += format(item['name']) + ":  & " + format(item['date'])
	# txt += "<td>" + item['name'] + ": &nbsp; </td>"
	# txt += "<td>" + item['date'] + "</td>"
	return txt


def miniul(item):
	txt = ""
	txt += "\\begin{itemize}"
	for x in item['text']:
		txt += "\\item " + process(x) +  "\n"
	txt += "\\end{itemize}"
	return txt

def ul(item):
	if item['type']!= 'ul':
		raise ValueError

	txt = ""
	txt += "\\begin{itemize}"
	for x in item['text']:
		txt +=  process(x) 
	txt += "\\end{itemize}"
	return txt

def li(item):
	if item['type']!= 'li':
		raise ValueError

	txt = ""
	txt += "\\item "
	for x in item['text']:
		txt +=  process(x) 
		if x['type'] not in ['miniul','dates']:
			txt += " \n"
		txt += " \n"
	txt += ""
	return txt




def title(item):

	txt = "\\section{"
	txt += format(item['text'])
	txt += "}"
	if item['tag']:
		txt += "\\label{" + simplify(item['tag'])+  "}"

	return txt

def item(item):
	txt =""
	# if 'title' in item:
	# 	txt += "<h2 "
	# 	if getAcc(item):
	# 		txt += "id=\"{}\" >".format(getAcc(item)['slug'])
	# 		txt += getAcc(item)['main']	 + ": "
	# 	else:
	# 		txt += " >"
	# 	txt += item['title']
	# 	txt += "</h2>"

	if 'objects' in item:
		for y in item['objects']:
			txt += (process(y))
	return txt

def tag(item):
	global email

	return format(item['content']) + " (\\cref{" +simplify(item['slug'])  +"})"



def toc(items):
	html = ""
	html += "\\section{Table of Content}"


	return html + process(document['toc'])
	# html += 
	# for x in items:
	# 	if getAcc(x):
	# 		[{
	# 		"type": "text",
	# 		"text": tag(x) } for x in items if getAcc(x)]
	# 		html += tag(x) + "<br>"
	# return html

def doDates(document):
	html = ""
	html += "\\section{Deadlines}"
	html += "\\label{deadlines}"

	return html + process(document['dates'])

for x in document:
	print(x)
html = """\\documentclass{article}

\\usepackage[table]{xcolor}
\\usepackage[utf8]{inputenc}
\\usepackage[parfill]{parskip}
\\usepackage{tabulary}
\\PassOptionsToPackage{hyphens}{url}
\\usepackage{hyperref}    
\\usepackage[capitalize]{cleveref}
\\begin{document}
"""
html += "\\title{SIGLOG Monthly "  +  str(document['number']) + "}"

html += "\\date{" + document['renderdate'].strftime("%B %d, %Y") + "}"

html +="""\\maketitle


\\href{https://lics.siglog.org/newsletters/}{Past Issues}
 - 
\\href{https://lics.siglog.org/newsletters/inst.html}{How to submit an announcement}
"""

html += toc(document)

html += doDates(document)

for x in document['items']:
	html += item(x)


html += "\n\n\nTo the \\href{http://siglog.org/}{SIGLOG} or \\href{https://lics.siglog.org}{LICS} website"
html += "\\end{document}"

with open("editions/"+document['number'] + ".tex", "w") as f:
	f.write(html)

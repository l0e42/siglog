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

def text(item):
	txt =  item['text']
	txt = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+([a-zA-Z]|[0-9]|\/)+",  '<a href=\"\g<0>\">\g<0></a>',txt)	
	return txt

def info(item):
	return item['text']

def meta(item):
	return "<p class=\"meta\">" + text(item) + "</p>"

def dates(item):

	if len(item['text']) == 1:
		return item['text'][0]['name'] + ": " + item['text'][0]['date'] + "<br>"
	else:
		txt = ""
		txt += "<table>"
		for y,x in enumerate(item['text']):
			if y %2 == 0:
				txt += "<tr>" + process(x) +  " </tr>"
			else:
				txt += "<tr class=\"odd\">" + process(x) +  " </tr>"
		txt += "</table>"
	return txt

def date(item):
	txt = ""
	txt += "<td>" + item['name'] + ": &nbsp; </td>"
	txt += "<td>" + item['date'] + "</td>"
	return txt


def miniul(item):
	txt = ""
	txt += "<ul>"
	for x in item['text']:
		txt += "<li>" + process(x) +  " </li>"
	txt += "</ul>"
	return txt

def ul(item):
	if item['type']!= 'ul':
		raise ValueError

	txt = ""
	txt += "<ul>"
	for x in item['text']:
		txt +=  process(x) 
	txt += "</ul>"
	return txt

def li(item):
	if item['type']!= 'li':
		raise ValueError

	txt = ""
	txt += "<li>"
	for x in item['text']:
		txt +=  process(x) 
		if x['type'] not in ['miniul','dates']:
			txt += "<br/>"
	txt += "</li>"
	return txt




def title(item):
	txt = "<h2>"
	if item['tag']:
		txt += "<a id=\"{}\" name=\"{}\" ></a>".format(item['tag'],item['tag'])

	txt += item['text']
	txt += "</h2>"
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

	# if email:
	# 		return item['content']
	# else:
	return "<a href=\"#{}\">{}</a>".format(item['slug'],item['content'])



def toc(items):
	html = ""
	html += "<h2>"
	html += "<a name=\"toc\" id=\"toc\"></a>"
	html += "Table of Content"
	html += "</h2>"


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

	html += "<h2>"
	html += "<a name=\"deadlines\" id=\"deadlines\"></a>"
	html += "Deadlines"
	html += "</h2>"


	return html + process(document['dates'])

for x in document:
	print(x)
html = """<!DOCTYPE html><html lang="en">
<head>
 <meta charset="UTF-8">
<style>
.main{
	max-width: 800px;
	font-family: monospace, monospace;
	font-size:13px;
}
table tr td {
	font-family: monospace, monospace;
	font-size: 13px;
}
.siglog {
    top: 4px;
    position: relative;
}
.meta {
	margin:0;
	margin-left:20px;
}
h2{
	margin-bottom:0;
	margin-top:20px;
	font-size:18px;;
}
ul{
	margin:0;
	padding-left: 20px;
}

h1 {
    font-size: 22px;
    margin:0;
}
.odd {
	background: #DDD;
}
</style>"""
html += """
<title>SIGLOG Monthly {}</title>
</head><body><div class="main">
""".format(document['number'])
if email :
	html += """
<h1>SIGLOG Monthly {}</h1>
""".format(document['number'])
else:
	html += """
<h1><img alt="SIGLOG" src= " data:image/png;base64,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" 
class="siglog" /> Monthly {}</h1>
""".format(document['number'])

html += "<i>" + document['renderdate'].strftime("%B %d, %Y") + "</i><br>"
if email:
	html += """
<a href="https://lics.siglog.org/newsletters/{}.html"> View Online</a>
 - 
""".format(document['number'])
html +="""
<a href="https://lics.siglog.org/newsletters/">Past Issues</a>
 - 
<a href="https://lics.siglog.org/newsletters/inst.html">How to submit an announcement</a>
"""

html += toc(document)

html += doDates(document)

for x in document['items']:
	html += item(x)


html += "<br><br>To the <a href=\"http://siglog.org/\">SIGLOG</a> or <a href=\"https://lics.siglog.org\">LICS</a> website"
html += "</div>"
if email:
	html += "<br>\n" 
	html += "Kind regards, <br>\n"
	html += "David Purser <br>\n"
	html += "MPI-SWS"

html +="</body></html>"

import os
if email:
	with open("editions/"+ document['number'] + ".email.tmp.html", "w") as f:
		f.write(html)

	command = "css-inliner " +"editions/"+ document['number'] + ".email.tmp.html > "  +"editions/"+ document['number'] + ".email.html"
	os.system(command)
	os.remove("editions/"+document['number'] + ".email.tmp.html")
	print(command)

else:
	with open("editions/"+document['number'] +  ".html", "w") as f:
		f.write(html)

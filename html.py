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
	txt = "<h2 "
	if item['tag']:
		txt += "id=\"{}\" name=\"{}\" >".format(item['tag'],item['tag'])
	else:
		txt += " >"
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

	if email:
			return item['content']
	else:
		return "<a href=\"#{}\">{}</a>".format(item['slug'],item['content'])



def toc(items):
	html = ""
	html += "<h2 id=\"toc\" >"
	html += "TOC"
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

	html += "<h2 id=\"deadlines\" >"
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
	font-size:13px;
}
.siglog {
    height: 21px;
    top: 4px;
    position: relative;
    margin-right: 6px;
}
.meta {
	margin:0;
	padding:0;
	margin-left:10px;

}
h2{
	margin-bottom:0;
	margin-top:20px;
	font-size:18px;;
}
ul{
	margin:0;
	margin-left: 0; 
	padding-left: 20px;
}

h1 {
	display: inline-block;
    font-size: 22px;
    margin:0;
}
.odd {background: #CCC;}
</style>"""
html += """
<title>SIGLOG Monthly {}</title>
</head><body><div class="main">
""".format(document['number'])
if email :
	html += """
<h1>SIGLOG Monthly {}</h1>
<br>
""".format(document['number'])
else:
	html += """
<img alt="SIGLOG" src= "data:image/png;base64,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" 
class="siglog" /><h1>Monthly {}</h1>
<br>
""".format(document['number'])

html += "<i>" + dateparser.parse("today").strftime("%B %d, %Y") + "</i><br>"
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
html += "</div></body></html>"

with open(document['number'] + (".email" if email else "" )+ ".html", "w") as f:
	f.write(html)

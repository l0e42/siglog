import dateparser
import re
import sys
from pprint import pprint

try:
	arg1 = sys.argv[1]
	print(arg1)
	import glob, os
	file = [x for x in glob.glob(arg1 + "*.txt")]
	print(file[0])
except:
	print("No argument, or file not found")
	exit()



document = {
	'dates': {},
	'items': [],
	'number': arg1

}

def info(current, data):

	addObject(current,{
		'type': 'info',
		'text': data
	})
	if 'info' not in current:
		current['info'] = []
	current['info'].append(data)

def meta(current, data):

	addObject(current,{
		'type': 'meta',
		'text': data
	})

def ul(current, data):

	if 'objects' not in current:
		current['objects'] =[]

	if len(current['objects']) ==0 or not current['objects'][-1]['type'] == "ul":
		current['objects'].append({
			'type': 'ul',
			'text': []
		})

	current['objects'][-1]['text'].append({
		'type':"li",
		'text': []
	})

	uladd(current,data)

def ulobjectadd(current,obj):
	if isUL(current):
		current['objects'][-1]['text'][-1]['text'].append(obj)
	else:
		print("not a UL")
		raise ValueError
		exit()

def uladd(current,data):

	data = re.sub(r"\s*\*","",data)
	return ulobjectadd(current, {
			'type':'text',
			'text': data
		})

def miniul(current,data):
	if isUL(current):

		data = re.sub(r"\s*-","",data)
		if len(current['objects'][-1]['text'][-1]['text'])  ==0 or current['objects'][-1]['text'][-1]['text'][-1]['type'] != 'miniul':
			current['objects'][-1]['text'][-1]['text'].append({
				'type':'miniul',
				'text': []
			})
		
		current['objects'][-1]['text'][-1]['text'][-1]['text'].append({
			'type':'text',
			'text':data
		})

	else:
		print("not a UL")
		exit()

def extractDate(right):
	if "(" in right:
		right = right.split("(")[0]
	try: 
		right = dateparser.parse(right).strftime("%b %d, %Y")
		return right
	except:
		# really need it to pass here
		print("failed", right)
		exit()
		pass

def date(current,data):

	
	infomation = data.split(":")
	left = re.sub("-d[v|M|h]*", "", infomation[0])
	left = left.replace("-d", "")
	left= left.strip()
	right = infomation[1].strip()
	
	global document
	if bool(re.match(r"\s*-dM",line)):
		document['dates'][left] = [{
			'name': left,
			'verbatim': right,
			'real': dateparser.parse(extractDate(right))
		}]
		return

	if isUL(current):
		if len(current['objects'][-1]['text'][-1]['text'])  ==0 or current['objects'][-1]['text'][-1]['text'][-1]['type'] != 'dates':
			
			current['objects'][-1]['text'][-1]['text'].append({
				'type':'dates',
				'text': []
			})
	
		
		if bool(re.match(r"\s*-dh",line)):
			right = extractDate(right)
			if current['acc'] not in document['dates']:
				document['dates'][current['acc']] = []

			document['dates'][current['acc']].append({
			'name':left,
			'date': right,
			'real': dateparser.parse(right)
		})

		if bool(re.match(r"\s*-dv",line)):
			right = infomation[1].strip()	
		else: 
			try: 
				right = dateparser.parse(infomation[1].strip()	).strftime("%b %d, %Y")
			except:			
				right = infomation[1].strip()	
				pass

		current['objects'][-1]['text'][-1]['text'][-1]['text'].append({
			'type':'date',
			'name':left,
			'date': right
		})

	else:
		print("not a UL")
		exit()

def isUL(current):
	if 'objects' not in current:
		return False
	if len(current['objects']) == 0:
		return False
	if current['objects'][-1]['type'] == 'ul':
		return True

def addObject(current, item):
	if 'objects' not in current:
		current['objects']= []
	current['objects'].append(item)

def title(current, data):

	if ':' in data:
		acc = data.split(":")[0].strip()
		title = data.split(":")[1].strip()

	else: 
		title = data.strip()
		acc = None

	current['title'] = title
	current['acc'] = acc
	addObject(current, {
		'type': 'title',
		'tag': re.sub(r"\s","_",acc) if acc else None,
		'text': data
	})


with open(file[0], 'r') as f:
	Lines = f.readlines() 
	  
	count = 0
	# Strips the newline character 
	current = {}

	for line in Lines: 
		line = line.replace("\n","")

		if line.strip() == "":
			print('new block')
			document['items'].append(current)
			current = {}
		elif  bool(re.match(r"[A-Z|a-z|0-9]", line)):
			if 'title' not in current:
				print('title', line)
				title(current,line)
			else:
				print('info',line)
				info(current, line)
		elif bool(re.match(r"\s*[A-Z|a-z|0-9]",line))  and not isUL(current):
			meta(current,line)
		elif bool(re.match(r"\s*[A-Z|a-z|0-9]",line))  and isUL(current):
			uladd(current,line)
		elif bool(re.match(r"\s*\*",line)):
			ul(current,line)
		elif bool(re.match(r"\s*-d",line)):
			date(current,line)
		elif bool(re.match(r"\s*-",line)):
			miniul(current,line)
		else:
			print("don't know how to handel", line)
			raise ValueError


types = [", ".join(x['info']).split(" ")[0] for x in document['items'] if 'info' in x]
output = []

elements  = [{
			"type": "li",
			"text": [{"type":"tag", 
						'slug': 'deadlines',
						'content': 'DEADLINES'
					}]
			}]


for typ in types:
	if typ not in output:
		output.append(typ)

		if typ == "CALL":
			elements.append(
			{
				"type": "li",
				"text": [{ "type": "text", "text" : 'CALLS'},
					{
					"type":"miniul",
					"text": [{
								"type": "tag",
								"slug": re.sub(r"\s","_",x['acc']),
								"content": "{} {}".format(x['acc'], "({})".format(", ".join(x['info'])) if 'info' in x else '')
								} for x in document['items'] if 'acc' in x and x['acc'] and  "CALL" in ", ".join(x['info'])]
					}
				]
			})
		else: 
			jobs = [x for x in document['items'] if 'info' in x and typ in x['info']]
			if len(jobs) > 0:
				elements.append({
							"type": "li",
							"text": [{ "type": "text", "text" : typ + 'S'},
								{
								"type":"miniul",
								"text": [{
											"type": "tag",
											"slug": re.sub(r"\s","_",x['acc']),
											"content": "{}".format(x['acc'])
											} for x in jobs]
								}
							]
						})
print(jobs)

document['toc'] = {
		"type": "ul",
		"text": elements
	}


lst = list(document['dates'].items())
print(lst)
lst.sort(key=lambda x: x[1][0]['real'])
print(lst)

ul = {
			'type':'dates',
			'text': []
		}
	
for x,t in lst:
	data =  ", ".join([y['verbatim'] if 'verbatim' in y else y['date'] + " ({})".format(y['name'].replace("submission","").strip())  for y in t])
	ul['text'].append({
	'type':'date',
	'name': x,
	'date': data
})			
document['dates'] = ul
document['parsedate'] = dateparser.parse("today")



pprint(document)
import pickle
pickle.dump(document, open( "save.p", "wb" ) )


import json
from bs4 import BeautifulSoup as bs
import requests
import os
import re
import MySQLdb

def insert_data():

	name_map = {
		'班级': 'class',
		"班級": 'class',
		'班次': 'class',
		'学号': 'stud_no',
		'组别': 'group',
		'媒介': 'medium',
		"创作心路": 'creative_mind',
		"作品简介": 'description',
		"作品介绍": 'description',
		"简介": 'description',
		"感想": "thought", 
		"": ""
	}

	data = json.load(open("data.json", 'r', encoding="utf-8"))[9]['components']['block1']['items'][0]['components']['block1']['items'][0]['components']['block1']['items']
	data2 = [[]]
	for i in [i for i in data if i['type'] != "Spacer"]:
		if i['type'] == "Separator":
			data2.append([])
		else:
			data2[-1].append(i)

	result = []

	for i in [i for i in data2 if i]:
		if i[0]['type'] == "RichText": 
			name, id = bs(i[0]['value'], 'lxml').text[1:].split("S")
			name = name.split("》")[0]
			id = 'S'+re.sub(r'（.*?）', '', id)
			items = i[1]['components']
			stud_name = bs(items['text1']['value'], 'lxml').text.strip()
		else:
			items = i[0]['components']
			
			name, id = stud_name, id = bs(items['text1']['value'], 'lxml').text.strip().split("S")
			name = name.split("》")[0]
			id = "S"+re.sub(r'（.*?）', '', id)

		if not os.path.exists(f"../../assets/exhibition/{id}.jpg"):
			open(f"../../assets/exhibition/{id}.jpg", "wb").write(requests.get(f"https://user-images.strikinglycdn.com/res/hrscywv4p/image/upload/c_limit,fl_lossy,h_9000,w_1200,f_auto,q_auto/{items['media1']['image']['storageKey']}.jpeg").content)

		meta = dict([(v:=re.split(r":|：", i[0])) and [name_map[v[0].strip() if v[0].strip() in name_map else "班级"], v[1].strip() if len(v) > 1 else v[0].strip()] for i in eval(str([list(i.children) for i in bs(items['text2']['value'], 'lxml').find_all('span')]).replace(", <br/>, ", '],['))])

		meta2 = dict([((v:=re.split(r":|：", w) if (w:=bs(items['text3']['value'], 'lxml').text.strip()) else ["", ""]) and [name_map[v[0].strip()], v[1].replace("\xa0", "")])])
		if '' in meta2: meta2 = {}

		if len(i) >= 3:
			meta3 = dict([((v:=re.split(r":|：", w) if (w:=bs(i[2]['value'], 'lxml').text) else ["", ""]) and [name_map[v[0].strip()], v[1].replace("\xa0", "")])])
		else: meta3 = {}

		result.append({
			"id": id,
			"name": name,
			"stud_name": stud_name,
			**meta, 
			**meta2,
			**meta3
		})

	print([i['class'] for i in result if 'class' in i])
	
	conn = MySQLdb.connect(user='thecodeb_thecodeb', passwd='redaxe3636', host='thecodeblog.net', db='thecodeb_colorsoflife', charset="gbk")
	c = conn.cursor()

	for i in [(
		i['id'],
		i['name'].replace("\u2022", "|").replace("\u200b", "").replace("\xa0", "") if 'name' in i else "", 
		i['stud_name'].replace("\u200b", "").replace("\xa0", ""),
		i['class'].replace("\u200b", "").replace("\xa0", "") if "class" in i else "",
		int(i['stud_no']) if "stud_no" in i else None,
		i['group'].replace("\u200b", "").replace("\xa0", "") if 'group' in i else "",
		i['medium'].replace("\u200b", "").replace("\xa0", "") if "medium" in i else "",
		i['description'].replace("\u200b", "").replace("\xa0", "").replace("\U0001f926", "").replace("\U0001f3fb", "").replace("\u200d", "").replace("\ufe0f", "").replace("\u270c", "").replace("\U0001f4ab", "") if "description" in i else "",
		i['thought'].replace("\u200b", "").replace("\xa0", "").replace("\U0001f926", "").replace("\U0001f3fb", "").replace("\u200d", "").replace("\ufe0f", "").replace("\u270c", "").replace("\U0001f4ab", "") if "thought" in i else "",
		i['creative_mind'].replace("\u200b", "").replace("\xa0", "").replace("\U0001f926", "").replace("\U0001f3fb", "").replace("\u200d", "").replace("\ufe0f", "").replace("\u270c", "").replace("\U0001f4ab", "") if "creative_mind" in i else ""

	) for i in result]:
		c.execute("INSERT INTO exhibition (id, name, stud_name, class, stud_no, group_, medium, description, thought, creative_mind) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", i)

	conn.commit()


conn = MySQLdb.connect(user='thecodeb_thecodeb', passwd='redaxe3636', host='thecodeblog.net', db='thecodeb_colorsoflife', charset="gbk")
c = conn.cursor()
c.execute('UPDATE exhibition SET description = SUBSTRING(description, 1, CHAR_LENGTH(description) - 2) WHERE RIGHT(description, 2) = "感想"')
conn.commit()
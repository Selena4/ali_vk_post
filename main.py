import json
import os
import sys
import random
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import vk_api
import time

os.system('clear')
#--------------------------------------------------------

items_id = []
item = open("items_id", "r")
for line in item:
	line_2 = line
	if line[len(line)-1:] == "\n":
		line_2 = line[:-1]
	items_id.append(line_2)

item.close()

#----------------------Config-----------------------------


login = ""
password = ""
tbp = 28800 #time between posts (unixtime-format)
group_id = 0 #int, group that will be post
group_ph_id = 0 #int, group that will be save photos
album_id = 0 #int, album in group_ph_id


#---------------------------------------------------------

tries = 0
time = time.time()
hashtag = '#ali #aliexpress #hoodie #али #алиэкспресс #худи #толстовка'
symbols = ["0","1","2","3","4","5","6","7","8","9","-"]

#---------------------------------------------------------

def show_ids():
	text_id = ''
	links = open("items_id", 'r')
	for i in links:
		id = i
		if i[len(i) -1: ]== "\n":
			id = i[:-1]
		text_id = text_id + id + ', '
	links.close()
	text_id = text_id[:-1]
	os.system('clear')
	print('items\' id: ' + text_id)
	return
	
#---------------------------------------------------------

def check_inf():
	os.system('clear')
	try:
		vk_session = vk_api.VkApi(login, password)
		vk_session.auth()
		vk = vk_session.get_api()			
	except:
		print('failed to log in. please check settings or your connection')
		return
	print('group_id: ' + str(group_id))
	print("members: " + str(vk.groups.getMembers(group_id=group_id)["count"]))
	print('account_id: ' + str(vk.users.get(access_token=True)[0]['id']))
	print('posts on the wall: ' + str(vk.wall.get(owner_id=int(-1 * group_id))["count"]))

#---------------------------------------------------------

def dolrate():
	main_url = r"https://api.exchangerate-api.com/v4/latest/USD"
	response = requests.get(main_url)
	data = response.json()
	os.system('clear')
	drate = data['rates']['RUB']
	print('dollar rate now is: ' + str(data['rates']["RUB"]) + 'RUB')
	
def drate():
	main_url = r"https://api.exchangerate-api.com/v4/latest/USD"
	response = requests.get(main_url)
	data = response.json()
	drate = data['rates']['RUB']

#---------------------------------------------------------

def number_links():
	handle = open("links", "r")
	vlinks = 0
	for line in handle:
		vlinks = vlinks + 1
	os.system('clear')
	print('number of links: ' + str(vlinks))

#---------------------------------------------------------
def backup():
	os.system('cat links > links_backup')
	os.system('clear')
	print('backup successfully, check links_backup')
def restore():
	os.system('cat links_backup > links')  
	os.system('clear')
	print('restore successfully, check links')

#---------------------------------------------------------

def settings():
	global login,password,tbp,group_id,group_ph_id,album_id
	while True:
		os.system('clear')
		print('1) login:		' + login)
		print('2) password:		' + password)
		print('3) time beetween posts:	' + str(tbp))
		print('4) group_id:		' + str(group_id))
		print('5) group_ph_id:		' + str(group_ph_id))
		print('6) album_id:		' + str(album_id))
		print('7) exit')
		choice = input('>> ')
		if choice == '1':
			login = input('new login: ')
		if choice == '2':
			password = input('new password: ')
		if choice == '3':
			tbp = input('time beetween posts(in unixtime): ')
		if choice == '4':
			group_id = int(input('group that will be post products(integer): '))
		if choice == '5':
			group_ph_id = int(input('group that will be save images on vk\'s server(integer): '))
		if choice == '6':
			album_id = int(input('album with photos in group_ph_id: '))
		if choice == '7':
			os.system('clear')
			print('settings have been save')
			return

#---------------------------------------------------------

def check_lfch():
	links = open("links", 'r')
	ids = []
	ids_copy = []
	new_ids = ''
	for i in links:
		link = i
		if i[len(i) -1: ]== "\n":
			link = i[:-1]
		ids.append(link[31:link.index(";")-5])
	links.close()
	
	links = open("items_id", 'r')
	for i in links:
		link = i
		if i[len(i) -1: ]== "\n":
			link = i[:-1]
		ids.append(link)
	links.close()
	if '' in ids:
		ids = ids[:-1]


	lfch = open('links_for_check','r')
	for ll in lfch:
		link = ll
		if ll[len(ll) -1: ]== "\n":
			link = ll[:-1]
		id = link[31:-5]
		if id in ids:
			print(id + ' is used already')
			ids_copy.append(id)
		else:
			new_ids = new_ids + link + '\n'


	lfch.close()
	lfch = open('links_for_check','w')
	lfch.write(new_ids)
	lfch.close()
	print('ids: ' + str(ids_copy) + ' was deleted from the file')
	return
		
#---------------------------------------------------------

def create_post(url,urlcash,num):
	sizes = ''
	sex = ''
	brand = ''
	material = ''
	types = ''
	price_rub = ''
	names = []
	attachments = ''

#-----------------Parsing data of product-----------------
	
	html = urlopen(url).read()
	bsObj = bs(html,'html.parser')
	for i in bsObj.findAll('script'):
		if "window.runParams" in i.text:
			script = i.text
	database = script	 
	for k in range(2):
		database = database[database.index('{')+1:]
	change = 'data = {'
	for l in range(len(database)):
		if database[l:l+5] == "false":
			change = change + "F"
			continue
		elif database[l:l+4] == "true":
			change = change + "T"
			continue
		elif database[l:l+9] == "csrfToken":
			break
		else:
			change = change + database[l]
	
	change = change[:-26]
	exec(change, globals())

#----------------Checking item in a database---------------

	if data["actionModule"]["productId"] in items_id:
		print('product' + str(data["actionModule"]["productId"]) + ' was used. sorry.')
	else:
		items_id.append(data["actionModule"]["productId"])

#--------------------------Sizes---------------------------

	for size in data["skuModule"]["productSKUPropertyList"][1]["skuPropertyValues"]:
		sizes = sizes + size["propertyValueName"] + ", " 	
	sizes = sizes[:-2]

#-----------------Converting RUB to Dollars----------------

	try:
		price = data["priceModule"]["formatedActivityPrice"][:-5]
	except:
		price = data["priceModule"]["formatedPrice"][:-5]
	for m in price:
		if m == ",":
			price_rub = price_rub + "."
		elif m in symbols:
			price_rub = price_rub + m
		else:
			continue
	if "-" in price_rub:
		first_price = price_rub[:price_rub.index('-')]
		second_price = price_rub[price_rub.index('-')+1:]	
		first_usd = round(float(first_price) /drate,2)
		second_usd = round(float(second_price) / drate,2)
		price_usd = str(first_usd) + "-" + str(second_usd)
	else:
		price_usd = round(float(price_rub) / drate,2)
	all_price = str(price_usd) + '$ / ' + str(price_rub) + 'RUB'

#----------------------------------------------------------

	for z in data["specsModule"]["props"]:
		if z["attrName"] == "Бренд":
			brand = z["attrValue"]
			brand = brand[:1].upper() + brand[1:]
		elif z["attrName"] == "Материал":
			material = z["attrValue"]
			material = material[:1] + material[1:].lower()
		elif z["attrName"] == "Пол":
			sex = z["attrValue"]
			sex_eng = {"Женщина":"Female","Мужчины":"Male"}
			sex = sex_eng[sex]
		elif z["attrName"] == "Тип товара":
			types = z["attrValue"]
	
	if sex == '':
		sex = "Male/Female"
	if brand == '':
		brand = "None"
	if material == '':	
		material = "None"
	if types == '':	
		types = "None"
	if sizes == '':
		sizes = "None"

#--------------------Downloading photos---------------------

	photos = data['imageModule']['imagePathList']
	for photo in photos:
		
		name = ''
		for _ in range(20):
			name = name + chr(random.randint(97,122))
		names.append(name)
		img_data = requests.get(photo).content
		with open('photos/' + name + '.jpg', 'wb') as handler:
    			handler.write(img_data)

#-----------------------------------------------------------

	upload = vk_api.VkUpload(vk_session)
	for n in names:
		photo = upload.photo('photos/' + n + '.jpg',album_id = album_id,group_id=group_ph_id)
		attachments = attachments + 'photo' + str(photo[0]['owner_id']) + "_" + str(photo[0]['id']) + ','
	attachments = attachments[:-1]
	vk.wall.post(owner_id=int(-1 * group_id),attachments = attachments, message=brand + " " + all_price + '\nSex: ' + sex + "\nType: " + types + "\nMaterial: " + material + "\nSize: " + sizes + "\n\n" + linkcash + '\n\n' + hashtag,publish_date = time + (tbp * num))
	print('post #' + str(num) + ' was posted successfully')  

#-----------------------------------------------------------

def main_post():
	try:
		vk_session = vk_api.VkApi(login, password)
		vk_session.auth()
		vk = vk_session.get_api()			
	except:
		os.system('clear')
		print('failed to log in. please check settings or your connection')
		return
	print('group_id: ' + str(group_id))
	print("members: " + str(vk.groups.getMembers(group_id=group_id)["count"]))
	print('account_id: ' + str(vk.users.get(access_token=True)[0]['id']))
	print('posts on the wall: ' + str(vk.wall.get(owner_id=int(-1 * group_id))["count"]))
	handle = open("links", "r")
	vlinks = 0
	for line in handle:
		vlinks = vlinks + 1
	print('number of links: ' + str(vlinks))

#---------------------------------------------------------

	handle = open("links", "r")
	for line in handle:
		links = line
		if links[len(links)-1:] == "\n":
			links = links[:-1]
		link = links[:links.index(';')]
		linkcash = links[links.index(';')+1:]
		create_post(link,linkcash,tries) 
		tries = tries + 1
	handle.close()
	handle = open("links", "w")
	handle.write('')
	handle.close()

#--------------------------------------------------------

	ids_item = ''
	for h in items_id:
		ids_item = ids_item + str(h) + '\n'
	item = open("items_id", "w")
	item.write(ids_item)
	item.close()

#--------------------------------------------------------


def main():
	try:
		drate()
	except:
		print('check your connection')

	commands = {
	"1": "main_post()",
	"2": "settings()",
	"3": "check_lfch()",
	"4": "backup()",
	"5": "show_ids()",
	"6": "number_links()",
	"7": "check_inf()",
	"8": "dolrate()",
	"952": "restore()",
	}
	while True:
		try:
			print('Choose an operation:')
			print('1) start posting')
			print('2) check settings')
			print('3) check file \'links_for_check\' to matches')
			print('4) make backup links')
			print('5) print all items\' ids')
			print('6) print the number of links')
			print('7) check information about group')
			print('8) check rate of dollar')
			print('952) restore links from backup')
			print('0) exit')		
			choice = input('>> ')
			if choice == "0":
				break
			if choice in commands.keys():
				exec(commands[choice])
			else:
				os.system('clear')
				print('incorrect command')
		except:
			os.system('clear')		
			print('ERROR')
if __name__ == '__main__':
	main()

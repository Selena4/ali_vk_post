import random
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import vk_api
import time
 
vk_session = vk_api.VkApi('****','****')
vk_session.auth()
time = time.time()
tries = 1
vk = vk_session.get_api()
hashtag = '#ali #aliexpress #hoodie #али #алиэкспресс #худи #толстовка'
def create_post(url,urlcash,num):
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
    sizes = '' 
    sex = ''
    brand = ''
    material = ''
    types = ''
    numbers = ["0","1","2","3","4","5","6","7","8","9","-"]
    for size in data["skuModule"]["productSKUPropertyList"][1]["skuPropertyValues"]:
        sizes = sizes + size["propertyValueName"] + ", "    
    sizes = sizes[:-2]
    try:
        price = data["priceModule"]["formatedActivityPrice"][:-5]
    except:
        price = data["priceModule"]["formatedPrice"][:-5]
    price_rub = ''
    for m in price:
        if m == ",":
            price_rub = price_rub + "."
        elif m in numbers:
            price_rub = price_rub + m
        else:
            continue       
    if "-" in price_rub:
        first_price = price_rub[:price_rub.index('-')]
        second_price = price_rub[price_rub.index('-')+1:]  
        first_usd = round(float(first_price) * 0.016,2)
        second_usd = round(float(second_price) * 0.016,2)
        price_usd = str(first_usd) + "-" + str(second_usd)
    else:
        price_usd = round(float(price_rub) * 0.016,2)
   
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
    all_price = str(price_usd) + '$ / ' + str(price_rub) + 'RUB'
    photos = data['imageModule']['imagePathList']
    names = []
    attachments = ''
    for photo in photos:
       
        name = ''
        for _ in range(20):
            name = name + chr(random.randint(97,122))
        names.append(name)
        img_data = requests.get(photo).content
        with open('photos/' + name + '.jpg', 'wb') as handler:
                handler.write(img_data)
    upload = vk_api.VkUpload(vk_session)
    for n in names:
        photo = upload.photo('photos/' + n + '.jpg',album_id = 266713678,group_id=186814318)
        attachments = attachments + 'photo' + str(photo[0]['owner_id']) + "_" + str(photo[0]['id']) + ','
    attachments = attachments[:-1]
    vk.wall.post(owner_id=-186779764,attachments = attachments, message=brand + " " + all_price + '\nSex: ' + sex + "\nType: " + types + "\nMaterial: " + material + "\nSize: " + sizes + "\n\n" + linkcash + '\n\n' + hashtag,publish_date = time + (43200 * num))
    print('post #' + str(num) + ' was posted succesfully')  
 
print('group_id: 186779764')
print("members: " + str(vk.groups.getMembers(group_id=186779764)["count"]))
print('account_id: ' + str(vk.users.get(access_token=True)[0]['id']))
print('posts on wall: ' + str(vk.wall.get(owner_id=-186779764)["count"]))
handle = open("links", "r")
vlinks = 0
for line in handle:
    vlinks = vlinks + 1
print('value of links: ' + str(vlinks))
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

import time
from bs4 import BeautifulSoup
import re
import json
import requests
import time
import re
import datetime
from datetime import date
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
bd = myclient["mydatabase"]
row = bd["customers"]

def getTitle(html):        
    title = html.find("h1")
    title_value = title.get_text()
    return {"title":title_value.strip()}

def getDescription(html):
    description = html.find("div",class_="item-description__text")
    description_value = description.get_text()    
    return {"description":description_value.join(description_value.split())}
def getComercialKind(html):
    kind = html.find("p",class_="card-title")
    kind_value = kind.get_text()    
    return {"kind":kind_value.join(kind_value.split())}
def getLatLang(html):
    p = re.compile('var dynamicMapProperties = (.*);')        
    scripts = html.find_all("script", {"src":False})
    
    el = 14
    indice = 0
    for script in scripts: 
        indice = indice + 1       
        if script:                     
            if indice == el:
                print(type(script))
                print(script)    
                
            result = script.prettify().find('geeks') 
            print(result)
            m = p.search(script.string)
            if m:
                print(script)
                print m.group(1)
    
def getUniqueCode(html):
    code = html.find("span",class_="item-info__id-number")    
    code_value = code.get_text()    
    return {"code":code_value.replace("#","")}
def getSpecs(html):
    specs = html.find_all('li',class_="specs-item")    
    items = []
    for spec in specs:
        title = spec.find("strong")
        title_value = title.get_text()
        value = spec.find("span")
        value_value = value.get_text()
        items.append({title_value.strip():value_value.strip()})
    response = {}    
    for item in items:        
        response.update(item) 
    return response
def getPublicationDate(html):
    info = html.find("div",class_="info-property-date")
    value = info.find("p",class_="info")
    fecha = value.get_text()    
    campo = fecha.split("-")
    f_date = date(int(campo[2]),int(campo[1]),int(campo[0]))
    l_date = date.today()    
    delta = l_date - f_date        
    return {"date":str(fecha),"delta":str(delta.days)}

cantidadRegistros = 0
flag = True
url = 'https://www.portalinmobiliario.com/arriendo/departamento/concepcion-biobio/_OrderId_BEGINS*DESC'
fullDate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
month = datetime.datetime.now().strftime("%m")
year = datetime.datetime.now().strftime("%Y")
response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')
anuncios = soup.find_all("li", class_="ui-search-layout__item")
for anuncio in anuncios:       
    a_tag = anuncio.find('a', href=True)
    url = a_tag['href']
#    print("url : "+str(url))
    response = requests.get(url)
    anuncio_html = BeautifulSoup(response.text,'html.parser')
    title = getTitle(anuncio_html)    
    #print(title)
    description = getDescription(anuncio_html)
    #print(description)
    kind = getComercialKind(anuncio_html)
    #print(description)
    specs = getSpecs(anuncio_html)
    #print(specs)
    publication = getPublicationDate(anuncio_html)
    #print(publication)
    code = getUniqueCode(anuncio_html)
    #print(code)
    #getLatLang(anuncio_html)
    #mydict = { "name": "John", "address": "Highway 37" }
    final_dict = {}
    final_dict.update(title)
    #final_dict.update(description)
    final_dict.update(kind)
    final_dict.update(specs)
    final_dict.update(publication)
    final_dict.update(code)
    print(final_dict)
    x = row.insert_one(final_dict)

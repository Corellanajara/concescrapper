import time
from bs4 import BeautifulSoup
import re
import json
import requests
import time
import re
import datetime
from datetime import date


def getTitle(html):    
    #print((html))
    title = html.find("h1")
    title_value = title.get_text()
    print(title_value)
def getDescription(html):
    description = html.find("div",class_="item-description__text")
    description_value = description.get_text()
    print(description_value)
def getComercialKind(html):
    kind = html.find("p",class_="card-title")
    kind_value = kind.get_text()
    print(kind_value)
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
    print("Codigo unico : " + code_value)
def getSpecs(html):
    specs = html.find_all('li',class_="specs-item")    
    for spec in specs:
        title = spec.find("strong")
        value = spec.find("span")
        print(str(title.get_text().encode('utf-8')) + " : "+str(value.get_text().encode('utf-8')))
def getPublicationDate(html):
    info = html.find("div",class_="info-property-date")
    value = info.find("p",class_="info")
    fecha = value.get_text()
    print("fecha "+ fecha)
    campo = fecha.split("-")

    f_date = date(int(campo[2]),int(campo[1]),int(campo[0]))
    l_date = date.today()    
    delta = l_date - f_date    
    print("Fecha Publicacion : " + str(fecha) )
    print("Dias desde publicacion : " + str(delta.days))

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
    getTitle(anuncio_html)
    getDescription(anuncio_html)
    getComercialKind(anuncio_html)
    getSpecs(anuncio_html)
    getPublicationDate(anuncio_html)
    getUniqueCode(anuncio_html)
    getLatLang(anuncio_html)
    

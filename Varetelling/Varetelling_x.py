import datetime
import tkinter as tk
import os
import json

from standardFunc import generate_item, generate_item_for_regestry


def hentInnhold(filnavn,telling=False):
    infile = open(filnavn, encoding="utf-8")
    try:
        innhold = json.load(infile)
    except json.decoder.JSONDecodeError:
        innhold = None    
        print("Need a JSON file")
        
    infile.close()
    return innhold

def findItem(contents,item_to_find={},barcode=0):
    if barcode:
        Barcode = str(barcode)
    else:
        Barcode = str(item_to_find["Barcode"])
    try:
        return contents[Barcode]
    except KeyError:
        return None

def placeItem(item_to_place,contents):
    Barcode = str(item_to_place["Barcode"])
    try:
        return contents[Barcode]
    except KeyError:
        return None
    return addItem(item_to_place)

def addItem(Item):
    OK = 1
    if not isinstance(Item, dict):
        return not OK

    strekkode = str(Item["Barcode"])
    name = Item["Name"]
    vol = Item["Volume"]
    drink_type = Item["Type"]
    amount = Item["Amount"]
    Varekoder_innhold = hentInnhold("beholdning.json")
    index = findItem(Varekoder_innhold,Item) 
    if index == None:
        addedItem = generate_item_for_regestry(strekkode,name,vol, drink_type,amount)
        Varekoder_innhold.update(addedItem)
    else:
        old_amount = index["Amount"]
        new_amount = old_amount+amount
        Varekoder_innhold[strekkode]["Amount"] = new_amount
    

    Varekoder_innhold = json.dumps(Varekoder_innhold, indent=2, ensure_ascii=False )
    
    updated_Contents = open("beholdning.json","w",encoding="utf-8")
    updated_Contents.write(Varekoder_innhold)
    updated_Contents.close()
    return Varekoder_innhold


def findItemInContents(Barcode):
    Varekoder_innhold = hentInnhold("beholdning.json")
    item = findItem(Varekoder_innhold,barcode=Barcode)

    VareType = "Unknown"
    VareNavn = "Unknown"
    Mengde = "Unknown"
    if item != None:
        VareType = item["Type"]
        VareNavn = item["Name"]
        Mengde = item["Volume"]
    return VareType, VareNavn, Mengde

def Sale(BarCode):
    VareType, VareNavn, Mengde = findItemInContents(BarCode)
    sale_item = generate_item(BarCode,VareNavn,Mengde,VareType,-1)
    addItem(sale_item)

    today = datetime.datetime.today()
    year = today.year
    month = today.month
    day = today.day
    hour = today.hour
    minute = today.minute
    second = today.second
    Sale_file = "Salgsfiler/Sale_%d-%d-%d.csv" %(day,month,year)
    sale = open(Sale_file,"a+",encoding="utf-8")
    sale.write("%d:%d:%d; %s; %s; %s; %f  \n"%(hour,minute,second,BarCode, VareType, VareNavn,Mengde))
    sale.close()

if __name__ == "__main__":
    beholdning = hentInnhold("beholdning.json")

    Cola = generate_item(1,"Cola",0.5,"Soda",1)
    #addItem(Cola)
    beholdning = hentInnhold("beholdning.json")

    print(findItem(beholdning,barcode=1))
    print(Sale(1))
    
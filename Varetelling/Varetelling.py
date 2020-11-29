import datetime
import tkinter.filedialog as tkf
import tkinter.messagebox as tkm
import os
import json

from standardFunc import generate_item, generate_item_for_regestry


def hentInnhold(filnavn,telling=False):
    infile = open(filnavn, encoding="utf-8")
    fileending = filnavn[filnavn.find("."):]
    if fileending == ".json":
        try:
            innhold = json.load(infile)
        except json.decoder.JSONDecodeError:
            innhold = None
            print("Need a JSON file")
    elif fileending == ".csv":
        innhold = []
        for linje in infile:
            linje = linje.replace("\n","")                  #Remove next line sign
            linje = linje.split(";")                        #Split the line for its values
            innhold.append(linje)
    infile.close()

    return innhold

def findItem(contents,item_to_find):
    if isinstance(item_to_find,dict):
        Barcode = str(item_to_find["Barcode"])
        
    else:
        Barcode = item_to_find
    
    
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
    OK = True
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
    item = findItem(Varekoder_innhold,Barcode)
    
    VareType = "Unknown"
    VareNavn = "Unknown"
    Mengde = "Unknown"
    if item != None:
        VareType = item["Type"]
        VareNavn = item["Name"]
        Mengde = item["Volume"]
    return VareType, VareNavn, Mengde

def Sale(BarCode):
    OK = True
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
    sale.write("%d:%d:%d; %s; %s; %s; %s  \n"%(hour, minute, second, BarCode, VareType, VareNavn, Mengde))
    sale.close()
    
    return OK

def telling():
    sale_dir = os.getcwd()+"/Salgsfiler"
    try:
        file_path_string = tkf.askopenfilename(initialdir = sale_dir)
        dagens_salg = hentInnhold(file_path_string,telling=True)
    except FileNotFoundError:
        tkm.showinfo("Warning","Need Sale-file!")
        return False

    if not dagens_salg:
        return False

    dagens_salg_sortert = []
    counted = False
    for item in dagens_salg:
        strekkode = item[1]
        drikk_type = item[2]
        drikk_navn = item[3]
        counted = False
        for counted_item in dagens_salg_sortert:
            counted_strekkode = counted_item[0]
            if strekkode == counted_strekkode:
                counted_item[3] +=1
                counted = True
                break
        if not counted:
            dagens_salg_sortert.append([strekkode,drikk_type,drikk_navn,1])

    file_path_string = file_path_string[file_path_string.find("Sale"):]
    saleDate = file_path_string[file_path_string.find("_")+1:file_path_string.find(".")]
    Salefile_counted = "Salgsfiler/Sale_counted_%s.csv" %(saleDate)
    
    sale = open(Salefile_counted,"a+",encoding="utf-8")

    for salg in dagens_salg_sortert:
        sale.write("%s, %s: %d\n"%(salg[1],salg[2],salg[3]))
    sale.close()
    os.system("Notepad.exe " + Salefile_counted)

def lastSales(numberOfSalesToFetch = 5):
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    day = today.day
    file_path_string = "Salgsfiler/Sale_%d-%d-%d.csv" %(day,month,year)
    #file_path_string = "Salgsfiler/Sale_16-10-2020.csv"
    Sales = hentInnhold(file_path_string,telling=True)
    numberOfSales = len(Sales)
    return Sales[numberOfSales-numberOfSalesToFetch:]
    

if __name__ == "__main__":
    beholdning = hentInnhold("beholdning.json")

    Cola = generate_item(1,"Cola",0.5,"Soda",1)
    #addItem(Cola)
    beholdning = hentInnhold("beholdning.json")

    print(findItem(beholdning,1))
    print(Sale(1))
    telling()
    
import datetime
import tkinter as tk
import os
import QuickSorting as QS
import json



def hentInnhold(filnavn,telling=False):
    infile = open(filnavn, encoding="utf-8")
    innhold = []
    for linje in infile:
        linje = linje.replace("\n","")                  #Remove next line sign
        linje = linje.split(";")                        #Split the line for its values
        innhold.append(linje)
        if not telling:
            if len(linje)>3:
                    linje[3] = float(linje[3])                #Cast the number from str to float. 
    infile.close()
    return innhold

def hentInnhold_salg(filnavn):
    innhold = hentInnhold(filnavn)
    for idx,linje in enumerate(innhold):
        innhold[idx] = linje[0]
    return innhold

def countItems(array_to_count, to_count_for):
    NoItems = 0
    for item in array_to_count:
        if int(item) == int(to_count_for):
            NoItems+=1
    return NoItems

def genererDiff(vare_koder,salg):
    diff_tabell = []
    for vare in vare_koder:
        NoItems = countItems(salg,vare[0])*-1
        diff_tabell.append([vare[0],vare[1], vare[2],NoItems])
    return diff_tabell


def findItem(item_to_find, array_to_search_in):
    for idx, item in enumerate(array_to_search_in):
        if item[0] == item_to_find:
            return idx
    return None



def addItem(Item):
    strekkode, VareType, VareNavn, Mengde, Antall_inn = Item
    Varekoder_innhold = hentInnhold("beholdning.csv")
    
    index = findItem(strekkode,Varekoder_innhold)
    if index == None:
        Varer_file = open("Varer.csv",'a+', encoding="utf-8")
        Varer_file.write("\n%s;%s;%s;%s"%(strekkode,VareType,VareNavn, Mengde))
        Varer_file.close()
    regulerBeholdning(strekkode,VareType, VareNavn, Mengde, Antall_inn)
    

def regulerBeholdning(strekkode,VareType, VareNavn, Mengde, Antall_diff):
    beholdning_innhold = hentInnhold("beholdning.csv")
    beholdning_index = findItem(strekkode,beholdning_innhold)
    if beholdning_index == None:
        Antall = 0
        index = len(beholdning_innhold)
    else:
        index = beholdning_index
        Antall = int(beholdning_innhold[index][4])

    beholdning_file = open("beholdning.csv",'r', encoding="utf-8")
    contents = beholdning_file.readlines()
    beholdning_file.close()
    
    if beholdning_index != None:
        contents.pop(index)

    contents.insert(index, "%s;%s;%s;%s;%d\n" %(strekkode,VareType,VareNavn,Mengde,Antall+Antall_diff))
    beholdning_file = open("beholdning.csv",'w', encoding="utf-8")
    beholdning_file.writelines(contents)
    beholdning_file.close()

def Sale(BarCode):
    VareType, VareNavn, Mengde = findItemInContents(BarCode)
    regulerBeholdning(BarCode,VareType,VareNavn, Mengde, -1)

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

def lastSales(numberOfSalesToFetch = 5):
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    day = today.day
    file_path_string = "Salgsfiler/Sale_%d-%d-%d.csv" %(day,month,year)
    file_path_string = "Salgsfiler/Sale_16-10-2020.csv"
    Sales = hentInnhold(file_path_string,telling=True)
    numberOfSales = len(Sales)
    return Sales[numberOfSales-numberOfSalesToFetch:]
    

    

def findItemInContents(BarCode):
    Varekoder_innhold = hentInnhold("Varer.csv")
    index = findItem(BarCode,Varekoder_innhold)
    VareType = "Unknown"
    VareNavn = "Unknown"
    Mengde = "Unknown"
    if index != None:
        VareType = Varekoder_innhold[index][1]
        VareNavn = Varekoder_innhold[index][2]
        Mengde = Varekoder_innhold[index][3]
    return VareType, VareNavn, Mengde

def UpdateContents(sale_file):
    vare_koder = hentInnhold("Varer.csv")
    #vare_koder = StdSort(vare_koder)
    salg = hentInnhold_salg(sale_file)
    diff_tabell = genererDiff(vare_koder,salg)
    for linje in diff_tabell:
        regulerBeholdning(linje[0],linje[1],linje[2],linje[3],linje[4])
    

def StdSort(array, sortParam = 1):
    array = sorted(array,key=lambda l:l[sortParam])
    #print(array)
    return array

def oppdaterBeholdning(beholdning,VarerDiff):
    beholdning = StdSort(beholdning)
    for vare in beholdning:
        for idx,vareDiff in enumerate(VarerDiff):
            try:
                vareDiff.index(vare[0])
                break
            except ValueError:
                beholdning.append(vare)

        vare[2] = vare[2] + VarerDiff[idx][2]
    return beholdning
    
def telling():
    sale_dir = os.getcwd()+"/Salgsfiler"
    file_path_string = tk.filedialog.askopenfilename(initialdir = sale_dir)
    dagens_salg = hentInnhold(file_path_string,telling=True)
    if not dagens_salg:
        return False
    dagens_salg_sortert = []
    counted = False
    for item in dagens_salg:
        counted = False
        for counted_item in dagens_salg_sortert:
            if item[1] == counted_item[0]:
                counted_item[3] +=1
                counted = True
                break   
        if not counted:
            dagens_salg_sortert.append([item[1],item[2],item[3],1])
    
    dagens_salg_sortert = StdSort(dagens_salg_sortert,0)

    file_path_string = file_path_string[file_path_string.find("Sale"):]
    saleDate = file_path_string[file_path_string.find("_"):file_path_string.find(".")]
    Salefile_counted = "Sale_counted_%s.csv" %(saleDate)
    
    sale = open(Salefile_counted,"a+",encoding="utf-8")
    for salg in dagens_salg_sortert:
        sale.write("%s, %s: %d\n"%(salg[1],salg[2],salg[3]))
    sale.close()
    os.system("Notepad.exe " + Salefile_counted)


if __name__ == "__main__":
    None
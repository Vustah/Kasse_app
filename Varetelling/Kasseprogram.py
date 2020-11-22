import os
from Varetelling import addItem,Sale,UpdateContents,hentInnhold, findItemInContents, telling, lastSales
from standardFunc import generate_item, generate_item_for_regestry
from DisplayContents import oppdaterSkjerm
import threading
import datetime
from appJar import gui
import json


sale_file = "sale_file.csv" 
system_color = "Light blue"
system_text_color ="White"

def SystemSettings():
    app.setPadding([10,5])
    app.setBg(system_color)
    #app.setTextBg(system_text_color)

def updateContentsFunc():
    app.startTab("Update Contents")
    app.setBg(system_color)

    app.setStretch("both")
    app.setSticky("ew")
    app.addButton("Find File",press,0,0)
    app.addButton("Update",press,0,1)
    app.addLabel("sf1",sale_file,1,0,2)
    app.addLabel("up1"," ",2,0,2)

    app.stopTab()

def oppdaterSkjermThread(app):
    oppdaterSkjerm(app,intern=True)
    oppdaterSkjerm(app)

def press(button):
    global sale_file
    if button == "Add":
        addItemInRegestry()
        return
    elif button == "Salg":
        Salg()
        lastSalesToday()
        return
    elif button == "Find File":
        sale_file = app.openBox()
        app.setLabel("sf1",sale_file)
        app.clearLabel("up1")
        app.setLabelBg("up1",system_color)

    elif button == "Update":
        if sale_file:
            UpdateContents(sale_file)
            app.setLabel("up1","UPDATED CONTENTS")
            app.setLabelBg("up1","red")
        
    elif button == "Display Screen":
        
        launchSubWindow("Varer Inne")
    
    elif button == "Add Item":
        launchSubWindow("Add Item")
        setCheckItemEnter()
    
    elif button == "GlaTime":
        launchSubWindow("Normal Operation")
        returnToDefaultEnter()
    
    elif button == "Telling":
        telling()

    elif button == "See Contents":
        launchSubWindow("Contents")

    thread = threading.Thread(target=oppdaterSkjermThread, args=(app))
    thread.start()
    

def launchSubWindow(win):
    app.showSubWindow(win)


def Salg():
    strekKode = str(app.getEntry("Strekkode på salg"))
    app.clearAllEntries()
    if strekKode:
        Sale(strekKode)
        thread = threading.Thread(target=oppdaterSkjermThread, args=(app,))
        thread.start()

def checkIfItemExists():
    strekKode = str(app.getEntry("Strekkode"))
    VareType, VareNavn, Mengde = findItemInContents(strekKode)
    if VareType == "Unknown" or VareNavn == "Unknown" or Mengde == "Unknown":
        return None
    else:
        app.setEntry("Varetype", VareType, callFunction=False)
        app.setEntry("Varenavn", VareNavn, callFunction=False)
        app.setEntry("Mengde", Mengde, callFunction=False)


def addItemInRegestry():
    strekKode = str(app.getEntry("Strekkode"))
    Varenavn = app.getEntry("Varenavn")
    Varetype = app.getEntry("Varetype")
    Mengde = app.getEntry("Mengde")
    try:
        Antall_inn = int(app.getEntry("Antall"))
    except:
        Antall_inn = 0
    new_Item = generate_item_for_regestry(strekKode,Varenavn,Varetype,Mengde,Antall_inn)
#    addItem(new_Item)
    addItem([strekKode,Varetype,Varenavn,Mengde,Antall_inn])
    app.clearAllEntries()
    
def clearAllFields():
    app.clearAllEntries()
            
def AddItemWindow():
    app.startSubWindow("Add Item")
    SystemSettings()
    app.setSticky("ne")
    app.addButton("Add",press,5,3)

    #Labels
    app.addLabel("l1","Strekkode"   ,0,1) 
    app.addLabel("l4","Varetype"    ,1,1)
    app.addLabel("l2","Varenavn"    ,2,1)
    app.addLabel("l5","Mengde [L]"  ,3,1)
    app.addLabel("l3","Antall"      ,4,1)

    #Inputfield
    app.addEntry("Strekkode",0,2,2,0) #Fylle ut resten passert på strekkoden, om varen allerede eksister?
    varetyper = ["Øl","Glutenfritt","Cider","Brus","Alkoholfritt","Vin"]
    app.addAutoEntry("Varetype" ,varetyper,1,2,2,0)
    app.addEntry("Varenavn" ,2,2,2,0)
    app.addEntry("Mengde"   ,3,2,2,0)
    app.addEntry("Antall"   ,4,2,2,0)
    
    
    #app.appendAutoEntry("Varetype", varetyper)

    app.setStopFunction(setRegestryEnter)
    app.stopSubWindow()

def seeContents():
    app.startSubWindow("Contents")
    app.setInPadding(x=100,y=75)
    app.startScrollPane("Content",disabled="horizontal")
    SystemSettings()
    oppdaterSkjerm(app,intern=True,offset=2)
    app.stopScrollPane()
    app.stopSubWindow()


numberOfSalesToFetch = 5
def configLastSales():
    for i in range(numberOfSalesToFetch-1,-1,-1):
        app.addLabel("Sale_"+str(i))

def lastSalesToday():
    sisteSalg = lastSales(numberOfSalesToFetch)
    for idx in range(len(sisteSalg)-1, -1, -1):
        date = sisteSalg[idx][0]
        Type = sisteSalg[idx][2]
        name = sisteSalg[idx][3]
        mengde = float(sisteSalg[idx][4])
        logText = "%s: %s,%s,%.1f"%(date,Type,name,mengde)
        app.setLabel("Sale_"+str(idx), logText)


def NormalOperationWindow():
    app.startSubWindow("Normal Operation")
    SystemSettings()

    app.setBg(system_color)

    app.setStretch("collumn")
    app.setSticky("ne")
    app.addButton("Salg",press,1,2)
    app.setSticky("ew")
    configLastSales()
    lastSalesToday()
    app.addLabelEntry("Strekkode på salg",0,0,3,0)


    app.stopSubWindow()

def ItemsInRegestryButton():    
    app.startSubWindow("Varer Inne", modal=False)
    SystemSettings()
    oppdaterSkjerm(app,reopen=False)
    app.stopSubWindow()

def endOfDayCount():
    return



def setRegestryEnter():
    try:
        app.disableEnter()
    except:
        None
    return True

def setCheckItemEnter():
    try:
        app.enableEnter(checkIfItemExists)
    except:
        app.disableEnter()    
        app.enableEnter(checkIfItemExists)
    return True

def returnToDefaultEnter():
    try:
        app.enableEnter(Salg)
    except:
        app.disableEnter()    
        app.enableEnter(Salg)
    return True

def configButtons():
    app.addButton("GlaTime", press,0,0)
    app.addButton("Display Screen", press,1,1)
    app.addButton("Add Item", press,0,1)
    app.addButton("Telling", press, 1,0)
    app.addButton("See Contents", press, 2,0)

app = gui("Gla`timen Kasseprogram")

def main():
    
    app.startTabbedFrame("Gla`time")
    app.setTabbedFrameTabExpand("Gla`time", expand=True)
    app.setFont("Times")
    
    

    configButtons()
    AddItemWindow()
    NormalOperationWindow()
    ItemsInRegestryButton()
    seeContents()
    endOfDayCount()

    
    
    app.stopTabbedFrame()
    app.go()

if __name__ == "__main__":
    main() 


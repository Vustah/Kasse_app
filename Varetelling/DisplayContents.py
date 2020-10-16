from Varetelling import hentInnhold

def oppdaterSkjerm(app,Varer_Inne = None,intern=False,offset=0,reopen=True):
    if Varer_Inne == None:
        Varer_Inne = hentInnhold("beholdning.csv")

    if intern:
        plassering = "INN_"
        headerFont = 20
        normalFont = int(headerFont*0.75)

    else:    
        plassering = "UT_"
        headerFont = 50
        normalFont = int(headerFont*0.75)
        if reopen:
            app.openSubWindow("Varer Inne")

    try:
        window_header_font = "Times "+str(headerFont)+" bold"
        app.addLabel(plassering+"Type","Type",offset,0).config(font=window_header_font)
        app.setLabelAnchor(plassering+"Type","w")

        app.addLabel(plassering+"VareNavn","Navn",offset,1).config(font=window_header_font)
        app.setLabelAnchor(plassering+"VareNavn","w")
        
        app.addLabel(plassering+"Mengde","Mengde",offset,2).config(font=window_header_font)
        app.setLabelAnchor(plassering+"Mengde","center")
        
        if intern:
            app.addLabel(plassering+"Antall","Antall",offset,3).config(font=window_header_font)
            app.setLabelAnchor(plassering+"Antall","center")
        
    except:
        pass


    
    for idx,vare in enumerate(Varer_Inne):
        try:
            StrekKode = vare[0]
        except:
            print(vare)
            print("Failed to extract data: StrekKode")
            return 

        try:
            VareType = vare[1]
        except:
            print(vare)
            print("Failed to extract data: Varetype")
            return 

        try:
            VareNavn = vare[2]
        except:
            print(vare)
            print("Failed to extract data: Varenavn")
            return 

        try:
            Mengde = str(vare[3]) + "L"
        except:
            print(vare)
            print("Failed to extract data: Mengde")
            return 

        try:
            Antall = int(vare[4])
        except:
            print(vare)
            print("Failed to extract data: Antall")
            return 

        first_collumn = plassering+"V0"+str(idx)
        second_collumn = plassering+"V1"+str(idx)
        third_collumn = plassering+"V2"+str(idx)
        fourth_collumn = plassering+"V3"+str(idx)

        try:
            app.setLabel(first_collumn,VareType)
            app.setLabelFg(first_collumn,"black")
            app.getLabelWidget(first_collumn).config(font="Times "+str(normalFont))

            app.setLabel(second_collumn,VareNavn)
            app.setLabelFg(second_collumn,"black") 
            app.getLabelWidget(second_collumn).config(font="Times "+str(normalFont))


            app.setLabel(third_collumn,Mengde)
            app.setLabelFg(third_collumn,"black")
            app.getLabelWidget(third_collumn).config(font="Times "+str(normalFont))

            if intern:
                app.setLabel(fourth_collumn,Antall)
                app.setLabelFg(fourth_collumn,"black")
                app.getLabelWidget(fourth_collumn).config(font="Times "+str(normalFont))
        except:
            app.setPadding(15,5)
            app.setStretch("both")
            app.setSticky("nw")
            app.addLabel(first_collumn,VareType, idx+offset+1, 0).config(font="Times "+str(normalFont))
            app.setLabelAnchor(first_collumn,"w")

            app.addLabel(second_collumn,VareNavn, idx+offset+1, 1).config(font="Times "+str(normalFont))
            app.setLabelAnchor(second_collumn,"w")

            app.addLabel(third_collumn,Mengde, idx+offset+1, 2).config(font="Times "+str(normalFont))
            app.setLabelAnchor(third_collumn,"w")

            if intern:
                app.addLabel(fourth_collumn,Antall, idx+offset+1, 3).config(font="Times "+str(normalFont))
                app.setLabelAnchor(fourth_collumn,"w")
        
        if Antall >= 1 and Antall <= 3:
            app.setLabelFg(first_collumn,"red")
            app.setLabelFg(second_collumn,"red")
            app.setLabelFg(third_collumn,"red")
            
            if intern:
                app.setLabelFg(fourth_collumn,"red")
        
        if Antall < 1:
            app.setLabelFg(first_collumn,"gray")
            app.getLabelWidget(first_collumn).config(font="Times "+str(normalFont)+" overstrike")

            app.setLabelFg(second_collumn,"gray") 
            app.getLabelWidget(second_collumn).config(font="Times "+str(normalFont)+" overstrike")
        
            app.setLabelFg(third_collumn,"gray")
            app.getLabelWidget(third_collumn).config(font="Times "+str(normalFont)+" overstrike")
        
            if intern:
                app.setLabelFg(fourth_collumn,"gray")
                app.getLabelWidget(fourth_collumn).config(font="Times "+str(normalFont)+" overstrike")
        

    if not intern and reopen:
        app.stopSubWindow()
        
    return Varer_Inne
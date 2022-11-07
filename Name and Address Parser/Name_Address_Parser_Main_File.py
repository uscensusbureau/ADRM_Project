import tkinter as tk					
from tkinter import ttk
from datetime import date
import tkinter.filedialog as fd
import tkinter.messagebox as msg
import NameParser___Module as NModule
import pandas as pd
from functools import partial
import json
import NameAddressParser__Module as NaM
import Address_Parser__Module as AdM

class NameAddressParser:
    
    root = tk.Tk()
    tabControl = ttk.Notebook(root)
    tabControl.pack(expand = 1, fill ="both")
    def __init__(self, today = date.today()):
        NameAddressParser.root.title("Parser - US Census Bureau "+ str(today))
        NameAddressParser.root.geometry("1280x720")
        NameAddressParser.NameParser()
        NameAddressParser.AddressParser()
        NameAddressParser.NameAddressParser()
        NameAddressParser.root.mainloop()

    def Process_Name_Parser(tab1):
        df = fd.askopenfilenames( filetypes=[("TXT", ".txt")]) #this file is used to give UI for the user to open a file
        jsonData=NModule.ExtractNames(df[0])
        jsonData = json.dumps(jsonData, indent=2)
        with open('OutputNameParsedFile.txt', 'w') as out_file:
            json.dump(NModule.ExtractNames(df[0]), out_file, sort_keys = True, indent = 4,ensure_ascii = False)
            msg.showinfo("Success!","Parsing is Successful !  Output File Name 'OutputAddressParsedFile' is Generated")
            
        text = tk.Text(tab1, height=28)
        text.grid(row=140, column=10, sticky=tk.EW)
        
        # create a scrollbar widget and set its command to the text widget
        scrollbar = ttk.Scrollbar(tab1, orient='vertical', command=text.yview)
        scrollbar.grid(row=140, column=11, sticky=tk.NS)
        
        #  communicate back to the scrollbar
        text['yscrollcommand'] = scrollbar.set

        text.insert('end', jsonData)
        # except:
        #     msg.showinfo("Alert!","File Reading Error !")

        return 
    
    
    def Process_Address_Parser(tab1):
        msg.showinfo("Choose File","Select Input File")

        df = fd.askopenfilenames( filetypes=[("TXT", ".txt")]) #this file is used to give UI for the user to open a file
        
        msg.showinfo("Choose File","Select Truth File")
        
        truth = fd.askopenfilenames( filetypes=[("TXT", ".txt")]) #this file is used to give UI for the user to open a file
        
        Output=AdM.Address_Parser(df[0],truth[0])
        jsonData = json.dumps(Output[0], indent=2)
        with open('OutputAddressParsedFile.txt', 'w') as out_file:
            json.dump(jsonData, out_file, sort_keys = True, indent = 4,ensure_ascii = False)
            msg.showinfo("Success!","Parsing is Successful, Output File Name 'OutputAddressParsedFile' is Generated!")
            
        text = tk.Text(tab1, height=24)
        text.grid(row=140, column=10, sticky=tk.EW)
        
        # create a scrollbar widget and set its command to the text widget
        scrollbar = ttk.Scrollbar(tab1, orient='vertical', command=text.yview)
        scrollbar.grid(row=140, column=11, sticky=tk.NS)
        
        #  communicate back to the scrollbar
        text['yscrollcommand'] = scrollbar.set

        text.insert('end', jsonData)
        
        
        text1 = tk.Text(tab1, height=5)
        text1.grid(row=10, column=30, sticky=tk.NW)
        
        # create a scrollbar widget and set its command to the text widget
        
        #  communicate back to the scrollbar
        String="% of Parsed Name and Address"
        String+="= "+str(round(Output[1],2))
        String+="\n% of Correctly parsed Addresses= "+str(round(Output[2],2))
        text1.insert('end', String)
        # except:
        #     msg.showinfo("Alert!","File Reading Error !")

        return 
    
    
    
    def Process_Name_Address_Parser(tab1):
        df = fd.askopenfilenames( filetypes=[("TXT", ".txt")]) #this file is used to give UI for the user to open a file
        ReturnVal=NaM.NameandAddressParser(df[0])
        jsonData = json.dumps(ReturnVal[0], indent=2)
        with open('OutputNameAddressParsedFile.txt', 'w') as out_file:
            json.dump(jsonData, out_file, sort_keys = True, indent = 4,ensure_ascii = False)
            msg.showinfo("Success!","Parsing is Successful, Output File Name 'OutputNameAddressParsedFile' is Generated!")
            
        text = tk.Text(tab1, height=28)
        text.grid(row=80, column=10, sticky=tk.EW)
        
        # create a scrollbar widget and set its command to the text widget
        scrollbar = ttk.Scrollbar(tab1, orient='vertical', command=text.yview)
        scrollbar.grid(row=80, column=11, sticky=tk.NS)
        
        #  communicate back to the scrollbar
        text['yscrollcommand'] = scrollbar.set

        text.insert('end', jsonData)
        
        
        text1 = tk.Text(tab1, height=5)
        text1.grid(row=10, column=30, sticky=tk.NW)
        
        # create a scrollbar widget and set its command to the text widget
        
        #  communicate back to the scrollbar
        String="Percentage of Parsed Name and Address"
        String+="= "+str(round(ReturnVal[1],2))
        text1.insert('end', String)
 

        return 


    
    
    
    def NameParser():
        tab1 = ttk.Frame(NameAddressParser.tabControl)
        NameAddressParser.tabControl.add(tab1, text ='Name Parser')
        ttk.Label(tab1, 
          text ="Please Choose a Pipe Delimitted File").grid(column = 0, 
                               row = 0,
                               padx = 5,
                               pady = 5)  
        Nbutton = ttk.Button(tab1, text ="Choose Single",width=30, command=partial(
    NameAddressParser.Process_Name_Parser, tab1)).grid(column = 50, 
                             row = 40,
                             padx = 30,
                             pady = 30) 
    def AddressParser():
        tab2 = ttk.Frame(NameAddressParser.tabControl)
        NameAddressParser.tabControl.add(tab2, text ='Address Parser')
        ttk.Label(tab2, 
          text ="Please Choose a Pipe Delimitted File").grid(column = 0, 
                               row = 0,
                               padx = 5,
                               pady = 5)  
                                                             
        Nbutton = ttk.Button(tab2, text ="Choose Single",width=30,  command=partial(
    NameAddressParser.Process_Address_Parser, tab2)).grid(column = 50, 
                             row = 40,
                             padx = 30,
                             pady = 30) 
        

    def NameAddressParser():
        tab3 = ttk.Frame(NameAddressParser.tabControl)
        NameAddressParser.tabControl.add(tab3, text ='Name and Address Parser')
        ttk.Label(tab3, 
          text ="Please Choose a Pipe Delimitted File").grid(column = 0, 
                               row = 0,
                               padx = 5,
                               pady = 5)  
        Nbutton = ttk.Button(tab3, text ="Choose Single",width=30,  command=partial(
        NameAddressParser.Process_Name_Address_Parser, tab3)).grid(column = 50, 
                                 row = 40,
                                 padx = 30,
                                 pady = 30)   

        
        
        
name=NameAddressParser()


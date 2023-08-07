# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 11:22:18 2023

@author: onais
"""
import tkinter as tk
from tkinter import messagebox
from datetime import date
from tkinter import ttk

import tkinter as tk					
from tkinter import ttk,simpledialog,DISABLED
from datetime import date
import tkinter.filedialog as fd
import tkinter.messagebox as msg
import pandas as pd
from functools import partial
import json
import NameParser___Module as NModule
import NameAddressParser__Module as NaM
import Address_Parser__Module as AdM
import SingleNameParser_Module as NAD_API
import SingleAddressParser_Module as AD_API
import SingleNameAddressParser_Module as ADN_API
from datetime import datetime
import os
import subprocess
import hashlib
import Address_parser_mixc_methods as mx
import Address_parser_approval_form as approvalform

class NAP_GUIBuilder(tk.Tk):
    def __init__(self):
        # Set the geometry of the window
        
        super().__init__()
        self.title("Parser - "+ str(date.today()))
        # self.geometry("1280x720")
        self.NAP_GUIBuilder_CreateTabs()
        screen_width = self.winfo_screenwidth()
        
        screen_height = self.winfo_screenheight()

        self.geometry(f"{screen_width}x{screen_height}")
        self.state('zoomed')
    def NAP_GUIBuilder_CreateTabs(self):
        
        #Create Tabs Depending on the init for root (tk.Tk)
        
        self.tabControl = ttk.Notebook(self)
        self.tabControl.pack(expand = 1, fill ="both")
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text ='Address Parser')
        
        # self.tab3 = ttk.Frame(self.tabControl)
        # self.tabControl.add(self.tab3, text ='Comparison Tab')
        
        
        self.tab4 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab4, text ='Mapping Approval Form')
        
        # Calling Different Methods with respect to the tab
        self.NAP_GUIBuilder_AddressParser()
        # self.NAP_GUIBuilder_ComparisonTab()
        self.NAP_GUIBuilder_MappingApprovalForm()
        

    def NAP_GUIBuilder_AddressParser(self):
        
        # adress_misc = ad_misc()
        
        Instance = mx.Address_parser_misc()
        
        # ttk.Label(self.tab2, text ="Please Choose a Pipe Delimitted File"). grid(column = 0, 
        #                        row = 0,
        #                        padx = 5,
        #                        pady = 5)  
        ttk.Button(self.tab2, text ="Choose Batch File",width=30, command=Instance.Process_Address_Parser_Single_input).grid(column = 5, 
                             row = 50,
                             padx = 10,
                             pady = 10)
        
        ttk.Label(self.tab2, text ="Please Choose a Pipe Delimitted File"). grid(column = 0, 
                               row = 0,
                               padx = 5,
                               pady = 5)  
        
        ttk.Button(self.tab2, text ="Choose Single File (input)",width=30, command=Instance.Process_Address_Parser_Single_input).grid(column = 5, 
                             row = 30,
                             padx = 10,
                             pady = 10)
        
        ttk.Button(self.tab2, text ="Choose Two Files (input and test)",width=30, command=Instance.Process_Address_Parser_Test).grid(column = 5, 
                              row = 60,
                              padx = 0,
                              pady = 0)
        
        ttk.Label(self.tab2,text="Enter Address").grid(column = 4, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10) 
        
        single_input = tk.Text(self.tab2,width=80,height=3,wrap=tk.WORD)
        single_input.grid(column = 5, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10) 
        ttk.Label(self.tab2, 
          text ="OR").grid(column = 5, 
                               row = 15,
                               padx = 0,
                               pady = 0) 
        s=ttk.Style()
        s.theme_use("clam")
        s.configure('Treeview',rowheight=45)
        
        tree = ttk.Treeview(self.tab2, column=["Mask Token","Address Token","Address Component","Exception","File"] ,show='headings',height=10)

        for item in tree.get_children():
            tree.delete(item)
        tree.column("# 1", width=60, stretch='YES')
        tree.heading("# 1", text="Mask Token")
        
        tree.column("# 2", width=200, stretch='YES')
        tree.heading("# 2", text="Address Token")
        
        tree.column("# 3", width=80, stretch='YES')
        tree.heading("# 3", text="Address Component")
        
        tree.column("# 4", width=60, stretch='YES')
        tree.heading("# 4", text="Exception")
        
        tree.column("# 5", width=60, stretch='YES')
        tree.heading("# 5", text="File Name")
        ttk.Button(self.tab2, text ="Submit", command=lambda:Instance.Single_Address(single_input, self.tab2,tree),width=30).grid(column = 7, 
                                 row = 10)    
        #tree.pack(side=tk.LEFT)

    # def NAP_GUIBuilder_ComparisonTab(self):
    #     comaprison_instance = mx.Address_parser_misc()
    #     ttk.Button(self.tab3, text ="Choose Batch File",width=30, command=comaprison_instance.Process_Address_Parser_Test).grid(column = 0, 
    #                          row = 0,
    #                          padx = 10,
    #                          pady = 10)
        
    #     return
    
    
    def NAP_GUIBuilder_MappingApprovalForm(self):
       
        import textwrap
        
        
        def wrap(string, lenght=60):
            return '\n'.join(textwrap.wrap(string, lenght))
        
        
        approval_form_instance=approvalform.submission_form()
        
        ttk.Button(self.tab4, text="Choose an Exception File", width=30, command=lambda: approval_form_instance.Browse_File([],False,form_frame,canvas,table_frame,label1,label2,label3,self.tab4)).pack(side="top", padx=0, pady=0)


        label1 = tk.Label(self.tab4, height=2, width=20, text="Mask Token")
        label1.configure(font=("Arial", 12),relief=tk.RAISED)



        label2 = tk.Label(self.tab4, height=2, width=20,text="Adress Token")
        label2.configure(font=("Arial", 12), relief=tk.RAISED)


        label3 = tk.Label(self.tab4, height=2, width=20,text="Address Component")
        label3.configure(font=("Arial", 12), relief=tk.RAISED)

        
        label1.pack_forget()
        label2.pack_forget()
        label3.pack_forget()
        
        
        form_frame = ttk.Frame(self.tab4,width=360,height=800)
        form_frame.pack(side=tk.RIGHT,fill=tk.BOTH,padx=100, pady=30)
        # form_frame.place(x=900,y=10)
        
        table_frame = ttk.Frame(self.tab4)

        # table_frame.pack(side=tk.LEFT,pady=5,padx=20)
        # table_frame.place(x=30,y=90)
        # table_frame.configure(height=420)
        # canvas = tk.Canvas(table_frame,width=580,height=420)
        # canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        # canvas.place(x=30,y=50)
        table_frame.pack(side=tk.LEFT,pady=50,padx=0)
        table_frame.place(x=30,y=90)
        table_frame.configure(height=650)
        canvas = tk.Canvas(table_frame,width=580,height=420)
        canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        
        
        def DateTime():
            # Get the current date and time
            # label = ""
            now = datetime.now()
            current_date = now.strftime("%m-%d-%Y")
            
        
            
            DateTime_label = ttk.Label(self.tab4, text=f"Date: {current_date}", font=("Arial", 12))
            DateTime_label.pack(side=tk.TOP, padx=10, pady=5)

    
if __name__ == "__main__":
    Run= NAP_GUIBuilder()
    Run.mainloop()



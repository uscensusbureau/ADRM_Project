# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 23:22:02 2023

@author: akkka
"""
import tkinter.filedialog as fd
import tkinter.messagebox as msg
import Address_Parser__Module as AdM
import tkinter as tk
from tkinter import ttk,simpledialog,DISABLED
import SingleAddressParser_Module as AD_API
import textwrap
import os
import test_Main


class Address_parser_misc():
    def __init__(self):
        self
    
    
    def Process_Address_Parser_Test(self):
        msg.showinfo("Choose File","Select Input File")

        df = fd.askopenfilenames( filetypes=[("TXT", ".txt"),("JSON",".json")]) 
        if df:
            msg.showinfo("Choose File","Select Truth File")
            
            truth = fd.askopenfilenames( filetypes=[("TXT", ".txt"),("JSON",".json")]) #this file is used to give UI for the user to open a file
            
            if truth:
                Output=AdM.Address_Parser(df[0],TruthSet=truth[0])
                if Output[0]:
                    msg.showinfo("Success",Output[1])
                else:
                    msg.showerror("Error!", Output[1])                
                
              
                # except:
                #     msg.showinfo("Alert!","File Reading Error !")
            else: msg.showerror("Alert!","Truth file is required!")
        else: msg.showerror("Alert","Please select input file.")
        return
    
    
    def Process_Address_Parser_Single_input(self):
        msg.showinfo("Choose File","Select Input File in Pipe Delimited Format \n For Example: 1 | 'Your Address Here'")

        df = fd.askopenfilenames(filetypes=[("TXT", ".txt"),("JSON",".json")],initialdir = "Test Data") 
        if df:
            Output=AdM.Address_Parser(df[0])
            
            if Output[0]:
                msg.showinfo("Success",Output[1])
            else:
                msg.showerror("Error!", Output[1])
        else: msg.showerror("Alert","Please select input file.")
        return
    
    def Single_Address(self, single_input ,tab2,tree):
        
        def submit():
            # Get the checkbox state
            checkbox_state = checkbox_var.get()
            # Print the checkbox state
            if checkbox_var.get():
                # AD_API.Address_Parser()
                AD_API.throwException(originalInput=single_input.get("1.0","end-1c"), initials=initial)
                msg.showinfo("Exception","Forced Exception is Created!")
            else:
                msg.showinfo("Exception","Check the box to create an Exception")

        # checkbox_var = tk.IntVar()

        # # Create the checkbox
        # checkbox = ttk.Checkbutton(tab2, text="Forced Exception", variable=checkbox_var)
        # checkbox.grid(row=12, column=5, padx=10, pady=10)

        # # Create the submit button
        # submit_button = ttk.Button(tab2, text="Forced Exception", command=submit)
        # submit_button.grid(row=13, column=5, padx=10, pady=10)
        ### toggle_state = tk.StringVar(value="No")


        ### Create the form elements with custom styling
        ### Forced_Except_Label = ttk.Label(tab2, text="Forced Exception? ", font=("Arial", 12))
        ### Forced_Except_Label.grid(row=5, column=0, sticky=tk.W, pady=5)
        ### toggle_button = ttk.Checkbutton(tab2, onvalue="Yes", offvalue="No", variable=toggle_state, style="Toggle.TCheckbutton")

        ### toggle_button.grid(row=5, column=0,columnspan=2, pady=5)
        ### style.configure("Toggle.TCheckbutton", font=("Arial", 14))
        
        
        
        
        initial = simpledialog.askstring("Optional", "Your Initials")
        print(single_input.get("1.0","end-1c"))
        Convert=AD_API.Address_Parser(single_input.get("1.0","end-1c"),initial,originalInput=single_input.get("1.0","end-1c"))
        
        Result=Convert[0]
        
        if Result:
            checkbox_var = tk.IntVar()

            # Create the checkbox
            checkbox = ttk.Checkbutton(tab2, text="Forced Exception", variable=checkbox_var)
            checkbox.grid(row=60, column=5, padx=10, pady=10)

            # Create the submit button
            submit_button = ttk.Button(tab2, text="Submit", command=submit)
            submit_button.grid(row=61, column =5 , padx=10, pady=10)
        
        try:  
            
            for item in tree.get_children():
                tree.delete(item)
            tree.insert('','end',values=(self.wrap('Mask'),self.wrap(Convert[1]),"","",""))
            for m in Result["Output"]:  
                tree.insert('', 'end', values=(self.wrap(m[1]),self.wrap(m[2]),self.wrap(m[0])))
            
        except:
           
            for item in tree.get_children():
                tree.delete(item)
            tree.insert('','end',values=("","",Convert[1],Convert[2]))


        
        
        
        tree.grid(row=55, column=5, sticky=tk.EW)
        

    def wrap(self, string, lenght=36):
        return '\n'.join(textwrap.wrap(string, lenght))


import tkinter as tk					
from tkinter import ttk,simpledialog,DISABLED
from datetime import date
import tkinter.filedialog as fd
import tkinter.messagebox as msg
# import pandas as pd
# from functools import partial
import json
import subprocess
import NameParser___Module as NModule
import NameAddressParser__Module as NaM
import Address_Parser__Module as AdM
import SingleNameParser_Module as NAD_API
import SingleAddressParser_Module as AD_API
import SingleNameAddressParser_Module as ADN_API
import os
from datetime import datetime


# Main Class for the name and address parsing, on individual level
class NameAddressParser:
    
    root = tk.Tk()
    tabControl = ttk.Notebook(root)
    tabControl.pack(expand = 1, fill ="both")

    
    
    #init function for creating th GUI as Tkinter
    def __init__(self, today = date.today()):
        NameAddressParser.root.title("Parser - US Census Bureau "+ str(today))
        NameAddressParser.root.geometry("1280x720")
        NameAddressParser.NameParser()
        NameAddressParser.AddressParser()
        NameAddressParser.NameAddressParser()
        NameAddressParser.ApprovalForm()
        NameAddressParser.root.mainloop()


    #Process for Name Parser, wherein after the click of the button "Choose Two Files" this method is triggered
 
    
    #Process for Address Parser, wherein after the click of the button "Choose Two Files" this method is triggered
     

    
    #Process for Address Parser, wherein after the click of the button "Choose Two Files" this method is triggered
     
    
    # This method is for creating a TAB in the GUI for Name Parser
    def NameParser():
        tab1 = ttk.Frame(NameAddressParser.tabControl)
        NameAddressParser.tabControl.add(tab1, text ='Name Parser')
        ttk.Label(tab1, 
          text ="Please Choose a Pipe Delimitted File").grid(column = 0, 
                               row = 0,
                               padx = 0,
                               pady = 0)  
        def Process_Name_Parser_input():
            msg.showinfo("Choose File","Select Input File")

            df = fd.askopenfilenames( filetypes=[("TXT", ".txt"),("JSON",".json")]) 
            if df:
                Output=NModule.ExtractNames(df[0])
                if Output[0]:
                    msg.showinfo("Success",Output[1])
                else:
                    msg.showerror("Error!", Output[1])
            else: msg.showerror("Alert","Please select input file.")
            return
        
        def Process_Name_Parser():
            msg.showinfo("Choose File","Select Input File")
            #this file is used to give UI for the user to open a Input file
            df = fd.askopenfilenames( filetypes=[("TXT", ".txt")]) 
            if(df):
                msg.showinfo("Choose File","Select Truth File")
                #this file is used to give UI for the user to open a truth file
                truth = fd.askopenfilenames( filetypes=[("TXT", ".txt"),("JSON",".json")]) 
                
                
                
                if truth:
                    Output=NModule.ExtractNames(df[0],TruthSet=truth[0])
                    if Output[0]:
                        msg.showinfo("Success",Output[1])
                    else:
                        msg.showerror("Error!", Output[1])                
                    
                  
                    # except:
                    #     msg.showinfo("Alert!","File Reading Error !")
                else: msg.showerror("Alert!","Truth file is required!")
            else: msg.showerror("Alert","Please select input file.")
            return
                
                
                
                
                
                
                
                
                
                
                
                
               
        Nbutton = ttk.Button(tab1, text ="Choose Two Files (input and test)",width=30, command=Process_Name_Parser).grid(column = 5, 
                             row = 60,
                             padx = 10,
                             pady = 10)
        NbuttonSingle = ttk.Button(tab1, text ="Choose Single File (input)",width=30, command=Process_Name_Parser_input).grid(column = 5, 
                             row = 50,
                             padx = 10,
                             pady = 10)
        
        Or_Label=ttk.Label(tab1,text="Enter Name").grid(column = 4, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10) 
        nad=tk.StringVar()
        single_input = ttk.Entry(tab1,width=100,textvariable=nad).grid(column = 5, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10)
        ttk.Label(tab1, 
          text ="OR").grid(column = 5, 
                               row = 15,
                               padx = 0,
                               pady = 0) 

        
        
        def Single_Name(): 
            Convert=NAD_API.ExtractNames(nad.get())
            msg.showinfo("Output",Convert)
        
        ttk.Button(tab1, text ="Submit",width=20, command=Single_Name).grid(column =7, 
                                 row =10)    
                                      
                                              
    # This method is for creating a TAB in the GUI for Address Parser
    def AddressParser():
        tab2 = ttk.Frame(NameAddressParser.tabControl)
        NameAddressParser.tabControl.add(tab2, text ='Address Parser')
        ttk.Label(tab2, 
          text ="Please Choose a Pipe Delimitted File").grid(column = 0, 
                               row = 0,
                               padx = 5,
                               pady = 5)  
        def Clear():
            # Run the file again using subprocess
            tab2.destroy()
            subprocess.call(["python", "Name_Address_Parser_Main_File.py"])
                                                     
        def Process_Address_Parser():
            msg.showinfo("Choose File","Select Input File")

            df = fd.askopenfilenames( filetypes=[("TXT", ".txt"),("JSON",".json")]) 
            if df:
                msg.showinfo("Choose File","Select Truth File")
                
                truth = fd.askopenfilenames( filetypes=[("TXT", ".txt")]) #this file is used to give UI for the user to open a file
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
        
        
        def Process_Address_Parser_input():
            msg.showinfo("Choose File","Select Input File")

            df = fd.askopenfilenames( filetypes=[("TXT", ".txt"),("JSON",".json")]) 
            if df:
                Output=AdM.Address_Parser(df[0])
                if Output[0]:
                    msg.showinfo("Success",Output[1])
                else:
                    msg.showerror("Error!", Output[1])
            else: msg.showerror("Alert","Please select input file.")
            return
        
        
<<<<<<< Updated upstream
        Nbutton = ttk.Button(tab2, text ="Choose Two Files (input and test)",width=30, command=Process_Address_Parser).grid(column = 5, 
                             row = 60,
                             padx = 10,
                             pady = 10)
=======
        # Nbutton = ttk.Button(tab2, text ="Choose Two Files (input and test)",width=30, command=Process_Address_Parser).grid(column = 5, 
        #                      row = 60,
        #                      padx = 10,
        #                      pady = 10)
        
>>>>>>> Stashed changes
        NbuttonSingle = ttk.Button(tab2, text ="Choose Single File (input)",width=30, command=Process_Address_Parser_input).grid(column = 5, 
                             row = 50,
                             padx = 10,
                             pady = 10)
        
        Or_Label=ttk.Label(tab2,text="Enter Address").grid(column = 4, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10) 
        
        nad=tk.StringVar()
        single_input = ttk.Entry(tab2,width=100,textvariable=nad).grid(column = 5, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10) 
        ttk.Label(tab2, 
          text ="OR").grid(column = 5, 
                               row = 15,
                               padx = 0,
                               pady = 0) 
        # text = tk.Text(tab2, height=24)
        # text.grid(row=55, column=5, sticky=tk.EW)
        
        # # create a scrollbar widget and set its command to the text widget
        # scrollbar = tk.Scrollbar(tab2, orient='vertical', command=text.yview)
        # scrollbar.grid(column=6, row=55, rowspan=2,  sticky="ns")
        
        # #  communicate back to the scrollbar
        # text['yscrollcommand'] = scrollbar.set
        
        
        # text_result = tk.Text(tab2, height=5,width=30)
        # text_result.grid(row=55, column=7,padx=20,pady=20)
        
        import textwrap


        def wrap(string, lenght=60):
            return '\n'.join(textwrap.wrap(string, lenght))
        
        
        tree = ttk.Treeview(tab2, column=["Address Component","Address Token","Mask Token","Exception","File"] ,selectmode="extended",show='headings',height=10)
        for item in tree.get_children():
            tree.delete(item)
        tree.column("# 1", width=50, stretch='YES')
        tree.heading("# 1", text="Address Component")
        
        tree.column("# 2", width=200, stretch='YES')
        tree.heading("# 2", text="Address Token")
        
        tree.column("# 3", width=200, stretch='YES')
        tree.heading("# 3", text="Mask Token")
        
        tree.column("# 4", width=50, stretch='YES')
        tree.heading("# 4", text="Exception")
        
        tree.column("# 5", width=200, stretch='YES')
        tree.heading("# 5", text="File Name")
        
        
        def Single_Address():
            
<<<<<<< Updated upstream
=======
            def submit():
                # Get the checkbox state
                checkbox_state = checkbox_var.get()
                # txtMask_1 = tk.StringVar()
                # txtFirstPhaseList = tk.StringVar()
                # txtInitials = tk.StringVar()
                # Mask_1 = txtMask_1.get()
                # FirstPhaseList = txtFirstPhaseList.get()
                # initials = txtInitials.get()
                # Print the checkbox state
                if checkbox_state:
                    # AD_API.Address_Parser()
                    AD_API.throwException(originalInput=nad.get(), initials=initial)
                    msg.showinfo("Exception","Forced Exception is Created!")
                else:
                    msg.showinfo("Exception","Check the box to create an Exception")

            
            
            
>>>>>>> Stashed changes
            s = ttk.Style()
            s.configure('Treeview', rowheight=35, background="black", 
                fieldbackground="black", foreground="white")
            
            
            initial = simpledialog.askstring("Optional", "Your Initials")
           
            Convert=AD_API.Address_Parser(nad.get(),initial)
            
            Result=Convert[0]
            
<<<<<<< Updated upstream
=======
            if Result:
                checkbox_var = tk.IntVar()

                # Create the checkbox
                checkbox = ttk.Checkbutton(tab2, text="Forced Exception", variable=checkbox_var)
                checkbox.grid(row=60, column=5, padx=10, pady=10)

                # Create the submit button
                submit_button = ttk.Button(tab2, text="Submit", command=submit)
                submit_button.grid(row=61, column =5 , padx=10, pady=10)
                
            
>>>>>>> Stashed changes
            try:  
                
                for item in tree.get_children():
                    tree.delete(item)
                tree.insert('','end',values=(wrap('Mask'),wrap(Convert[1]),"","",""))
                for k, v in Result["Output"].items():  
                    tree.insert('', 'end', values=(wrap(k),wrap(v[1]),wrap(v[0])))
                
            except:
               
                for item in tree.get_children():
                    tree.delete(item)
                tree.insert('','end',values=("","",Convert[1],Convert[2]))


            
            
            
            tree.grid(row=55, column=5, sticky=tk.EW)
            
            
        
        ttk.Button(tab2, text ="Submit",width=30, command=Single_Address).grid(column = 7, 
                                 row = 10)    

        return



    def NameAddressParser():
        
        tab3 = ttk.Frame(NameAddressParser.tabControl)
        NameAddressParser.tabControl.add(tab3, text ='Name and Address Parser')
        ttk.Label(tab3, 
          text ="Please Choose a Pipe Delimitted File").grid(column = 0, 
                               row = 0,
                               padx = 5,
                               pady = 5)  
        def Process_Name_Address_Parser():
            msg.showinfo("Select File","Please select the input file")
            df = fd.askopenfilenames( filetypes=[("TXT", ".txt")]) #this file is used to give UI for the user to open a file
            if df:
                # msg.showinfo("Select File","Please select the input file")
                # truth = fd.askopenfilenames( filetypes=[("TXT", ".txt")])
                # if truth:
                ReturnVal=NaM.NameandAddressParser(df[0])
                jsonData = json.dumps(ReturnVal[0], indent=2)
                with open('OutputNameAddressParsedFile.txt', 'w') as out_file:
                    json.dump(jsonData, out_file, sort_keys = True, indent = 4,ensure_ascii = False)
                    msg.showinfo("Success!","Parsing is Successful, Output File Name 'OutputNameAddressParsedFile' is Generated!")         
                # text = tk.Text(tab3, height=28)
                # text.grid(row=80, column=10, sticky=tk.EW)
                
                # # create a scrollbar widget and set its command to the text widget
                # scrollbar = ttk.Scrollbar(tab3, orient='vertical', command=text.yview)
                # scrollbar.grid(row=80, column=11, sticky=tk.NS)
                
                # #  communicate back to the scrollbar
                # text['yscrollcommand'] = scrollbar.set

                # text.insert('end', jsonData)
                
                
                # text1 = tk.Text(tab3, height=5)
                # text1.grid(row=10, column=30, sticky=tk.NW)
                
                # create a scrollbar widget and set its command to the text widget
                
                #  communicate back to the scrollbar
                String="Percentage of Parsed Name and Address"
                String+="= "+str(round(ReturnVal[1],2))
                String+="\n% of Correctly parsed Addresses= "+str(round(ReturnVal[1],2))
                text.delete("1.0",'end-1c')
                text_result.delete("1.0",'end-1c')
            
                text.insert('end', jsonData)
                text_result.insert('end', String)
            # else: msg.showerror("Warning","Truth file is required.")
            else: msg.showerror("Warning","Input file is not selected.")

            return
        Or_Label=ttk.Label(tab3,text="Enter Name And Address").grid(column = 4, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10) 
        Nbutton = ttk.Button(tab3, text ="Choose Two Files",width=30, command= Process_Name_Address_Parser).grid(column = 5, 
                             row = 50,
                             padx = 10,
                             pady = 10)
        nad=tk.StringVar()
        single_input = ttk.Entry(tab3,width=100,textvariable=nad).grid(column = 5, 
                                 row = 10,
                                 padx = 10,
                                 pady = 10)
        ttk.Label(tab3, 
          text ="OR").grid(column = 5, 
                               row = 15,
                               padx = 0,
                               pady = 0) 
        text = tk.Text(tab3, height=24)
        text.grid(row=55, column=5, sticky=tk.EW)
        
        # create a scrollbar widget and set its command to the text widget
        scrollbar = tk.Scrollbar(tab3, orient='vertical', command=text.yview)
        scrollbar.grid(column=6, row=55, rowspan=2,  sticky="ns")
        
        #  communicate back to the scrollbar
        text['yscrollcommand'] = scrollbar.set
        
        
        text_result = tk.Text(tab3, height=5,width=30)
        text_result.grid(row=55, column=7,padx=20,pady=20)
        
        def Single_Name_Address(): 
            Convert=ADN_API.NameandAddressParser(nad.get())
            msg.showinfo("Output",Convert)
        
        ttk.Button(tab3, text ="Submit",width=30, command=Single_Name_Address).grid(column = 7, 
                                 row = 10)
        return
    def ApprovalForm():
        tab4 = ttk.Frame(NameAddressParser.tabControl)
        NameAddressParser.tabControl.add(tab4, text ='Mapping Approval Form')
        Stat={}
        file_name = ""
        Input_name = ""
        
        def DateTime():
            # Get the current date and time
            # label = ""
            now = datetime.now()
            current_date = now.strftime("%m-%d-%Y")
            
        
            
            DateTime_label = ttk.Label(tab4, text=f"Date: {current_date}", font=("Arial", 12))
            DateTime_label.pack(side=tk.TOP, padx=10, pady=5)
        
            
            
        
        
        def Clear():
            # Run the file again using subprocess
            tab4.destroy()
            subprocess.call(["python", "Name_Address_Parser_Main_File.py"])
            
        
        
        def Browse_File():
            global df, Stat, file_name, Input_name
            msg.showinfo("Choose File", "Select an Exception File")
            df = fd.askopenfilenames(filetypes=[("JSON", ".json")])
            if df:
                with open(df[0], "r+", encoding="utf8") as f:
                    Stat = json.load(f)
                Mask = list(Stat.keys())[1]
                file_name = os.path.basename(df[0])
                if "INPUT" in Stat:
                    Input_name = Stat["INPUT"]
                    Stat.pop("INPUT")
                else:
                    Input_name = ""
                    msg.showwarning("FileError", "Please Select an Appropriate Exception file.")
                Exception_file_name_entry = ttk.Entry(form_frame, font=("Arial", 12),width=42)
                Exception_file_name_entry.insert(0,file_name)
                Exception_file_name_entry.configure(state=DISABLED)
                Exception_file_name_entry.grid(row=1, column=1, pady=5)
                Exception_file_name_entry.configure(background="#ffffff", foreground="#000000")
                
                
                
                Input_entry = ttk.Entry(form_frame, font=("Arial", 12),width=42)
                Input_entry.insert(0,Input_name)
                Input_entry.configure(state=DISABLED)
                Input_entry.grid(row=2, column=1, pady=5)
                Input_entry.configure(background="#ffffff", foreground="#000000")
                
                
                Mask_entry = ttk.Entry(form_frame, font=("Arial", 12),width=42)
                Mask_entry.insert(0,Mask)
                Mask_entry.configure(state=DISABLED)
                Mask_entry.grid(row=5, column=1, pady=5)
                Mask_entry.configure(background="#ffffff", foreground="#000000")
                def submit_form():
                    # Retrieve the entered values and process the form data
                    global Stat
                    Exception_file_name = Exception_file_name_entry.get()
                    Input = Input_entry.get()
                    # for i in table_rows:
                    #     if not dropdown_var.get():
                    #         messagebox.showerror("Error", "")
                    #         return False
                        
                    region = region_var.get()
                    type_value = Type_var.get()
                    approval = Approval_List_var.get()
                    pattern = Mask_entry.get()
                    # component_values = dropdown_var.get()
                    table_data = []
                    today = datetime.now()
                    addValid = toggle_state.get()
                    
                    for row in table_rows[1:]:
                        column1 = row[0].get("1.0", tk.END).strip()
                        column2 = row[1].get("1.0", tk.END).strip()
                        column3 = row[2].get()
                        
                        table_data.append((column1, column2, column3))
                    
                    # Perform validation checks
                    if not Exception_file_name:
                        msg.showerror("Error", "Exception File Name is required.")
                        return False
                    if not Input:
                        msg.showerror("Error", "Input is required.")
                        return False
                    if not region:
                        msg.showerror("Error", "Region is required.")
                        return False
                    if not type_value:
                        msg.showerror("Error", "Type is required.")
                        return False
                    if not addValid:
                        msg.showerror("Error", "Please Select 'Yes/No' for DataBase Validation")
                        return False
                    if not approval:
                        msg.showerror("Error", "Approval Field is required.")
                        return False
                    # if not component_values:
                    #     messagebox.showerror("Error", "All Components are required.")
                    #     return False
                    form_data = {
                        "Exception_file_name": Exception_file_name,
                        "Input": Input,
                        "Region": region,
                        "Type": type_value,
                        "Token Pattern": pattern,
                        "Approved By": (f"{approval} at {today}"),
                        "Table Data": table_data
                    }
                    rejection_data = {
                        "Exception_file_name": Exception_file_name,
                        "Input": Input,
                        "Token Pattern": pattern,
                        "Rejected By": (f"{approval} at {today}"),
                    }
                    
                    print(toggle_state.get())
                    if toggle_state.get() == "Yes":
                        # file_path = r""
                        if not Exception_file_name:
                            msg.showerror("Error", "Exception File Name is required.")
                            return False
                        if not Input:
                            msg.showerror("Error", "Input is required.")
                            return False
                        if not region:
                            msg.showerror("Error", "Region is required.")
                            return False
                        if not type_value:
                            msg.showerror("Error", "Type is required.")
                            return False
                        if not approval:
                            msg.showerror("Error", "Approval Field is required.")
                            return False
                        
                        with open("Validation_DB.txt", 'r+') as file:
                            try:
                                existing_data = json.load(file)
                            except json.JSONDecodeError:
                                existing_data = []
                        
                            # Append the new data to the existing data list
                            existing_data.append(form_data)
                            
                            # Set the file's current position at the beginning
                            file.seek(0)
                            
                            # Write the updated data back to the file
                            json.dump(existing_data, file, indent=4)
                            file.truncate()
                        
                        # messagebox.showinfo("Demo", "Address is added to Validation DataBase")
                        print(f"Exception_file_name: {Exception_file_name}")
                        print(f"Input: {Input}")
                        print(f"Region: {region}")
                        print(f"Type: {type_value}")
                        print(f"Token Pattern: {pattern}")
                        
                        if toggle_state.get() == "Yes":
                            msg.showinfo("Info", "Address Added to Validation DataBase!")
                            print(f"Approved By: {approval} at {today}")
                        elif toggle_state.get() == "No":
                            msg.showinfo("Info", "Address is not Approved!")#\nPlease Select a New Exception File")
                            # Clear()
                        print("Table Data:")
                        
                        for data in table_data:
                            print(data)
                    
                    # elif toggle_state.get() == "No":
                    #     if not approval:
                    #         messagebox.showerror("Error", "Approval Field is required.")
                    #         return False# messagebox.showinfo("Demo", "Address not added to Validation DataBase")
                    elif toggle_state.get() == "No":
                        if not approval:
                            msg.showerror("Error", "Approval Field is required.")
                            return False# messagebox.showinfo("Demo", "Address not added to Validation DataBase")
                        
                        
                        with open("ADDR_Rejection_DB.txt", 'r+') as r_file:
                            try:
                                previous_data = json.load(r_file)
                            except json.JSONDecodeError:
                                previous_data = []
                        
                            # Append the new data to the existing data list
                            previous_data.append(rejection_data)
                            
                            # Set the file's current position at the beginning
                            r_file.seek(0)
                            
                            # Write the updated data back to the file
                            json.dump(previous_data, r_file, indent=4)
                            r_file.truncate()
                        print(rejection_data)
                        msg.showinfo("Info", "Address is not Approved")#\nPlease Select a New Exception File")
                        # Clear()
                    
                    return form_data, rejection_data
                
                
                
                def add_table_row(m):
                    global Stat
                    # Add a new row to the table
                    row = []
                    
                    dropdown_values = ["",
                      "USAD_SNO",
                      "USAD_SPR",
                      "USAD_SNM",
                      "USAD_SFX",
                      "USAD_SPT",
                      "USAD_ANM",
                      "USAD_ANO",
                      "USAD_CTY",
                      "USAD_STA",
                      "USAD_ZIP",
                      "USAD_ZP4",
                      "USAD_BNM",
                      "USAD_BNO",
                      "USAD_RNM",
                      "USAD_RNO",
                      "USAD_ORG",
                      "USAD_MDG",
                      "USAD_MGN",
                      "USAD_HNM",
                      "USAD_HNO"]
                    
                    # Create the text widgets for the first two columns with scrollbars
                    text1 = tk.Text(table_inner_frame, height=2, width=20, wrap=tk.WORD)
                    text1.insert('1.0',m[0])
                    text1.configure(font=("Arial", 12), relief=tk.SOLID,state=DISABLED)
                    text1.grid(row=len(table_rows) + 1, column=0, sticky="nsew", padx=5, pady=5)
                    row.append(text1)
        
                    text2 = tk.Text(table_inner_frame, height=2, width=20, wrap=tk.WORD)
                    text2.insert('1.0',m[1])
                    text2.configure(font=("Arial", 12), relief=tk.SOLID,state=DISABLED)
                    text2.grid(row=len(table_rows) + 1, column=1, sticky="nsew", padx=5, pady=5)
                    row.append(text2)
        
                    # Create the dropdown for the last column
                    dropdown_var = tk.StringVar(tab4)
                    dropdown = ttk.Combobox(table_inner_frame ,textvariable = dropdown_var, values=dropdown_values, font=("Arial", 12), state="readonly")
                    dropdown.grid(row=len(table_rows) + 1, column=2, sticky="nsew", padx=5, pady=5)
                    row.append(dropdown)
        
                    # Update the row-span for the labels in the previous rows
                    for r in range(len(table_rows)):
                        table_rows[r][0].grid(row=r + 1, column=0, sticky="e")
                        table_rows[r][1].grid(row=r + 1, column=1, sticky="e")
                        table_rows[r][2].grid(row=r + 1, column=2, sticky="e")
        
                    # Append the new row to the table rows list
                    table_rows.append(row)
        
                    set_row_colors()  # Set alternate row colors
        
                    # Update the canvas scroll region
                    def update_size(e=None):
                        canvas["scrollregion"] = canvas.bbox("all")
                    canvas.bind('<Configure>', update_size)
                    # canvas.config(scrollregion=(0,0,400,800))
                    # canvas.configure(scrollregion=canvas.bbox("all"))
                    
                    
        
        
        
                def set_cell_color(cell, color):
                    cell.configure(background=color)
        
                def set_row_colors():
                    global Stat
                    for i, row in enumerate(table_rows):
                        if i % 2 == 0:
                            set_cell_color(row[0], "#F0F0F0")  # Light gray background
                            set_cell_color(row[1], "#F0F0F0")  # Light gray background
                            set_cell_color(row[2], "#F0F0F0")  # Light gray background
                        else:
                            set_cell_color(row[0], "#FFFFFF")  # White background
                            set_cell_color(row[1], "#FFFFFF")  # White background
                            set_cell_color(row[2], "#FFFFFF")  # White background
                
                table_rows = []
                scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=canvas.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                canvas.configure(yscrollcommand=scrollbar.set)
                # canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.configure(scrollregion=canvas.bbox("all"))
                table_inner_frame = ttk.Frame(canvas)
                table_inner_frame.pack(fill=tk.BOTH, expand=True)
                canvas.create_window((0, 0), window=table_inner_frame, anchor=tk.NW)
                label1 = tk.Label(table_inner_frame, height=2, width=20, text="Mask Token")
        
                label1.configure(font=("Arial", 12), fg="#000000", background="#ffffff", relief=tk.SOLID, state=DISABLED)
                label1.grid(row=len(table_rows) + 1, column=0, sticky="nsew", padx=5, pady=5)
        
        
                label2 = tk.Label(table_inner_frame, height=2, width=20,text="Adress Token")
                label2.configure(font=("Arial", 12), relief=tk.SOLID,state=DISABLED)
                label2.grid(row=len(table_rows) + 1, column=0, sticky="nsew", padx=5, pady=5)
        
                label3 = tk.Label(table_inner_frame, height=2, width=20,text="Address Component")
                label3.configure(font=("Arial", 12), relief=tk.SOLID,state=DISABLED)
                label3.grid(row=len(table_rows) + 1, column=0, sticky="nsew", padx=5, pady=5)
                rows=[]
        
                rows.append(label1)
                rows.append(label2)
                rows.append(label3)
                
                for r in range(len(table_rows)):
                    table_rows[r][0].grid(row=r + 1, column=0, sticky="e")
                    table_rows[r][1].grid(row=r + 1, column=1, sticky="e")
                    table_rows[r][2].grid(row=r + 1, column=2, sticky="e")
        
                # Append the new row to the table rows list
                table_rows=[]
                table_rows.append(rows)
        
                # print(Stat.items())
                for key, value in Stat.items():
                    for m in value:
                        m=list(m.items())
                        add_table_row(m[0])
                        
                submit_button = ttk.Button(tab4, text="Submit", command=submit_form, style="Submit.TButton") #, 
                submit_button.pack(pady=10)
            
                # Create a custom style for the buttons
                style = ttk.Style(tab4)
                style.configure("Submit.TButton", font=("Arial", 12, "bold"), foreground="black", background="#4CAF50")
                
                # Clear Button Future reference 
                
                # clear_button = ttk.Button(tab4, text="Clear", command=Clear, style="Submit.TButton") #, 
                # clear_button.pack(pady=15)
                # # Create a custom style for the buttons
                # style = ttk.Style(tab4)
                # style.configure("Submit.TButton", font=("Arial", 12, "bold"), foreground="black", background="#4CAF50")
            else:
                msg.showerror("Alert", "Please select an Exception File.")
            return Stat,Input_name,file_name
        
        
        ttk.Button(tab4, text="Choose an Exception File", width=30, command=Browse_File).pack(side="top", padx=1, pady=1)
        
        
        # Create the form frame
        form_frame = ttk.Frame(tab4)
        form_frame.pack(padx=20, pady=20)
        
        
        
        
        
        
        
        
        
        Exception_file_name_label = ttk.Label(form_frame, text="Exception File Name:", font=("Arial", 12))
        Exception_file_name_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        # Exception_file_name_entry = ttk.Entry(form_frame, font=("Arial", 12),width=42)
        # Exception_file_name_entry.insert(0,file_name)
        # Exception_file_name_entry.configure(state=DISABLED)
        # Exception_file_name_entry.grid(row=1, column=1, pady=5)
        # Exception_file_name_entry.configure(background="#ffffff", foreground="#000000")
                
        Input_label = ttk.Label(form_frame, text="Input:", font=("Arial", 12))
        Input_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        # Input_entry = ttk.Entry(form_frame, font=("Arial", 12),width=42)
        # Input_entry.insert(0,Input_name)
        # Input_entry.configure(state=DISABLED)
        # Input_entry.grid(row=2, column=1, pady=5)
        # Input_entry.configure(background="#ffffff", foreground="#000000")
        
        Mask_label = ttk.Label(form_frame, text="Token Pattern:", font=("Arial", 12))
        Mask_label.grid(row=5, column=0, sticky=tk.W, pady=5)
        # Mask_entry = ttk.Entry(form_frame, font=("Arial", 12),width=42)
        # Mask_entry.insert(0,Mask)
        # Mask_entry.configure(state=DISABLED)
        # Mask_entry.grid(row=5, column=1, pady=5)
        # Mask_entry.configure(background="#ffffff", foreground="#000000")
        
        region_label = ttk.Label(form_frame, text="Region: *", font=("Arial", 12))
        region_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        regions = ["","US", "Puerto Rico"]
        region_var = tk.StringVar(tab4)
        region_dropdown = ttk.Combobox(form_frame, textvariable=region_var, values=regions, font=("Arial", 12),width=40)
        region_dropdown.grid(row=3, column=1, pady=5)
        region_dropdown.configure(state="readonly")
        
        Type_label = ttk.Label(form_frame, text="Type: *", font=("Arial", 12))
        Type_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        Types=["","Individual Address","PO Box Address","Highway Contract Address","Military Address","Attention line Address","Roural Route Address","Puerto Rico Address","University Address"]
        Type_var = tk.StringVar(tab4)
        Type_dropdown = ttk.Combobox(form_frame, textvariable=Type_var, values=Types, font=("Arial", 12),width=40)
        Type_dropdown.grid(row=4, column=1, pady=5)
        Type_dropdown.configure(state = "readonly")
        
        table_frame = ttk.Frame(tab4)
        table_frame.pack(pady=10)
        
        canvas = tk.Canvas(table_frame, width=650, height=200)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        toggle_state = tk.StringVar(value="")
        
        # Create the form elements with custom styling
        Validation_DB_Label = ttk.Label(form_frame, text="Add to DataBase Validation?", font=("Arial", 12))
        Validation_DB_Label.grid(row=6, column=0, sticky=tk.W, pady=5)
        toggle_dropdown = ttk.Combobox(form_frame, textvariable=toggle_state, values=["","Yes", "No"], font=("Arial", 12),width=40, state="readonly")
        toggle_dropdown.grid(row=6, column=1, sticky=tk.W, pady=5)
        
        Approval_label = ttk.Label(form_frame, text="Approved By:", font=("Arial", 12))
        Approval_label.grid(row=7, column=0, sticky=tk.W, pady=5)
        Approval_List = ["", "Committee Member_1", "Committee Member_2", "Committee Member_3"]
        Approval_List_var = tk.StringVar(tab4)
        Approval_List_dropdown = ttk.Combobox(form_frame,textvariable=Approval_List_var,values=Approval_List,font=("Arial", 12),width=40)
        Approval_List_dropdown.grid(row=7, column=1, sticky=tk.W, pady=5)
        Approval_List_dropdown.configure(state="readonly")
        
        return
        
        
        
        
        
name=NameAddressParser()
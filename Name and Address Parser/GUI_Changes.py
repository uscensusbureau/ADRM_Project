import tkinter as tk
from tkinter import ttk,DISABLED
from tkinter import messagebox
from datetime import date
from ttkthemes import ThemedStyle
import json


#Opening Exception File
Stat={}
with open('Exception_Output.json', 'r+', encoding='utf8') as g:
    Stat = json.load(g)

Input_name=Stat["INPUT"]
Stat.pop("INPUT")



def submit_form():
    # Retrieve the entered values and process the form data
    
    Exception_file_name = Exception_file_name_entry.get()
    Input = Input_entry.get()
    # for i in table_rows:
        
    region = region_var.get()
    type_value = Type_var.get()
    # component_values = dropdown_var.get()
    table_data = []
    
    
    for row in table_rows[1:]:
        column1 = row[0].get("1.0", tk.END).strip()
        column2 = row[1].get("1.0", tk.END).strip()
        column3 = row[2].get()
        table_data.append((column1, column2, column3))
    
    # Perform validation checks
    if not Exception_file_name:
        messagebox.showerror("Error", "Exception File Name is required.")
        return False
    if not Input:
        messagebox.showerror("Error", "Input is required.")
        return False
    if not region:
        messagebox.showerror("Error", "Region is required.")
        return False
    if not type_value:
        messagebox.showerror("Error", "Type is required.")
        return False
    # if not component_values:
    #     messagebox.showerror("Error", "All Components are required.")
    #     return False
    form_data = {
        "Exception_file_name": Exception_file_name,
        "Input": Input,
        "Region": region,
        "Type": type_value,
        "Table Data": table_data
    }
    
    print(toggle_state.get())
    if toggle_state.get() == "Yes":
        # file_path = r""
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
    else:
        pass# messagebox.showinfo("Demo", "Address not added to Validation DataBase")
    print(f"Exception_file_name: {Exception_file_name}")
    print(f"Input: {Input}")
    print(f"Region: {region}")
    print(f"Type: {type_value}")
    print("Table Data:")
    
    messagebox.showinfo("Demo", "success")
    for data in table_data:
        print(data)
    
    
    
    return form_data

# def toggle_button():
#     if toggle_state.get()=="Yes":
        
#         file_path = r"C:\Users\skhan2\Desktop\Census Bureau Research\CensusBureauNameAddress\Name and Address Parser\myfile.json"
#         with open(file_path, "w") as out_file:
#             json.dump(submit_form(), out_file, indent=4)

#     else:
#         toggle_state.set("No")
        
        
def add_table_row(m):
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
    dropdown_var = tk.StringVar(window)
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
    for i, row in enumerate(table_rows):
        if i % 2 == 0:
            set_cell_color(row[0], "#F0F0F0")  # Light gray background
            set_cell_color(row[1], "#F0F0F0")  # Light gray background
            set_cell_color(row[2], "#F0F0F0")  # Light gray background
        else:
            set_cell_color(row[0], "#FFFFFF")  # White background
            set_cell_color(row[1], "#FFFFFF")  # White background
            set_cell_color(row[2], "#FFFFFF")  # White background

# Create the main window
window = tk.Tk()
window.title("Approval Form")

# Set the window background color
window.configure(bg="#ffffff")

# Create the form frame
form_frame = ttk.Frame(window)
form_frame.pack(padx=20, pady=20)


style = ThemedStyle(window)
style.set_theme("xpnative")  # Apply the "adapta" theme

# Create the form frame
form_frame = ttk.Frame(window)
form_frame.pack(padx=20, pady=20)

# Create the form elements with custom styling
Exception_file_name_label = ttk.Label(form_frame, text="Exception File Name:", font=("Arial", 12))
Exception_file_name_label.grid(row=0, column=0, sticky=tk.W, pady=5)
Exception_file_name_entry = ttk.Entry(form_frame, font=("Arial", 12),width=40)
Exception_file_name_entry.insert(0, "File_Name_Exception.json")
Exception_file_name_entry.configure(state=DISABLED)

Exception_file_name_entry.grid(row=0, column=1, pady=5)
Exception_file_name_entry.configure(background="#ffffff", foreground="#000000")

Input_label = ttk.Label(form_frame, text="Input:", font=("Arial", 12))
Input_label.grid(row=1, column=0, sticky=tk.W, pady=5)
Input_entry = ttk.Entry(form_frame, font=("Arial", 12),width=40)
Input_entry.insert(0,Input_name)
Input_entry.configure(state=DISABLED)
Input_entry.grid(row=1, column=1, pady=5)
Input_entry.configure(background="#ffffff", foreground="#000000")


region_label = ttk.Label(form_frame, text="Region:", font=("Arial", 12))
region_label.grid(row=3, column=0, sticky=tk.W, pady=5)
regions = ["","US", "Puerto Rico"]
region_var = tk.StringVar(window)
region_dropdown = ttk.Combobox(form_frame, textvariable=region_var, values=regions, font=("Arial", 12),width=40)
region_dropdown.grid(row=3, column=1, pady=5)
region_dropdown.configure(state="readonly")



Type_label = ttk.Label(form_frame, text="Type:", font=("Arial", 12))
Type_label.grid(row=4, column=0, sticky=tk.W, pady=5)
Types=["","Individual Address","PO Box Address","Highway Contract Address","Military Address","Attention line Address","Roural Route Address","Puerto Rico Address","University Address"]
Type_var = tk.StringVar(window)
Type_dropdown = ttk.Combobox(form_frame, textvariable=Type_var, values=Types, font=("Arial", 12),width=40)
Type_dropdown.grid(row=4, column=1, pady=5)
Type_dropdown.configure(state = "readonly")

table_frame = ttk.Frame(window)
table_frame.pack(pady=10)

canvas = tk.Canvas(table_frame, width=650, height=200)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

table_inner_frame = ttk.Frame(canvas)
table_inner_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.configure(scrollregion=canvas.bbox("all"))
canvas.create_window((0, 0), window=table_inner_frame, anchor=tk.NW)


# Create a variable to store the toggle state
toggle_state = tk.StringVar(value="No")


# Create the form elements with custom styling
Validation_DB_Label = ttk.Label(form_frame, text="Add this address to DataBase Validation? ", font=("Arial", 12))
Validation_DB_Label.grid(row=5, column=0, sticky=tk.W, pady=5)
toggle_button = ttk.Checkbutton(form_frame, onvalue="Yes", offvalue="No", variable=toggle_state, style="Toggle.TCheckbutton")

toggle_button.grid(row=5, column=0,columnspan=2, pady=5)
style.configure("Toggle.TCheckbutton", font=("Arial", 14))






submit_button = ttk.Button(window, text="Submit", style="Submit.TButton") #, command=submit_form
submit_button.pack(pady=10)

# Create a custom style for the buttons
style = ttk.Style(window)
style.configure("Submit.TButton", font=("Arial", 12, "bold"), foreground="black", background="#4CAF50")

table_rows = []

# Store the table rows in a list
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


for key, value in Stat.items():
    for m in value:
        m=list(m.items())
        add_table_row(m[0])

#Salman
# def on_region_selected(event):
#     region = region_var.get()
#     if region:
#         Type_dropdown.config(state="readonly")
#     else:
#         Type_dropdown.config(state="disabled")
#         Type_var.set("")  # Clear the selected value

# region_var.trace_add("write", on_region_selected)

window.mainloop()

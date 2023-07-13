import tkinter as tk

DrpDict = {'Key1': 'Value1', 'Key2': 'Value2'}

def on_select(value):
    selected_key = [key for key, val in DrpDict.items() if val == value][0]
    print(selected_key)  # You can perform actions based on the selected key here

root = tk.Tk()
root.title("Dropdown Example")

selected_value = tk.StringVar(root)
selected_value.set(list(DrpDict.values())[0])  # Set initial selected value

dropdown = tk.OptionMenu(root, selected_value, *DrpDict.values(), command=on_select)
dropdown.pack()

root.mainloop()

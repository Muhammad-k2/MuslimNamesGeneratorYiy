"""MuslimNames is application to generate and search muslim names from dual webserver 'SearchTruth' and 'MuslimNames' webserver, it uses muslim_scraper to
fetch data from server and it can generate muslims names with meanings from A-Z and can search names also with provided meaning. 

Features.
1.Search names with meanings.
2.Generate muslim names with meanings and translation.
3.Random names generator with meanings.
4.All Names list support both geneder with meanings.
5.Work with python3 and support for lower versions.

MuslimNames : V 1.0
Dated 25-05-2019
written by Haseeb mir (haseebmir.hm@gmail.com)  
"""

#Import API and GUI modules.
import muslim_scraper as scraper
from tkinter import *
from tkinter import messagebox

#Color constants
APP_UI = "SpringGreen4"

fields = ("Name","Gender","Letter","Limit")

#Method to update searched names on UI form.
def search_name(entries):
    try:
        result_text.delete(1.0,END) 
        name = entries[fields[0]].get()

        gender = None
        if check_var_male.get():
            gender = "m"
        elif check_var_female.get():
            gender = "f"

        if not name or not gender:
            messagebox.showinfo("INFO","Name or gender are missing.")
            return

        name_list = scraper.searchTruth_search(name,gender)	
        if name_list != None:    
            for name in name_list:
                result_text.insert(INSERT,name + "\n\n")
    except Exception as ex:
        messagebox.showinfo("INFO","Exception occured : " + str(ex))		                	

#Method to update generated names on UI form.
def generate_names(entries):
    try:
        result_text.delete(1.0,END) 
        letter = entries[fields[2]].get()
        limit = entries[fields[3]].get()

        gender = None
        if check_var_male.get():
            gender = "m"
        elif check_var_female.get():
            gender = "f"

        if not letter or not gender:
            messagebox.showinfo("INFO","Letter and gender are missing.")
            return

        if limit:    
            name_list = scraper.muslimNames_names(letter,gender,True,False,int(limit))
        else:
            name_list = scraper.muslimNames_names(letter,gender,True,False)
        
        if name_list != None:
            for name in name_list:
                for i in range(len(name)):
                    result_text.insert(INSERT,name[i] + "\n")

    except Exception as ex:
        messagebox.showinfo("INFO","Exception occured : " + str(ex))

#Method to update random generated names on UI form.
def random_names(entries):
    try:
        result_text.delete(1.0,END) 
        limit = entries[fields[3]].get()

        if limit:   
            name_list = scraper.muslimNames_random(int(limit),True)
        else:
            name_list = scraper.muslimNames_random()     
            
        if name_list != None:    
            for name in name_list:
                result_text.insert(INSERT,name + "\n")
    except Exception as ex:
        messagebox.showinfo("INFO","Exception occured : " + str(ex))        
                    	

#Method to make form UI fields on screen.
def make_form(root, fields):
   entries = {}
   bg = APP_UI
   for field in fields:  
      row = Frame(root)
      ent = Entry(row)	
      lab = Label(row,width=10, text=field, anchor="w",background = bg)      
      row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
      lab.pack(side = LEFT)
      ent.pack(side = RIGHT, expand = YES, fill = X)
      entries[field] = ent
   return entries

#Clear all the entries of form.
def clear_entry(entries):

    for field in fields:
        entries[field].delete(0, "end")
    result_text.delete(1.0,END)   

 #Main method to initialize and render interface items on screen.
if __name__ == "__main__":
   try:     
        root = Tk()
        root.title("Muslim Names V 1.0")
        root.configure(background=APP_UI)
        root.resizable(False, False)
        root.geometry("500x700")
        ents = make_form(root, fields)
        root.bind("<Return>", (lambda event, e = ents: fetch(e)))

        #Render all buttons.
        search_btn = Button(root, text = "Search Name",fg = APP_UI,command=(lambda e = ents: search_name(e)))
        search_btn.place(relx=0.1,rely=0.25,anchor=CENTER)

        names_btn = Button(root, text = "Generate Names",fg = APP_UI,command=(lambda e = ents: generate_names(e)))
        names_btn.place(relx=0.4,rely=0.25,anchor=CENTER)

        random_btn = Button(root, text="Random Names",fg = APP_UI,command=(lambda e = ents: random_names(e)))
        random_btn.place(relx=0.7,rely=0.25,anchor=CENTER)

        clear_btn = Button(root, text="Clear",fg = APP_UI,command=(lambda e = ents: clear_entry(e)))
        clear_btn.place(relx=0.9,rely=0.25,anchor=CENTER)

        #Render checkbox.
        check_var_male = IntVar()
        cb = Checkbutton(root, text = "Male", variable = check_var_male,onvalue = 1, offvalue = 0, height=1,width = 20)
        cb.pack(side = RIGHT)
        cb.place(relx=0.38, rely=0.08,anchor=CENTER)
        cb.config(background = APP_UI,foreground = "black")

        check_var_female = IntVar()
        cb = Checkbutton(root, text = "Female", variable = check_var_female,onvalue = 1, offvalue = 0, height=1,width = 23)
        cb.pack(side = RIGHT)
        cb.place(relx=0.78, rely=0.08,anchor=CENTER)
        cb.config(background = APP_UI,foreground = "black")

        result_text = Text(root,height=28,width=58)
        result_text.place(relx=0.03, rely=0.28)
        result_text.configure(font=("Symbol",15, "bold"))

        root.mainloop()

   except Exception as ex:
   		messagebox.showinfo("Exception occured : " + ex)    	    





from passGenerate import generate as G
from tkinter import *
from tkinter import messagebox as msg
from datetime import datetime as dt
#import cprint 
import pandas as pd
import os
import subprocess


LIGHT_GREEN ="#c8f8ce" #"#bce7c8"
GREEN = "#56d19b"
window = Tk()
window.title("Password Manager")
window.geometry("500x520")
window.config(padx=15, pady=15, bg=LIGHT_GREEN)
canva = Canvas(width=450, height=354,bg=LIGHT_GREEN, highlightthickness=0) 
img = PhotoImage(file="3dLock.png")
canva.create_image(230, 170,image=img)
canva.grid(column=1, row=0)
csv_file ='usersCount.csv'
rd_pressed = 0
max_count = None



#-------------------------------------------------------

## checks if the current entries already exist
def entry_doesnt_exist(username, website):
    website = website.replace("https://", "")
    Site = ""
    name = ""
    doesnt_EXIST = True
    with open("Locker/data.txt", "r") as F:
        lines = F.readlines()
        for line in lines:
            parts = line.split("||")
            for part in parts:
                part = part.strip()  
                if part.startswith("Website:"):
                    Site = part.split(":")[1].strip()  
                elif part.startswith("Email/UserName:"):
                    name = part.split(":")[1].strip()  
                    #print(f"name : {name}, username: {username}")       
                    #print(f"website: {website}, Site: {Site}")
            if username == name and website == Site:
                alrdy_exst.config(text="user / email & website already exist ")
                doesnt_EXIST = False
                #return doesnt_EXIST
                break
                alrdy_exst.config(text="")
    #subprocess.run([batch_file_path, after_COMMAND])
        return doesnt_EXIST

#-----------------------------------------------------

#### checking exisiting csv file

def check_current_csv():
    global csv_file
    if not os.path.isfile(csv_file):
        return False
    else:
        return True

#-------------------------------------------------------

##taking the suggestion for user entry from the most mentioned user

if check_current_csv():
    dataFrame = pd.read_csv(csv_file)
    max_count = dataFrame["count"].max()
    max_user_rows = dataFrame[dataFrame["count"] == max_count]
    max_user_name = max_user_rows["UserName/Email"].iloc[0] 
    #print(max_user_name)

#-------------------------------------------------------
    
### creating new Data Frame and saving it
    
def create_and_save_dataFrame(username):
    newData = pd.DataFrame({"UserName/Email": [username], "count": [1]})
    #dataFrame = pd.concat([dataFrame, newData], ignore_index=True)
    newData.to_csv(f'{csv_file}', index=False)

#---------------------------------------
       
### updating count for each cases
    
def update_count(username):
    if check_current_csv():
        global csv_file
        dataFrame = pd.read_csv(csv_file)
        
        if username in dataFrame["UserName/Email"].values:
            dataFrame.loc[dataFrame["UserName/Email"]== username, "count"]+= 1
        else:
            new_row = pd.DataFrame({"UserName/Email": [username], "count": [1]})
            dataFrame = pd.concat([dataFrame, new_row], ignore_index=True)

        dataFrame.to_csv(csv_file, index=False)
    else:
        create_and_save_dataFrame(username)

#----------------------------------------
## commands

def save_inpt():
    WBSITE = website.get()
    USRNAME = usr_name.get()
    PASSWD = passwd.get()
    if len(WBSITE) == 0 or len(PASSWD) == 0:
            msg.showinfo(title="Error: Empty TextBox", message="Make sure you fill all fields !!")
    else:
        is_k = msg.showinfo(title=WBSITE, message=f"These are the detailed Entered : \n 💠Email / UserName : {USRNAME} \n 💠Password : {PASSWD} \n Is it K to save ?"  )
        if is_k:
            if entry_doesnt_exist(website=WBSITE, username=USRNAME):
                date_time = dt.now()
                TIME = date_time.strftime("%H:%M") #date("%Y-%m-%d") Time ("%H:%M:%S")
                DATE = date_time.strftime("%Y-%m-%d")
                with open("Locker/data.txt", "a") as f:
                    f.writelines(f"Date: {DATE} Time: {TIME}  ---|| Website: {WBSITE} || Email/UserName: {USRNAME} || pass: {PASSWD} \n")
            
                update_count(usr_name.get())
                website.delete(0, 'end')
                usr_name.delete(0, 'end')
                passwd.delete(0, 'end')
                usr_name.insert(0, max_user_name)

        else:
            pass
            #save_inpt()
           
        
    
    
    

    
   


def show_hide_radio():
    global rd_pressed
    rd_pressed += 1
    rd = radio_state.get()
    print(rd)
 
    if rd_pressed % 2 == 0:
        radio_state.set(0)
        passwd.config(show="#")
    else:
        #radio_state.set(1)
        passwd.config(show="")

def GeneratePassword():
    Passwd = G()
    passwd.config(show="")
    passwd.delete(0, END)
    passwd.insert(0, Passwd)




#-------------------------------------------------
    
## Entries
    
website = Entry(fg="grey")
website.place(x=150, y=380, width=230)
website.focus()

usr_name = Entry(fg="grey")
usr_name.insert(0, max_user_name)
usr_name.place(x=150, y=405, width=230)


passwd = Entry(fg="grey", show="#")
passwd.place(x=150, y=430, width=180)

#----------------------------------------

## labels

wb_label = Label(text="Website: ", font=("Arial", 8, "bold"), bg=LIGHT_GREEN)
wb_label.place(x=83, y=380)

usr_name_label = Label(text="Email / User Name: ", font=("Arial", 8, "bold"), bg=LIGHT_GREEN)
usr_name_label.place(x=30, y=405)

passwd_label = Label(text="Password: ", font=("Arial", 8, "bold"), bg=LIGHT_GREEN)
passwd_label.place(x=72, y=430)

alrdy_exst = Label(text="", font=("Arial", 9, "bold"), bg=LIGHT_GREEN, fg="red")
alrdy_exst.place(x=170, y=355)
#-------------------------------------------

## buttons
#btn = PhotoImage(file="btn.png")
generate_btn = Button(text="Generate", width=7, bg = GREEN, command=GeneratePassword)
generate_btn.place( x=395, y=430)


add_btn = Button(text="Add", width=10, bg = GREEN, command=save_inpt)
add_btn.place( x=200, y=460)

radio_state = IntVar()
shw_hide_pass = Radiobutton(text="show",value=1, variable= radio_state, command=show_hide_radio, bg=LIGHT_GREEN, font=("Arial", 7, "bold"))
shw_hide_pass.place(x=335, y=430)


window.mainloop()









from passGenerate import generate as G
from tkinter import *
from tkinter import messagebox as msg
from datetime import datetime as dt
#import cprint 
import pandas as pd
import os, json
from queue import Queue


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
rd_pressed = False
initial_press= 0
max_count = None
radio_state = False

press_state_queue = Queue()



#-------------------------------------------------------

## checks if the current entries already exist
def entry_doesnt_exist(username_email_input, website):
    website = website.replace("https://", "")
    Site = ""
    Email_username = ""
    doesnt_EXIST = True
    with open("Locker/data.jdon", "r") as F:
        pass_details = json.load(F)
        for details in pass_details:
            Site = details["website"]
            Email_username = details["email_or_username"]
            if username_email_input == Email_username and website == Site:
                alrdy_exst.config(text="you already have a recored of these entries ")
                doesnt_EXIST = False
                break
    
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
            if entry_doesnt_exist(website=WBSITE, username_email_input=USRNAME):
                date_time = dt.now()
                TIME = date_time.strftime("%H:%M") #date("%Y-%m-%d") Time ("%H:%M:%S")
                DATE = date_time.strftime("%Y-%m-%d")
                with open("Locker/data.json", "a") as f:
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
    rd_state = None
    global initial_press, rd_pressed
    initial_press += 1
    # rd_pressed = True if not rd_pressed else False
    # rd_state = radio_state.get()
    # set(1) means no show 
    #the default is show
    #when I press for the first time it should put the button in a noshow state set(1)
    #when the dot is present means that it's in a 0 state 
    #when pressing the generate password button the state changes to 0 (dot on)
    #I need to add to the queue something that make the initail condition do the opposite which is set(1) 
    try:
        if initial_press > 1:
            rd_state = press_state_queue.get()
            print("summoned the last queue")
            print(f"last queue: {rd_state}")
        
        if  rd_state  :
            radio_state.set(0)
            press_state_queue.put(False)
            print(f"set = 0 : {radio_state.get()}")
            passwd.config(show="")
        else:
            press_state_queue.put(True)
            radio_state.set(1)
            print("adding to the true queue")
            
            print(f"set = 1 : {radio_state.get()}")
            passwd.config(show="#")
    except Exception as e:
        print(f"[!] Queue error: {e}")
    
    # if rd_pressed  :
    #     radio_state.set(1)
    #     passwd.config(show="#")
    # else:
    #     radio_state.set(0)
    #     passwd.config(show="")

#-------------------------------------------------
        
## generates and adds the generated password to the input field
        
def GeneratePassword():
    Passwd = G()
    passwd.config(show="")
    passwd.delete(0, END)
    passwd.insert(0, Passwd) 
    rd_state = radio_state.get()
    print(rd_state)
    press_state_queue.put(False)
    if rd_state:
        
        radio_state.set(0)
        print(f"set = 0 : {radio_state.get()}")
        passwd.config(show="")

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
shw_hide_pass = Radiobutton(text="show",value=0, variable= radio_state, command=show_hide_radio, bg=LIGHT_GREEN, font=("Arial", 7, "bold"))
shw_hide_pass.place(x=335, y=430)



window.mainloop()




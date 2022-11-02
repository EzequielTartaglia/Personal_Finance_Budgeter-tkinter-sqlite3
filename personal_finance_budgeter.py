#Personal Finance Budgeter 
#Dev. Ezequiel M. Tartaglia

#Modules
from datetime import datetime
from tkinter import ttk 
from tkinter import *
import sqlite3
#import pandas as pn
#import numpy as np
#from muttlib.gsheetsconn import GSheetsClient

class Item: 

    db_name = 'data_base.db'

    #Run something from the database
    def run_query(self,query,parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query,parameters)
            conn.commit()
        return result
    
    #Function to get the items from the database
    def get_items(self):
        #Clean table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #Quering data
        query = 'SELECT * FROM item ORDER BY price ASC'
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('',0,text= row[1], values= row[2])
    #Function to validate if one label is empty
    def validation(self):
        #Only validate the value (.get()) inside the labels
        return len(self.name.get()) != 0 and len(self.price.get()) != 0 
    
    #Function to add new item
    def add_item(self):
        
        #If the labels have information
        if self.validation():
           #Request
           query = 'INSERT INTO item VALUES(NULL,?,?)'
           #From where the values are getting
           parameters = (self.name.get(),self.price.get())
           #Save the information in SQlite (DB browser)
           self.run_query(query,parameters)
           self.message['text'] = 'Item {} added to the Data base'.format(self.name.get())
           #Reset the form
           self.name.delete(0,END)
           self.price.delete(0,END)
        
        #If the labels don't have information
        else:
           self.message['text'] = 'Name or price is empty'.format(self.name.get())
        self.get_items()

    #Function to delete one item
    def delete_item(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as error:
            self.message['text'] = 'Please select a record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM item WHERE name = ?'
        self.run_query(query,(name, ))
        self.message['text'] = 'Record {} delete successfully'.format(name)
        self.get_items()
    
    #Function to edit values in a new window
    def edit_item(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as error:
            self.message['text'] = 'Please select a record'
            return
        before_edit_name = self.tree.item(self.tree.selection())['text']
        before_edit_price = self.tree.item(self.tree.selection())['values'][0]




        ############################################################################ Open new window ##################################################################################
        self.edit_window = Toplevel()
        self.edit_window.geometry("200x130") #Dimentions of the windows
        self.edit_window.title = 'Edit item'
            #Old name
        Label(self.edit_window, text = 'Old name: ').grid(row = 0, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = before_edit_name), state = 'readonly').grid(row = 0, column = 2)
            #Edit name
        Label(self.edit_window, text = 'New name: ').grid(row = 1, column = 1)
        new_name = Entry(self.edit_window)
        new_name.grid(row = 1, column = 2)
            #Old price
        Label(self.edit_window, text = 'Old price: ').grid(row = 2, column = 1)
        Entry(self.edit_window, textvariable = StringVar(self.edit_window, value = before_edit_price), state = 'readonly').grid(row = 2, column = 2)
            #Edit price
        Label(self.edit_window, text = 'New price: ').grid(row = 3, column = 1)
        new_price = Entry(self.edit_window)
        new_price.grid(row = 3, column = 2)
            #Submit Button
        Button(self.edit_window, text = 'Update', command = lambda: self.edit_records(new_name.get(),before_edit_name,new_price.get(),before_edit_price)).grid(row = 4, column = 2, sticky = W + E)

    #Function to save records(update) in the data base
    def edit_records(self,new_name,name,new_price,old_price):
        query = 'UPDATE item SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name,new_price,name,old_price)
        self.run_query(query,parameters)
        #Close the edit window
        self.edit_window.destroy()
        self.message['text'] = 'Record {} updated successfully'.format(name)
        self.get_items()
        #################################################################
    
    
    
    ############################################################################################### MAIN ########################################################################################
    #Total price
    
    def __init__(self,window): 
        
        db_name = 'data_base.db'

        #Function to receive the total price
        def total_price(db_name):
            db = sqlite3.connect(db_name)
            cursor = db.cursor()
            cursor.execute('SELECT * FROM item')
            result = cursor.fetchall()
            
            #Total price
            total_price = 0
            for item in result:
                price = item[2]
                total_price += price
            return total_price

        #Validation
        def login():
            if user.get() == "e" and password.get() == "e":
                
                #Instructions
                title_of_program = Label(text="Personal Finance Budgeter",font=50).grid(row=1,column=0,columnspan=2,sticky=W+E)
                description_of_program = Label(text="Instructions of use:\n 1) If you have income of money, place it in positive the price \n 2) If you have debts or payments to make, add the '-' to the price \n 3)To update the total you must log out and re-enter").grid(row=2,column=0,columnspan=2,sticky=W+E)
                ps_description_of_program = Label(text="Ps: If the total is negative, that implies that your losses \n are greater than your profits, otherwise, it is the balance in favor").grid(row=3,column=0,columnspan=2)

                #Delete the user_information
                login_user.destroy()
                login_user_entry.destroy()
                login_password.destroy()
                login_password_entry.destroy()
                frame_login.destroy()

                #Current time (at the moment to sign in)
                window.title(f"Logged as {user.get().capitalize()} - {datetime.strftime((datetime.now()),'%H:%M %d/%m')}")
                ########################################################
                
                    #Create a Frame Container (Container of elements)
                frame = LabelFrame(self.wind, text="Add a new Item")
                frame.grid(row = 5, column=0, columnspan= 3, pady=20)

                    #################### Name Label ########################
                Label(frame, text= 'Name: ').grid(row= 6, column= 0)
                self.name = Entry(frame)
                self.name.focus()
                self.name.grid(row=6,column=1)
                    ########################################################
                
                    ######################## Price Label ###################
                Label(frame, text= 'Price: ').grid(row= 7, column= 0)
                self.price = Entry(frame)
                self.price.grid(row=7,column=1)
                    ########################################################
                
                    #################### Button Save #######################
                ttk.Button(frame, text="Save item", command = self.add_item).grid(row = 8, columnspan = 2, sticky = W + E)
                    #Output message
                self.message = Label(text= '', fg ='red')
                self.message.grid(row = 8, column = 0, columnspan = 2, sticky= W + E)
                    ########################################################

                    ####################### Table ##########################
                self.tree = ttk.Treeview(height = 10, columns = 2)
                self.tree.grid(row=9,column=0,columnspan=2) #Create grid
                self.tree.heading('#0', text="Name", anchor=CENTER)#Left heading(Name)
                self.tree.heading('#1',text="Price", anchor=CENTER)#Right heading(Price)
                    ##### Buttons #####
                ttk.Button(text = 'DELETE', command= self.delete_item).grid(row = 10, column = 0, sticky = W + E)
                ttk.Button(text = 'EDIT', command = self.edit_item).grid(row = 10, column = 1, sticky = W + E)

                    ################## Get items from SQlite ###############
                self.get_items()
                    ########################################################

                    #################### Total acumulator ##################
                #Get the acumulator (total price)
                total_price_items = total_price(db_name)
                Label(text=f"The total amount is: $ {total_price_items} - Last updated: {datetime.strftime((datetime.now()),'%H:%M %d/%m')}").grid(row=11,column=0,columnspan=2)
                    ######################WORKING############################


            else:
                window.title("Fail")

        #Save window
        self.wind = window
        window.geometry("400x600") #Dimentions of the windows 
        window.resizable(width=False, height = False) #Fix size for the user
        ######################### Title ########################
        #Window Title
        self.wind.title('Personal Finance Budgeter')
        ########################################################

        ######################### Login ########################
        frame_login = LabelFrame(self.wind, text="Login")
        frame_login.grid(row = 5, column=5, columnspan= 3, padx=110,pady=200)
        #User
        user=StringVar()
        login_user = Label(frame_login, text="User: ")
        login_user.grid(row=0 , column= 5)
        login_user_entry = Entry(frame_login,width=30,textvariable=user)
        login_user_entry.grid(row=1, column= 5)
        login_user_entry.focus()

        #Password
        password=StringVar()
        login_password = Label(frame_login, text="Password: ")
        login_password.grid(row=2 , column=5 )
        login_password_entry = Entry(frame_login,width=30,textvariable=password)
        login_password_entry.grid(row=3, column= 5)
        
        #Button
        Button(frame_login,text="Login", command = login).grid(row = 4, column=5, pady=5)




def main():
    #Home window 
    window = Tk()
    app = Item(window)
    window.mainloop()


if __name__ == '__main__':
    main()


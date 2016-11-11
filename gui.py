#!/usr/bin/env python3

## IMPORT

# System modules
from PIL import ImageTk, Image
import fnmatch
import os
import tkinter as tk
import time

# Our modules
from Database.database import *
from OpenALPR.reader import *
from RDW.rdwClient import *
from Utils.emailSMTP import *

# Load classes
db = DatabaseClass()
mail = EmailSmtp()
rdw = RdwClient()

# Basic class that frame classes import
class Pag(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
    def show(self):
        self.lift()

 #Frame class to put in window container
class controle(Pag):
    def __init__(self):
        super().__init__()
        label = tk.Label(self, text='dit is de controle pagina')
        label.pack(side='bottom')
        self.initialize()

    # Function that initializes the widgets
    def initialize(self):
        global info
        global var

        # Add images to dropdown
        images = []
        for img in os.listdir(r'./Images'):
            images.append(img)
        images = tuple(images)

        # Create images dropdown
        var = tk.StringVar()
        var.set(images[0])
        drop = tk.OptionMenu(self, var, *images, command = self.callback)
        drop.place(x=10, y=10)

        # Creates a Tkinter compatible image
        raw = Image.open('./Images/' + var.get()).resize((562, 314), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(raw)

        # Place the image
        self.imgwidget = tk.Label(self, image=img, relief=tk.GROOVE, borderwidth=2)
        self.imgwidget.place(x=10, y=50)

        # Get plate info
        info = image_to_list('./Images/' + var.get())

        # Place OpenALPR info in left textbox
        self.leftwidget = tk.Text(self, relief=tk.GROOVE, borderwidth=2, highlightthickness=0, width=29)
        self.leftwidget.insert(0.0, self.left(info))
        self.leftwidget.place(x=10, y=377)

        # Place some more info in the right textbox
        self.rightwidget = tk.Text(self, relief=tk.GROOVE, borderwidth=2, highlightthickness=0, width=49)
        self.rightwidget.insert(0.0, self.right(info))
        self.rightwidget.place(x=228, y=377)

        tk.Button(self, text='volgende', command=mainpage.Register).pack()

    # Function that updates the images and widgets
    def callback(self, e):
        # Create a Tkinter compatible image
        raw = Image.open('./Images/' + var.get()).resize((562, 314), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(raw)

        # Replace the image
        self.imgwidget.configure(image=img)
        self.imgwidget.image = img

        # Get plate info
        info = image_to_list('./Images/' + var.get())

        # Place OpenALPR info in left textbox
        self.leftwidget.insert(0.0, "\n ---------------------------\n\n\n")
        self.leftwidget.insert(0.0, self.left(info))

        # Place some more info in the right textbox
        self.rightwidget.delete(0.0, tk.END)
        self.rightwidget.insert(0.0, self.right(info))

    # Function thats creates the left textbox text
    def left(self, info):
        if len(info) == 0:
            return(' No license plate detected!\n\n')

        text = ''
        count = 0

        for _ in info:
            text += ' Possibility #' + str(count) + ':\n\n'
            text += '  String     = ' + str(info[count]['plate']) + '\n'
            text += '  Confidence = ' + str(info[count]['confidence']) + '\n'
            text += '  Region     = ' + str(info[count]['region']) + '\n'
            text += '\n'

            count += 1

        return(text)

    #function that creates the right textbox text
    def right(self, info):
        global data
        if len(info) == 0:
            return('\n\n    [×] ?\n')

        # Try to get the data from the database
        try:
            used = 'db'
            data = db.get_customer_history_by_numberplate(info[0]['plate'], 1)[0]
        except IndexError:
            used = 'rdw'
            rdw.fetch_by_plate(info[0]['plate'])
            data = rdw.get_plate_data()
            if data == None:
                used = 'none'

        print('DEBUG: ' + used)

        if used != 'none':
            # Check if the car matches our criteria (diesel and older than 2001)
            if self.validate_plate(data['parking_car_releasedate'], data['parking_car_fuel']):
                text = '\n\n   [-] ' + info[0]['plate']
            else:
                text = '\n\n   [+] ' + info[0]['plate']

            text += '\n\n    * Voertuig soort: ' + data['parking_car_type']
            text += '\n    * Intrichting: ' + data['parking_car_body']
            text += '\n    * Merk: ' + data['parking_car_name']
            text += '\n    * Brandstof type: ' + data['parking_car_fuel']
            text += '\n    * Cilinder inhoud: ' + str(data['parking_car_cylinder_capacity'])
            text += '\n    * Datum afgifte: ' + str.split(data['parking_car_releasedate'], '-')[0]

        # Place data in db
        if used == 'rdw':
            db.checkin(info[0]['plate'], data['parking_car_fuel'], str.split(data['parking_car_releasedate'], '-')[0], data['parking_car_name'], data['parking_car_type'], data['parking_car_body'], str(data['parking_car_cylinder_capacity']))
        elif used == 'none':
            text = '\n\n   [×] ' + info[0]['plate']

        return(text)

    #function that checks what fuel the car uses and wich year the car is from.
    #if certain conditions are met, then the car is not allowed.
    def validate_plate(self, fuel_type, year) -> bool:
        if fuel_type.lower() == 'diesel' and int(year[0]) < 2001:
            return(False)
        else:
            return(True)

#Frame class to put in window container
class uitcheck(Pag):

    #global to use in the rest of the code
    global datalink

    #frame initialization
    def __init__(self):
        super().__init__()
        label = tk.Label(self, text='dit is de pagina voor factuurgegevens')
        label.pack(side='bottom')
        self.initialize()

    #function that initializes the widgets
    def initialize(self):
        global var3
        global voornaam
        global achternaam
        global geboorteDatum
        global adres
        global postcode
        global woonplaats
        global e_mail

        geslacht = ['man',
                    'vrouw']
        var3 = tk.StringVar()
        var3.set(geslacht[0])

        w = tk.OptionMenu(self, var3, *geslacht)
        w.pack()

        tk.Label(self, text='Voornaam:').pack(side='top', anchor=tk.N)
        voornaam = tk.Entry(self)
        voornaam.pack(side='top', anchor=tk.N)

        tk.Label(self, text='Achternaam:').pack(side='top', anchor=tk.N)
        achternaam = tk.Entry(self)
        achternaam.pack(side='top', anchor=tk.N)

        tk.Label(self, text='Geboortedatum:').pack(side='top', anchor=tk.N)
        geboorteDatum = tk.Entry(self)
        geboorteDatum.pack(side='top', anchor=tk.N)

        tk.Label(self, text='Adres:').pack(side='top', anchor=tk.N)
        adres = tk.Entry(self)
        adres.pack(side='top', anchor=tk.N)

        tk.Label(self, text='Postcode:').pack(side='top', anchor=tk.N)
        postcode = tk.Entry(self)
        postcode.pack(side='top', anchor=tk.N)

        tk.Label(self, text='Woonplaats:').pack(side='top', anchor=tk.N)
        woonplaats = tk.Entry(self)
        woonplaats.pack(side='top', anchor=tk.N)

        tk.Label(self, text='E-mail:').pack(side='top', anchor=tk.N)
        e_mail = tk.Entry(self)
        e_mail.pack(side='top', anchor=tk.N)

        tk.Button(self, text='Schrijf in', command=self.printlab).pack(side='top', anchor=tk.N)

    #function that enters information into the sql database
    def printlab(self):
        db.insert_customer(voornaam.get(), achternaam.get(), adres.get(), postcode.get(), var3.get(), woonplaats.get(), e_mail.get())
        mainpage.DoneReg()

#Frame class to put in window container
class betaal(Pag):
    #frame initialization
    def __init__(self):
        super().__init__()
        tk.Label(self, text = 'selecteer uw betaalmethode:').pack()
        self.initialize()

    #function that initializes the widgets
    def initialize(self):
        global set
        set = 0
        contant = tk.Button(self, text = 'contant betalen', command = self.setting).place(rely = 0.1, relx = 0.5, anchor = tk.CENTER)
        factuur = tk.Button(self, text = 'factuur', command = self.setting2).place(rely=0.15, relx = 0.5, anchor = tk.CENTER)

    #Function that sets a flag to define wich frame to switch to
    def setting(self):
        global set
        set = 1
        mainpage.func()

    #Function that sets a flag to define wich frame to switch to
    def setting2(self):
        global set
        set = 2
        mainpage.func()

#Frame class to put in window container
class done(Pag):
    #frame initialization
    def __init__(self):
        super().__init__()
        self.initialize()

    #function that initializes the widgets
    def initialize(self):
        tk.Label(self, text = 'u heeft contant betaald').place(rely = 0.2, relx = 0.5, anchor = tk.CENTER)
        tk.Label(self, text = 'U bent klaar, U kunt nu gaan').place(rely = 0.1, relx = 0.5, anchor = tk.CENTER)
        tk.Button(self, text = 'volgende klant', command = mainpage.start).place(rely = 0.4, relx = 0.5, anchor = tk.CENTER)

#Frame class to put in window container
class done2(Pag):
    #frame initialization
    def __init__(self):
        super().__init__()
        self.initialize()

    #function that initializes the widgets
    def initialize(self):
        global invoice
        ServData = {}
        tk.Label(self, text = 'U krijgt een factuur per e-mail gestuurd').place(rely = 0.2, relx = 0.5, anchor = tk.CENTER)
        tk.Label(self, text = 'U bent klaar, U kunt nu gaan').place(rely = 0.1, relx = 0.5, anchor = tk.CENTER)

        #kenId = db.get_customer_id_by_numberplate('4-FYA-A')
        try:
            ServData = db.get_customer_details_by_numberplate(info[0]['plate'])
            #print(db.get_customer_details_by_customer_id('1'))
            email_server.set_subject('Factuur Parkeren')
            email_server.set_to_address(ServData['customer_email'])
            #print(ServData)
            invoice = {
                'id': 1337,
                'date': time.time(),
                'due_date': time.time(),
                'description': 'Parking noodle parkeer garage',
                'price': time.time() * 0.6,
                'client': {
                    'name': ServData['customer_firstname'] + ' ' + ServData['customer_lastname'],
                    'address': ServData['customer_address'],
                    'city': ServData['customer_city'],
                    'zip-code': ServData['customer_postcode'],
                    'country': 'Nederland'
                }
            }
            email_server.send_invoice_mail(invoice)
        except:
           pass
        tk.Button(self, text = 'volgende klant', command = mainpage.start).place(rely = 0.4, relx = 0.5, anchor = tk.CENTER)

#window to create a framecontainer + a way to switch frames
class mainpage(tk.Frame):
    #frame initialization
    def __init__(self):
        super().__init__()
        self.initialize()

    #function that initializes the widgets
    def initialize(self):

        #globals to use in other functions
        global p1
        global p2
        global p3
        global p5
        global p6

        #variables get assigned here
        p1=controle()
        p2=uitcheck()
        p3=done()
        p5=betaal()
        p6=done2()

        #creation of container and buttonframe
        self.buttonframe = tk.Frame(self)
        self.container = tk.Frame(self)
        self.buttonframe.pack(side="top", fill="x", expand=False)
        self.container.pack(side="top", fill="both", expand=True)

        #assignement where frames have to go
        p1.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p6.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        p1.show()

    #function to switch frame
    def DoneReg():
        p6.lift()

    #function to switch frame, based on a statement
    def Register():
        if controle.validate_plate(data['parking_car_release_date'], data['parking_car_fuel']):
            CusEx = db.get_customer_history_by_numberplate(info[0]['plate'], 1)
            print(CusEx)
            CusEx2 = CusEx[0]
            if CusEx2['parking_id'] == 0:
                p2.lift()
            else:
                p6.lift()
        else:
            tk.Label(controle, text='Wouter komt stompen').pack()
            email_server.send_stomp_mail()

    #function to switch frame
    def start():
        p1.lift()

    #function to switch frame, based on a statement
    def func():
        if set == 1:
            p3.lift()
        if set == 2:
            p6.lift()

#mainloop to render window
if __name__ == "__main__":
    root = tk.Tk()
    main = mainpage()
    main.pack(side='top', fill='both', expand=True)
    root.geometry('2048x680')
    root.mainloop()

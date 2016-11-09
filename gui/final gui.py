from Database.databaseClass import DatabaseClass
from Utils.emailSMTP import EmailSmtp
import tkinter as tk
import fnmatch
import os
import time
from PIL import ImageTk, Image

database = DatabaseClass()
email_server = EmailSmtp()

class Pag(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
    def show(self):
        self.lift()

class controle(Pag):
    def __init__(self):
        super().__init__()
        label = tk.Label(self, text='dit is de controle pagina')
        label.pack(side='bottom')
        self.initialize()
    def initialize(self):
        global brandstof
        global afgifte
        self.brandstoffen=[
            ('diesel', '1'),
            ('benzine', '2'),
            ('gas', '3'),
            ('elektrisch', '4')
        ]
        brandstof=tk.IntVar()
        brandstof.set('1')
        tk.Label(self, text='hoofdbrandstof?', justify=tk.LEFT, padx=20).pack(side='top', anchor=tk.N)
        for txt, val in self.brandstoffen:
            tk.Radiobutton(self,
                text=txt,
                padx = 20,
                variable = brandstof,
                value = val).pack(side='top', anchor=tk.S)
        tk.Label(self, text='afgifte datum').pack(side='top', anchor=tk.N)
        afgifte = tk.Entry(self)
        afgifte.pack(side='top', anchor=tk.N)
        tk.Button(self, text='vergelijk', command=mainpage.verbod).pack(side='top', anchor=tk.N)

class uitcheck(Pag):
    global datalink
    def __init__(self):
        super().__init__()
        label = tk.Label(self, text='dit is de pagina voor factuurgegevens')
        label.pack(side='bottom')
        self.initialize()

    def initialize(self):
        global var
        global voornaam
        global achternaam
        global geboorteDatum
        global adres
        global postcode
        global woonplaats
        global e_mail

        geslacht = ['man',
                    'vrouw']
        var = tk.StringVar()
        var.set(geslacht[0])

        w = tk.OptionMenu(self, var, *geslacht)
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

    def printlab(self):
        database.insert_customer(voornaam.get(), achternaam.get(), adres.get(), postcode.get(), var.get(), woonplaats.get(), e_mail.get())
        mainpage.DoneReg()

class betaal(Pag):
    def __init__(self):
        super().__init__()
        tk.Label(self, text = 'selecteer uw betaalmethode:').pack()
        self.initialize()
    def initialize(self):
        global set
        set = 0
        contant = tk.Button(self, text = 'contant betalen', command = self.setting).place(rely = 0.1, relx = 0.5, anchor = tk.CENTER)
        factuur = tk.Button(self, text = 'factuur', command = self.setting2).place(rely=0.15, relx = 0.5, anchor = tk.CENTER)

    def setting(self):
        global set
        set = 1
        mainpage.func()

    def setting2(self):
        global set
        set = 2
        mainpage.func()

class done(Pag):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        tk.Label(self, text = 'u heeft contant betaald').place(rely = 0.2, relx = 0.5, anchor = tk.CENTER)
        tk.Label(self, text = 'U bent klaar, U kunt nu gaan').place(rely = 0.1, relx = 0.5, anchor = tk.CENTER)
        tk.Button(self, text = 'volgende klant', command = mainpage.start).place(rely = 0.4, relx = 0.5, anchor = tk.CENTER)

class done2(Pag):
    def __init__(self):
        super().__init__()
        self.initialize()
    def initialize(self):
        global invoice
        ServData = {}
        tk.Label(self, text = 'U krijgt een factuur per e-mail gestuurd').place(rely = 0.2, relx = 0.5, anchor = tk.CENTER)
        tk.Label(self, text = 'U bent klaar, U kunt nu gaan').place(rely = 0.1, relx = 0.5, anchor = tk.CENTER)

        #kenId = database.get_customer_id_by_numberplate('4-FYA-A')
        ServData = database.get_customer_details_by_numberplate('4-FYA-AA')
        #print(database.get_customer_details_by_customer_id('1'))
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
        #email_server.send_invoice_mail(invoice)
        tk.Button(self, text = 'volgende klant', command = mainpage.start).place(rely = 0.4, relx = 0.5, anchor = tk.CENTER)

class SQLcheck(Pag):
    def __init__(self):
        super().__init__()
        self.initialize()
    def initialize(self):
        global images
        global value
        global value2
        global curPos
        value2 = 0

        def callback(curPos):
            PILimage = Image.open('./kentekens/' + images[curPos]).resize((562, 314), Image.ANTIALIAS)
            LabImage = ImageTk.PhotoImage(PILimage)

            imgLab.configure(image =LabImage)
            imgLab.image = LabImage

        images = {}
        value = 0
        for image in os.listdir(r'./kentekens'):
            if fnmatch.fnmatch(image, '*.jpg'):
                if image in images:
                    continue
                else:
                    images[value] = image
                value += 1
                #print(images)

        PILimage = Image.open('./kentekens/' + images[value2]).resize((562, 314), Image.ANTIALIAS)
        LabImage = ImageTk.PhotoImage(PILimage)

        imgLab = tk.Label(self, image = LabImage)
        imgLab.image = LabImage
        imgLab.place(relx = 0.5, rely = 0.3, anchor = tk.CENTER)

        def valueUp():
            global value2
            value2 +=1
            curPos = value2
            callback(curPos)

        def valueDown():
            global value2
            value2 -=1
            curPos = value2
            callback(curPos)

        backBut = tk.Button(self, text='Previous image', command = lambda:valueDown()).place(relx = 0.29, rely = 0.55)
        forBut = tk.Button(self, text ='Next image', command = lambda:valueUp()).place(relx=0.66, rely = 0.55)

        tk.Button(self, text='Selecteer Kenteken', command=mainpage.Register).place(relx = 0.5, rely = 0.7, anchor=tk.CENTER)

class mainpage(tk.Frame):
    def __init__(self):
        super().__init__()
        self.initialize()
    def initialize(self):
        global p1
        global p2
        global p3
        global p4
        global p5
        global p6

        p1=controle()
        p2=uitcheck()
        p3=done()
        p4=SQLcheck()
        p5=betaal()
        p6=done2()

        self.buttonframe = tk.Frame(self)
        self.container = tk.Frame(self)
        self.buttonframe.pack(side="top", fill="x", expand=False)
        self.container.pack(side="top", fill="both", expand=True)

        p1.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        p6.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(self.buttonframe, text="Controle", command=p1.lift)
        b2 = tk.Button(self.buttonframe, text="Uitchecken", command=p2.lift)
        b3 = tk.Button(self.buttonframe, text="SQL", command=p4.lift)
        b4 = tk.Button(self.buttonframe, text="betaal methode", command=p5.lift)
        b5 = tk.Button(self.buttonframe, text = 'done factuur', command = p6.lift)

        #b1.pack(side="right")
        #b2.pack(side="right")
        #b3.pack(side="right")
        #b4.pack(side="right")
        #b5.pack(side="right")

        p4.show()

    def verbod():
        if brandstof.get() == 1 and int(afgifte.get()) <= 2000:
            tk.Label(text='Wouter komt je stompen').pack()
            print('verbod')
        else:
            print('toegestaan')
            p4.lift()

    def DoneReg():
        p6.lift()

    def Register():
        CusEx = database.get_customer_history_by_numberplate('4-FYA-AA', 1)
        print(CusEx)
        CusEx2 = CusEx[0]
        if CusEx2['parking_id'] == 0:
            p2.lift()
        else:
            p6.lift()
    def start():
        p4.lift()

    def func():
        if set == 1:
            p3.lift()
        if set == 2:
            p6.lift()


if __name__ == "__main__":
    root = tk.Tk()
    main = mainpage()
    main.pack(side='top', fill='both', expand=True)
    root.geometry('2048x680')
    root.mainloop()

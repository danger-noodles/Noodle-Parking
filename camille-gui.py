#!/usr/bin/env python3

## IMPORTS

# Installed modules
from PIL import ImageTk, Image
import fnmatch
import os
import tkinter as tk
import time

# Our modules
from Database.database import *
from OpenALPR.reader import *
from RDW.rdwClient import *


## FUNCTIONS

# Function that updates the image and textboxes, gets called by window.bind
def callback(e) -> None:
    # Creates a Tkinter compatible image
    raw = Image.open('./Images/' + var.get()).resize((562, 314), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(raw)

    # Replace the image
    imgwidget.configure(image=img)
    imgwidget.image = img

    # Get plate info
    info = image_to_list('./Images/' + var.get())

    # Place OpenALPR info in left textbox
    leftwidget.insert(0.0, "\n ---------------------------\n\n\n")
    leftwidget.insert(0.0, left(info))

    # Place some more info in the right textbox
    rightwidget.delete(0.0, tk.END)
    rightwidget.insert(0.0, right(info))

# Function thats creates the left textbox text
def left(info) -> str:
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

# Function thats creates the right textbox text, also sends some info to the db possibly
def right(info) -> str:
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
        if validate_plate(data['parking_car_releasedate'], data['parking_car_fuel']):
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

# This function checks if a car matches our criteria
# (diesel and older than 2001)
def validate_plate(fuel_type, year) -> bool:
    if fuel_type.lower() == 'diesel' and int(year[0]) < 2001:
        return(False)
    else:
        return(True)


## EXECUTE

# Crate main window
window = tk.Tk()
window.geometry('586x705')
window.resizable(width=False, height=False)
window.wm_title('Noodle Parking')

# Add images to dropdown
images = []
for img in os.listdir(r'./Images'):
    images.append(img)
images = tuple(images)

# Create images dropdown
var = tk.StringVar()
var.set(images[0])
drop = tk.OptionMenu(window, var, *images, command = callback)
drop.place(x=10, y=10)

# Creates a Tkinter compatible image
raw = Image.open('./Images/' + var.get()).resize((562, 314), Image.ANTIALIAS)
img = ImageTk.PhotoImage(raw)

# Place the image
imgwidget = tk.Label(window, image=img, relief=tk.GROOVE, borderwidth=2)
imgwidget.place(x=10, y=50)

# Get plate info
info = image_to_list('./Images/' + var.get())

# Place OpenALPR info in left textbox
leftwidget = tk.Text(window, relief=tk.GROOVE, borderwidth=2, highlightthickness=0, width=29)
leftwidget.insert(0.0, left(info))
leftwidget.place(x=10, y=377)

# Load RDW and database class
rdw = RdwClient()
db = DatabaseClass()

# Place some more info in the right textbox
rightwidget = tk.Text(window, relief=tk.GROOVE, borderwidth=2, highlightthickness=0, width=49)
rightwidget.insert(0.0, right(info))
rightwidget.place(x=228, y=377)

# Start the GUI loop
window.mainloop()

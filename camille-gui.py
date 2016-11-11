#!/usr/bin/env python3

## IMPORTS

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
from SMTP.email import *
from Utils.config import *


## FUNCTIONS

# Function that updates the image and textboxes, gets called by window.bind
def callback(e) -> None:
    # Create a Tkinter compatible image
    raw = Image.open('./Images/' + var.get()).resize((562, 314), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(raw)

    # Replace the image
    imgwidget.configure(image=img)
    imgwidget.image = img

    # Get license plate info from OpenALPR
    plate_info = image_to_list('./Images/' + var.get())

    # Place OpenALPR info in the left textbox
    leftwidget.insert(0.0, "\n ---------------------------\n\n\n")
    leftwidget.insert(0.0, left_text(plate_info))

    # Place some more info in the right textbox
    # This is mainly info gathered from the rdw or db
    rightwidget.delete(0.0, tk.END)
    rightwidget.insert(0.0, right_text(plate_info))

# Function thats creates the left textbox text
def left_text(info) -> str:
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

# Function thats creates the right textbox text
# Also sends some info to the db possibly
def right_text(info) -> str:
    if len(info) == 0:
        print('DEBUG: none')
        return('\n\n    [×] ?\n')

    # Try to get the data from the database
    try:
        used = 'db'
        data = db.get_customer_history_by_numberplate(info[0]['plate'], 1)[0]
    # If the license plate is not found in the db, try using the rdw
    except IndexError:
        used = 'rdw'
        rdw.fetch_by_plate(info[0]['plate'])
        data = rdw.get_plate_data()
        # Don't gather data if nothing could be found in either the db or rdw
        if data == None:
            used = 'none'

    print('DEBUG: ' + used)

    if used != 'none':
        # Check if the car matches our criteria (diesel and older than 2001)
        if validate_plate(data['parking_car_releasedate'], data['parking_car_fuel']):
            text = '\n\n   [+] ' + info[0]['plate']
        else:
            text = '\n\n   [-] ' + info[0]['plate']

            # Send mail notifying admin
            # TODO: This doesn't work, someone else can fix it.
            mail.send_stomp_mail()

        text += '\n\n    * Voertuig soort: ' + data['parking_car_type']
        text += '\n    * Intrichting: ' + data['parking_car_body']
        text += '\n    * Merk: ' + data['parking_car_name']
        text += '\n    * Brandstof type: ' + data['parking_car_fuel']
        text += '\n    * Cilinder inhoud: ' + str(data['parking_car_cylinder_capacity'])
        text += '\n    * Datum afgifte: ' + str.split(data['parking_car_releasedate'], '-')[0]
    else:
        text = '\n\n   [×] ' + info[0]['plate']

    # Place data in db if rdw was used to gather data
    if used == 'rdw':
        db.checkin(info[0]['plate'], data['parking_car_fuel'], str.split(data['parking_car_releasedate'], '-')[0], data['parking_car_name'], data['parking_car_type'], data['parking_car_body'], data['parking_car_cylinder_capacity'])

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
# TODO: Is the `r` needed here?
for img in os.listdir(r'./Images'):
    images.append(img)
images.sort()
images = tuple(images)

# Create images dropdown
var = tk.StringVar()
var.set(images[0])
drop = tk.OptionMenu(window, var, *images, command = callback)
drop.place(x=10, y=10)

# Create a Tkinter compatible image
raw = Image.open('./Images/' + var.get()).resize((562, 314), Image.ANTIALIAS)
img = ImageTk.PhotoImage(raw)

# Place the image
imgwidget = tk.Label(window, image=img, relief=tk.GROOVE, borderwidth=2)
imgwidget.place(x=10, y=50)

# Get plate info
plate_info = image_to_list('./Images/' + var.get())

# Place OpenALPR info in left textbox
leftwidget = tk.Text(window, relief=tk.GROOVE, borderwidth=2, highlightthickness=0, width=29)
leftwidget.insert(0.0, left_text(plate_info))
leftwidget.place(x=10, y=377)

# Load rdw, mail and db classes
rdw = RdwClient()
db = DatabaseClass()
mail = EmailSmtp()

# Set mail subject and adress
mail.set_subject('Diesel auto probeerd in te checken!')

# Place some more info in the right textbox
# This is mainly info gathered from the rdw 
rightwidget = tk.Text(window, relief=tk.GROOVE, borderwidth=2, highlightthickness=0, width=49)
rightwidget.insert(0.0, right_text(plate_info))
rightwidget.place(x=228, y=377)

# Start the GUI loop
window.mainloop()

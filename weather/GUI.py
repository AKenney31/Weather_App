from tkinter import *
from tkinter import messagebox
from weather.Draw import draw
from turtle import *

import requests
from configparser import ConfigParser


class GUI:
    def __init__(self):
        self.url = 'http://api.openweathermap.org/data/2.5/weather?zip={},{}&appid={}'
        self.config_file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(self.config_file)
        self.api_key = self.config['api_key']['key']

        self.zip_code = None
        self.app = Tk()
        self.app.title("Weather")
        self.app.geometry('700x350')
        self.app.configure(bg='navy blue')

        self.location = StringVar()
        self.add_text_box = Entry(self.app, textvariable=self.location)
        self.add_text_box.pack(side=TOP)

        self.button = Button(self.app, text='Search', width=12, command=self.search)
        self.button.pack(side=TOP)

        self.location_label = Label(self.app, text='Welcome', font=('bold', 20))
        self.location_label.configure(bg='navy blue', fg='white')
        self.location_label.pack()

        self.temp_label = Label(self.app, text='and Press Search', font=('plain', 14))
        self.temp_label.configure(bg='navy blue', fg='white')
        self.temp_label.pack(side=BOTTOM)

        self.weather = Label(self.app, text='Type Zip Code', font=('plain', 14))
        self.weather.configure(bg='navy blue', fg='white')
        self.weather.pack(side=BOTTOM)

        self.canvas = Canvas(self.app, width=100, height=100)
        self.canvas.configure(bg='black', border=None)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.draw_intro_canvas()

        self.app_loop()

    def search(self):
        self.zip_code = self.location.get()
        self.display_weather()

    def display_weather(self):
        w = self.get_weather()
        if w is None:
            messagebox.showerror('Error', 'Cannot recognize zip code {}'.format(self.zip_code))
        else:
            self.location_label['text'] = '{}, {}'.format(w[0], w[1])
            self.temp_label['text'] = '{:.2f}°F'.format(w[2])
            self.weather['text'] = w[3]
            draw(self.canvas, w[3])

    def get_weather(self):
        result = requests.get(self.url.format(self.zip_code, '', self.api_key))
        if result:
            # Data and JSon variables are extracted from a weather api openweathermap.org
            json = result.json()
            city = json['name']
            country = json['sys']['country']
            temp_kelvin = json['main']['temp']
            temp_fahrenheit = (temp_kelvin - 273.15) * 9 / 5 + 32
            weather = json['weather'][0]['main']
            return city, country, temp_fahrenheit, weather
        else:
            return None

    def draw_intro_canvas(self):
        t = RawTurtle(self.canvas)
        t.hideturtle()
        draw(self.canvas, 'Clear')
        t.penup()
        t.setposition(-5, -40)
        t.fillcolor('white')
        t.color('white')
        t.pendown()
        t.begin_fill()
        t.circle(10)
        t.setposition(5, -40)
        t.circle(6)
        t.setposition(-15, -40)
        t.circle(5)
        t.end_fill()

    def app_loop(self):
        self.app.mainloop()

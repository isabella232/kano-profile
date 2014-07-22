
#!/usr/bin/env python

# first_screen.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# First screen of profile on first run
# Launched on straight after kano-settings
# Dependent on internet connection

#from gi.repository import Gtk

import sys
from kano_login.login import Login
from kano_login.about_you import AboutYou
from kano_login.templates.template import Template
from kano_login.data import get_data
from kano.network import is_internet
from kano_profile_gui.images import get_image


def create_template(string):
    data = get_data(string)
    img_width = 590
    img_height = 270

    header = data["LABEL_1"]
    subheader = data["LABEL_2"]
    image_filename = get_image("login", "", data["TOP_PIC"], str(img_width) + 'x' + str(img_height))
    kano_button_label = data["KANO_BUTTON"]
    orange_button_label = data["ORANGE_BUTTON"]
    template = Template(image_filename, header, subheader, kano_button_label, orange_button_label)
    return template


class FirstScreen():
    def __init__(self, win):

        self.win = win

        # Hacky way of moving the window back to the centre
        # Get current coordinates, then move the window up by 100 pixels
        x, y = self.win.get_position()
        self.win.move(x, y - 100)

        self.template = create_template("FIRST_SCREEN")
        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.next_screen)
        self.template.orange_button.connect("button_release_event", self.login_screen)
        self.win.show_all()

    def login_screen(self, widget, event):
        self.win.clear_win()
        Login(self.win)

    def next_screen(self, widget, event):
        self.win.clear_win()

        if is_internet:
            AboutYou(self.win)
        else:
            NoInternet(self.win)


class NoInternet():
    def __init__(self, win):

        self.win = win
        self.template = create_template("NO_INTERNET")

        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.next)
        self.template.orange_button.connect("button_release_event", self.login)
        self.win.show_all()

    def connect(self, widget, event):
        # close window and launch wifi config
        sys.exit(0)

    def register_later(self, widget, event):
        self.win.clear_win()
        RegisterLater(self.win)


class RegisterLater():
    def __init__(self, win):
        self.win = win
        self.template = create_template("REGISTER_LATER")

        self.win.add(self.template)
        self.template.kano_button.connect("button_release_event", self.exit)
        self.win.show_all()

    def exit(self, widget, event):
        # close window and launch wifi config
        sys.exit(0)

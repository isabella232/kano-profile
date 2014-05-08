#!/usr/bin/env python

# login.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# UI for login screen

from gi.repository import Gtk

from components import heading, green_button
from kano.world.functions import login as login_
from kano.profile.profile import load_profile
from kano_login import gender

win = None
box = None


def activate(_win, _box):
    global win, box

    win = _win
    box = _box
    username_entry = Gtk.Entry()
    password_entry = Gtk.Entry()

    title = heading.Heading("Log in", "Open up your world")

    profile = load_profile()
    if 'email' in profile and profile['email']:
        username = profile['email']
    else:
        username = 'Email'

    username_entry.props.placeholder_text = username
    password_entry.props.placeholder_text = 'Password'
    password_entry.set_visibility(False)

    login = green_button.Button("LOG IN")
    login.button.connect("button_press_event", log_user_in, username_entry, password_entry, _win)

    # if we want to add a not-registered button, uncomment out the lines below
    not_registered = Gtk.Button("Not registered?")
    not_registered.get_style_context().add_class("not_registered")
    not_registered.connect("clicked", register)

    container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    container.pack_start(username_entry, False, False, 0)
    container.pack_start(password_entry, False, False, 0)

    valign = Gtk.Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=1)
    padding = 10
    valign.set_padding(padding, padding, 0, 0)
    valign.add(container)
    _box.pack_start(title.container, False, False, 0)
    _box.pack_start(valign, False, False, 0)
    _box.pack_start(login.box, False, False, 30)
    _box.pack_start(not_registered, False, False, 0)

    _win.show_all()


def register(event):
    global win, box

    win.update()
    gender.activate(win, box)


def log_user_in(button, event, username_entry, password_entry, win):
    username_text = username_entry.get_text()
    password_text = password_entry.get_text()

    success, text = login_(username_text, password_text)

    if not success:
        print "error = " + str(text)
        dialog = Gtk.MessageDialog(win, 0, Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.OK, "Houston, we have a problem")
        dialog.format_secondary_text(text)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.destroy()
        else:
            dialog.destroy()

    else:
        dialog = Gtk.MessageDialog(win, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, "Logged in!")
        dialog.format_secondary_text("Yay!")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            dialog.destroy()
            Gtk.main_quit()
        else:
            dialog.destroy()
            Gtk.main_quit()


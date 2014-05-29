#!/usr/bin/env python

# account_confirm.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# UI for confirming to the user they've registered

from gi.repository import Gtk
from components import heading, green_button
from kano_profile_gui.images import get_image

win = None
box = None


def activate(_win, _box):
    global win, box

    win = _win
    box = _box

    win.clear_box()

    if win.age < 13:
        title = "Now get your parents to confirm..."
        description = "We've sent an email to: "
        check_your_email = "Bug them to check their email in 14 days or less - \n                         or you'll lose your profile!"
    else:
        title = "Almost there..."
        description = "To check that you’re the real deal - \n               we sent an email to: "
        check_your_email = "Click on the link within two weeks to confirm your profile"

    nextB = green_button.Button("GOT IT")
    nextB.button.connect("button_press_event", go_next)
    nextB.button.connect("key_press_event", go_next)

    title = heading.Heading(title, description)

    label1 = Gtk.Label(win.email)
    label1.get_style_context().add_class("confirm_email")

    # Done by eye
    label1.set_alignment(0.5, 0)

    label2 = Gtk.Label(check_your_email)
    label2.get_style_context().add_class("confirm_email_info")
    label2.set_alignment(0.5, 0)

    box.pack_start(title.container, False, False, 0)
    box.pack_start(label1, False, False, 5)
    box.pack_start(label2, False, False, 20)
    box.pack_start(nextB.align, False, False, 15)
    box.show_all()


def confirmation_screen():
    global win, box

    win.unpack_grid()

    img_width = 590
    img_height = 270

    img = Gtk.Image()

    filename = get_image("login", "", "profile-created", str(img_width) + 'x' + str(img_height))
    img.set_from_file(filename)

    doneB = green_button.Button("DONE")
    doneB.button.connect("button_press_event", finish)
    doneB.button.connect("key_press_event", finish)

    title = heading.Heading("Profile created!", "You’re connected and cool. Let’s check out your character.")

    container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    container.pack_start(img, False, False, 0)
    container.pack_start(title.container, False, False, 0)
    container.pack_start(doneB.align, False, False, 15)
    doneB.set_padding(0, 10, 0, 0)
    win.add(container)
    win.show_all()


def go_next(button, event):
    if not hasattr(event, 'keyval') or event.keyval == 65293:
        confirmation_screen()


def finish(button, event):
    if not hasattr(event, 'keyval') or event.keyval == 65293:
        Gtk.main_quit()

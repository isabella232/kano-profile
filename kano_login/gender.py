#!/usr/bin/env python

# gender.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# Set nickname of user

from gi.repository import Gtk

from components import heading, green_button, kano_dialog
from kano_login import birthday
import kano_profile_gui.components.constants as constants

win = None
box = None


# TODO: change dropdown to current selected
# TODO: change wizard pop up styling
def activate(_win, _box):
    global win, box

    win = _win
    box = _box

    win.clear_box()

    next_button = green_button.Button("NEXT", win)

    gender_combo = Gtk.ComboBoxText()
    gender_combo.append_text("Girl")
    gender_combo.append_text("Boy")
    gender_combo.append_text("Wizard")
    gender_combo.connect("changed", on_gender_combo_changed, next_button.button)
    gender_combo.get_style_context().add_class("gender_dropdown_list")

    title = heading.Heading("Gender", "Boy, girl or wizard?")

    valign = Gtk.Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=1)
    padding = 10
    valign.set_padding(padding, padding, 0, 0)

    next_button.button.connect("button_press_event", update, gender_combo)
    next_button.button.set_sensitive(False)

    box.pack_start(title.container, False, False, 0)
    box.pack_start(gender_combo, False, False, 30)
    box.pack_start(next_button.align, False, False, 10)

    # At this point the window has not seen the top bar or box child widget yet.
    win.show_all()


def on_gender_combo_changed(gender_combo, button):
    if gender_combo.get_active_text() == "Wizard":
        callback = gender_combo.set_active(0)
        kano_dialog.KanoDialog("You're only fooling yourself...", "I'm afraid you are not a wizard", callback, constants.media + "/images/icons/you_are_not_a_wizard.png")

    button.set_sensitive(True)


def update(arg1=None, arg2=None, gender_combo=None):
    global win, box

    active_text = gender_combo.get_active_text()
    win.gender = active_text
    win.update()
    birthday.activate(win, box)

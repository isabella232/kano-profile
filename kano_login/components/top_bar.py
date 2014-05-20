#!/usr/bin/env python

# top_bar.py
#
# Copyright (C) 2014 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU General Public License v2
#
# This controls the styling of the (pretend) top window bar.

from gi.repository import Gtk
from . import icons
import kano_login.components.cursor as cursor

TOP_BAR_HEIGHT = 44
SPACE_TAKEN = 150
HEADER_SPACE = 25


class Top_bar():
    def __init__(self, WINDOW_WIDTH, win):

        # Makes it easier to centre other widgets even if we change this
        self.height = TOP_BAR_HEIGHT

        # This is to give the correct colour of the top bar as Event Boxes are the only containers that we can colour
        # This contains everything, but can't pack directly into as is only a simple container
        self.background = Gtk.EventBox()
        self.background.set_size_request(WINDOW_WIDTH, TOP_BAR_HEIGHT)
        self.background.style = self.background.get_style_context()
        self.background.style.add_class('top_bar_container')

        # Main title of the window bar.
        self.header = Gtk.Label("Kano")
        self.header.get_style_context().add_class("header")

        self.align_header = Gtk.Alignment(xalign=1, yalign=0, xscale=0, yscale=0)
        self.align_header.add(self.header)
        # space of buttons and header text takes up about 220
        # so we have WINDOW_WIDTH - 220 of space to play with
        # move header 50 to the left
        padding_left = (WINDOW_WIDTH - SPACE_TAKEN) / 2 - HEADER_SPACE
        padding_right = (WINDOW_WIDTH - SPACE_TAKEN) / 2 + HEADER_SPACE
        self.align_header.set_padding(13, 0, padding_left, padding_right)

        # Icons of the buttons
        self.pale_prev_arrow = icons.set_from_name("pale_left_arrow")
        self.pale_next_arrow = icons.set_from_name("pale_right_arrow")
        self.dark_prev_arrow = icons.set_from_name("dark_left_arrow")
        self.dark_next_arrow = icons.set_from_name("dark_right_arrow")
        self.cross = icons.set_from_name("cross")

        # Prev Button
        self.prev_button = Gtk.Button()
        self.prev_button.set_size_request(TOP_BAR_HEIGHT, TOP_BAR_HEIGHT)
        self.prev_button.set_can_focus(False)
        self.prev_button.get_style_context().add_class("top_bar_button")
        self.prev_button.set_image(self.pale_prev_arrow)

        # Next button
        self.next_button = Gtk.Button()
        self.next_button.set_size_request(TOP_BAR_HEIGHT, TOP_BAR_HEIGHT)
        self.next_button.set_can_focus(False)
        self.next_button.get_style_context().add_class("top_bar_button")
        self.next_button.set_image(self.pale_next_arrow)

        # Close button
        self.close_button = Gtk.Button()
        self.close_button.set_image(self.cross)
        self.close_button.set_size_request(TOP_BAR_HEIGHT, TOP_BAR_HEIGHT)
        self.close_button.set_can_focus(False)
        self.close_button.get_style_context().add_class("top_bar_button")
        self.close_button.connect('button-press-event', self.close_window, win)

        # Main container holding everything
        self.container = Gtk.Grid()
        self.container.attach(self.prev_button, 0, 0, 1, 1)
        self.container.attach(self.next_button, 1, 0, 1, 1)
        self.container.attach(self.align_header, 2, 0, 1, 1)
        self.container.attach(self.close_button, 3, 0, 1, 1)
        self.container.set_size_request(WINDOW_WIDTH, 44)
        self.background.add(self.container)

        self.close_hand_handler = self.close_button.connect('enter-notify-event',
                                                            cursor.hand_cursor, win)
        self.close_arrow_handler = self.close_button.connect('leave-notify-event',
                                                             cursor.arrow_cursor, win)
        self.next_hand_handler = self.next_button.connect('enter-notify-event',
                                                          cursor.hand_cursor, win)
        self.next_arrow_handler = self.next_button.connect('leave-notify-event',
                                                           cursor.arrow_cursor, win)
        self.prev_hand_handler = self.prev_button.connect('enter-notify-event',
                                                          cursor.hand_cursor, win)
        self.prev_arrow_handler = self.prev_button.connect('leave-notify-event',
                                                           cursor.arrow_cursor, win)
        # On start, disable the prev and next buttons
        self.disable_prev()
        self.disable_next()

    def disable_prev(self):
        self.prev_button.set_sensitive(False)
        self.prev_button.set_image(self.pale_prev_arrow)

    def enable_prev(self):
        self.prev_button.set_sensitive(True)
        self.prev_button.set_image(self.dark_prev_arrow)

    def disable_next(self):
        self.next_button.set_sensitive(False)
        self.next_button.set_image(self.pale_next_arrow)

    def enable_next(self):
        self.next_button.set_sensitive(True)
        self.next_button.set_image(self.dark_next_arrow)

    def set_prev_callback(self, callback):
        self.prev_button.connect("button_press_event", callback)

    def set_next_callback(self, callback):
        self.next_button.connect("button_press_event", callback)

    def disconnect_handlers(self):
        self.close_button.disconnect(self.close_hand_handler)
        self.close_button.disconnect(self.close_arrow_handler)
        self.next_button.disconnect(self.next_hand_handler)
        self.next_button.disconnect(self.next_arrow_handler)
        self.prev_button.disconnect(self.prev_hand_handler)
        self.prev_button.disconnect(self.prev_arrow_handler)

    def close_window(self, event, button, win):
        self.disconnect_handlers()
        cursor.arrow_cursor(None, None, win)
        Gtk.main_quit()


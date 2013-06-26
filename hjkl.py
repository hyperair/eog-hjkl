# -*- coding: utf-8 -*-
# Copyright 2013, Chow Loong Jin <hyperair@debian.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import GObject, Eog, Gdk


class HJklPlugin(GObject.Object, Eog.WindowActivatable):
    window = GObject.property(type=Eog.Window)
    evtcookie = None

    directions_map = {
        'h': Gdk.KEY_Left,
        'j': Gdk.KEY_Down,
        'k': Gdk.KEY_Up,
        'l': Gdk.KEY_Right
    }

    @property
    def view(self):
        return self.window.get_view()

    def handle_scroll(self, widget, event):
        assert widget is self.view

        if event.state & Gdk.ModifierType.MODIFIER_MASK != 0:
            return False

        try:
            keyval = self.directions_map[chr(event.keyval).lower()]
        except (ValueError, KeyError):
            return False

        newevent = event.copy()
        newevent.key.keyval = keyval
        newevent.key.send_event = True
        newevent.key.state = (newevent.state & Gdk.ModifierType.MODIFIER_MASK |
                              Gdk.ModifierType.MOD1_MASK)
        newevent.put()

        return True

    def do_activate(self):
        self.evtcookie = self.view.connect('key-press-event',
                                           self.handle_scroll)
        print self.evtcookie

    def do_deactivate(self):
        self.view.disconnect(self.evtcookie)
        self.evtcookie = None

# window.py
#
# Copyright 2022 Daniel Svitan
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

from gi.repository import Gtk
import time, threading


@Gtk.Template(resource_path='/com/streamer272/PyQuiz/window.ui')
class PyquizWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'PyquizWindow'

    age_box = Gtk.Template.Child()
    age_entry = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("Iiniting!!!!")


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'PyQuiz'
        self.props.version = '0.1.0'
        self.props.authors = ['Daniel Svitan']
        self.props.copyright = '2022 Daniel Svitan'
        self.props.logo_icon_name = 'com.streamer272.PyQuiz'
        self.props.modal = True
        self.set_transient_for(parent)


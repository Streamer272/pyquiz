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
from .question import questions


@Gtk.Template(resource_path='/com/streamer272/PyQuiz/window.ui')
class PyquizWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'PyquizWindow'

    ok_button = Gtk.Template.Child()
    current_question = 0

    q_label = Gtk.Template.Child()
    q_entry = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.q_label.set_text(questions[self.current_question].question)
        self.ok_button.connect("clicked", self.on_ok_clicked)

    def on_ok_clicked(self, _):
        q_entry_buffer = self.q_entry.get_buffer()
        questions[self.current_question].answer = q_entry_buffer.get_text()
        q_entry_buffer.set_text("", -1)
        self.q_entry.grab_focus_without_selecting()

        if (self.current_question + 1 >= len(questions)):
            return self.finish()
        self.current_question += 1
        self.q_label.set_text(questions[self.current_question].question)

    def finish(self):
        self.q_label.set_text("Thank you for completing the survey!")
        self.ok_button.hide()
        self.q_entry.hide()


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


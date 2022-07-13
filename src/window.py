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

from gi.repository import Gtk, Gio, Gdk
from .question import StrQuestion, IntQuestion, YNQuestion, questions


@Gtk.Template(resource_path='/com/streamer272/PyQuiz/window.ui')
class PyquizWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'PyquizWindow'

    old_input_int_value: str = "0"
    current_question = 0
    correct_answers = 0
    finished = False

    ok_button: Gtk.Button = Gtk.Template.Child()
    q_label: Gtk.Label = Gtk.Template.Child()

    q_yes_no_button: Gtk.CheckButton = Gtk.Template.Child()
    q_input_str_entry: Gtk.Entry = Gtk.Template.Child()
    q_input_int_entry: Gtk.Entry = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        action = Gio.SimpleAction.new("next", None)
        print("enter is", Gtk.accelerator_name(65293, Gdk.ModifierType.CONTROL_MASK))
        action.connect("activate", self.on_ok_clicked)
        self.add_action(action)
        kwargs.get("application").set_accels_for_action("win.next", ["<primary>Return"])

        self.ok_button.connect("clicked", self.on_ok_clicked)
        self.q_input_str_entry.connect("activate", self.on_ok_clicked)
        self.q_input_int_entry.connect("activate", self.on_ok_clicked)
        self.q_input_int_entry.connect("changed", self.on_input_int_change)
        self.q_input_int_entry.set_input_purpose(Gtk.InputPurpose.NUMBER)

        self.render_question()

    def on_ok_clicked(self, *_args, **_kwargs):
        if self.finished:
            self.destroy()

        self.check_question_answer()

        if (self.current_question + 1 >= len(questions)):
            return self.finish()
        self.current_question += 1
        self.render_question()

    def on_input_int_change(self, _):
        q_entry_buffer = self.q_input_int_entry.get_buffer()
        value = q_entry_buffer.get_text()
        try:
            float(value)
            self.old_input_int_value = value
        except ValueError:
            q_entry_buffer.set_text(self.old_input_int_value, -1)

    def render_question(self):
        question = questions[self.current_question]
        self.q_label.set_text(question.question)

        if isinstance(question, YNQuestion):
            self.q_yes_no_button.show()
            self.q_input_str_entry.hide()
            self.q_input_int_entry.hide()
        elif isinstance(question, StrQuestion):
            self.q_yes_no_button.hide()
            self.q_input_str_entry.show()
            self.q_input_int_entry.hide()
            self.q_input_str_entry.grab_focus_without_selecting()
        elif isinstance(question, IntQuestion):
            self.q_yes_no_button.hide()
            self.q_input_str_entry.hide()
            self.q_input_int_entry.show()
            self.q_input_int_entry.grab_focus_without_selecting()

    def check_question_answer(self):
        question = questions[self.current_question]

        if isinstance(question, YNQuestion):
            if question.check_answer(self.q_yes_no_button.get_active()):
                self.correct_answers += 1
            self.q_yes_no_button.set_active(False)

        elif isinstance(question, StrQuestion):
            q_entry_buffer = self.q_input_str_entry.get_buffer()
            if question.check_answer(q_entry_buffer.get_text()):
                self.correct_answers += 1
            q_entry_buffer.set_text("", -1)

        elif isinstance(question, IntQuestion):
            self.old_input_int_value = "0"
            q_entry_buffer = self.q_input_int_entry.get_buffer()

            value = 0
            try:
                value = int(q_entry_buffer.get_text())
            except ValueError:
                pass

            if question.check_answer(value):
                self.correct_answers += 1
            q_entry_buffer.set_text("", -1)

    def finish(self):
        self.finished = True

        self.q_label.set_text(f"You got {self.correct_answers} {'answer' if self.correct_answers == 1 else 'answers'} correctly")
        self.ok_button.set_label("Quit")

        self.q_yes_no_button.hide()
        self.q_input_str_entry.hide()
        self.q_input_int_entry.hide()


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


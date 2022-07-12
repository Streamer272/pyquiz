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
from .question import QuestionType, questions


@Gtk.Template(resource_path='/com/streamer272/PyQuiz/window.ui')
class PyquizWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'PyquizWindow'

    current_question = 0
    correct_answers = 0

    ok_button: Gtk.Button = Gtk.Template.Child()
    q_label: Gtk.Label = Gtk.Template.Child()

    q_yes_no_button: Gtk.CheckButton = Gtk.Template.Child()
    q_input_str_entry: Gtk.Entry = Gtk.Template.Child()
    q_input_int_entry: Gtk.Entry = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.q_input_int_entry.set_input_purpose(Gtk.InputPurpose.NUMBER)
        self.ok_button.connect("clicked", self.on_ok_clicked)
        self.render_question()

    def on_ok_clicked(self, _):
        self.check_question_answer()

        if (self.current_question + 1 >= len(questions)):
            return self.finish()
        self.current_question += 1
        self.render_question()

    def render_question(self):
        question = questions[self.current_question]
        self.q_label.set_text(question.question)

        if question.question_type == QuestionType.yes_no:
            self.q_yes_no_button.show()
            self.q_input_str_entry.hide()
            self.q_input_int_entry.hide()
            self.q_yes_no_button.grab_focus_without_selecting()
        elif question.question_type == QuestionType.input_str:
            self.q_yes_no_button.hide()
            self.q_input_str_entry.show()
            self.q_input_int_entry.hide()
            self.q_input_str_entry.grab_focus_without_selecting()
        elif question.question_type == QuestionType.input_int:
            self.q_yes_no_button.hide()
            self.q_input_str_entry.hide()
            self.q_input_int_entry.show()
            self.q_input_int_entry.grab_focus_without_selecting()

    def check_question_answer(self):
        question = questions[self.current_question]

        if question.question_type == QuestionType.yes_no:
            question = questions[self.current_question]
            question.answer = "Yes" if self.q_yes_no_button.get_active() else "No"
            self.q_yes_no_button.set_active(False)

            if question.answer in question.correct_answers:
                question.answered_correctly = True
                self.correct_answers += 1

        elif question.question_type == QuestionType.input_str:
            question = questions[self.current_question]
            q_entry_buffer = self.q_input_str_entry.get_buffer()
            question.answer = q_entry_buffer.get_text()
            q_entry_buffer.set_text("", -1)

            if question.answer.lower() in [str(i).lower() for i in question.correct_answers]:
                question.answered_correctly = True
                self.correct_answers += 1

        elif question.question_type == QuestionType.input_int:
            question = questions[self.current_question]
            q_entry_buffer = self.q_input_int_entry.get_buffer()
            question.answer = str(q_entry_buffer.get_text())
            q_entry_buffer.set_text("", -1)

            if int(question.answer) in question.correct_answers:
                question.answered_correctly = True
                self.correct_answers += 1

    def finish(self):
        self.q_label.set_text(f"You got {self.correct_answers} {'answer' if self.correct_answers == 1 else 'answers'} correctly")
        self.ok_button.hide()

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


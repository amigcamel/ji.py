"""Main app settings."""
# -*- coding: utf-8 -*-
from itertools import chain
from tkinter import (
    Frame,
    Tk,
    BOTH,
    Button,
    Menu,
    Label,
    Text,
    messagebox,
    END,
    N, S, W, E,
    StringVar,
    OptionMenu,
)

from . import quiz


class Window(Frame):  # noqa: D101

    def __init__(self, master=None):  # noqa: D107
        Frame.__init__(self, master)
        self.master = master

        self.quizzes = list(chain.from_iterable(quiz.QUIZ_DICT.values()))
        self.total_quiz_num = len(self.quizzes)
        self.quiz = self.quizzes[0]()
        self.init_window()

        # Key bindings
        self.bind('<M1-E>', self.quit)

    def gen_quiz(self):
        """Generate quiz."""
        self.quiz = self.quizzes[0]()
        self.snippet.delete('1.0', END)
        self.snippet.insert(END, self.quiz.init_text)
        self.title['text'] = self.chanllenge_status
        self.question['text'] = self.quiz.description

    @property
    def chanllenge_status(self):
        """Return chanllenge status."""
        left = self.total_quiz_num - len(self.quizzes)
        return f'已完成練習題數: {left}/{self.total_quiz_num}'

    def init_window(self):
        """Initalize window."""
        self.master.title('吉.py')
        self.pack(fill=BOTH, expand=1, padx=10, pady=10)

        # menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu, tearoff=0)
        file.add_command(label='離開', command=self.quit)
        menu.add_cascade(label='檔案', menu=file)

        edit = Menu(menu, tearoff=0)
        edit.add_command(label='這是什麼', command=self.about)
        menu.add_cascade(label='關於', menu=edit)

        quiz_type_label = Label(self, text='題目類型', font=('Helvetica', 14))
        quiz_type_label.grid(row=0, column=0, sticky=W)

        option_list = ['全部'] + list(quiz.QUIZ_DICT.keys())
        self.drop_var = StringVar()
        self.drop_var.set(option_list[0])  # default choice
        self.drop_menu = OptionMenu(
            self, self.drop_var, *option_list, command=self.select_quiz_type)
        self.drop_menu.configure(width=15)
        self.drop_menu.grid(row=0, column=1, sticky=W)

        self.question = Label(
            self, text=self.quiz.description, font=('Helvetica', 14, 'bold'))
        self.question.grid(
            row=2, column=0, columnspan=4, sticky=N + W, pady=10)

        self.snippet = Text(
            self,
            highlightbackground='#D1D0CE',
            font=('Courier New', 14),
        )
        self.snippet.grid(row=1, column=0, columnspan=4, sticky=N + S + W + E)

        self.submit_button = Button(self, text='送出', command=self.submit)
        self.submit_button.grid(row=3, column=0, columnspan=4, sticky=W + E)

        self.title = Label(
            self, text=self.chanllenge_status, font=('Helvetica', 10))
        self.title.grid(row=4, column=0, sticky=W)

        self.skip_button = Button(
            self, text='跳過', command=self.skip, width=15)
        self.skip_button.grid(row=4, column=1)

        self.hint_button = Button(
            self, text='提示', command=self.hint, width=15)
        self.hint_button.grid(row=4, column=2)

        self.reset_button = Button(
            self, text='重設', command=self.reset, width=15)
        self.reset_button.grid(row=4, column=3)

        self.snippet.insert(END, self.quiz.init_text)

    def select_quiz_type(self, value):
        """Select quiz type."""
        if value == '全部':
            self.quizzes = list(chain.from_iterable(quiz.QUIZ_DICT.values()))
        else:
            self.quizzes = quiz.QUIZ_DICT[value]
        self.total_quiz_num = len(self.quizzes)
        self.gen_quiz()

    def submit(self):
        """Submite snippet."""
        snippet = self.snippet.get('1.0', END)
        status, message = self.quiz(snippet)
        if status == -2:
            pass
        elif status == -1:
            messagebox.showerror('語法錯誤', message)
        elif status == 0:
            messagebox.showwarning('', '答案或方法錯誤')
        elif status == 1:
            messagebox.showinfo('水喔', '好棒棒!')
            if len(self.quizzes) == 1:
                self.title['text'] = '全部練習完畢囉～'
            else:
                del self.quizzes[0]
                self.gen_quiz()

    def skip(self):
        """Skip to next quiz."""
        quiz = self.quizzes.pop(0)
        self.quizzes.insert(len(self.quizzes), quiz)
        self.gen_quiz()

    def reset(self):
        """Reset initial text."""
        ans = messagebox.askquestion(
            '確定重設?', '當前編輯將被清空', icon='warning')
        if ans == 'yes':
            self.gen_quiz()

    def hint(self):
        """Provide hint."""
        messagebox.showinfo('提示', self.quiz.hint or '沒有提示')

    def quit(self):
        """Quit app."""
        exit()

    def about(self):
        """Show about info."""
        messagebox.showinfo('阿吉關心您', '只要有心，人人都是py神')


def run_app():
    """Run this app."""
    root = Tk()

    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()

    position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
    position_down = int(root.winfo_screenheight() / 2 - window_height / 2)

    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(position_right, position_down))
    root.minsize(600, 500)
    Window(root)
    root.mainloop()


if __name__ == '__main__':
    run_app()

# -*- coding: utf-8 -*-
import inspect
import random

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
)

from . import quiz


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        self.quizzes = self.collect_quizzes()
        self.total_quiz_num = len(self.quizzes)
        self.quiz = self.quizzes[0]()
        self.init_window()

        # Key bindings
        self.bind('<M1-E>', self.quit)

    def gen_quiz(self):
        if not self.quizzes:
            return f'已完成練習題數: {left}/{self.total_quiz_num}'
            return
        self.quiz = self.quizzes[0]()
        self.snippet.delete('1.0', END)
        self.snippet.insert(END, self.quiz.init_text)
        self.title['text'] = self.chanllenge_status

    def collect_quizzes(self):
        quizzes = []
        for name, obj in inspect.getmembers(quiz):
            if inspect.isclass(obj):
                mro = obj.mro()
                if mro[1] == quiz.Quiz:
                    quizzes.append(obj)
        random.shuffle(quizzes)
        return quizzes

    @property
    def chanllenge_status(self):
        left = self.total_quiz_num - len(self.quizzes)
        return f'已完成練習題數: {left}/{self.total_quiz_num}'

    def init_window(self):
        self.master.title('吉.py')
        self.pack(fill=BOTH, expand=1, padx=10, pady=10)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label='Exit', command=self.quit)
        menu.add_cascade(label='File', menu=file)

        edit = Menu(menu)
        edit.add_command(label='這是什麼', command=self.about)
        menu.add_cascade(label='關於', menu=edit)

        self.title = Label(self, text=self.chanllenge_status)
        self.title.grid(row=0, column=1, columnspan=2, sticky=N+E)

        question = Label(self, text=self.quiz.description)
        question.grid(row=1, column=0, sticky=N)

        self.snippet = Text(self, 
                            highlightbackground='#D1D0CE')
        self.snippet.grid(row=2, column=0, columnspan=2, sticky=N+S+W+E)

        self.submit_button = Button(
            self, text='送出', command=self.submit, width=40)
        self.submit_button.grid(row=3, column=0, rowspan=2)

        self.hint_button = Button(
            self, text='提示', command=self.hint, width=10)
        self.hint_button.grid(row=3, column=1)

        self.reset_button = Button(
            self, text='重設', command=self.reset, width=10)
        self.reset_button.grid(row=4, column=1)

        self.snippet.insert(END, self.quiz.init_text)

    def submit(self):
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

    def reset(self):
        ans = messagebox.askquestion(
            '確定重設?', '當前編輯將被清空', icon='warning')
        if ans == 'yes':
            self.gen_quiz()

    def hint(self):
        ans = messagebox.askquestion(
            '真的不再想一下嗎?', '確定要提示?', icon='warning')
        if ans == 'yes':
            messagebox.showinfo('提示', self.quiz.hint)

    def quit(self):
        exit()

    def about(self):
        messagebox.showinfo('阿吉關心您', '只要有心，人人都是py神')


def run_app():
    root = Tk()

    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()

    position_right = int(root.winfo_screenwidth()/2 - window_width/2)
    position_down = int(root.winfo_screenheight()/2 - window_height/2)

    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(position_right, position_down))
    root.minsize(600, 500)
    app = Window(root)
    root.mainloop()


if __name__ == '__main__':
    run_app()

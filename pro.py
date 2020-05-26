import os
import re
from collections import Counter
from tkinter import *

WORDS = {}
with open('unigrams.txt', encoding="utf-8") as f:
    for line in f:
        key, value = line.split()
        value = int(value)
        WORDS[key] = int(value)


def P(word):
    N = sum(WORDS.values())
    P = WORDS[key] / N
    return P


def edits1(word):
    letters = 'йцукенгшщзхъфывапролджэячсмитьбю'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]
    edits1 = set(deletes + transposes + replaces + inserts)
    return edits1


def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def known(words):
    return set(w for w in words if w in WORDS)


def candidates(word):
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])


def correction(word):
    return max(candidates(word), key=P)


def print_answer(word):
    global window1
    answer = Label(window1, text='Слово пишется так                    ', font=("Arial Bold", 11))
    answer.grid(column=0, row=3)
    word_out = Text(window1, width=20, height=1)
    word_out.grid(column=1, row=3)
    word_out.insert(1.0, word)


def main():
    word = ss.get()
    right_answer = correction(word)
    print_answer(right_answer)


def clicked1():
    global window1
    window1 = Toplevel(window)
    window1.overrideredirect = True
    window1.geometry('600x200')
    z = Entry(window1, width=20, textvariable=ss)
    lbl = Label(window1, text='Введите слово для проверки орфографии', font=("Arial Bold", 11))
    lbl.grid(column=0, row=0)
    z.grid(column=1, row=0)
    z.focus()
    btn3 = Button(window1, text="ВВОД", command=main).place(x=410, y=0, width = 65, height = 24)
    window1.mainloop()


def text(filename, coding):
    with open(filename, 'r', encoding=coding) as file:
        text = file.read()
    text = text.lower()
    words = re.findall(r'[а-яёА-ЯЁ]+\-?[а-яёА-ЯЁ]+', text)
    return words


def spellcorrector_of_text():
    file = open('correction.txt', 'w+')
    file.close()
    file = name_of_file.get()
    code = coding_of_file.get()
    words = text(file, code)
    for w in words:
        right_answer = correction(w)
        if not right_answer == w:
            with open('correction.txt', 'a', encoding='utf-8') as f:
                f.write('Возможно, вы имели в виду не '+ str(w) + ', а '+ str(right_answer).upper() + '.'+'\n')
    global window2
    if not os.stat("correction.txt").st_size == 0:
        answer_text = Label(window2, text='Вы допустили опечатки:', font=("Arial Bold", 11))
        answer_text.grid(column=0, row=2)
        text_out = Text(window2, wrap=WORD)
        text_out.place(x=50, y=70, width=400, height=100)
        yscroll = Scrollbar(window2, command=text_out.yview)
        yscroll.place(x=450, y=70, height=100)
        text_out.config(yscrollcommand=yscroll.set)
        with open('correction.txt', 'r', encoding = 'utf-8') as corr:
            text_out.insert(0.0, corr.read())
    else:
        answer_text = Label(window2, text='В вашем тексте нет опечаток!', font=("Arial Bold", 11))
        answer_text.grid(column=0, row=2)

def clicked2():
    global window2
    window2 = Toplevel(window)
    window2.overrideredirect = True
    window2.geometry('600x200')
    lbl1 = Label(window2, text='Введите название вашего файла с расширением', font=("Arial Bold", 11))
    lbl1.grid(column=0, row=0)
    a = Entry(window2, width=10, textvariable=name_of_file)
    a.grid(column=1, row=0)
    lbl2 = Label(window2, text='Введите кодировку вашего файла', font=("Arial Bold", 11))
    lbl2.grid(column=0, row=1)
    b = Entry(window2, width=10, textvariable=coding_of_file)
    b.grid(column=1, row=1)
    btn4 = Button(window2, text="ВВОД", command=spellcorrector_of_text).place(x=410, y=10, width=70)
    window.mainloop()


window = Tk()
window1 = 1
window2 = 2
window.title("Добро пожаловать в приложение PythonGrammer")
window.geometry('750x200')
ss = StringVar()
ss.set("")
name_of_file = StringVar()
name_of_file.set("")
coding_of_file = StringVar()
coding_of_file.set("")
lbl = Label(window,
            text="Здравствуйте, уважаемый пользователь! \n Сейчас вы используете программу по поиску орфографических ошибок в словах на русском языке.\n Где бы вы хотели искать ошибки? Выберите нужный вариант.",
            font=("Arial Bold", 12))
lbl.grid(column=0, row=0)
btn1 = Button(window, text="В словах", command=clicked1).place(x=200, y=100, width=100)
btn2 = Button(window, text="В тексте", command=clicked2).place(x=400, y=100, width=100)
window.mainloop()

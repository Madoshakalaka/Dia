import os
from tkinter import *
import queue

with open(os.devnull, 'w') as f:
	oldstdout = sys.stdout
	sys.stdout = f

	import pygame

	sys.stdout = oldstdout

pygame.mixer.init()
pygame.mixer.music.load('assets/click.wav')

master = Tk()
master.title("人工智障")
master.geometry("1400x1000")
master.grid_columnconfigure(0, weight=1)
master.grid_rowconfigure(0, weight=1)

frame = Frame(master)
# s = Scrollbar(frame, orient = VERTICAL)

counter = 0
current = 0
e = Entry(master, font=('Verdana', 30, 'bold'))
e.grid(row=1, column=0, sticky=W + E)
b = Button(master, text="clear", width=5, height=5)

b.grid(row=1, column=1)
s = Scale(master)
s.grid(row=0, column=1, sticky=N + S)


def clear(*args):
	global counter
	global current

	del args
	pygame.mixer.music.play(0)
	frame.place(rely=0)
	counter = 0
	current = 0
	s.config(to=0)
	for child in frame.winfo_children():
		child.destroy()


b.bind("<Button-1>", clear)


def scroll(*args):
	global current
	# ('scroll', '1', 'pages')
	# ('scroll', '-1', 'units')
	# ('scroll', '1', 'units')
	# ('moveto', '0.0')
	# print(args[0])
	if args[0] == '0':
		frame.place(rely=0)
	else:
		frame.place(rely=-0.132 * int(args[0]))
	current = int(args[0])
	s.set(current)


def scrollUporDown(args):
	global current

	d = args.delta

	if d > 0:
		if current > 0:
			current -= 1
			scroll(current)
	else:
		if current < counter - 7:
			current += 1
			scroll(current)


def addText(side, text):
	global counter
	pygame.mixer.music.play(0)
	t = Text(frame, height=8)
	t.tag_configure('big', font=('Verdana', 30, 'bold'), justify=side)

	t.insert(END, text, 'big')
	t.config(state="disabled")
	t.grid(row=counter, column=0, sticky=W + E)
	counter += 1

	s.config(to=max(counter - 7, 0))
	s.set(max(counter - 7, 0))


def postAsSur(text):
	pygame.mixer.music.play(0)
	addText(RIGHT, text)


def submit():
	text = e.get()
	addText(LEFT, text)
	e.delete(0, END)
	transferer.put(text)


def initialize():
	mainloop()


def yieldAll():
	results = []
	while not transferer.empty():
		try:
			results.append(transferer.get(block=False))
		except queue.Empty:
			break

	return results


transferer = queue.Queue()

e.bind('<Return>', lambda x: submit())

frame.grid(row=0, column=0, sticky=W + E)
frame.grid_columnconfigure(0, weight=1)
frame.place(rely=0)

# addText(LEFT, "123123")
# addText(RIGHT, "345345345")
# addText(LEFT, "你妈死了")
master.bind("<MouseWheel>", scrollUporDown)
s.config(command=scroll, width=30)

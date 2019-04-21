import os
from tkinter import *
import queue
from tkinter.font import nametofont

with open(os.devnull, 'w') as f:
	oldstdout = sys.stdout
	sys.stdout = f

	import pygame

	sys.stdout = oldstdout

pygame.mixer.init()


relyDict = dict()
sound = pygame.mixer.Sound('assets/click.wav')

master = Tk()
master.title("人工智障")

# for 2k screen, width, height
geom = 1400, 1000
master.geometry("%dx%d" % geom)

master.grid_columnconfigure(0, minsize=1400*14//15)
master.grid_rowconfigure(0, minsize=1000*14//15)

master.grid_columnconfigure(1, minsize=1400//15)
master.grid_rowconfigure(1, minsize=1000//15)

frame = Frame(master, width=geom[0] * 14 // 15)
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
	sound.play()
	frame.place(rely=0)
	counter = 0
	current = 0
	s.config(to=0)
	for child in frame.winfo_children():
		child.destroy()


b.bind("<Button-1>", clear)


def scroll(*args):
	# print(-(frame.winfo_reqheight()-geom[1]*14/15) / geom[1])
	# print(-14/(6*15) * int(args[0]))
	global current
	# ('scroll', '1', 'pages')
	# ('scroll', '-1', 'units')
	# ('scroll', '1', 'units')
	# ('moveto', '0.0')
	# print(args[0])
	if args[0] == '0':
		frame.place(rely=0)
	else:

		frame.place(rely=relyDict[int(args[0])])
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
	sound.play()

	# print(font)
	# print(frame.winfo_reqheight())
	# print(geom[1] * 14 / 15 // 6)
	entryFrame = Frame(frame, width=geom[0] * 14 // 15, height=geom[1] * 14 / 15 // 6, bg='red')
	entryFrame.grid(row=counter, column=0, sticky=W+E+N+S)
	entryFrame.grid_propagate(False)

	t = Entry(entryFrame, textvariable=StringVar(), font='Verdana 30 bold', justify=side)

	# t.configure(font=('Verdana', 30, 'bold'), justify=side)

	# font = nametofont(t.cget("font"))
	# print(font.measure("0"))
	# print(t.winfo_width())
	# print(t.winfo_reqwidth())

	t.insert(END, text)

	t.config(state="disabled")
	# print(counter * geom[1] * 14 / 15 // 6)
	t.place(x=0, y=0, width=geom[0] * 14 // 15, height=geom[1] * 14 / 15 // 6)

	frame.update()

	print(counter)
	print(-(frame.winfo_reqheight()-geom[1]*14/15) / geom[1])
	if counter >= 6:
		relyDict[counter-5] = -(frame.winfo_reqheight()-geom[1]*14/15) / geom[1]
		# print(relyDict)

	# print(t.bbox(END))
	counter += 1

	s.config(to=max(counter - 6, 0))
	s.set(max(counter - 6, 0))


def postAsSur(text):
	sound.play()
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

# frame.grid_columnconfigure(0, weight=1)
frame.place(rely=0)

# addText(LEFT, "123123")
# addText(RIGHT, "345345345")
# addText(LEFT, "你妈死了")
master.bind("<MouseWheel>", scrollUporDown)
# s.config(command=scroll, width=geom[0] // 10)
s.config(command=scroll, width=geom[0] // 15)

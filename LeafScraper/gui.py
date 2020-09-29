import tkinter as tk

HEIGHT = 700
WIDTH = 800

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg='#80c1ff')
frame.place(relx=.25, rely=.25, relwidth=.5, relheight=.5)

button = tk.Button(frame, text = "test button")
button.pack(side='left')

label = tk.Label(frame, text="this is a label", bg='yellow')
label.pack()

entry = tk.Entry(frame, bg='green')
entry.pack(side='right')

root.mainloop()
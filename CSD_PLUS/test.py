import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from main import CSD_PLUS
from mcts import MCTS
from PIL import ImageTk,Image

def _about_me():
    messagebox.showinfo('About', 'CSD-PLUS Framework')


def readFile(filename):
    str = open(filename, 'r').read()
    return str


def BA_ALGO():
    solver = CSD_PLUS(W=W_String.get(),
                      Z_prime=Z_String.get(),
                      sens_patterns=['cced', 'ccbc'],
                      k=k.get(),
                      delta=deleter.get(),
                      C=C_Value.get(),
                      multiplier=multiplier.get(),
                      tau=tau.get(),
                      maxHorizon=horizon.get())
    ghosts, distortion = solver.meaure_performance(Z_String.get())
    d_before.set(distortion)
    ghosts_before.set(ghosts)
    ans, shortest = solver.BA_ALGO(theta=100)
    ghosts, distortion = solver.meaure_performance(ans[-1])
    d_after.set(distortion)
    ghosts_after.set(ghosts)
    master.update()


def MCTS_ALGO():
    solver = CSD_PLUS(W=W_String.get(),
                      Z_prime=Z_String.get(),
                      sens_patterns=['cced', 'ccbc'],
                      k=k.get(),
                      delta=deleter.get(),
                      C=C_Value.get(),
                      multiplier=multiplier.get(),
                      tau=tau.get(),
                      maxHorizon=horizon.get())
    plan = solver.MCST_ALGO(solver.tasks)
    ghosts, distortion = solver.meaure_performance(Z_String.get())
    d_before.set(distortion)
    ghosts_before.set(ghosts)
    ghosts, distortion = solver.meaure_performance(plan[-1][0])
    d_after.set(distortion)
    ghosts_after.set(ghosts)
    master.update()


# GUI-INTERFACE
master = Tk()
master.title("String Sanitization - Final Year Project")

W_String = tk.StringVar()
Z_String = tk.StringVar()
d_before = tk.IntVar()
d_after = tk.IntVar()
ghosts_before = tk.IntVar()
ghosts_after = tk.IntVar()
k = tk.IntVar()
tau = tk.IntVar()

# menu = Menu(master)
# master.config(menu=menu)
# filemenu = Menu(menu)

menubar = Menu(master)

master.config(menu=menubar)
master.geometry("800x800")

canvas = Canvas(master, width = 300, height = 300)
canvas.pack()
img = ImageTk.PhotoImage(Image.open("logo.png"))
canvas.create_image(20, 20, anchor=NW, image=img)


# img= ImageTk.PhotoImage(file='logo.png')
# Label(master,image=img).pack()
# master = Frame(master)
# master.grid(row=0, column=0, sticky=W)

passw_label = tk.Label(master, text='Original String', font=('calibre', 15, 'bold')).grid(row=0, column=0)
# creating a entry for password
passw_entry = tk.Entry(master, textvariable=W_String, font=('calibre', 15, 'normal')).grid(row=0, column=1)
passw_label = tk.Label(master, text='Sanitized String', font=('calibre', 15, 'bold')).grid(row=0, column=2)
# creating a entry for password
passw_entry = tk.Entry(master, textvariable=Z_String, font=('calibre', 15, 'normal')).grid(row=0, column=3)

tk.Button(text="Running with BA!", fg="black", command=BA_ALGO, bg="gray93").grid(row=1, column=0, sticky=W)
tk.Button(text="Running with MCTS!", fg="black", command=MCTS_ALGO, bg="gray93").grid(row=1, column=1, sticky=W)

tk.Label(text="Number of Deletes:", fg="black", bg="gray93").grid(row=3, column=0, sticky=W)
deleter = Scale(from_=0, to=10, resolution=1, orient=HORIZONTAL, bg="gray93")
deleter.grid(row=3, column=1, sticky=W)
deleter.set(5)

tk.Label(text="UTC_C Parameter:", fg="black", bg="gray93").grid(row=4, column=0, sticky=W)
C_Value = Scale(from_=0, to=300, resolution=10, orient=HORIZONTAL, bg="gray93")
C_Value.grid(row=4, column=1, sticky=W)
C_Value.set(150)
tk.Label(text="Pruning Parameter:", fg="black", bg="gray93").grid(row=5, column=0, sticky=W)
horizon = Scale(from_=0, to=10, resolution=1, orient=HORIZONTAL, bg="gray93")
horizon.grid(row=5, column=1, sticky=W)
horizon.set(5)

tk.Label(text="Length of Pattern k:", fg="black", bg="gray93").grid(row=6, column=0, sticky=W)
k = Scale(from_=0, to=10, resolution=1, orient=HORIZONTAL, bg="gray93")
k.grid(row=6, column=1, sticky=W)
k.set(5)

tk.Label(text="Number Of Deletes", fg="black", bg="gray93").grid(row=3, column=0, sticky=W)
deleter = Scale(from_=0, to=10, resolution=1, orient=HORIZONTAL, bg="gray93")
deleter.grid(row=3, column=1, sticky=W)
deleter.set(5)

tk.Label(text="Tau:", fg="black", bg="gray93").grid(row=7, column=0, sticky=W)
tau = Scale(from_=0, to=20, resolution=1, orient=HORIZONTAL, bg="gray93")
tau.grid(row=7, column=1, sticky=W)
tau.set(10)

tk.Label(text="Multiplier:", fg="black", bg="gray93").grid(row=8, column=0, sticky=W)
multiplier = Scale(from_=0, to=1, resolution=1, orient=HORIZONTAL, bg="gray93")
multiplier.grid(row=8, column=1, sticky=W)
multiplier.set(1)

tk.Label(text="Max-Sims/decision", fg="black", bg="gray93").grid(row=3, column=2, sticky=W)
max_sims = Scale(from_=0, to=200, resolution=1, orient=HORIZONTAL, bg="gray93")
max_sims.grid(row=3, column=3, sticky=W)
max_sims.set(100)

tk.Label(text="Distortion Before:", bg="gray93").grid(row=4, column=2, sticky=W)
d1 = tk.Label(textvariable=d_before, bg="gray93")
d1.grid(row=4, column=3, sticky=W)

tk.Label(text="Distortion After:", bg="gray93").grid(row=5, column=2, sticky=W)
d2 = tk.Label(textvariable=d_after, bg="gray93")
d2.grid(row=5, column=3, sticky=W)

tk.Label(text="Ghosts/Losts Before:", bg="gray93").grid(row=6, column=2, sticky=W)
g1 = tk.Label(textvariable=ghosts_before, bg="gray93")
g1.grid(row=6, column=3, sticky=W)

tk.Label(text="Ghosts/Losts After:", bg="gray93").grid(row=7, column=2, sticky=W)
g2 = tk.Label(textvariable=ghosts_before, bg="gray93")
g2.grid(row=7, column=3, sticky=W)

# master.columnconfigure(0, weight=1)
# master.rowconfigure(1, weight=1)
mainloop()

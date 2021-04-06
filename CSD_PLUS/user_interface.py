import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from model import solver
from PIL import ImageTk, Image
from matplotlib.figure import Figure
import DataProcessing

global filename
filename = ''


def _about_me():
    messagebox.showinfo('About', 'CSD-PLUS Framework')


def _upload_action(event=None):
    global filename
    filename = filedialog.askopenfilename()
    print('Selected:', filename)


def create_solver_instance():
    return solver(w=W_String.get(),
                  z=Z_String.get(),
                  sensitive_patterns=DataProcessing.readMultiLineFile(filename),
                  k=k.get(),
                  delta=deleter.get(),
                  c=C_Value.get(),
                  omega=multiplier.get(),
                  tau=tau.get(),
                  tolerance=tolerance.get(),
                  max_simulations=max_sims.get())


def _run_GD():
    run = create_solver_instance()
    ghosts1, distortion1 = run._get_distortion(Z_String.get())
    d_before.set(distortion1)
    ghosts_before.set(ghosts1)
    ans = run._GD_ALGO()
    ghosts2, distortion2 = run._get_distortion(ans)
    d_after.set(distortion2)
    ghosts_after.set(ghosts2)
    plot_graph(ans=run.GD_track, solver=run)


def _run_ELLS():
    run = create_solver_instance()
    H = run._ELLS_ALGO(run.root, run.max_simulations)
    ghosts1, distortion1 = run._get_distortion(Z_String.get())
    d_before.set(distortion1)
    ghosts_before.set(ghosts1)
    ghosts2, distortion2 = run._get_distortion(H)
    d_after.set(distortion2)
    ghosts_after.set(ghosts2)
    plot_graph(ans=run.ELLS_track, solver=run)


def plot_graph(ans, solver):
    fig1 = Figure(figsize=(5, 4),
                  dpi=70)
    fig2 = Figure(figsize=(5, 4),
                  dpi=70)
    d = []
    g = []
    for i in ans:
        g_v, d_v = solver._get_distortion(i)
        d.append(d_v)
        g.append(g_v)
    plot1 = fig1.add_subplot(111)
    plot2 = fig2.add_subplot(111)
    canvas1 = FigureCanvasTkAgg(fig1, master=master)
    canvas2 = FigureCanvasTkAgg(fig2, master=master)
    plot1.plot(d, color='r')
    plot2.plot(g)
    plot2.set_ylabel('GhostsLosts Sum')
    plot1.set_ylabel('Distortion Level')
    plot1.title.set_text('N-SP Distortion level vs Number of Deletions')
    plot2.set_xlabel('Number Of Deletions')
    plot2.title.set_text('SP Distortion level vs Number of Deletions')
    plot1.set_xlabel('Number Of Deletions')
    canvas1.draw()
    canvas2.draw()
    canvas1.get_tk_widget()
    canvas2.get_tk_widget()
    canvas1.get_tk_widget().grid(row=9, column=0, columnspan=3, rowspan=5, sticky=W)
    canvas2.get_tk_widget().grid(row=9, column=3, columnspan=5, rowspan=5, sticky=W)
    master.update()


# GUI-INTERFACE
master = Tk()
master.title("String Sanitization - Final Year Project")
master.pack_propagate(0)
W_String = tk.StringVar()
Z_String = tk.StringVar()
d_before = tk.IntVar()
d_after = tk.IntVar()
ghosts_before = tk.IntVar()
ghosts_after = tk.IntVar()
k = tk.IntVar()
tau = tk.IntVar()
max_sims = tk.IntVar()
menubar = Menu(master)

master.config(menu=menubar)
master.geometry("870x700")
master.highlightbackground = "black"
sq_fit_size = 300
logoIm = Image.open('logo.png')
logoIm = logoIm.resize((100, 90), Image.ANTIALIAS)
test = ImageTk.PhotoImage(logoIm)
label1 = Label(image=test).place(x=750, y=0)

# Original String W
original = tk.Label(master, text='Original String', font=('calibre', 15, 'bold'), bg="white smoke").grid(row=0,
                                                                                                         column=0)

original_entry = tk.Entry(master,
                          textvariable=W_String,
                          font=('calibre', 14, 'normal'),
                          bg='mint cream', ).grid(row=0, column=1)

# Sanitized String Z
sanitized = tk.Label(master,
                     text='Sanitized String',
                     font=('calibre', 15, 'bold'),
                     bg="white smoke").grid(row=0, column=2)

sanitized_entry = tk.Entry(master,
                           textvariable=Z_String,
                           font=('calibre', 15, 'normal'),
                           bg='mint cream').grid(row=0, column=3)

# Sensitive Pattern file upload button
tk.Button(master,
          text='+ sensitive patterns file',
          command=_upload_action,
          borderwidth=2,
          relief="groove",
          bg="lavender").grid(row=1, column=3)

# Main button for GD-ALGO
tk.Button(text="Running with GD-ALGO!", bg="lavender", fg="black", command=_run_GD).grid(row=1, column=0, sticky=W)

# Main button for ELLS-ALGO
tk.Button(text="Running with ELLS-ALGO!", fg="black", command=_run_ELLS, bg="lavender").grid(row=1, column=1, sticky=W)

# Delta
tk.Label(text="Number of Deletes:",
         fg="black",
         bg="lavender",
         borderwidth=2,
         relief="raised").grid(row=3, column=0, sticky=W)

deleter = Scale(from_=0, to=10, resolution=1, orient=HORIZONTAL, bg="mint cream", troughcolor="white")
deleter.grid(row=3, column=1, sticky=W)
deleter.set(5)

# Exploration parameter
tk.Label(text="UTC_C Parameter:",
         fg="black",
         bg="lavender",
         borderwidth=2,
         relief="raised").grid(row=4, column=0, sticky=W)

C_Value = Scale(from_=0, to=300, resolution=10, orient=HORIZONTAL, bg="mint cream", troughcolor="white")
C_Value.grid(row=4, column=1, sticky=W)
C_Value.set(150)

# Pruning parameter
tk.Label(text="Tolerance:",
         fg="black",
         bg="lavender",
         borderwidth=2,
         relief="raised").grid(row=5, column=0, sticky=W)

tolerance = Scale(from_=0, to=10, resolution=1, orient=HORIZONTAL, bg="mint cream", troughcolor="white")
tolerance.grid(row=5, column=1, sticky=W)
tolerance.set(5)

# Pattern length k
tk.Label(text="Length of Pattern k:",
         fg="black", bg="lavender",
         borderwidth=2,
         relief="raised").grid(row=6, column=0, sticky=W)

k = Scale(from_=0, to=10, resolution=1, orient=HORIZONTAL, bg="mint cream", troughcolor="white")
k.grid(row=6, column=1, sticky=W)
k.set(5)

# Tau
tk.Label(text="Tau:", fg="black", bg="lavender", borderwidth=2, relief="raised").grid(row=7, column=0, sticky=W)
tau = Scale(from_=0, to=20, resolution=1, orient=HORIZONTAL, bg="mint cream", troughcolor="white")
tau.grid(row=7, column=1, sticky=W)
tau.set(10)

# Omega
tk.Label(text="Omega:", fg="black", bg="lavender", borderwidth=2, relief="raised").grid(row=8, column=0, sticky=W)
multiplier = Scale(from_=0, to=1, resolution=0.1, orient=HORIZONTAL, bg="mint cream", troughcolor="white")
multiplier.grid(row=8, column=1, sticky=W)
multiplier.set(1)

# Max number of simulations
tk.Label(text="Max-Sims/decision", fg="black", bg="lavender", borderwidth=2, relief="raised").grid(row=3, column=2,
                                                                                                   sticky=W)
max_sims = Scale(from_=0, to=200, resolution=1, orient=HORIZONTAL, bg="mint cream", troughcolor="white")
max_sims.grid(row=3, column=3, sticky=W)
max_sims.set(100)

# non-spurious pattern distortion before deletions
tk.Label(text="N-SP distortion before:", bg="lavender", borderwidth=2, relief="raised").grid(row=4, column=2, sticky=W)
d1 = tk.Label(textvariable=d_before).grid(row=4, column=3, sticky=W)

# non-spurious pattern distortion after deletions
tk.Label(text="N-SP distortion after:", bg="lavender", borderwidth=2, relief="raised").grid(row=5, column=2, sticky=W)
d2 = tk.Label(textvariable=d_after).grid(row=5, column=3, sticky=W)

# spurious pattern distortion before deletions
tk.Label(text="SP distortion before:", bg="lavender", borderwidth=2, relief="raised").grid(row=6, column=2, sticky=W)
g1 = tk.Label(textvariable=ghosts_before).grid(row=6, column=3, sticky=W)

# spurious pattern distortion before deletions
tk.Label(text="SP distortion After:", bg="lavender", borderwidth=2, relief="raised").grid(row=7, column=2, sticky=W)
g2 = tk.Label(textvariable=ghosts_after).grid(row=7, column=3, sticky=W)

# Start application
mainloop()

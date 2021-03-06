import numpy as np
import random as random
import itertools
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from main import CSD_PLUS

_default_root = None
def convert_to_string(index, str):
    return str[:index] + str[index + 1:]

def readFile(filename):
    str = open(filename, 'r').read()
    return str

def aboutMe():
    messagebox.showinfo('About', 'This is CSD-PLUS Model seeks to solve String Sanitization Problem \n Final Year Project\n Kings College London \n Ye Mao ')

W = 'ccedbbbbbbabbabbccbc'
Z = 'ccadbacbdedabbbcccccacacacaa'
# Z = ''
k = 4
#
solver = CSD_PLUS(W=W, sens_patterns=['cced','ccbc'], k=k, multiplier=1, tau=2)
# non_sens_w = solver.non_sen_w
# list = [i for i in range(len(Z))]
# delta = 3
# capacity = 10000
ans, shortest = solver.BA_ALGO(delta=5, theta=100, Z=Z)


tau1,distor1 = solver.meaure_performance(Z)
print(ans)
print('++++++TPM++++++++')
print('TPM: distortion', distor1)
print('TPM: tua-ghosts & tau-losts', tau1)
print()
tau2,distor2 = solver.meaure_performance(ans[-1])
print('+++++BA-ALGO+++++')# W = 'abbabba'
print('BA-ALGO: distortion', distor2)
print('BA-ALGO: tua-ghosts & tau-losts',tau2)

# ans1, shortest1 = solver.EX_ALGO(Z=Z,delta=5)
# # print(ans1)
# tauDistortion,distortion = solver.meaure_performance(Z=ans1)
# print('+++++EX-ALGO+++++')# W = 'abbabba'
# print('BA-ALGO: distortion', distortion)
# print('BA-ALGO: tua-ghosts & tau-losts',
#       tauDistortion)




import os
import tarfile
import tkinter as tk
from tkinter import scrolledtext
from xml.etree.ElementTree import Element, SubElement, tostring
import time
import threading

def process_string(input_str, prefix):
    if input_str.startswith(prefix):
        input_str = input_str[len(prefix)+1:]
    if '/' in input_str and len(input_str)>1:
        input_str = input_str.split('/')[0]
    return input_str

class Emulator:
    def __init__(self, computer_name, fs_path):
        self.computer_name = computer_name
        self.fs_path = fs_path
        self.log_path = "./log.xml"
        self.script_path = "./script.sh"
        self.current_dir = "./"
        self.root = tk.Tk()
        self.root.title(f"{self.computer_name} Emulator")
        self.root.configure(bg='black')
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=100, height=30, bg='black', fg='white', insertbackground='white')
        self.text_area.pack(padx=10, pady=10)
        self.entry = tk.Entry(self.root, width=100, bg='black', fg='white', insertbackground='white')
        self.entry.bind("<Return>", self.process_command)
        self.entry.pack(padx=10, pady=10)
        self.text_area.tag_config("green", foreground="green")
        self.text_area.insert(tk.END, f"{self.computer_name}:{self.current_dir}$ ", "green")
        self.log = Element('log')
    def run(self):
        self.root.mainloop()
if __name__=="__main__":
   emulator = Emulator(computer_name="MyComputer", fs_path="./vfs.tar")
   emulator.run()

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
    
    def process_command(self, event):
        command = self.entry.get()
        self.entry.delete(0, tk.END)
        self.execute_command(command)
        self.text_area.insert(tk.END, f"{self.computer_name}:{self.current_dir}$ ","green")
    
    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return
        cmd = parts[0]
    
        log_entry = SubElement(self.log, 'command', attrib={'input': command})
    
        self.text_area.insert(tk.END, command + "\n")
        if cmd == 'ls':
            self.ls()
        elif cmd == 'cd':
            self.cd(parts[1] if len(parts) > 1 else [])
        elif cmd == 'exit':
            self.exit()
        elif cmd == 'clear':
            self.clear()
        elif cmd == 'find':
            self.find(parts[1] if len(parts) > 1 else '.')
        elif cmd == 'uniq':
            self.uniq(parts[1] if len(parts) > 1 else '')
        elif cmd == 'script':
            self.run_script(self.script_path)
            return
        else:
            log_entry.text = f"Command {cmd} not found.\n"
            self.text_area.insert(tk.END, log_entry.text)
   
        
    def ls(self):
        with tarfile.open(self.fs_path, "r:*") as tar:
            for member in tar.getmembers():
                if member.name.startswith(self.current_dir) and \
                    os.path.dirname(member.name) == self.current_dir:
                    self.text_area.insert(tk.END, process_string(member.name, self.current_dir) + "\n")
                    
    def cd(self, path):
         if path == "..":
             if self.current_dir != "/":
                 self.current_dir = "/".join(self.current_dir.split("/")[:-1]) or "/"
         else:
             new_path = os.path.join(self.current_dir, path).replace("\\", "/")
             with tarfile.open(self.fs_path, "r") as tar:
                 members = tar.getnames()
                 if new_path in members:
                     self.current_dir = new_path
                 else:
                     self.text_area.insert(tk.END, f"No such directory: {path}\n")
                 
    def exit(self):
         with open(self.log_path, "wb") as f:
             f.write(tostring(self.log))
         self.root.quit()
     
    def clear(self):
         self.text_area.delete(1.0, tk.END)
     
    def find(self, pattern):
         with tarfile.open(self.fs_path, "r:*") as tar:
             matches=[]
             for member in tar.getmembers():
                 if (pattern in member.name.split("/")[-1] and self.current_dir in member.name):
                     matches.append(member.name)
             if matches:
                 self.text_area.insert(tk.END, "Found:\n" + "\n".join(matches) + "\n")
             else:
                 self.text_area.insert(tk.END, f"No files found matching pattern: {pattern}\n")
    def uniq(self, path):
         if not path:
             self.text_area.insert(tk.END, "Usage: uniq <file_path>\n")
             return
     
         try:
             with tarfile.open(self.fs_path, "r") as tar:
                 member = tar.getmember(self.current_dir+'/'+path)
                 if member.isfile():
                     file = tar.extractfile(member)
                     lines = file.read().decode('utf-8').splitlines()
                     unique_lines = set(lines)
                     self.text_area.insert(tk.END, "\n".join(unique_lines) + "\n")
                 else:
                     self.text_area.insert(tk.END, f"{path} is not a file.\n")
         except KeyError:
             self.text_area.insert(tk.END, f"No such file: {path}\n")

     
if __name__=="__main__":
   emulator = Emulator(computer_name="MyComputer", fs_path="./vfs.tar")
   emulator.run()

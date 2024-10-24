
import unittest
import os
import tarfile
import tkinter as tk
from tkinter import scrolledtext
from xml.etree.ElementTree import Element, SubElement, tostring
import time
import threading
from EmulatorVFS import Emulator, process_string  # Импортируем ваш эмулятор и функцию process_string

class TestEmulator(unittest.TestCase):

    def setUp(self):
        self.emulator = Emulator(computer_name="TestComputer", fs_path="./vfs.tar")

    def tearDown(self):
        self.emulator.root.destroy()

    def test_process_string(self):
        self.assertEqual(process_string("vfs/test1/abc.txt", "vfs/test1"), "abc.txt")

    def test_ls_root(self):
        self.emulator.current_dir="./vfs"
        self.emulator.ls()
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn("test1", output)
        self.assertIn("test2", output)
        self.assertIn("test3", output)

    def test_ls_subdirectory(self):
        self.emulator.current_dir="./vfs/test1"
        self.emulator.ls()
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn("abc.txt", output)

    def test_cd(self):
        self.emulator.cd("vfs/test1")
        self.assertEqual(self.emulator.current_dir, "./vfs/test1")

    def test_cd_nonexistent(self):
        self.emulator.cd("nonexistent")
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn("No such directory: nonexistent", output)

    def test_clear(self):
        self.emulator.text_area.insert(tk.END, "Some text")
        self.emulator.clear()
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertEqual(output.strip(), "")

    def test_find(self):
        self.emulator.find("abc.txt")
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn("vfs/test1/abc.txt", output)

    def test_find_nonexistent(self):
        self.emulator.find("nonexistent")
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn("No files found matching pattern: nonexistent", output)

    def test_uniq(self):
        self.emulator.cd("vfs/test1")
        self.emulator.uniq("abc.txt")
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn("abc", output)
        self.assertIn("neabc", output)

    def test_uniq_nonexistent(self):
        self.emulator.uniq("nonexistent.txt")
        output = self.emulator.text_area.get("1.0", tk.END)
        self.assertIn("No such file: nonexistent.txt", output)


if __name__ == "__main__":
    unittest.main()

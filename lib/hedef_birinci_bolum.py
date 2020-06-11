from tkinter import ttk
from tkinter import *

class Birinci_Bolum():
    def __init__(self):
        super().__init__()

    def Birinci_Bolum_Menu(self):
        self.tree = ttk.Treeview(self.hedef)

        self.tree["columns"] = ("bir", "iki", "uc", "dort", "bes")
        self.tree.column("#0", width=30, minwidth=70)
        self.tree.column("bir", width=10, minwidth=30)
        self.tree.column("iki", width=200, minwidth=100)
        self.tree.column("uc", width=15, minwidth=15)  # stretch=tk.NO boyutu değiştiremez
        self.tree.column("dort", width=5, minwidth=140)
        self.tree.column("bes", width=15, minwidth=15)

        self.tree.heading("#0", text="Host", anchor=W)
        self.tree.heading("bir", text="Method", anchor=W)
        self.tree.heading("iki", text="URL", anchor=W)
        self.tree.heading("uc", text="Status", anchor=W)
        self.tree.heading("dort", text="Lenght", anchor=W)
        self.tree.heading("bes", text="MIME type", anchor=W)

        self.folder1 = self.tree.insert("", 1, text=str(self.host),
                                        values=(str(), "/bing/les/ter?q=tedsadsa", "401", "156000", "JSON"))
        self.tree.pack(side=TOP, fill=X)

if __name__ == "__main__":
   print(Birinci_Bolum)
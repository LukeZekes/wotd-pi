from tkinter import *
from tkinter import ttk
root = Tk()
root.attributes("-fullscreen", 1)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe_style = ttk.Style()
mainframe_style.configure("Main.TFrame", background="RoyalBlue")

mainframe = ttk.Frame(root, style="Main.TFrame")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

# Label text variables
date = StringVar()
date.set("MM/DD/YYYY")
date_label = ttk.Label(mainframe, textvariable=date)
date_label.grid(column=2, row=0, sticky=(E))

wotd = StringVar()
wotd.set("WOTD")
wotd_label = ttk.Label(mainframe, textvariable=wotd)
wotd_label.grid(column=0, row=1, sticky=(W))

pron = StringVar()
pron.set("Pron")
pron_label = ttk.Label(mainframe, textvariable=pron)
pron_label.grid(column=0, row=2, sticky=(W))

definition = StringVar()
definition.set("def def def def def def def")
definition_label = ttk.Label(mainframe, textvariable=definition)
definition_label.grid(column=0, row=3, columnspan=2, sticky=(N, W))
root.mainloop()
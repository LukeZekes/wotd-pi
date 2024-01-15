from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from datetime import date, datetime
from string import Template
from bs4 import BeautifulSoup
import requests
import regex as re
import os

LOG_FILE = "./log.txt"
def log(data):
  f = open(LOG_FILE, 'a')
  f.write('--------------------\n')
  f.write(datetime.now().strftime("%B %d %Y %H:%M:%S") + ": ")
  f.write(str(data))
  f.write("\n")
  f.close()
class WOTDDisplay(Tk):
  TIME_TO_UPDATE = 360000
  def __init__(self):
    Tk.__init__(self)
    self.attributes("-fullscreen", 1)
    # self.overrideredirect(True)
    # self.geometry("638x377+0+0")

    # Text variables
    self.date_text = StringVar()
    self.wotd_text = StringVar()
    self.pron_text = StringVar()
    self.def_text = StringVar()

    self.last_day_updated = date.today() # If date.today() > self.last_day_updated, it is the next day and the display should be updated
    self.wotd_updated_today = False
    self.update(first_update=True)
    # Create fonts
    date_font = Font(family="Cambria", size=12)
    wotd_font = Font(family="Times New Roman", size=48, weight="bold")
    pron_font = Font(family="Cambria", size=24, slant="italic")
    def_font = Font(family="Cambria", size=16)

    # Make main grid fill the window
    self.columnconfigure(0, weight=1)
    self.rowconfigure(0, weight=1)

    mainframe_style = ttk.Style()
    mainframe_style.configure("Main.TFrame", background="red")

    mainframe = ttk.Frame(self, style="Main.TFrame")
    mainframe.grid(column=0, row=0, sticky=(N, S, E, W))

    centerframe_style = ttk.Style()
    centerframe_style.configure("Center.TFrame")

    centerframe = ttk.Frame(mainframe, style="Center.TFrame")
    centerframe.grid_propagate(False)
    centerframe.grid(column=1, row=1, sticky=(N, S, E, W))
    # Make main grid responsive
    mainframe.columnconfigure(0, weight=1, uniform="a")
    mainframe.columnconfigure(1, weight=16, uniform="b")
    mainframe.columnconfigure(2, weight=1, uniform="a")

    mainframe.rowconfigure(0, weight=1, uniform="a")
    mainframe.rowconfigure(1, weight=12, uniform="b")
    mainframe.rowconfigure(2, weight=1, uniform="a")

    centerframe.columnconfigure(0, weight=1)
    centerframe.rowconfigure(0, weight=1, uniform="c")
    centerframe.rowconfigure(5, weight=1, uniform="c")

    # Label text variables
    label_style = ttk.Style()
    label_style.configure("Label.TLabel")
    date_style = ttk.Style()
    date_style.configure("Date.TLabel", background="white")

    date_label = ttk.Label(mainframe, textvariable=self.date_text, font=date_font, style="Date.TLabel")
    date_label.grid(column=0, row=0, sticky=(N, W), padx=(5, 0))

    wotd_label = ttk.Label(centerframe, textvariable=self.wotd_text, font=wotd_font, style="Label.TLabel")
    wotd_label.grid(column=0, row=1)

    pron_label = ttk.Label(centerframe, textvariable=self.pron_text, font=pron_font, style="Label.TLabel")
    pron_label.grid(column=0, row=2)

    definition_label = ttk.Label(centerframe, textvariable=self.def_text, font=def_font, style="Label.TLabel", wraplength=400)
    definition_label.grid(column=0, row=3, rowspan=2)

  # Fetch data from dictionary.com and update the display
  def update(self, first_update = False):
    # Check if it is a different day that the last time the display was updated
    # Date and word must be updated separately, since the dictionary.com word of the day doesn't change until some time after midnight EST
    current_date = date.today()
    if (first_update or self.last_day_updated < current_date):
      log("Updating date")
      self.last_day_updated = current_date
      self.date_text.set(current_date.strftime('%D'))
      self.wotd_updated_today = False
      

    if (first_update or not self.wotd_updated_today):
      data = self.get_word_of_the_day()
      if data["word"] != self.wotd_text.get():
        log("WotD has changed on dictionary.com - updating text")
        self.wotd_text.set(data["word"])
        self.pron_text.set(data["pronounciation"])
        self.def_text.set(Template('$POS: $DEFINITION').safe_substitute(POS=data["pos"], DEFINITION=data["definition"]))
        self.wotd_updated_today = True

    self.after(self.TIME_TO_UPDATE, self.update)

  '''
  Fetch data from dictionary.com
  Returns data in the format
    result = {
      "word": "",
      "pronounciation": "",
      "pos":"",
      "definition": "",
    }
  '''
  def get_word_of_the_day(self):
    log("Fetching data from dictionary.com")
    result = {
    "word": "",
    "pronounciation": "",
    "pos":"",
    "definition": "",
    }
    url = "https://www.dictionary.com/e/word-of-the-day/"
    html_document = requests.get(url).text
    soup = BeautifulSoup(html_document, "html.parser")

    # Locate important divs
    wotd_div = soup.find(attrs={"class": "otd-item-wrapper-content"})
    # The indices are weird because there are newline characters inserted in the HTML
    wotd_item = wotd_div.contents[1].contents[1] # Word and definition are in here
    wotd_extras = wotd_div.contents[11] # Origin of the word and examples

    # Isolate the desired information
    # Word
    word = wotd_item.contents[7].get_text(strip=True) # Using get_text() trims the newline characters around the word
    result["word"] = word
    # Pronounciation
    pron = wotd_item.contents[9].get_text(strip=True)
    # Format this string to only get the phonetic respelling
    pron = pron.replace(" ", "") # Remove the extra spaces inside the brackets
    pron = re.search(r"\[.*\]\[", pron).group(0)
    pron = pron[0:len(pron) - 1]
    result["pronounciation"] = pron  
    # Part of speech
    pos_div = wotd_item.contents[11].contents[1]
    pos = pos_div.contents[1].get_text(strip=True)
    result["pos"] = pos
    # Definition
    definition = pos_div.contents[3].get_text(strip=True)
    result["definition"] = definition
    log(result)
    return result

try:
  os.environ["DISPLAY"] = ":0"
  window_root = WOTDDisplay()
  window_root.mainloop()
except BaseException as e: # Catch errors and write to log.txt
  log(type(e).__name__)
  for a in e.args:
    log(" ".join([a, "\n"]))
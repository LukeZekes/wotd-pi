from bs4 import BeautifulSoup
import requests
import regex as re
# Get word of the day page from dictionary.com
def get_word_of_the_day():
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
  return result
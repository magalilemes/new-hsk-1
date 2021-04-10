import csv
from gtts import gTTS
import os
import pinyin
from pinyin.cedict import translate_word

wordlist = open('wordlist.txt', 'r')

sep1 = '｜'
sep2 = '（'

# Ignore first 6 lines
for i in range(6):
  wordlist.readline()

# This is where Anki stores all media on Ubuntu. It's possibly different in
# other operating systems.
media_folder = os.environ['HOME'] + '/.local/share/Anki2/User 1/collection.media/'

with open('hsk1.csv', 'w', newline='') as file:

  writer = csv.writer(file)
  writer.writerow(['Simplified Chinese', 'Pinyin', 'Meaning', 'Audio'])  
  retrieve_word = str.maketrans('', '', '0123456789 ')
  
  row = [None]*4
  for line in wordlist.readlines():

    # Just HSK 1 for now
    if (line == '\n'): break

    row[0] = line.translate(retrieve_word).rstrip('\n').split(sep1, 1)[0].split(sep2, 1)[0]
    row[1] = pinyin.get(row[0])
    meaning = translate_word(row[0])

    # If there's no translation available, then I'll retrieve it manually myself
    if (meaning != None):
      row[2] = ', '.join(meaning)
    else:
      row[2] = ''
    row[3] = '[sound:' + row[0] + '.mp3]'
    
    audio = gTTS(text=row[0], lang='zh-CN', slow=False)
    audio.save(media_folder + row[0] + '.mp3')

    writer.writerow(row)
    row = [None]*4

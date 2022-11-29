#! /usr/bin/env python3

import sys
import json
import html
import browser_cookie3
import requests

cj = browser_cookie3.chrome()
puz_url = sys.argv[1]
puz_url = puz_url.replace("puzzles","play")

page = requests.get(puz_url,cookies=cj)

for line in page.text.split('\n'):
    if 'oApp.puzzle_json' in line: 
         json_text = line
         json_text = json_text[35:-1]

#load the clean text into json object. 
xword_data = json.loads(json_text)

title = xword_data.get('data').get('headline')
puz_author = xword_data.get('data').get('copy').get('setter')
if (puz_author == ''):
    puz_author = xword_data.get('data').get('copy').get('publisher')
#the number of rows
rows = (xword_data['data']['copy']['gridsize']['rows'])
#the number of cols
cols = (xword_data['data']['copy']['gridsize']['cols'])
puz_copyright = xword_data.get('data').get('copy').get('date-publish')
grid_contents = (xword_data['data']['grid'])
clue_contents = (xword_data['data']['copy']['clues'])
clue_acrosses = (clue_contents[0])
clue_downs = (clue_contents[1])

# open a filehandle for the puz text file, same name as the title with a .txt
out_file = open(title + ".txt", 'w')
out_file.write("<ACROSS PUZZLE>")
out_file.write("\n")
out_file.write("<TITLE>")
out_file.write("\n")
out_file.write(title)
out_file.write("\n")
out_file.write("<AUTHOR>")
out_file.write("\n")
out_file.write (puz_author)
out_file.write("\n")
out_file.write("<COPYRIGHT>")
out_file.write("\n")
if puz_copyright != None :
    out_file.write(puz_copyright)
    out_file.write("\n")
else:
    out_file.write("Unknown Times Puzzle")
out_file.write("<SIZE>")
out_file.write("\n")
out_file.write(rows)
out_file.write("x")
out_file.write(cols)
out_file.write("\n")
out_file.write("<GRID>")
out_file.write("\n")
for row in grid_contents:
    for square in row:
        if (square['Letter']==""):
            out_file.write(".")
        else:
            out_file.write(square['Letter'])
    out_file.write("\n")    
out_file.write("<ACROSS>")
out_file.write("\n")
for clue in clue_acrosses['clues']:
    clue_text = html.unescape(clue['clue']) 
    clue_length = (clue['format']) 
    out_file.write(clue_text + " (" + clue_length + ")")
    out_file.write("\n")
out_file.write("<DOWN>")
out_file.write("\n")
for clue in clue_downs['clues']:
    clue_text = html.unescape(clue['clue'])
    clue_length = (clue['format']) 
    out_file.write(clue_text + " (" + clue_length + ")")
    out_file.write("\n")
out_file.write("<NOTEPAD>")
out_file.write("\n")
out_file.close()
print("Writing file " + title)


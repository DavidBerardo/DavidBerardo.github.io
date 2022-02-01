import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

'''
TODO:
brighten background once meta solved
add spreadsheet links
make it possible to enter puzzle solutions
compare solution with true value
click to change puzzle status
'''


def write(s):
	hf.write(s + '\n')

def gen_puzzle_html(puzzle):
	colors = ["rgb(220,220,220,0.5)","rgb(200,93,38,0.6)","rgb(76,190,108,0.9)"]
	write('<div class=puzzleCell>')
	border_rad = [3,7,5][puzzle.meta]
	font_size = [20,30,24][puzzle.meta]
	#print(puzzle.name,puzzle)
	write(f'<div class="puzzleInner"  style="background-color:{colors[puzzle.status]}; font-size:{font_size}px;border: {border_rad}px solid;border-color:rgb(0,0,0,0.8)">')
	write(f'<div class="initial">{"Meta: "*(puzzle.meta > 0) + puzzle.name}</div>')
	write('<div class="hovered" style="font-size:20px">')
	write(f'<div ><a href="{puzzle.puzzlink}" target="_blank">Puzzle</a></div>')
	write(f'<div ><a href="{puzzle.sheetlink}" target="_blank">Spreadsheet</a></div>')
	write('</div>')
	write('</div>')
	#write(f'<div style="color:rgb(0,75,0); background-color:rgb(255,255,255,0)" contenteditable="true"><b><spoiler>{"SOLUTION"*(puzzle.status==2)}</spoiler></b></div>')
	write(f'<div style="color:rgb(0,75,0); background-color:rgb(255,255,255,0)" contenteditable="{"false" if puzzle.status==2 else "true"}"><b><spoiler>{puzzle.solution}</spoiler></b></div>')
	write('</div>')
	return

def gen_header(p_round,ministry=False,solves = []):
	write('<div style="text-align: center">')
	write(f'<a href = "{p_round.url}" target="_blank">')
	write(f'<img src="{p_round.logo}" id="{p_round.name}" alt="{p_round.name}">')
	write('</a>')
	if ministry:
		write(f'<p style="text-align:center; font-size:25px">Solved: {solves[0]}/{p_round.n_puzzles} + {solves[1]}/5 + {solves[2]}/2</p>')
	elif len(p_round.puzzles) == 0:
		write(f'<p style="text-align:center; font-size:25px">Solved: {p_round.meta_solved}/1</p>')
	else:
		write(f'<p style="text-align:center; font-size:25px">Solved: {p_round.solved}/{p_round.n_puzzles} + {p_round.meta_solved}/1</p>')

def gen_ps_col(ps_round,cols=3,borderstyle="",meta_width=65):
	print(ps_round.name,ps_round.meta.color)
	write(f'<div class = "column" style="{borderstyle}; background-color: {ps_round.meta.color}">')
	gen_header(ps_round)
	write(f'<div class="puzzlesContainer">')
	write(f'<div class="grid-container" style="grid-template-columns: auto; width:{meta_width}%; margin: auto">\n')
	gen_puzzle_html(ps_round.meta)
	write('</div>')

	offset = 1.4 if cols == 5 else 2.1
	write(f'<div class="grid-container" style="grid-template-columns: {f"{int(100/cols)-offset}% "*cols}; float:center; width: 75%; margin:auto;">')
	#write(f'<div class="grid-container" style="grid-template-columns: {"1fr"*cols}; float:center; grid-column-end: auto; width: 90%; margin:auto;">')
	
	for p in ps_round.puzzles:
		gen_puzzle_html(p)
	write('</div>')

	write('</div>')
	write('</div>')	
	write('</div>')

def gen_m_content(p_round):
	write(f'<div class = "column"  style="background-color: {p_round.meta.color}">')
	#write(f'<div class = "column">')
	m_solves = [np.sum([p.status//2 for p in ministry.all_puzzles if p.meta == i]) for i in [0,2,1]]
	gen_header(ministry,ministry=True,solves = m_solves)
	write(f'<div class="grid-container" style="grid-template-columns: 50% 50%; width:55%; margin: auto">\n')
	for p in p_round.all_puzzles:
		if p.meta == 1: gen_puzzle_html(p)
	write('</div>')
	write(f'<div class="grid-container" style="grid-template-columns: {"18.6% "*5}; width:75%; margin: auto">\n')
	for p in p_round.all_puzzles:
		if p.meta == 2: gen_puzzle_html(p)
	write('</div>')

	write(f'<div class="grid-container" style="grid-template-columns: {"18.7% "*5}; float:center; width: 80%; margin:auto">')
	for p in p_round.puzzles:
		gen_puzzle_html(p)
	write('</div>')

	write('</div>')

def gen_ps_row(left,right):
	write('<div class="row">')
	gen_ps_col(left,borderstyle="border: 5px solid black;")
	gen_ps_col(right,borderstyle="border: 5px solid black;")
	write('</div>')
	return

def line_to_puzz(puzz_line):
	name = puzz_line['Name']
	status = int(puzz_line['State'])
	puzzlink = puzz_line['Link']
	sheetlink = puzz_line['Spreadsheet']
	meta = int(puzz_line['Meta'])
	solution = puzz_line['Solution']
	return puzzle(name,status,puzzlink,sheetlink,meta,solution)

class puzzle:
	def __init__(self,name,status,puzzlink,sheetlink,meta,solution):
		self.name = name
		self.status = status
		self.puzzlink = puzzlink
		self.sheetlink = sheetlink
		self.meta = meta
		self.status = status
		self.solution = solution
		self.color = None

class p_round:

	def __init__(self,name,puzzles,color):
		self.name = name
		self.logo = name.replace(' ','_').replace('-','_').lower() + '_logo.png'
		#print(self.logo)
		url = name.replace(' ','-')
		self.url = f'https://www.bookspace.world/round/{url.lower()}/'

		self.all_puzzles = [line_to_puzz(puzzles.iloc[i]) for i in range(len(puzzles))]
		for p in self.all_puzzles:
			p.color = color
		self.puzzles = [p for p in self.all_puzzles if p.meta == 0]
		self.meta = [p for p in self.all_puzzles if p.meta == 1][0]

		self.solved = np.sum([p.status // 2 for p in self.puzzles])
		self.n_puzzles = len(self.puzzles)

		self.meta_solved = self.meta.status // 2
		self.color=color

#load spreadsheet info
data = pd.read_csv('mitmh_2022_puzz_info.csv')
data = data.replace(np.nan, '', regex=True)


round_names = data['Round'].unique()

round_colors = ["#4CABf8","#6A41EF","#405868","#9A75A5","#B9CA19","#3CBDCF","#F66001","#F7CF52","#F9B5B8","#253729","#EFECDF","#3BB8B7","#92BFDE","#F0EEEE"]
round_colors = [r + '77' for r in round_colors]

color_dict = {round_names[i]:round_colors[i] for i in range(len(round_names))}
print(color_dict)
#pen station rounds
ps_rounds = [p_round(i,data[data['Round']==i],color=color_dict[i]) for i in round_names[2:-2]]

hf = open('index.html','w+')

write('<!DOCTYPE html>')
write('<html>')
write('<head>')
write('<link rel="stylesheet" href="website.css">')
write('<script src="scripts.js"></script>')
write('</head>')
write('<body>')

#generate navbar
write('<div class="navbar" id="navbar">')
write(f'<a onclick="scrollToTargetAdjusted(\'{round_names[0]}\')">{round_names[0]}</a>')
write(f'<a onclick="scrollToTargetAdjusted(\'{round_names[1]}\')">{round_names[1]}</a>')
write(f'<a onclick="scrollToTargetAdjusted(\'Pen Station\')">Pen Station</a>')
for i in range(5):
	#write(f'<a onClick="navClick("{r}")">{r}</a>')
	#write(f'<a class="anchor" href="#{round_names[2+2*i]}" style="top:-150px">{round_names[2+2*i]}/{round_names[2+2*i+1]}</a>')
	write(f'<a onclick="scrollToTargetAdjusted(\'{round_names[2+2*i]}\')">{round_names[2+2*i]}/{round_names[2+2*i+1]}</a>')
write(f'<a onclick="scrollToTargetAdjusted(\'{round_names[-2]}\')">{round_names[-2]}</a>')
write(f'<a onclick="scrollToTargetAdjusted(\'{round_names[-1]}\')">{round_names[-1]}</a>')
write('</div>')

#title at top of page
write('<div style="text-align:center; margin:auto; font-size:50px;"><b>MIT Mystery Hunt 2022<b></div>')
write('<br><hr /><br>')
write('<div style="text-align:center; margin:auto; font-size:30px;"><b>⭐Astro Pals Progress Tracker⭐<b></div>')
write('<br>')

#generate investigation stuff
intro = p_round(round_names[0],data[data["Round"]==round_names[0]],color=color_dict[round_names[0]])
gen_ps_col(intro,cols=5,meta_width=25)

#write('<br><hr /><br>')

#generate ministry stuff
ministry = p_round(round_names[1],data[data["Round"]==round_names[1]],color=color_dict[round_names[1]])
gen_m_content(ministry)
write('</div>')

#write('<br><hr /><br>')

#generate ps title
write('<div class = "column" style="background: rgb(0,0,0,0); border: None">')
write('<div style="text-align: center">')
write(f'<a href = "https://www.bookspace.world/pen-station/" target="_blank">')
write(f'<img src="pen_station_logo.png" id="Pen Station" alt="pen_station" width="400" height="auto">')
write('</a>')
write(f'<p style="text-align:center; font-size:25px">Sub-Rounds Solved: {np.sum([p.meta.status//2 for p in ps_rounds])}/10</p>')

#generate ps puzzle
for i in range(5):
	left = ps_rounds[2*i]
	right = ps_rounds[2*i+1]
	#print(left.name,right.name)
	gen_ps_row(left,right)
write('</div>')

#write('<br><hr /><br>')

#generate Plot Device
finale = p_round(round_names[-2],data[data["Round"]==round_names[-2]],color=color_dict[round_names[-2]])
gen_ps_col(finale,cols=5)

#write('<br><hr /><br>')


#finale Puzzle
last_puzz = p_round(round_names[-1],data[data["Round"]==round_names[-1]],color=color_dict[round_names[-1]])
print(last_puzz.name)
gen_ps_col(last_puzz)
write('</body>')
write('</html>')
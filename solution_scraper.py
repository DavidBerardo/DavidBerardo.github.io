import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import urllib
import urllib.request
import html.parser
import requests
from requests.exceptions import HTTPError
from socket import error as SocketError
from http.cookiejar import CookieJar 

puzzle_info = pd.read_csv('mitmh_2022_puzz_info.csv')
sols = []
for p in range(len(puzzle_info)):
	rot_sol = ''
	try:
		solution_url = puzzle_info.iloc[p]['Link'] + 'solution'
		req = urllib.request.Request(solution_url)
		cj = CookieJar()
		opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
		response = opener.open(req)

		raw_response = response.read().decode('utf8',errors='ignore')
		response.close()

		for i in raw_response.split('\n'):
			if 'Answer' in i:
				plain_sol = i.split('>')[1].split('<')[0]
				
				rot_sol = ''
				for s in plain_sol:
					if s == ' ':continue
					rot_sol+=chr((ord(s)-65+13)%26+65)
				sol = rot_sol
				break
		print(puzzle_info.iloc[p]['Name'],' - ',rot_sol)
	except:
		print('BAD URL FOR PUZZLE: ',puzzle_info.iloc[p]['Name'])
	
	sols.append(rot_sol)

puzzle_info['Solutions'] = sols
puzzle_info.to_csv('test.csv')

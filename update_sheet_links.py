import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#link example
#https://docs.google.com/spreadsheets/d/13goNwRQxR6sce_QzbH4sA1s13UTqAqxweEb_200YnhA/edit?usp=sharing

d = pd.read_csv('mitmh_2022_puzz_info.csv')
file_data = open('drive_ids.txt','r+').readlines()

s_urls = ['#']*len(d)
for f in file_data:
	title = ' '.join(f.strip().split()[1:-2])[:-1]
	if 'Meta' in title:
		title = title[6:]
	found = len(d[d['Name']==title])
	ind = d[d['Name']==title].index[0]
	print(f.strip().split()[-1] )
	s_urls[ind]='https://docs.google.com/spreadsheets/d/' + f.strip().split()[-1] + '/edit?usp=sharing'

d['Spreadsheet'] = s_urls
d.to_csv('mitmh_2022_puzz_info.csv')
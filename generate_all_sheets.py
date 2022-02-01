import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
from openpyxl import Workbook

data = pd.read_csv('mitmh_2022_puzz_info.csv')

round_names = data['Round'].unique()

if not(os.path.isdir('all_rounds')):
	os.mkdir('all_rounds')
for rn in round_names:
	puzzles = data[data['Round']==rn]
	if not(os.path.isdir('all_rounds/' + rn)):
		os.mkdir('all_rounds/'+rn)
	for p in puzzles.iloc:
		#df = pd.DataFrame(list())
		pname = p['Name'].replace('/',' - ')
		#df.to_csv('all_rounds/' + rn + '/' + 'Meta: '*(p['Meta']>0) + pname + '.csv')
		wb = Workbook()
		wb.save(filename = 'all_rounds/' + rn + '/' + 'Meta: '*(p['Meta']>0) + pname + '.xlsx')
import numpy as np
from pprint import pprint

'''
recursive sudoku solver
only 9x9 sudokus are compatible
'''

def sudfromcsv(filepath,sep=','):
	with open(filepath) as f:
		sud = np.zeros((9,9),dtype=int)
		data = f.read().split('\n')
		while '' in data:
			data.remove('')
		for i,line in enumerate(data):
			a = line.split(sep)
			while '' in a:
				a.remove('')
			for j,e in enumerate(a):
				sud[i,j] = e
	return sud

def is_sud_solved(sud):

	#check each row and each column to have all nums 1-9
	for num in range(1,10):

		#check each row and column contains num
		for i in range(9):

			#check i th row
			if not num in sud[i,:]:
				return False

			#check i th column
			if not num in sud[:,i]:
				return False

		#check each 3x3 submatrix contains num
		for i in range(3):
			for j in range(3):
				if not num in sud[i*3:i*3+3 , j*3:j*3+3] :
					return False

	return True

def recursive_sud_solve():
	global sud_0

	for i in range(9):
		for j in range(9):
			if sud[i,j]==0:
				for num in range(1,10):
					sud_0[i,j] = num
					recursive_sud_solve()
				sud[i,j]=0

	#backtracking
	if not is_sud_solved(sud_0):
		return

	print(sud_0)
	input()
	return


sud = sudfromcsv('infile_easy.csv',sep='\t')
sud_0 = sud.copy() #global, don't change it

print('input:\n',sud)
print('solution\n')

recursive_sud_solve()




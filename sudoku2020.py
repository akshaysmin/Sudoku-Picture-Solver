#!usr/bin/env python3
import numpy as np
from copy import deepcopy

class element:
	#a number in sudoku
	def __init__(self, name, rows, columns):
		self.name = name
		self.rows = rows #list
		self.columns = columns #list
		self.boxes   = self.boxes(self.rows,self.columns) #list of box names 0-8
	
	def boxes(self,rows,columns):
		boxes  = []
		boxmap = ((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2))
		for x,y in zip(rows,columns):
			boxes.append(boxmap.index((x//3,y//3)))
		return boxes

class box:
	#small 3x3 box in sudoku
	def __init__(self, name, elements):#elements is list of element objects in the box
		self.name    = int(name) #int
		self.rows    = self.box_rows(self.name)#tuple
		self.columns = self.box_columns(self.name)#tuple
		self.element_names   = [element.name for element in elements]
		self.element_rows    = []
		self.element_columns = []
		element_rows_temp    = [element.rows for element in elements]
		element_columns_temp = [element.columns for element in elements]

		for rows,columns in zip(element_rows_temp,element_columns_temp):
			for r,c in zip(rows,columns):
				if r in self.rows and c in self.columns:
					elementrow = r #possible error: elementrow get assigned value more than once in this loop
					elementcol = c
			self.element_rows.append(elementrow)
			self.element_columns.append(elementcol)

		#self.cells    = self.get_cells(self.rows, self.columns)#may be useful
		self.element_cells = self.get_cells(self.element_rows, self.element_columns)
		#print('element_names : ',self.element_names)
		#print(self.element_cells)

	def get_cells(self,rows,columns):
		rows    = [row%3 for row in rows]   #global -> local coordinates
		columns = [col%3 for col in columns]#global -> local coordinates
		cells   = []
		cellmap = ((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2))
		for x,y in zip(rows,columns):
			cells.append(cellmap.index((x,y)))
		return cells

	def get_row_and_column(self,cell,box_name):
		row, col  = cell//3, cell%3 #local coordinates
		col += (box_name%3)*3
		row += (box_name//3)*3
		return row,col #global coordinates
	
	def box_rows(self,name):
		rowmap = ((0,1,2),(0,1,2),(0,1,2),(3,4,5),(3,4,5),(3,4,5),(6,7,8),(6,7,8),(6,7,8))
		return rowmap[name]
	
	def box_columns(self,name):
		columnmap = ((0,1,2),(3,4,5),(6,7,8),(0,1,2),(3,4,5),(6,7,8),(0,1,2),(3,4,5),(6,7,8))
		return columnmap[name]
	
	def info(self):
		print('box name: ',self.name)
		print('box rows: ',self.rows)
		print('box columns: ',self.columns)
		print(self.as_box())
		print()
	
	def as_box(self):
		#returns box as numpy array
		outarray = np.zeros((3,3))
		for name,i,j in zip(self.element_names,self.element_rows,self.element_columns):
			outarray[i%3,j%3] = name
		return outarray
	

#useful functions

def as_sudoku(elements_list):
	#input : list of element objects in sudoku
	#output: described sudoku as numpy array

	out_array = np.zeros((9,9))
	for elem in elements_list:
		for i,j in zip(elem.rows,elem.columns):
			out_array[i,j] = elem.name
	return out_array

def get_box(row,column):
	boxname = (row//3)*3 + (column//3)
	return boxname

def from_terminal():
	print('Enter numbers one by one, enter zero for absence of number')
	n_info = (([],[]),([],[]),([],[]),([],[]),([],[]),([],[]),([],[]),([],[]),([],[])) #nine elements
	b_info = ([],[],[],[],[],[],[],[],[])	#each element list conatins indices of numbers conained in the box
	for i in range(9):
		print('Row : ',i)
		for j in range(9):
			b = get_box(i,j)
			#n = int(input(f'Row {i},Col {j} : '))
			while True:
				try:
					n = int(input(f'Row {i},Col {j},Box {b} : '))
					if 0<=n<=9:
						break
				except:
					print('Please enter a number from 0 to 9')

			if n != 0:
				n_info[n-1][0].append(i)#rows of number n
				n_info[n-1][1].append(j)#columns of number n
				b_info[b].append(n-1)

	numbers = (element(n,n_info[n-1][0],n_info[n-1][1]) for n in range(1,10)) #n means number (1-9)
	boxes = (box(n, [numbers[i] for i in b_info[n]]) for n in range(9)) # n is box number (0-8)
	return numbers, boxes

def cycle(numbers_list):

	for num in numbers_list:
		boxes_to_fill = list({0,1,2,3,4,5,6,7,8}-set(num.boxes))

		for boxname in boxes_to_fill:
			box = boxes[boxname]
			possible_locations = {0,1,2,3,4,5,6,7,8} - set(box.element_cells)

			for row in box.rows:
				if row in num.rows:
					e1 = (row%3)*3
					possible_locations -= {e1,e1+1,e1+2}

			for col in box.columns:
				if col in num.columns:
					possible_locations -= {0+col%3,3+col%3,6+col%3}

			if len(possible_locations) == 1:

				loc_to_fill = possible_locations.pop()
				row_to_fill, column_to_fill = box.get_row_and_column(loc_to_fill, box.name)

				#update datastructures/sudoku
				num.rows.append(row_to_fill)
				num.columns.append(column_to_fill)
				num.boxes.append(boxname)

				box.element_names.append(num.name)
				box.element_rows.append(row_to_fill)
				box.element_columns.append(column_to_fill)
				box.element_cells.append(loc_to_fill)

	return numbers_list

#initialise numbers and boxes
'''
numbers = (element(1,[1,3,4,5,6],[2,4,6,0,1]),element(2,[0,1,4,5,6,8],[6,5,8,1,4,0]),element(3,[0,2,3,5,7],[1,8,7,2,0]),element(4,[0,4,7,8],[8,5,2,3]),element(5,[0,4,8],[7,0,2]),element(6,[1,2,5,6,7],[6,4,3,5,8]),element(7,[1,2,3,6,7],[8,1,0,2,6]),element(8,[0,6,7],[2,0,3]),element(9,[2,7],[6,1]))	#index of this tuple is same as element.name
boxes = (box(0,[numbers[1-1],numbers[3-1],numbers[7-1],numbers[8-1]]),
		box(1,[numbers[2-1],numbers[6-1]]),
		box(2,[numbers[2-1],numbers[3-1],numbers[4-1],numbers[5-1],numbers[6-1],numbers[7-1],numbers[9-1],]),
		box(3,[numbers[1-1],numbers[2-1],numbers[3-1],numbers[5-1],numbers[7-1]]),
		box(4,[numbers[1-1],numbers[4-1],numbers[6-1]]),
		box(5,[numbers[1-1],numbers[2-1],numbers[3-1]]),
		box(6,[numbers[1-1],numbers[2-1],numbers[3-1],numbers[4-1],numbers[5-1],numbers[7-1],numbers[8-1],numbers[9-1]]),
		box(7,[numbers[2-1],numbers[4-1],numbers[6-1],numbers[8-1]]),
		box(8,[numbers[6-1],numbers[7-1]])
		)	#index of this tuple is same as box.name
'''
numbers,boxes = from_terminal()

print(as_sudoku(numbers))
#for box in boxes:
#	box.info()

#algorithm0
numbers_list = numbers


		
while True:
	cycle(numbers_list) #can speed up code if u remove filled out numbers from the list in every step
	print(as_sudoku(numbers))
	input()

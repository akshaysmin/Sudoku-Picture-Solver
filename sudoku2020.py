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
		print(self.name)
		print(self.element_names)
		print(element_rows_temp)

		for i,elementrows in enumerate(element_rows_temp):
			for j in elementrows:
				if j in self.rows:
					elementrow = j
			self.element_rows.append(elementrow)
		print(self.element_rows)
		print(element_columns_temp)
		for i,elementcolumns in enumerate(element_columns_temp):
			for j in elementcolumns:
				if j in self.columns:
					elementcolumn = j
			self.element_columns.append(elementcolumn)

		#self.cells    = self.get_cells(self.rows, self.columns)#may be useful
		self.element_cells = self.get_cells(self.element_rows, self.element_columns)
		print()
	def get_cells(self,rows,columns):
		rows    = [row%3 for row in rows]   #global -> local coordinates
		columns = [col%3 for col in columns]#global -> local coordinates
		cells   = []
		cellmap = ((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2))
		for x,y in zip(rows,columns):
			cells.append(cellmap.index((x,y)))
		return cells
	
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
		#print(self.as_box())
	
	def as_box(self):
		#returns box as numpy array
		outarray = np.zeros((3,3))
		for name,i,j in zip(self.element_names,self.element_rows,self.element_columns):
			print(name,i,j)
			#outarray[i,j] = name
		print()
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

#initialise numbers and boxes
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

print(as_sudoku(numbers))
for box in boxes:
	#box.as_box()
	print(box.as_box())
	
#algorithm0
numbers_left = numbers[:]



	










































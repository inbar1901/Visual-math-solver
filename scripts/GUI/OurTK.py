'''
Python 3.6 
Pytorch >= 0.4
This is our GUI - contain option to choose image, it detect the equation, solve it and show the solution written
in print and also handwritten
'''
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image,ImageTk
import tkinter
from tkinter import messagebox
import numpy as np
import torch
from sympy import *
import re
from for_test_V20 import for_test
from isDigitAppear import isDigitAppear
from isParamAppear import isParamAppear

 
def choosepic():
	"""
	choosing a pic to work with
	"""
	global Flag
	path_ = askopenfilename(
		initialdir=r'/home/inbarnoa/PycharmProjects/MathSolver/exampelsForPresentation')  # equations to show
	# 	#path_=askopenfilename(initialdir=r'/home/inbarnoa/PycharmProjects/MathSolver/equationParameter') # equation with parameter
	# path_ = askopenfilename(initialdir=r'/home/inbarnoa/PycharmProjects/MathSolver/equationNumbers')# equation with only numbers
	path.set(path_)
	global img_open
	img_open = Image.open(e1.get()).convert('L')
	img=ImageTk.PhotoImage(img_open)
	image1.config(image=img)
	image1.image=img #keep a reference

	var = tkinter.StringVar(value='')
	var.set('                                                                                                      ')

	e2=Label(root,textvariable = var , font = ('Arial', 25))
	e2.place(relx=0.05,y=500)

	Flag = False


def start_detection():
	"""
	function called by pressing the button start detection
	:return:
	"""
	global img_open
	global prediction, attention
	if Flag: # no image was chosen
		print (messagebox.showerror(title='Error', message='No Image'))
	else:
		img_open2 = torch.from_numpy(np.array(img_open)).type(torch.FloatTensor)
		img_open2 = img_open2/255.0
		img_open2 = img_open2.unsqueeze(0)
		img_open2 = img_open2.unsqueeze(0)

		var = tkinter.StringVar()
		e2 = Label(root, textvariable=var, font=('Arial', 25))
		e2.place(relx=0.1, y=470)
		var3 = tkinter.StringVar()
		var3.set("                                                                   \n                                          \n                                                        ")
		e3 = Label(root, textvariable=var3, font=('Arial', 25), anchor='s')
		e3.place(relx=0.1, y=480)
		var.set('Detecting...                             ')
		e2=Label(root,textvariable = var, font = ('Arial', 25))
		e2.place(relx=0.1,y=470)
		e2.update()

		attention, prediction = for_test(img_open2) # activate the recognition network
		global prediction_string
		prediction_string = ''
		print(prediction_string)

		img_open = np.array(img_open)

		for i in range(attention.shape[0]):
			if prediction[i] == '<eol>':
				continue
			else:
				prediction_string = prediction_string + prediction[i]
		print(prediction_string)
		if prediction_string.endswith("="): #numeric equation
			var.set("Equation: " + prediction_string + str(calcResult()) + "                                  \n\n                                                           ")
			e2 = Label(root, textvariable=var, font=('Arial', 25), anchor='s')
			e2.place(relx=0.1, y=470)
		else:
			var.set("Equation: " + prediction_string + "                                                               ")
			e2=Label(root,textvariable = var, font = ('Arial', 25), anchor='s')
			e2.place(relx=0.1,y=470)
			var3.set(str(calcResult()) + "                                                               ")
			e3.configure(textvariable=var3)
			e3.place(relx=0.09, y=480)
		image_file = ImageTk.PhotoImage(img_open)
		image1.config(image=image_file)
		image1.image=image_file
		image1.update()
		# var.set("Waiting for a new solution               ")

def calcResult():
	"""
	calculating the equation solution and creating result image
	"""
	global prediction_string
	if prediction_string.endswith("="): #this is an only numbers equation ends with =
		equation = prediction_string[0:-1]
		equation = equation.replace("cdot","*")
		print ("the equation is", equation)
		r1 = r"(\D)0+(\d+)"
		r2=r"\b0+(\d+)"
		equationNoZero= re.sub(r1,r"\1\2",equation)
		finalEq= re.sub(r2,r"\1",equationNoZero)
		# print("network output ", prediction_string)
		# print("equation after preprocessing ", finalEq)
		expr = sympify(finalEq)
		print("Sol is " + str(expr))
		# print("expression after sympify == sol  ", expr)
		sol_image_file = isDigitAppear(equation,str(expr),img_open)

		#creating solution image
		image_open2 = Image.fromarray(sol_image_file)
		image_file = ImageTk.PhotoImage(image_open2)
		l2.config(image=image_file)
		l2.image = image_file  # keep a reference
		l2.update()

		# updating equation type display
		var4 = tkinter.StringVar()
		var4.set("Numeric equation                                                    \n\n                                          ")
		e4 = Label(root, textvariable=var4, font=('Arial', 25), anchor='s')
		e4.place(relx=0.75, y=470)

		return expr
	else:
		#this is equation with a parameter
		eq_location = prediction_string.find('=')
		after_eq = prediction_string[eq_location+1:]
		equation = prediction_string[0:eq_location]+'-('+after_eq+')'
		equation = equation.replace("cdot", "*")
		predict_eq = prediction_string .replace("cdot","*")
		newEquation = equation
		count =0
		for i in range(len(equation)):
			s= equation[i]
			if s.isalpha():
				param = symbols(s) #define s as a param in equation solving
				# adding a mul symbol between two figures
				if i>=1 and newEquation[i-1+count].isalnum():
					newEquation = newEquation[:i+count]+"*"+newEquation[i+count:]
					count=count+1
				if newEquation [i+1+count].isalnum():
					newEquation = newEquation[:i+count+1]+"*"+newEquation[i+count+1:]
					count = count + 1

		#need to set the name of param to be the same
		r1 = r"(\D)0+(\d+)"
		r2=r"\b0+(\d+)"
		equationNoZero= re.sub(r1,r"\1\2",newEquation)
		finalEq= re.sub(r2,r"\1",equationNoZero)
		# print("network output ", prediction_string)
		# print("equation after preprocessing ",finalEq)

		expr = sympify(finalEq)
		# print("expression after sympify ", expr)
		# print("Parameter as Symbol ", param)
		sol = solve(expr,param)
		print ("sol is", str(sol))

		#creating solution image
		sol_image_file = isParamAppear(predict_eq,sol,img_open,param)
		image_open2 = Image.fromarray(sol_image_file)
		image_file = ImageTk.PhotoImage(image_open2)
		l2.config(image=image_file)
		l2.image = image_file  # keep a reference
		l2.update()

		# updating equation type display
		var4 = tkinter.StringVar()
		var4.set("Equation with parameter\n\n The parameter is " + str(param) + "      ")
		e4 = Label(root, textvariable=var4, font=('Arial', 25), anchor='s')
		e4.place(relx=0.74, y=470)

		return "\n\n Solution: " + str(sol)

root=Tk()		
root.geometry('1600x900')
root.title('Visual Math Solver')
Flag=True

path=StringVar()
bu2 = Button(root,text='Start Detection', font = ('Arial', 15, 'bold'), width = 18, height = 2,bg='light gray', command=start_detection)
bu1 = Button(root,text='Load Equation',font = ('Arial', 15, 'bold'), width = 18, height = 2, bg='light gray', command=choosepic)
e1=Entry(root,state='readonly',text=path)
title = tkinter.Label(root, text='Visual Math Solver',font=('Arial',40, 'bold'),width=25, height=2 )
title_1 = tkinter.Label(root, text='Your image:', font=('Arial', 25, 'bold'),)
title_2 = tkinter.Label(root, text='Result:', font=('Arial', 25, 'bold'),)
title_3 = tkinter.Label(root, text='Result Image:', font=('Arial', 25, 'bold')   )
title_4 = tkinter.Label(root, text='Equation type:', font=('Arial', 25, 'bold')   )

title.place(relx = 0.5, y = 50, anchor = CENTER)
bu1.place(relx=0.4,y=140, anchor = CENTER)
bu2.place(relx=0.6,y=140, anchor = CENTER)

title_1.place(relx=0.5,y=200, anchor = CENTER)
title_2.place(relx=0.10,y=400)
title_3.place(relx=0.5,y=700, anchor = CENTER)
title_4.place(relx=0.75,y=400)

image1=Label(root)
image1.place(relx=0.5,y=270, anchor = CENTER)
l2=Label(root)
l2.place(relx=0.5,y=760, anchor = CENTER)
img_trans_show=Label(root)
img_trans_show.place(x=550,y=150)

root.mainloop()



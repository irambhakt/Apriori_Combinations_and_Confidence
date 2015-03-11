#!/bin/python
import copy
from pycsv import *
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import pylab as py
l= []
y= []
map= []
tmp = []
combi= []
ranks= [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

def init():
	global l
	global y
	print "#######Reading from file output of Apriori................. {press enter to start}"
	xx= raw_input()
	f= open('b.txt', 'r')
	content= f.readline()
	l= content.strip('[]\n')
	con = f.readline()
	f.close()
	x= l.split(" ")
	y= con.split("\t")
	y= y[0:27]
	l= x
	print "Frame-set ==>", l
	print "Summation of columns ==>", y
	print "\n\nFinish reading and formatting the data............"

def giveNum(s):
    return int(s[1:])  #returns the integer hidden in column

def getVal(n):
    return y[n]

def genVal(m):
    z= []
    for i in m:
        n= giveNum(i)
        n= int(getVal(n-1))
        z+= [{i: n}]
    return z


def genrateCombinations():
	print "\nGenrating the Combinations......................."
	global combi, cpy_combi
	global l
	for i in range(0,len(l)):
	   combi+= [l[i:i+1] + l[i+1:]+l[0:i]]

	for i in range(0,len(l)):
		for j in range(i+1,len(l)):
		    tmp = [l[i]]+[l[j]]
		    tmp1 = copy.copy(tmp)
		    combi += [tmp]
		    tmp1.reverse()
		    combi += [tmp1]

	print "\nCombinations genrated are ::"
	for i in combi:
		print i

def mapping(a):
    for i in map:
        if a in i:
            return i.values()

def calRank():
	print "\nPress enter to start calculating the Confidence..............."
	xx= raw_input()
	j=0
	global ranks, combi
	for a in combi:
		tmp= copy.copy(a)
		if(len(tmp) > 2):
			for i in range(0,len(a)):
				if (i == 0):
					tmp[i]= mapping(tmp[i])[0]
				else:
					tmp[i]= giveNum(tmp[i])
		else:
			for i in range(0, len(a)):
				tmp[i] = mapping(tmp[i])[0]
			#print tmp, len(tmp)
		if(len(tmp) > 2):
				ranks[j]= float(workForUnion(tmp[1:]))/float(tmp[0])
				j= j+1
		else:
			if((sum(tmp[1:])/tmp[0]) > -1):
				ranks[j]= float(sum(tmp[1:]))/float(tmp[0])
				j= j+1

def display():
	for i in range(0, len(combi)):
		print "combinations is %30s   |  confidence is %20s" %(combi[i], ranks[i])
	print ranks[0:10]

def plot_confidence():
	n = 9
	tmp= []
	x_ax= tuple(ranks[0:9])#py.linspace(0,2,9,0.3)
	#x_ax= tuple(ranks[0:9])
	ind= np.arange(n)
	width= 0.80
	x= range(0,11)
	y= [0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9]
	#py.subplot(x,y,'r')
	fig, ax= plt.subplots()
	ax.plot(x,y,color= 'lightcoral', linewidth=5)
	rect1= ax.bar(ind, x_ax,width, color='#8B1C62')
	#ax.legend(rect1[0],('men'))
	ax.set_title(' Apririo confidence graph for various combinations', fontsize=15)
	ax.set_ylabel('(Confidence in % ) * 100', fontsize=15)
	ax.set_xlabel('Factors affecting failure', fontsize=15)
	ax.set_xticks(ind+width-0.40)
	for i in combi:
		tmp+= i[0:2]
	print tuple(tmp)
	ax.set_xticklabels(tuple(combi), fontsize=9)
	def autolabel(rects):
		# attach some text labels
		for rect in rects:
			height = rect.get_height()
			ax.text(float(rect.get_x())+float(rect.get_width()/2.), 1.05*height,'%f'%float(height),ha='center', va='bottom')
   	autolabel(rect1)
	mng = plt.get_current_fig_manager()
	mng.full_screen_toggle()
	plt.show()

def pieChart():
	tmp= []
	for i in combi:
		tmp+= i[0:2]
	print tuple(tmp)
	labels= tuple(combi)#'a', 'b', '2', '3', '4','5', '6', '7','5'
	colors = ['#8B8B00', '#FFD343', '#8B475D', 'lightcoral', '#FF9900', '#8B668B', '#8B7765','#61B2A7', '#2869AF']
	explode= (0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,)
	#cs=cm.Set1(np.arange(9)/9.)
	fracs= ranks[0:len(combi)]
	py.pie(fracs, labels=labels, colors= colors, explode= explode, autopct='%1.1f%%', shadow=True, startangle=90)
	mng = plt.get_current_fig_manager()
	mng.full_screen_toggle()
	py.show('equal')


if __name__ == "__main__":
	os.system("javac AprioriAlgo.java")
	os.system("java AprioriAlgo > out.txt")
	os.system("clear")
	os.system("cat out.txt | head -8 | tail -2 > b.txt")
	init()
	map= genVal(l)
	#print map		
	genrateCombinations()
	readCSV()
	calRank()
	#print len(l_csv)
	display()
	#dispCSV()
	#print ranks
	#display()
	plot_confidence()
	pieChart()

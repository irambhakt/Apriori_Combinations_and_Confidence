#!/bin/python
import copy
from pycsv import *
import os
import itertools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import pylab as py
l = []
y = []
map = []
tmp = []
combi = []
pieCombi = []
globalRank = 0.0
ranks= range(0, 500)
for i in range(0, 500):
	ranks[i]= 0.0

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
	j= 0
	for i in l:
		if ',' in i:
			l[j] = i.strip(',')
		j = j + 1
	l = list(set(l))
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

'''
def genrateCombinations():
	print "\nGenrating the Combinations......................."
	global combi, cpy_combi
	global l
	for i in range(0,len(l)):
	   combi+= [l[i:i+1] + l[i+1:]+l[0:i]]

	for i in range(0,len(l)):
		for j in range(i+1,len(l)):              # This guy works for limited number of combinations, so don't use, kept for memories.
		    tmp = [l[i]]+[l[j]]
		    tmp1 = copy.copy(tmp)
		    combi += [tmp]
		    tmp1.reverse()
		    combi += [tmp1]

	print "\nCombinations genrated are ::"
	for i in combi:
		print i
'''

def rest(a, b):
    #print a, b
    for i in a:
        #print i
        try:
            b.remove(i)
        except:
            "not in list..."
    #print b , type(b)
    return b

def genrateCombinations():
    global l, combi
    j=0
    for i in range(1, len(l)):
        for x in itertools.combinations(l,i):
            #print x
            j = j+1
            combi.append(list(x))
    genXY()


def genXY():
    global l, combi
    j=0
    for i in combi:
        i.sort()
    for i in range(0,len(combi)):
        combi[i] = [combi[i]] + [rest(combi[i], copy.copy(l))]

def mapping(a):
    for i in map:
        if a in i:
            return i.values()
'''
def calRank():
	print "\nPress enter to start calculating the Confidence..............."
	xx= raw_input()
	j=0
	global ranks, combi, globalRank
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
'''
def stripping():
	global combi
	ii, jj, kk = 0, 0, 0
	for i in combi:
	    jj=0
	    for j in i:
	        kk=0
	        for k in j:
	            combi[ii][jj][kk] = giveNum(combi[ii][jj][kk])-1
	            kk = kk+1
	        jj = jj+1
	    ii=ii+1

def calGlobalUnion():
	global combi, globalRank
	print combi[0][0]+combi[0][1]
	globalRank = workForUnion(combi[0][0]+combi[0][1])
	print  workForUnion(combi[0][0]+combi[0][1])
	return globalRank

def calRank():
	print "\nPress enter to start calculating the Confidence..............."
	xx= raw_input()
	j=0
	global ranks, combi, globalRank
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
	global combi
	n = len(ranks)
	tmp= []
	x_ax= tuple(ranks[0:n])#py.linspace(0,2,9,0.3)
	#x_ax= tuple(ranks[0:9])
	ind= np.arange(n)
	width= 0.80
	x= range(0,11)
	y= [0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9,0.9] # these x, y are for the straight line.
	#py.subplot(x,y,'r')
	fig, ax= plt.subplots()
	ax.plot(x,y,color= 'lightcoral', linewidth=2)
	rect1= ax.bar(ind, x_ax,width, color='#8B1C62')
	#ax.legend(rect1[0],('men'))
	ax.set_title(' Apririo confidence graph for various combinations', fontsize=17)
	ax.set_ylabel('(Confidence in % ) * 100', fontsize=15)
	ax.set_xlabel('Factors affecting failure', fontsize=15)
	ax.set_xticks(ind+width-0.40)
	for i in combi:
		tmp+= i[0:2]
	print tuple(tmp)
	ax.set_xticklabels(tuple(combi), fontsize=7)
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
	global ranks, combi
	tmp= []
	for i in combi:
		tmp+= i[0:2]
	print tuple(tmp)
	labels= tuple(pieCombi)#'a', 'b', '2', '3', '4','5', '6', '7','5'
	colors_list = ['#8B8B00', '#FFD343', '#8B475D', 'lightcoral', '#FF9900', '#8B668B', '#8B7765','#61B2A7', '#2869AF']
	j = 0
	colors= range(0, len(ranks))
	for i in range(0, len(ranks)):
		colors[i] = colors_list[j]
		j = i%len(colors_list)

	explode_list= range(0, len(ranks))
	for i in range(0, len(ranks)):
		explode_list[i] = 0.1
	explode = tuple(explode_list)
	#cs=cm.Set1(np.arange(9)/9.)
	fracs= ranks[0:len(combi)]
	py.pie(fracs, labels=labels, colors= colors, explode= explode, autopct='%1.1f%%', shadow=True, startangle=90)
	mng = plt.get_current_fig_manager()
	mng.full_screen_toggle()
	py.show('equal')


def moreThan90():
	global ranks, combi, pieCombi
	r= []
	j=0
	for i in ranks:
		if i > 0.89:
			r += [i]
			pieCombi += [combi[j]]
		j=j+1
	ranks = r
	print len(ranks), len(pieCombi)


if __name__ == "__main__":
	os.system("javac AprioriAlgo.java")
	os.system("java AprioriAlgo > out.txt")
	os.system("clear")
	os.system("cat out.txt | tail -2 > b.txt")
	init()
	map= genVal(l)
	#print map
	genrateCombinations()
	stripping()
	print len(combi)
	for i in combi:
		print i
	print globalRank
	xx = raw_input()
	readCSV()
	print calGlobalUnion()
	calRank()
	#print len(l_csv)
	display()
	#dispCSV()
	#print ranks
	#display()
	moreThan90()
	plot_confidence()
	pieChart()

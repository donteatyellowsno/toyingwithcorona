#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 00:50:18 2020

@author: gingerale
"""

import numpy as np
import numpy.random as random
import matplotlib.pyplot as pp
going=365

global y #data
y=[4,4,6,10,15,23,27,35,90,262,340,674,801]#,827,864,914,914]
#https://virusncov.com/covid-statistics/denmark
#simulate given parameters
def symptom(meet,rate,going):
    timeill=14#days ur ill
    global timeearl
    timeearl=4#days until you spread desease
    timeimun=3*7#days ur imune after sick. i guestimated 1 month since the first are already reinfected.
    cont=np.zeros(timeill)#number of infected and stage of approximated 2 week contageous, dunno if tht is the correct number of days
    cont[0]=1#patient zero in country
    health=800000#danes in copenhagen
    dead=0#self explanatory using german rate 1 death every 500 or so...
    imune=np.zeros(timeimun)
    r=rate#probability getting infected during encounter
    meet=meet#number of encounters in a day, can be simply touching handles and stuff
    x=[1]#keeping track of total infected with symptoms each day
    fatalities=[0]#keepin track of fatalities
    contagestage=np.zeros(timeearl)#infected but not contageous
    for n in range(timeearl+going):
        #encountering healthy people approximately
        if n>timeearl+len(y):
            meet=1#danish government reacted by not testing anymore and keeping most people home
            #rate=0.01#people practice more caution touching face hugs handwash
        meethealthy=random.binomial(meet*int(sum(cont)),health/(health+sum(contagestage)+sum(cont)+sum(imune)))
        if meethealthy>health:
            meethealthy=health
        health+=imune[n%timeimun]
        enddes=cont[(n+1)%timeill]
        thisdead=random.binomial(enddes,0.002)
        dead+=thisdead
        imune[n%timeimun]=enddes-thisdead#people recovering from sickness at end of desease
        cont[(n+1)%timeill]=contagestage[(n)%timeearl]#people turning contageous
        new=random.binomial(meethealthy,r)#newly infected
        contagestage[n%timeearl]=new#updating stage of contagestage
        health-=new#subtracting healthy people
        x.append(int(sum(cont)))#updating total sick people with symptoms
        fatalities.append(dead)
    return x,fatalities
best=[0,0,100000000000000]
montecarlos=20
#calculating a parameter that has the least error to the data
"""
for n in range(2,60):#number of people you rub their fluids in your face into
    for k in np.linspace(0.01,0.4,20):#chance of infection
        #monte carlo average trajectory
        result=[(np.array(symptom(n,k,len(y))[0][timeearl:len(y)+timeearl])) for j in range(montecarlos)]
        resul=[np.average([result[j][p] for j in range(montecarlos)]) for p in range(len(y))]#averaging tht monte carlo
        test=(np.array(y)-resul)#findin dat error or variance from data or watever
        new=np.dot(test,test)
        if new<best[2]:#finding a winner among parameters in the most inefficient way
            best[0]=n
            best[1]=k
            best[2]=new
"""
#this is my parameter calculated from 20 monte carlo experiments,
#feel free to uncomment out the commented out part and comment out my parameters
#to figure out your own parameters
best=[23, 0.19473684210526315, 37544.84499999998]
x,fat=symptom(best[0],best[1],going)#longrun experiment using found parameters
#t2=np.arange(len(y))+timeearl
#pp.plot(t2,y,label="data")
pp.figure()
pp.title("infected over time with data")
t1=np.arange(going+1+timeearl)
pp.plot(t1,x,label="prediction")
t2=np.arange(len(y))+timeearl
pp.plot(t2,y,label="data")
pp.ylabel("infected")
pp.xlabel("days")
#pp.ylim(0,1000)
pp.legend()
pp.figure()
pp.title("deaths")
pp.plot(t1,(np.array(fat)))
pp.ylabel("deaths (deaths+1)")
pp.xlabel("days")
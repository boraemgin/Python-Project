# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 20:10:51 2018

@author: user
"""

import os, time
import numpy as np
import matplotlib.pyplot as plt
'''
AIRFOILS THAT CANNOT OPENED
'''
cannotopen = []
def get_good_files (filename):
        
    try :
        with open ("coord_seligFmt/"+filename) as f:
            content = f.readlines()
    
    except:
        cannotopened.append(filename)
        print(filename, 'can not be opened')
        time.sleep(0.5)
        
    return cannotopen
    
for i, j, k in os.walk("coord_seligFmt/") :
    
    for i in k:
        
         [get_good_files(i)]
'''
GETTING AIRFOIL COORDINATES
'''
def get_foil_coordinates(filename):
    with open(filename) as f:
        content = f.readlines()
    arr = []
    for i in content:
        elements = i.strip().split()
    
        if len(elements) == 2:
    
            try:    
                x,y = float(elements[0]), float(elements[1])
                arr.append([x,y])
            except:
                pass
    return np.array(arr)
for i,j,k in os.walk('coord_seligFmt/'):
    k = [n for n in k if n not in cannotopen];  
    for i,j in enumerate(k):       
        filename = 'coord_seligFmt/' + j
        foil = get_foil_coordinates(filename)
        x,y = foil[:,0],foil[:,1]
        location = [a for a, b in enumerate(foil[:,0]) if b == min(x)]
        up=[]
        down=[]
        for i in range(len(foil)):
            if i <= location[0]:
                up.append(foil[i,1]) 
            else:
                down.append(foil[i,1])
        if len(up) != len(down):
            print(j)
            down.insert(0,min(x))
        up.reverse()
        '''
        CAMBER LINE
        '''
        camber=[]
        for i in range(min(len(up),len(down))):
            camber.append((up[i]+down[i])/2)
        '''
        MAXIMUM THICKNESS
        '''
        thicknesses=[]
        for i in range(min(len(up),len(down))):
            thicknesses.append(up[i]-down[i])
        maxthickness = max(thicknesses)
        maxthicknesslocation = [a for a, b in enumerate(thicknesses) if b == maxthickness]
        '''
        PANEL
        '''
        a = []
        b = []
        teta = []
        panel = 0
        while panel <= len(x)-1:
            a=np.append(a,x[panel])
            b=np.append(b,x[panel])
            panel += 1
        for loop, item in enumerate(range(0,len(b)-1)):
            if b[loop+1]>b[loop]:
                dy = b[loop+1]-b[loop]
            else:
                dy = b[loop]-b[loop+1]               
            dx = a[loop+1]-a[loop]
            M1 = dy/dx
            M2 = -1/M1
            teta = np.append(teta, (np.arctan(M2)))
            u = np.cos(teta)
            v = np.sin(teta)
        '''
        KUTTA CONDITION
        '''
        def Kutta_condition(a,b):
            w = []
            z = []
            for loop, item in enumerate(b):
                if(loop == int(1)):
                    break
                dyup = b[loop+1]-b[loop]
                dxup = a[loop+1]-a[loop]
                m1up = dyup/dxup
            n = a[::-1]
            m = b[::-1]
            for i in range(0, 2):
                w = np.append(w, n[i])
                z = np.append(z, m[i])
            for i, item in enumerate(w):
                if(i == int(1)):
                    break
                dylower = z[i]-z[i+1]
                dxlower = w[i]-w[i+1]
                m1lower = dylower/dxlower
                if(abs(m1up) == abs(m1lower)):
                    condition = print('AIRFOIL IS POINTED')
                else:
                    condition = print('AIRFOIL IS CUSPED')
                return condition
        
        print(j,len(x),len(y))
    
        plt.plot(x,y)
        plt.xlim(-0.01,1.01)
        plt.ylim(-0.25,0.25)
        plt.title(j)
        plt.axes().set_aspect('equal')
        plt.plot(x,y)
        location = [a for a, b in enumerate(foil[:,0]) if b == min(foil[:,0])] #location y when x = 0
        plt.plot([max(x),foil[0,1]],[min(x),foil[location[0],1]],label='Chord Line') #because chord line is a straight line that is from airfoils leading edge to trailing edge
        plt.plot(np.linspace(min(x),max(x),len(camber)),camber,label='Mean Camber Line')
        plt.vlines(x = (foil[len(thicknesses)+int(maxthicknesslocation[0]),0]),ymin=down[maxthicknesslocation[0]],ymax=up[maxthicknesslocation[0]],label='Maximum Thickness')
        plt.quiver(a,b,u,v)
        Kutta_condition(a,b)
        plt.plot()
        plt.legend()
        plt.show()
        
        time.sleep(0.1)

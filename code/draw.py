from fileinput import filename
from tkinter import *
from turtle import color
from turtle import left
import xml.etree.ElementTree as ET
from PIL import ImageTk,Image,ImageGrab
import urllib.request, base64
from cProfile import label
from skimage import feature
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from tkinter import *
from turtle import left
from PIL import ImageTk,Image

from matplotlib import container

root = Tk()



screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry("%dx%d+5+5"%(screen_width-50,screen_height-50))


def draw_line(event):
   global finsh
   global number_click 
   global click_number
   global line2
   global x1
   global y1
   global x2
   global y2
   global list
   global green_line
   if not(finsh):
        if(x1==0 & y1==0):
             x1=event.x
             y1=event.y
             pointList.append([x1,y1])
        else:
             x2=event.x
             y2=event.y
             if(green_line):
                 canvas.delete(green_line)
             green_line= canvas.create_line(pointList[0][0],pointList[0][1],x2,y2,fill='green',width=2)
             element=canvas.create_line(x1,y1,x2,y2,fill='red',width=2)
             list.append(element)
             click_number = 0
             x1=x2
             y1=y2
             pointList.append([x1,y1])


def deleteLine():
    global finsh
    global list
    global green_line
    global pointList
    global x1 
    global y1
    if not(finsh):
        if(len(list)):
            canvas.delete(list.pop())
            pointList.pop()
            if(green_line):
                canvas.delete(green_line)
                green_line= canvas.create_line(pointList[0][0],pointList[0][1],pointList[-1][0],pointList[-1][1],fill='green',width=2)
            print(pointList)
            [x1,y1]=pointList[-1]
        if((len(pointList))==1):
            pointList.pop()
            x1=y1=0
           
    


def deleteAll():
    global finsh
    global list
    global x1 
    global y1
    finsh = 0
    x1=y1=0
    global green_line 
    global pointList
    while(len(list)):
        canvas.delete(list.pop(),green_line)
    pointList=[]
    green_line=None
    

def Finsh():

    global list
    global green_line 
    global pointList
    global finsh

    # we make root element
    xmlList =ET.Element("pointList")
    # create sub element
    
    # insert pointlist element into sub elements
    sum=0
    perimetre=0
    desc = ET.SubElement(xmlList, "Titre")
    desc.text = e.get()
    desc = ET.SubElement(xmlList, "Identification_de_la_patiente")
    desc.text = ident.get()
    desc = ET.SubElement(xmlList, "Indications")
    desc.text = indic.get()
    coordinates = ET.SubElement(xmlList, "coordinates")
    for point in range(len(pointList)):

        coordinate = ET.SubElement(coordinates, "coordinate")
        absciss = ET.SubElement(coordinate, "absciss")
        absciss.text = str(pointList[point][0])
        ordinate = ET.SubElement(coordinate, "ordinate")
        ordinate.text = str(pointList[point][1])
        perimetre+= (((( pointList[point][0]- pointList[point-1][0] )**2) + ((pointList[point][1]-pointList[point-1][1])**2) )**0.5)
        
    peri = ET.SubElement(xmlList, "perimetre")
    peri.text = str(perimetre*0.21)+" mm"
    

    tree = ET.ElementTree(xmlList)
    # write the tree into an XML file
    tree.write("contoure_edge_points.xml", encoding ='utf-8', xml_declaration = True)
		
    finsh =1

    if(len(list)):

        canvas.delete(green_line)
        list.append(canvas.create_line(pointList[0][0],pointList[0][1],pointList[-1][0],pointList[-1][1],fill='red',width=2))
        green_line=None



line2=None
pointList=[]
list=[]
element=None
click_number=0
x1=x2=y1=y2=0
number_click=5
green_line =None
finsh =0



img= (Image.open("cancer6.jpg"))

#Resize the Image using resize method
resized_image= img.resize((int(screen_width*0.75)-10,int(screen_height*0.75)), Image.ANTIALIAS)
new_image= ImageTk.PhotoImage(resized_image)

#Add image to the Canvas Items
pbp=False
def pbpF():
    global pbp
    pbp=not pbp
    print(pbp)
canvas = Canvas(root, bg="blue",width=int(screen_width*0.75)-10,height=int(screen_width*0.4)-10)
canvas.grid(row=1,rowspan = 4) 
canvas.create_image(0,0, anchor=NW, image=new_image)
canvas.bind('<Button-1>',draw_line)
canvas.bind('<Button-3>',deleteLine)



container = Frame(root)
container.grid(row=1,column=2, pady = 5) 
button1=Button(container, text='DeleteAll!', command=deleteAll,fg="#CC3300",bg="#a9c3f9", width=15)
button1.grid(row=1,column=1, pady = 5)
button=Button(container, text='Back!', command=deleteLine,fg="#CC3300",bg="#a9c3f9",width=15)
button.grid(row=2,column=1, pady = 5)
button1=Button(container, text='Finsh!', command=Finsh,fg="#CC3300",bg="#a9c3f9", width=15)
button1.grid(row=3,column=1,pady = 5)

myLabel =Label(container,text=" ",font=('Arial 12'))
myLabel.grid(row=5,column=1,padx = 2, pady = 5)
myLabel =Label(container,text=" ",font=('Arial 12'))
myLabel.grid(row=6,column=1,padx = 2, pady = 5)
myLabel =Label(container,text=" ",font=('Arial 12'))
myLabel.grid(row=7,column=1,padx = 2, pady = 5)


myLabel =Label(container,text="Titre: ",font=('Arial 12'))
myLabel.grid(row=11,column=1,padx = 2, pady = 5)
e=Entry(container,width=40, fg="blue",borderwidth=5, font=('Arial 12'))
e.insert(0,"")
e.grid(row=12,column=1,padx = 2, pady = 5)

myLabel =Label(container,text="Identification de la patiente: ",font=('Arial 12'))
myLabel.grid(row=13,column=1,padx = 2, pady = 5)
ident=Entry(container,width=40, fg="blue",borderwidth=5, font=('Arial 12'))
ident.insert(0,"")
ident.grid(row=14,column=1,padx = 2, pady = 5)

myLabel =Label(container,text="Indications:",font=('Arial 12'))
myLabel.grid(row=15,column=1,padx = 2, pady = 5)
indic=Entry(container,width=40, fg="blue",borderwidth=5, font=('Arial 12'))
indic.insert(0,"")
indic.grid(row=16,column=1,padx = 2, pady = 5)


root.mainloop()

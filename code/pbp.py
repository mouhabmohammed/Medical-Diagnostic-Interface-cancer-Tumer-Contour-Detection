from fileinput import filename
from tkinter import *
from turtle import color
from turtle import left
from PIL import ImageTk,Image,ImageGrab
import urllib.request, base64

root = Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry("%dx%d+5+5"%(screen_width-10,screen_height-10))

def save_as_jpg(canvas,fileName):
    # save postscipt image 
    canvas.postscript(file = fileName + '.eps') 
    # use PIL to convert to PNG 
    img = Image.open(fileName + '.eps') 
    img.save(fileName + '.jpg', 'jpg') 

def getter(widget):
    x=root.winfo_rootx()+canvas.winfo_x()
    y=root.winfo_rooty()+canvas.winfo_y()
    x1=x+canvas.winfo_width()
    y1=y+canvas.winfo_height()
    ImageGrab.grab().crop((x,y,x1,y1)).save("cancer7.jpg")

def paint(event):
    color="red"
    x1,y1=(event.x-1),(event.y-1)
    x2,y2=(event.x+1),(event.y+1)
    canvas.create_oval(x1,y1,x2,y2,fill=color,outline=color)

img= (Image.open("cancer6.jpg"))

#Resize the Image using resize method
resized_image= img.resize((int(screen_width*0.75)-10,int(screen_height*0.75)), Image.ANTIALIAS)
new_image= ImageTk.PhotoImage(resized_image)

#Add image to the Canvas Items


canvas = Canvas(root, bg="white")
canvas.pack(expand=YES,fill=BOTH)
canvas.create_image(10,10, anchor=NW, image=new_image)
canvas.bind('<B1-Motion>',paint)

myBottun=Button(root, text='Click Me!', command=lambda: save_as_jpg(canvas,"fileName"),fg="red",bg="blue")
myBottun.pack(side=BOTTOM)

root.mainloop()
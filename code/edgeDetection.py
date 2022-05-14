from cProfile import label
from skimage import feature
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from tkinter import *
from turtle import left
from PIL import ImageTk,Image
 
def edge_detection(filename,sw,sh,x,y):
    image = cv2.imread(filename)

    image=cv2.resize(image, (int(sw*0.75)-10,int(sh*0.75)))
#gray 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY, 0.7)
#seuillage
    (T, thresh) = cv2.threshold(gray, x, 255, cv2.THRESH_BINARY)

#cv2.getStructuringElement()est utilisé pour définir un élément structurel comme elliptique, circulaire, rectangulaire
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 5))
    #cv2.morphologyEx() fait la différence entre la dilatation et l'érosion d'une image.
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
#transformer la forme rugueuse du contour à une forme lisse
#opérations morphologiques pour supprimer la partie indésirable de l'image de seuillage
    closed = cv2.erode(closed, None, iterations = 14)
    closed = cv2.dilate(closed, None, iterations = 13)

    def auto_canny(image, sigma=0.33):
        # compute the median of the single channel pixel intensities
        v = np.median(image)*2
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        # Lissez l'image à l'aide d'un filtre gaussien pour supprimer le bruit à haute fréquence
        #Calculez les représentations d'intensité du gradient de l'image.
        #Appliquez une suppression non maximale pour supprimer les réponses "fausses" à la détection des contours.
        #Appliquez le seuillage à l'aide d'une limite inférieure et supérieure sur les valeurs de gradient.
        #suivez les bords à l'aide de l'hystérésis en supprimant les bords faibles qui ne sont pas connectés aux bords forts.
        edged = cv2.Canny(image, lower, upper)

        return edged

    canny = auto_canny(closed)

    (cnts, _) = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(image, cnts, -1, (255, 0, 0), 1,)

    return image



class Detection:
    def __init__(self,master,image) : 
        self.sw = master.winfo_screenwidth()
        self.sh = master.winfo_screenheight()
        print(self.sw,self.sh)
        frame0 = Frame(master,highlightbackground="#9c8985", highlightthickness=2,width=self.sw*0.1,height=self.sh*0.75)
        # frame1.pack_propagate(0)
        # frame0.pack( side='left', expand='True')

        self.label0= Label(frame0,text="nothing...").pack()
        self.e0=Entry(frame0,width=20,fg="blue",borderwidth=5)
        self.e0.insert(0,"")
        self.e0.pack()
        master.geometry("%dx%d+5+5"%(self.sw-10,self.sh-10))
        frame1 = Frame(master,highlightbackground="#9c8985", highlightthickness=2,width=self.sw*0.75,height=self.sh*0.75)
       # frame1.pack_propagate(0)
        frame1.pack( side='right', expand='True')

        #Create a canvas
        canvas= Canvas(frame1, width= self.sw*0.75, height= self.sh*0.75)
        canvas.pack()
        #Load an image in the script
        # img= (Image.open("image5.jpg"))
        img = Image.fromarray(image, "RGB")
        #Resize the Image using resize method
        self.resized_image=img.resize((int(self.sw*0.75)-10,int(self.sh*0.75)), Image.ANTIALIAS)
        self.new_image= ImageTk.PhotoImage(self.resized_image)

        #Add image to the Canvas Items
        canvas.create_image(10,10, anchor=NW, image=self.new_image)
        canvas.mainloop()
        # canvas.mainloop()
root=Tk()
img=edge_detection('cancer6.jpg',750,750,145,145)
Detection(root,img)
root.mainloop()
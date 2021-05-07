import cv2 #Fotağrafı işlemek için
import easygui
import numpy as np #Fotağrafı saklamak için
import imageio #Fotağrafı almak için

import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image



top=tk.Tk()
top.geometry('500x500')
top.title(' Fotağraf Karikatürleştirme ')
top.configure(background='black')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

def yukleme():
    Fotagraf=easygui.fileopenbox()
    karikaturlestirme(Fotagraf)


def karikaturlestirme(Fotagraf):
    
    # fotagrafı oku
    gercekfotograf = cv2.imread(Fotagraf)
    
    gercekfotograf = cv2.cvtColor(gercekfotograf, cv2.COLOR_BGR2RGB)
                      

    # fotografın seçildiğini onayla
    if gercekfotograf is None:
        print("bulunmadı")
        sys.exit()

    ReSized1 = cv2.resize(gercekfotograf, (960, 540))
    #plt.imshow(ReSized1, cmap='gray')

    #gri ile dönüştürme
    grayScaleImage= cv2.cvtColor(gercekfotograf, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))
    #plt.imshow(ReSized2, cmap='gray')


    #yumusatmak için blur
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))
    #plt.imshow(ReSized3, cmap='gray')

    #çizgi film efekti için kenarların alınması.
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 9, 9)

    ReSized4 = cv2.resize(getEdge, (960, 540))
    #plt.imshow(ReSized4, cmap='gray')


    #kenari keskin olması lazım
    renkliFoto = cv2.bilateralFilter(gercekfotograf, 9, 300, 300)
    ReSized5 = cv2.resize(renkliFoto, (960, 540))
    #plt.imshow(ReSized5, cmap='gray')


    #maskeleme işlemi
    karikatur = cv2.bitwise_and(renkliFoto, renkliFoto, mask=getEdge)

    ReSized6 = cv2.resize(karikatur, (960, 540))
    #plt.imshow(ReSized6, cmap='gray')

    images=[ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    kaydet1=Button(top,text="Fotoğrafı Kaydet",command=lambda: kaydet(ReSized6, Fotagraf),padx=30,pady=5)
    kaydet1.configure(background='#364156', foreground='red',font=('calibri',10,'bold'))
    kaydet1.pack(side=TOP,pady=50)
    
    plt.show()
    
    
def kaydet(ReSized6, Fotagraf):
    yeniAD="Karikatur "
    path1 = os.path.dirname(Fotagraf)
    extension=os.path.splitext(Fotagraf)[1]
    path = os.path.join(path1, yeniAD+extension)
    cv2.imwrite(path, cv2.cvtColor(ReSized6, cv2.COLOR_RGB2BGR))
    I= "Fotağrafı " + yeniAD +"Adı ile Kaydet           "+ path
    tk.messagebox.showinfo(title=None, message=I)




yukleme=Button(top,text="Karikatürleştirmek İstediğin Resmi Seç",command=yukleme,padx=10,pady=5)
yukleme.configure(background='#364156', foreground='red',font=('calibri',10,'bold'))
yukleme.pack(side=TOP,pady=50)

top.mainloop()




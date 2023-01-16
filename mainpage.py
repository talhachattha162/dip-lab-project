import os
from tkinter import *
from tkinter import filedialog
import tkinter
from tkinter.messagebox import showinfo
import cv2
import matplotlib.pyplot as plt
from PIL import Image,ImageEnhance, ImageOps, ImageTk
import numpy as np
from tkinter.messagebox import showerror, showwarning, showinfo
#install for wand.image
#apt-get install libmagickwand-dev
#pip install Wand
from wand.image import Image as  wandImage
#pip install rembg
from rembg import remove
from PIL import ImageFilter

path=''
paths=[]

#image processing

def brightness(image,brightnessvalue):
  brightnessvalue=brightnessvalue/50
  enhancer = ImageEnhance.Brightness(image)
  brightnessimage=enhancer.enhance(brightnessvalue)
  return brightnessimage

def contrast(image,contrastvalue):
  contrastvalue=contrastvalue/50
  enhancer = ImageEnhance.Contrast(image)
  contrastimage = enhancer.enhance(contrastvalue)
  return contrastimage

def saturation(image,saturationvalue):
  saturationvalue=saturationvalue/50
  enhancer = ImageEnhance.Color(image)
  saturationimage = enhancer.enhance(saturationvalue)
  return saturationimage

def sharpness(image,sharpnessvalue):
  sharpnessvalue=sharpnessvalue/50
  enhancer = ImageEnhance.Sharpness(image)
  sharpnessimage = enhancer.enhance(sharpnessvalue)
  return sharpnessimage

def exposure(image,gammavalue):
  gammavalue=gammavalue/50
  image=convertToCv2Image(image)
  gamma_corrected=np.array(255*(image/255)**gammavalue,dtype='uint8')
  gamma_corrected=convertToPillowImage(gamma_corrected)
  return gamma_corrected

def tint(path,percentage):
  percentage=percentage/2
  with wandImage(filename=path) as image:
    image.tint(color ="green", alpha =f"rgb({percentage} %, 60 %, 80 %)")
    tintimage = np.array(image)
  tintimage=convertToPillowImage(tintimage)
  return tintimage

def convertToPillowImage(cv2image):
  pillowimage=Image.fromarray(cv2image)
  return pillowimage

def convertToCv2Image(pillowimage):
  cv2image=np.asarray(pillowimage)
  return cv2image

def gray(image):
  image=convertToCv2Image(image)
  grayimage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  grayimage=convertToPillowImage(grayimage)
  return grayimage

def negative(image):
  negativeimage = ImageOps.invert(image)
  return negativeimage


def resize(image,width,height):
  resizedimage=image.resize((width,height))
  return resizedimage

def flipping(image,flippedtype):#flipped type means horizontal or vertical
  if(flippedtype=='horizontal'):
    flippedImage = image.transpose(Image.FLIP_LEFT_RIGHT)
  elif(flippedtype=='vertical'):
    flippedImage = image.transpose(Image.FLIP_TOP_BOTTOM)
  return flippedImage

def rotate(image,angle):
  rotate_img= image.rotate(angle)
  return rotate_img

def calculateHistogram(image,path):
  image=convertToCv2Image(image)
  plt.hist(image[:,:,0])
  plt.savefig('hist.png')
  image=Image.open('hist.png')
  return image


def collage(imagespath,totalimgs):
    if totalimgs<=3:
      x=totalimgs*500
      y=500
    elif totalimgs==4 :
      x=1000
      y=1000
    elif totalimgs==5:
      x=2500
      y=500
    elif totalimgs==6:
      x=1500
      y=1000
    elif totalimgs==7:
      x=3500
      y=500
    elif totalimgs==8:
      x=2000
      y=1000
    elif  totalimgs==9:
      x=1500
      y=1500
    collageimage = Image.new(mode="RGB", size=(x, y))
    c=0
    for i in range(0,x,500):
        for j in range(0,y,500):
            photo = Image.open(imagespath[c])
            photo = photo.resize((500,500))        
            c+=1
            collageimage.paste(photo, (i,j))
    return collageimage


def removeBackground(image):
  output = remove(image)
  return output


def watermark(logo,image):
# height and width of the watermark image
  wm=convertToCv2Image(logo)
  image=convertToCv2Image(image)
  print(image.shape)
  h_wm, w_wm = wm.shape[:2]
# height and width of the image
  h_img, w_img = image.shape[:2]
# calculate coordinates of center of image
  center_x = int(w_img/2)
  center_y = int(h_img/2)
# calculate rio from top, bottom, right and left
  top_y = center_y - int(h_wm/2)
  left_x = center_x - int(w_wm/2)
  bottom_y = top_y + h_wm
  right_x = left_x + w_wm
# add watermark to the image
  roi = image[top_y:bottom_y, left_x:right_x]
  wm=cv2.resize(wm, (roi.shape[1], roi.shape[0]))
  result = cv2.addWeighted(roi, 1, wm, 0.3, 0)
  result=convertToPillowImage(result)
  return result


def pencilSketchGray(image):
    image=convertToCv2Image(image)  
    #sigma_s=>Range between 0 to 200
    #sigma_s=>Just like other smoothing filters sigma_s controls the size of the neighborhood
    #sigma_r Range between 0 to 1
    #sigma_r=>controls the how dissimilar colors within the neighborhood will be averaged
    #shade_factor ( range 0 to 0.1 ) is a simple scaling of the output image intensity.
    #The higher the value, the brighter is the result.
    sketchgrayimage, sketchcolorimage = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.1) 
    sketchgrayimage=convertToPillowImage(sketchgrayimage)
    return  sketchgrayimage

def pencilSketchColor(image):
    image=convertToCv2Image(image)  
    #sigma_s=>Range between 0 to 200
    #sigma_s=>Just like other smoothing filters sigma_s controls the size of the neighborhood
    #sigma_r Range between 0 to 1
    #sigma_r=>controls the how dissimilar colors within the neighborhood will be averaged
    #shade_factor ( range 0 to 0.1 ) is a simple scaling of the output image intensity.
    #The higher the value, the brighter is the result.
    sketchgrayimage, sketchcolorimage = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.1) 
    sketchcolorimage=convertToPillowImage(sketchcolorimage)
    return  sketchcolorimage

def addText(image,text,x,y):
  image=convertToCv2Image(image)
  cv2.putText(img=image, text=text, org=(x, y), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(0, 255, 0),thickness=2)
  image=convertToPillowImage(image)
  return image

def removeNoise(image,H):
  # Convert the image to grayscale
  cv2image=convertToCv2Image(image)
  gray_im=gray(cv2image)
  cv2image=convertToCv2Image(gray_im)
  # Apply a denoising filter
  denoised_image = cv2.fastNlMeansDenoising(cv2image, None, H, 7, 21)
  #Big h value perfectly removes noise 
  #but also removes image details, smaller h value preserves details but also preserves some noise
  #window_size
  #Size in pixels of the window that is used to compute weighted average for given pixel. Should be odd. 
  #Affect performance linearly: greater search_window - greater denoising time. Recommended value 21 pixels
  #blocksize
  #Size in pixels of the template patch that is used to compute weights. Should be odd. 
  #Recommended value 7 pixels
  denoised_image=convertToPillowImage(denoised_image)
  return denoised_image

def blur(image):
  blurimage=image.filter(ImageFilter.GaussianBlur(radius=7))
  return blurimage

def contour(image):
  countourimage=image.filter(ImageFilter.CONTOUR)
  return countourimage

def detail(image):
  detailimage=image.filter(ImageFilter.DETAIL)
  return detailimage

def edgeEnhance(image):
  edgeenhancedimage=image.filter(ImageFilter.EDGE_ENHANCE)
  return edgeenhancedimage

def edgeEnhancePro(image):
  edgeenhancedproimage=image.filter(ImageFilter.EDGE_ENHANCE_MORE)
  return edgeenhancedproimage

def emboss(image):
  embossimage=image.filter(ImageFilter.EMBOSS)
  return embossimage

def findEdges(image):
  findedges=image.filter(ImageFilter.FIND_EDGES)
  return findedges
  
#end
#image proccessing


#start
#utils

def newWindow(text):
    window=Tk()
    window.title(text)
    window.geometry("900x600")
    return window

def destroy_window(window):
    window.destroy()


def select_file():
    global path
    path1= filedialog.askopenfilename(initialdir='/home/talha/Pictures/') 
    path=path1

def select_files():
    global paths
    path1= filedialog.askopenfilename(initialdir='/home/talha/Pictures/',multiple=True) 
    paths=path1

def select_fileRotateResizeFlip(width,height,angle):
    select_file()
    image = Image.open(path)
    w,h=image.size
    width.set(w)
    height.set(h)
    angle.set(0.0)

def download2(image,name,ext):
    new_file_name =  f"{name}.{ext}"
    new_file_path = os.path.join('/home/talha/Downloads/', new_file_name)
    image.save(new_file_path)

def convertImageExtTo(image,name,imageext):
  rgb_image = image.convert("RGB")
  rgb_image.save(f"{name}.{imageext}")

#end
#utils


#main page

def mainPage():
    window1=newWindow('PhotoEditor')
    btn=Button(window1, text="Adjust Image", fg='green',command=lambda:gotoAdjustPage(window1))
    btn.pack()
    btn=Button(window1, text="Tint Image", fg='green',command=lambda:gotoTintPage(window1))
    btn.pack()
    btn=Button(window1, text="Gray and Negative Image", fg='green',command=lambda:gotoGrayAndNegativePage(window1))
    btn.pack()
    btn=Button(window1, text="Resize,Rotate,Flip Image", fg='green',command=lambda:gotoResizeRotateFlipPage(window1))
    btn.pack()
    btn=Button(window1, text="Histogram of Image", fg='green',command=lambda:gotoHistogramPage(window1))
    btn.pack()
    btn=Button(window1, text="Change the image extension", fg='green',command=lambda:gotoChangeImageExtPage(window1))
    btn.pack()
    btn=Button(window1, text="Make Collage", fg='green',command=lambda:gotoCollagePage(window1))
    btn.pack()
    btn=Button(window1, text="Remove Background", fg='green',command=lambda:gotoRemoveBackgroundPage(window1))
    btn.pack()
    btn=Button(window1, text="Add WaterMark", fg='green',command=lambda:gotoAddWaterMarkPage(window1))
    btn.pack()
    btn=Button(window1, text="Pencil Effect", fg='green',command=lambda:gotoPencilEffectPage(window1))
    btn.pack()
    btn=Button(window1, text="Add Text in image", fg='green',command=lambda:gotoAddTextPage(window1))
    btn.pack()
    btn=Button(window1, text="Remove Noise", fg='green',command=lambda:gotoRemoveNoisePage(window1))
    btn.pack()
    btn=Button(window1, text="Blur,Contour,Detail", fg='green',command=lambda:gotoBlurContourDetailPage(window1))
    btn.pack()
    btn=Button(window1, text="Edge Enhancer,Edge Ehancer Pro", fg='green',command=lambda:gotoEdgeEnhancerWithProPage(window1))
    btn.pack()
    btn=Button(window1, text="Emboss,Find Edges", fg='green',command=lambda:gotoEmbossFindEdgesPage(window1))
    btn.pack()
    window1.mainloop()
#end
#main page

#goto Navigations
#start

def gotoMainPage(window):
    destroy_window(window=window)
    mainPage()

def gotoAdjustPage(window):
    destroy_window(window=window)
    AdjustPage()

def gotoTintPage(window):
    destroy_window(window=window)
    TintPage()
def gotoGrayAndNegativePage(window):
    destroy_window(window=window)
    GrayAndNegativeImagePage()
def gotoResizeRotateFlipPage(window):
    destroy_window(window=window)
    ResizeRotateFlipImagePage()
def gotoHistogramPage(window):
    destroy_window(window=window)
    histogram()
def gotoChangeImageExtPage(window):
    destroy_window(window=window)
    ChangeImageExtPage()
def gotoCollagePage(window):
    destroy_window(window=window)
    CollagePage()
def gotoRemoveBackgroundPage(window):
    destroy_window(window=window)
    RemoveBackgroundPage()
def gotoAddWaterMarkPage(window):
    destroy_window(window=window)
    AddWaterMarkPage()
def gotoPencilEffectPage(window):
    destroy_window(window=window)
    PencilEffectPage()
def gotoAddTextPage(window):
    destroy_window(window=window)
    AddTextPage()
def gotoRemoveNoisePage(window):
    destroy_window(window=window)
    RemoveNoisePage()
def gotoBlurContourDetailPage(window):
    destroy_window(window=window)
    BlurContourDetailPage()
def gotoEdgeEnhancerWithProPage(window):
    destroy_window(window=window)
    EdgeEnhancerWithProPage()
def gotoEmbossFindEdgesPage(window):
    destroy_window(window=window)
    EmbossFindEdgesPage()

#end
#goto navigations


#start
#pages

def AdjustPage():
    window=newWindow('Adjust Image')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse", fg='green',command=select_file)
    btn.pack()
    label=Label(window,textvariable=path,foreground='green')
    label.pack()
    brightnessvalue = DoubleVar()
    contrastvalue = DoubleVar()
    saturationvalue = DoubleVar()
    exposurevalue = DoubleVar()
    sharpnessvalue = DoubleVar()
    brightnessvalue.set(50)
    contrastvalue.set(50)
    saturationvalue.set(50)
    exposurevalue.set(50)
    sharpnessvalue.set(50)
    slider1 = Scale(window,from_=0,to=100,label='Brightness',orient='horizontal',variable=brightnessvalue,)
    slider1.pack(pady=5)
    slider2 = Scale(window,from_=0,to=100,label='Contrast',orient='horizontal',variable=contrastvalue,)
    slider2.pack(pady=5)
    slider3 = Scale(window,from_=0,to=100,label='Saturation',orient='horizontal',variable=saturationvalue,)
    slider3.pack(pady=5)
    slider4 = Scale(window,from_=0,to=100,label='Exposure',orient='horizontal',variable=exposurevalue,)
    slider4.pack(pady=5)
    slider5 = Scale(window,from_=0,to=100,label='Sharpness',orient='horizontal',variable=sharpnessvalue,)
    slider5.pack(pady=5)
    btn1=Button(window, text="Upload", fg='green',command=lambda: adjustImageOutput(slider1,slider2,slider3,slider4,slider5,path,window))
    btn1.pack(pady=10)
    window.mainloop()

def TintPage():
    window=newWindow('Tint Image')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse", fg='green',command=select_file)
    btn.pack()
    label=Label(window,textvariable=path,foreground='green')
    label.pack()
    tintvalue = DoubleVar()
    tintvalue.set(2)
    slider1 = Scale(window,from_=0,to=100,label='Tint',orient='horizontal',variable=tintvalue,)
    slider1.pack(pady=5)
    tintvalue=slider1.get()
    btn1=Button(window, text="Upload", fg='green',command=lambda:tintOutput(window,tintvalue,path) )
    btn1.pack(pady=10)
    window.mainloop()


def GrayAndNegativeImagePage():
    window=newWindow('Gray and Negative Image')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse", fg='green',command=select_file)
    btn.pack()
    label=Label(window,textvariable=path,foreground='green')
    label.pack()
    btn1=Button(window, text="Convert to Gray Image", fg='green',command=lambda:grayOutput(window,path) )
    btn1.pack(pady=10)
    btn2=Button(window, text="Convert to Negative Image", fg='green',command=lambda:negativeOutput(window,path) )
    btn2.pack(pady=10)
    window.mainloop()

def ResizeRotateFlipImagePage():
    window=newWindow('Resize,Rotate,Flip Image')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    width=IntVar()
    height=IntVar()
    angle=DoubleVar()
    label1=Label(window,text='Width',foreground='green',)
    widthTB=Entry(window,textvariable=width)
    label2=Label(window,text='Height',foreground='green',)
    heightTB=Entry(window,textvariable=height)
    label3=Label(window,text='Angle',foreground='green',)
    angleTB=Entry(window,textvariable=angle)
    btn5=Button(window, text="Browse", fg='green',command=lambda:select_fileRotateResizeFlip(width,height,angle))
    btn5.pack()
    label=Label(window,foreground='green',textvariable=path)
    label.pack()
    label1.pack()
    widthTB.pack()
    label2.pack()
    heightTB.pack()
    label3.pack()
    angleTB.pack()
    options=['None','horizontal','vertical']
    flippedtype=StringVar()
    flippedtype.set( "None" )
    flippedtypeTB=OptionMenu( window , flippedtype , *options )
    flippedtypeTB.pack()
    btn1=Button(window, text="Upload", fg='green',command=lambda:resizeRotateFlipOutput(window,path,width,height,angle,flippedtype) )
    btn1.pack(pady=10)
    window.mainloop()

def histogram():
    window=newWindow('Histogram of the image')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse", fg='green',command=select_file)
    btn.pack()
    btn2=Button(window, text="Show Histogram", fg='green',command=lambda:histogramOutput(window,path) )
    btn2.pack(pady=10)
    window.mainloop()


def ChangeImageExtPage():
    window=newWindow('Change Image Extension')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    options=['jpg','jpeg','png']
    name=StringVar()
    label1=Label(window,text='Name of the image',foreground='green',)
    nameTB=Entry(window,textvariable=name)
    btn5=Button(window, text="Browse", fg='green',command=select_file)
    btn5.pack()
    label1.pack()
    nameTB.pack()
    imageext=StringVar()
    imageext.set( "jpg" )
    imageextTB=OptionMenu( window , imageext , *options )
    imageextTB.pack()
    btn1=Button(window, text="Save the image", fg='green',command=lambda:changeImageExtensionOutput(window,path,imageext,name) )
    btn1.pack(pady=10)
    window.mainloop()

def CollagePage():
    window=newWindow('Make Collage')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse", fg='green',command=select_files)
    btn.pack()
    btn2=Button(window, text="Make Collage", fg='green',command=lambda:collageOutput(window,paths) )
    btn2.pack(pady=10)
    window.mainloop()

def RemoveBackgroundPage():
    window=newWindow('Remove Background')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse", fg='green',command=select_file)
    btn.pack()
    btn2=Button(window, text="Remove Background", fg='green',command=lambda:removeBackgroundOutput(window,path) )
    btn2.pack(pady=10)
    window.mainloop()

def AddWaterMarkPage():
    window=newWindow('Add WaterMark')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse the logo", fg='green',command=select_file)
    btn.pack()
    btn=Button(window, text="Browse the image", fg='green',command=select_file)
    btn.pack()
    btn2=Button(window, text="Add WaterMark", fg='green',command=lambda:addWaterMarkPageOutput(window,paths) )
    btn2.pack(pady=10)
    window.mainloop()

def PencilEffectPage():
    window=newWindow('Pencil Effect')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse", fg='green',command=select_file)
    btn.pack()
    btn2=Button(window, text="Gray Pencil Effect", fg='green',command=lambda:grayPencilEffectOutput(window,path) )
    btn2.pack(pady=10)
    btn2=Button(window, text="Colored Pencil Effect", fg='green',command=lambda:colorPencilEffectOutput(window,path) )
    btn2.pack(pady=10)
    window.mainloop()

def AddTextPage():
    window=newWindow('Add Text to image')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse", fg='green',command=select_file)
    btn.pack()
    x=IntVar()
    y=IntVar()
    text=StringVar()
    thickness=IntVar()
    text.set('Hello')
    label4=Label(window,text='Text',foreground='green',)
    textTB=Entry(window,textvariable=text)
    label1=Label(window,text='X',foreground='green',)
    xTB=Entry(window,textvariable=x)
    label2=Label(window,text='Y',foreground='green',)
    yTB=Entry(window,textvariable=y)
    label4.pack()
    textTB.pack()
    label1.pack()
    xTB.pack()
    label2.pack()
    yTB.pack()
    btn2=Button(window, text="Add text", fg='green',command=lambda:addTextOutput(window,path,x,y,text) )
    btn2.pack(pady=10)
    window.mainloop()



def RemoveNoisePage():
    window=newWindow('Remove Noise')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse", fg='green',command=select_file)
    btn.pack()
    h=IntVar()
    h.set(30)
    label4=Label(window,text='H value : 30 recommended',foreground='green',)
    hTB=Entry(window,textvariable=h)
    label4.pack()
    hTB.pack()
    btn2=Button(window, text="Remove Noise", fg='green',command=lambda:removeNoiseOutput(window,h,path) )
    btn2.pack(pady=10)
    window.mainloop()

def BlurContourDetailPage():
    window=newWindow('Blur Contour Detail')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse", fg='green',command=select_file)
    btn.pack()
    btn2=Button(window, text="Convert Blur", fg='green',command=lambda:blurOutput(window,path) )
    btn2.pack(pady=10)
    btn2=Button(window, text="Contour Effect", fg='green',command=lambda:contourOutput(window,path) )
    btn2.pack(pady=10)
    btn2=Button(window, text="Detailed Image", fg='green',command=lambda:detailOutput(window,path) )
    btn2.pack(pady=10)
    window.mainloop()

def EdgeEnhancerWithProPage():
    window=newWindow('Edge Enhance and Edge Enhancer Pro')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse", fg='green',command=select_file)
    btn.pack()
    btn2=Button(window, text="Ehnace Edge", fg='green',command=lambda:edgeEnhancerOutput(window,path) )
    btn2.pack(pady=10)
    btn2=Button(window, text="Ehnace Edge Pro", fg='green',command=lambda:edgeEnhancerProOutput(window,path) )
    btn2.pack(pady=10)
    window.mainloop()

def EmbossFindEdgesPage():
    window=newWindow('Blur Contour Detail')
    btn2=Button(window, text="Back", fg='green',command=lambda:gotoMainPage(window) )
    btn2.pack(side='left')
    btn=Button(window, text="Browse", fg='green',command=select_file)
    btn.pack()
    btn2=Button(window, text="Emboss Effect", fg='green',command=lambda:embossOutput(window,path) )
    btn2.pack(pady=10)
    btn2=Button(window, text="Find Edges", fg='green',command=lambda:findEdgesOutput(window,path) )
    btn2.pack(pady=10)
    window.mainloop()

#end
#pages

#start
#processed image with output


def adjustImageOutput(slider1,slider2,slider3,slider4,slider5,path,window1):
   if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
   else:
    brightnessvalue=slider1.get()
    contrastvalue=slider2.get()
    saturationvalue=slider3.get()
    exposurevalue=slider4.get()
    sharpnessvalue=slider5.get()
    image = Image.open(path)
    image=brightness(image,brightnessvalue)
    image=contrast(image,contrastvalue)
    image=saturation(image,saturationvalue)
    image=sharpness(image,sharpnessvalue)
    image=exposure(image,exposurevalue)
    window2=Toplevel(window1)
    window2.title('Adjusted Image')
    test = ImageTk.PhotoImage(image)
    label1 = tkinter.Label(window2,image=test,height=550)
    label1.image = test
    label1.pack()
    btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'adjust','jpeg'))
    btn1.pack(pady=10)
    window2.mainloop


def tintOutput(window1,tintvalue,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Tint Image')
        image=tint(path,tintvalue)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'tint','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop


def grayOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Gray Image')
        image = Image.open(path)
        image=gray(image)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'gray','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop

def negativeOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Negative Image')
        image = Image.open(path)
        image=negative(image)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'negative','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop

def resizeRotateFlipOutput(window1,path,width,height,angle,flippedtype):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('resize rotate flip Image')
        image = Image.open(path)
        width=width.get()
        height=height.get()
        angle=angle.get()
        flippedtype=flippedtype.get()
        image=resize(image,width,height)
        image=rotate(image,angle)
        if(flippedtype!='None'):
            image=flipping(image,flippedtype)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'resizerotateflip','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop

def histogramOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Tint Image')
        image = Image.open(path)
        image=calculateHistogram(image,path)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'histogram','png'))
        btn1.pack(pady=10)
        var = StringVar()
        var.set('File saved in'+'downloads folder')
        label2 = tkinter.Label(window2,foreground='green',textvariable=var)
        label2.pack()
        window2.mainloop()

def changeImageExtensionOutput(window1,path,imageext,name):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        imageext=imageext.get()
        name=name.get()
        image = Image.open(path)
        image=convertImageExtTo(image,imageext=imageext,name=name)
        var = StringVar()
        var.set('File saved in current folder')
        label2 = tkinter.Label(window1,foreground='green',textvariable=var)
        label2.pack()
def collageOutput(window1,paths):
    if len(paths)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Collage Image')
        image=collage(paths,len(paths))
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'collage','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()

def removeBackgroundOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Remove Background')
        image=Image.open(path)
        image=removeBackground(image)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'removebackground','png'))
        btn1.pack(pady=10)
        window2.mainloop()
def addWaterMarkPageOutput(window1,paths):
    if len(paths)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Add Water Mark')
        image=Image.open(paths[0])
        image1=Image.open(paths[1])
        image=watermark(image,image1)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'watermark','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()
        
def grayPencilEffectOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Gray pencil effect')
        image=Image.open(path)
        image=pencilSketchGray(image)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'graypencil-effect','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()

def colorPencilEffectOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Color Pencil Effect')
        image=Image.open(path)
        image=pencilSketchColor(image)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'colorpencil-effect','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()


def addTextOutput(window1,path,x,y,text):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Add text Effect')
        image=Image.open(path)
        image=addText(image,text.get(),x.get(),y.get())
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'addtext-effect','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()

def removeNoiseOutput(window1,h,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Remove Noise')
        image=Image.open(path)
        image=removeNoise(image,h.get())
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'denoised','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()

def blurOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Blur Image')
        image=Image.open(path)
        image=blur(image)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'blur','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()


def contourOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Contour Image')
        image=Image.open(path)
        image=contour(image)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'contour','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()

def detailOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Contour Image')
        image=Image.open(path)
        image=detail(image)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'detail','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()

def edgeEnhancerOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('edge Ehnacer Pro Image')
        image=Image.open(path)
        image=edgeEnhance(image)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'edgeenhancer','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()


def edgeEnhancerProOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('edge Ehnacer Pro Image')
        image=Image.open(path)
        image=edgeEnhancePro(image)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'edgeenhancerpro','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()

def findEdgesOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('find Edges in Image')
        image=Image.open(path)
        image=findEdges(image)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'detail','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()

def embossOutput(window1,path):
    if len(path)==0:
        showerror(title='File not uploaded',message='Please upload the file')
    else:
        window2=Toplevel(window1)
        window2.title('Emboss Image')
        image=Image.open(path)
        image=emboss(image)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(window2,image=test,height=550)
        label1.image = test
        label1.pack()
        btn1=Button(window2, text="Download", fg='green',command=lambda:download2(image,'emboss','jpeg'))
        btn1.pack(pady=10)
        window2.mainloop()

#end
#image processing with output

mainPage()

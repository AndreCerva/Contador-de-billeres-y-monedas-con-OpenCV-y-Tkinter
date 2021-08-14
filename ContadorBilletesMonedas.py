"""
Created on Sat Jul 03 21:40:56 2021

@author: andre
"""
#Importamos las librerias necesarias, tkinter para la GUI, ImageTk from PIL para trabajar con imagenes en la GUI,
#messagebox para ventanas emergentes al dar click en un boton en la GUI, cv2 para la visión artificial, numpy para
#Trabajar con arrays
from tkinter import *
from tkinter import messagebox as mb
from PIL import ImageTk, Image
import cv2,imutils
import numpy as np
#Generamos variables aleatorias para poder utilizarlas entre funciones
global dinero,count,font,kernel2,kernel3,kernel4
count=1
#Creamos nuestras matrices kernel para trabajar con el ruido de las imagenes, con tecnicas de erosion y dilatacion
kernel2 = np.ones((5, 5), np.uint8)
kernel3 = np.ones((7, 7), np.uint8)
kernel4 = np.array(([0, 1, 0], [1, 1, 1], [0, 1, 0]), np.uint8)
#Función para contabilizar los billetes y dibujar cuando los detecta, recibe como parametros la fotografia tomada, el billete y la mascara 
def dibujar(mask,imag,co):
    global dinero,font
    contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        area = cv2.contourArea(c)
        if area > 10000 :
            M = cv2.moments(c)
            if (M["m00"] == 0): M["m00"] = 1
            x = int(M["m10"] / M["m00"])
            y = int(M['m01'] / M['m00'])
            if co==1:
                dinero += 20
                area = int(M['m00'])
                print("Area de una moneda de 20: " + str(area))
                cv2.putText(imag, ("20 peso"), (x, y), 5, 1, (255, 0, 0), 1)
            elif co==2:
                dinero += 50
                area = int(M['m00'])
                print("Area de una moneda de 50: " + str(area))
                cv2.putText(imag, ("50 peso"), (x, y), 5, 1, (255, 0, 0), 1)
            elif co==3:
                dinero += 200
                area = int(M['m00'])
                print("Area de una moneda de 200: " + str(area))
                cv2.putText(imag, ("200 peso"), (x, y), 5, 1, (255, 0, 0), 1)
                
#Funciones notice y about para mostrar informacion al usuario cuando la requiere
def notice():
    mb.showinfo("Info","Un resumen rapido de la utilización:\n\n Para tomar una lectura de cuanto dinero hay dar click en tomar captura"
                       "\n\nPara salir y terminar con el proceso dar click en el boton salir"
                "\n\nAl dar click en tomar captura se calculara el dinero que hay en la fotografia\n\nPara más información presionar la pestaña:Ayuda->Acerda de... ")
def about():
    mb.showinfo("Más info", "Proyecto versión 1 creado el 03/07/2021 por Andrés Cervantes\n\n"
                            "más información al correo: 17030913@itcelaya.edu.mx")
    
#Al dar click en iniciar a capturar, la camara web se activará y se podrá tomar una foto del dinero para contabilizarlo
#Recordar la importancia de la correcta iluminación!!!!, ademas de la cercania a la que se toma la foto
# una buena o mala iluminación cambiaran en gran medidas los parametros para dilatar y erosionar la imagen del ruido
#el que tan lejos o cerca se encuentre la imagen influira en el area de las monedas y cambiara el valor de estas
def iniciar():
    global Capturar,cap,im,Regresar,Salir,Iniciar,lblVideo
    Iniciar.grid_forget()
    Salir.grid_forget()
    Regresar.grid(column=1, row=2, padx=5, pady=5)
    im.grid_forget()
    Capturar.grid(column=0, row=2, padx=5, pady=5)
    lblVideo.grid(column=0, row=0, columnspan=2)
    #Para tomar una foto del dinero se debe hacer uso de una webcam, en caso de no contar con esta, se puede hacer uso
    #de la camara de un celular, conectado mediante una direccion IP con ayuda de la aplicación movil: IP Webcam 
    cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
    address = "http://192.168.1.65:8080/video"
    cap.open(address)
    visualizar()
#En la función mascaras, se crean estas para detectar el color de los billetes de 20, 50, 200 para distinguirlos entre
#Los billetes que se capturen en la fotografia
def mascaras(imaghsv,imag):
    global kernel2,kernel3,kernel4
    #Recordar trabajar en hsv
    billetede20claro = np.array([75, 30, 30], np.uint8)
    billetede20fuerte = np.array([140, 150, 150], np.uint8)
    billetede50claro = np.array([135, 15, 15], np.uint8)
    billetede50fuerte = np.array([179, 255, 255], np.uint8)
    billetede200claro = np.array([35, 5, 5], np.uint8)
    billetede200fuerte = np.array([75, 200, 200], np.uint8)
    mask20=cv2.inRange(imaghsv,billetede20claro,billetede20fuerte)
    mask50=cv2.inRange(imaghsv,billetede50claro,billetede50fuerte)
    mask200=cv2.inRange(imaghsv,billetede200claro,billetede200fuerte)
    #Procesamos la imagen para el ruido que será inevitable, recordar la importancia de la correcta iluminación
    mask20=cv2.morphologyEx(mask20,cv2.MORPH_OPEN,kernel4,iterations=2)
    mask20=cv2.morphologyEx(mask20,cv2.MORPH_CLOSE,kernel4,iterations=3)
    mask50=cv2.morphologyEx(mask50,cv2.MORPH_OPEN,kernel4,iterations=2)
    mask50=cv2.morphologyEx(mask50,cv2.MORPH_CLOSE,kernel4,iterations=3)
    mask200=cv2.morphologyEx(mask200,cv2.MORPH_OPEN,kernel4,iterations=2)
    mask200=cv2.morphologyEx(mask200,cv2.MORPH_CLOSE,kernel4,iterations=3)
    mask20 = cv2.resize(mask20, (800, 800))
    mask50 = cv2.resize(mask50, (800, 800))
    mask200 = cv2.resize(mask200, (800, 800))
    dibujar(mask20,imag,1)
    dibujar(mask50,imag,2)
    dibujar(mask200,imag,3)

#funcion procesar para cuando se capture una imagen, contabilizar el dinero en esta fotografia
def procesar():
    global img,dinero
    dinero=0
    #Se guarda la imagen que se capture
    imag = cv2.imread("Image{}.png".format(count))
    imagray = cv2.imread("Image{}.png".format(count),0)
    imaghsv=cv2.cvtColor(imag,cv2.COLOR_BGR2HSV)
    mascaras(imaghsv,imag)
    #Se genera un threshold para detectar las monedas, se le aplica morphology para eliminar el ruido
    blur = cv2.GaussianBlur(imagray, (5, 5), 1)
    _, th_2 = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
    th_2=cv2.morphologyEx(th_2, cv2.MORPH_OPEN,kernel4)
    th_2=cv2.morphologyEx(th_2, cv2.MORPH_CLOSE,kernel4,iterations=6)
    #Se capturan todos los contornos en la imagen binarizada
    contorns, _ = cv2.findContours(th_2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for i in contorns:
        area = cv2.contourArea(i)
        #Se procesa según el área del contorno será la cantidad de dinero, recordar la importancia de la altura de las fotos
        if area > 1800 and area < 2300:# 1 peso
            momentos = cv2.moments(i)
            if momentos['m00'] == 0: momentos['m00'] = 1
            cx = int(momentos['m10'] / momentos['m00'])
            cy = int(momentos['m01'] / momentos['m00'])
            area = int(momentos['m00'])
            print("Area de una moneda de 1: "+str(area))
            cv2.putText(imag,("$1"),(cx,cy),5,1,(255,0,0),1)
            dinero += 1
        if area > 2600 and area < 3500:  # 5 peso
            momentos = cv2.moments(i)
            if momentos['m00'] == 0: momentos['m00'] = 1
            cx = int(momentos['m10'] / momentos['m00'])
            cy = int(momentos['m01'] / momentos['m00'])
            area = int(momentos['m00'])
            print("Area de una moneda de 5: "+str(area))
            cv2.putText(imag, ("5 peso"), (cx, cy), 5, 1, (255, 0, 0), 1)
            dinero += 5
        if area > 3500 and area < 4100:  # 10 peso
            momentos = cv2.moments(i)
            if momentos['m00'] == 0: momentos['m00'] = 1
            cx = int(momentos['m10'] / momentos['m00'])
            cy = int(momentos['m01'] / momentos['m00'])
            area = int(momentos['m00'])
            print("Area de una moneda 10: "+str(area))
            cv2.putText(imag, ("10 peso"), (cx, cy), 5, 1, (255, 0, 0), 1)
            dinero += 10
    cv2.putText(imag, ("Dinero total= " + str(dinero)), (30, 50), 5, 1, (0), 1)
    imag = cv2.resize(imag, (800, 800))
    th_2 = cv2.resize(th_2, (800, 800))
    cv2.imshow('imagen{}'.format(count),imag)
    cancelar()
#Función para capturar imagen
def capturar():
    global imag,lblInputImage,count,frame,cap,lblVideo,Capturar,Regresar
    namecap = "Image{}.png".format(count)
    cv2.imwrite(namecap, frame)
    print("Image{} salved".format(count))
    lblVideo.grid_forget()
    Capturar.grid_forget()
    cap.release()
    Regresar.grid_forget()
    Regresar.grid(column=0, row=2, columnspan=2)
    procesar()
    count += 1
def salir():
    root.destroy()
def visualizar():
    global cap,frame
    if cap is not None:
        ret,frame=cap.read()
        if ret==True:
            frame=imutils.resize(frame,width=640)
            frame1=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)#PIL trabaja con las imagenes en RGB
            im=Image.fromarray(frame1)#Del arreglo del frame (video)
            img=ImageTk.PhotoImage(image=im)
            lblVideo.configure(image=img)
            lblVideo.image=img
            lblVideo.after(10,visualizar)#Ciclo que llama a la funcion cada 10milisegundos
        else:
            lblVideo.image=""
            cap.release()
#Funcion cancelar para salir o evitar
def cancelar():
    global cap,lblVideo,im,Iniciar,Salir,Capturar,Regresar
    lblVideo.grid_forget()
    Capturar.grid_forget()
    Regresar.grid_forget()
    im.grid(column=0, row=0, columnspan=2)
    Iniciar.grid(column=0, row=2, padx=5, pady=5)
    Salir.grid(column=1, row=2, padx=5, pady=5)
    cap.release()
#Menu principal del programa
#Configuraciones principales a la GUI 
cap=None
root=Tk()
root.title("Menu contador de monedas")
cuadro=Frame()
cuadro.pack()
cuadro.config(width="400",height="400",bg="lightblue",bd=35,relief="groove")
#------------------------------------------------------------------------------Menu Bar
menubar = Menu(root) #Creamos el menu en la raiz
root.config(menu=menubar)
ele = Menu(menubar, tearoff=0)#Configuración de visualización
ele.add_command(label="Info",command=notice)#Añadimos a la pestaña ele la subpestaña info
ele.add_separator()
ele.add_command(label="Acerca de...",command=about)#Añadim+os a la pestaña ele la subpestaña acerca de
menubar.add_cascade(label="Ayuda", menu=ele)#Al menu bar le creamos la pestaña ele llamada ayuda
#--------------------------------------------------------------------------------Main menu
Iniciar=Button(cuadro,text="Empezar a capturar",width=45,command=iniciar)
Iniciar.grid(column=0,row=2,padx=5,pady=5)
Regresar=Button(cuadro,text="Regresar",width=45,command=cancelar)
Salir=Button(cuadro,text="Salir",width=45,command=salir)
laba=Label(cuadro,text="Seleccione que desea hacer")
laba.grid(column=0,row=1,columnspan=2)
Salir.grid(column=1,row=2,padx=5,pady=5)
Capturar=Button(cuadro,text="Capturar imagen",width=45,command=capturar)
lblVideo=Label(cuadro)
ima = ImageTk.PhotoImage(Image.open("dinero.jpg"))
im = Label(cuadro, image = ima)
im.grid(column=0,row=0,columnspan=2)
lblInputImage = Label(cuadro)
root.mainloop()
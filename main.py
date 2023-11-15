#Ejecutar con python en vez de python3
import tkinter as tk 
from PIL import Image, ImageTk

ventana = tk.Tk()
ventana.geometry('1000x600')
ventana.title('Flappy Bird')

x = 150
y = 300
puntuacion = 0
velocidad = 10
fin_juego = False

img_pajaro = Image.open('img/bird.png')
img_pajaro = ImageTk.PhotoImage(img_pajaro)

img_tubo_arriba = Image.open('img/pipe.png')        
img_tubo_abajo = img_tubo_arriba.rotate(180)

img_tubo_arriba = ImageTk.PhotoImage(img_tubo_arriba)
img_tubo_abajo = ImageTk.PhotoImage(img_tubo_abajo)

img_reiniciar = Image.open('img/restart.png')
img_reiniciar = ImageTk.PhotoImage(img_reiniciar)

canvas = tk.Canvas(ventana, highlightthickness=0, bg= '#00bfff')
canvas.place(relwidth=1, relheight=1)

texto_puntuacion = canvas.create_text(50, 50, text='0', fill='white', font=('D3 Egoistism outline', 30))

pajaro = canvas.create_image(x, y, anchor='nw', image=img_pajaro)
tubo_arriba = canvas.create_image(1200, -550, anchor='nw', image=img_tubo_arriba)
tubo_abajo = canvas.create_image(1200, 550, anchor='nw', image=img_tubo_abajo)

def mover_pajaro_tecla(evento):
    global x, y
    if not fin_juego:
        y -= 30
        canvas.coords(pajaro, x, y)

ventana.bind("<space>", mover_pajaro_tecla)

def fin_del_juego():
    global fin_juego
    fin_juego = True

def mover_pajaro():
    global x, y
    y += 5
    canvas.coords(pajaro, x, y)
    if y < 0 or y > ventana.winfo_height():
        fin_del_juego()
    if not fin_juego:
        ventana.after(50, mover_pajaro)

def reiniciar_juego():
    global x, y, puntuacion, velocidad, fin_juego
    x = 150
    y = 300
    puntuacion = 0
    velocidad = 10
    fin_juego = False
    canvas.coords(pajaro, x, y)
    canvas.coords(tubo_arriba, 1200, -550)
    canvas.coords(tubo_abajo, 1200, 550)
    canvas.itemconfigure(texto_puntuacion, text="0")
    etiqueta_fin_juego.place_forget()
    boton_reiniciar.place_forget()

etiqueta_fin_juego = tk.Label(ventana, text="Perdiste", font=('D3 Egoistism outline', 30), fg="white", bg="#00bfff")
boton_reiniciar = tk.Button(ventana, border=0, image=img_reiniciar, activebackground='#00bfff', bg='#00bfff', command=reiniciar_juego)

ventana.after(50, mover_pajaro)

ventana.mainloop()

#Ejecutar con python en vez de python3
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.simpledialog
import random
import sqlite3
from login import nombre

print(nombre)

game = tk.Tk()
game.geometry('1000x600')
game.title('Flappy Bird')

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

canvas = tk.Canvas(game, highlightthickness=0, bg='#00bfff')
canvas.place(relwidth=1, relheight=1)

pajaro = canvas.create_image(x, y, anchor='nw', image=img_pajaro)
tubo_arriba = canvas.create_image(1200, -550, anchor='nw', image=img_tubo_abajo)
tubo_abajo = canvas.create_image(1200, 550, anchor='nw', image=img_tubo_arriba)

def conexionBD(consulta, parametros=()):
    with sqlite3.connect("Flappy-Bird.db") as conexion:
        cursor = conexion.cursor()
        cursor.execute(consulta, parametros)
        res = cursor.fetchall()
        conexion.commit()
        return res

def mover_pajaro_tecla(event):
    global x, y
    if not fin_juego:
        y -= 30
        canvas.coords(pajaro, x, y)


game.bind("<space>", mover_pajaro_tecla)


def mover_pajaro():
    global x, y
    y += 5
    canvas.coords(pajaro, x, y)
    if y < 0 or y > game.winfo_height():
        fin_del_juego()

    if not fin_juego:
        game.after(50, mover_pajaro)


def mover_tubo():
    global puntuacion, fin_juego, velocidad
    canvas.move(tubo_arriba, -velocidad, 0)
    canvas.move(tubo_abajo, -velocidad, 0)
    if canvas.coords(tubo_abajo)[0] < -100:
        puntuacion += 1
        velocidad += 1
        canvas.itemconfigure(texto_puntuacion, text=str(puntuacion))
        h = game.winfo_height()
        num = random.choice([i for i in range(160, h, 160)])
        canvas.coords(tubo_abajo, game.winfo_width(), num + 160)
        canvas.coords(tubo_arriba, game.winfo_width(), num - 900)

    if 0 < canvas.coords(tubo_abajo)[0] < 160:
        if canvas.bbox(pajaro)[0] < canvas.bbox(tubo_abajo)[2] and canvas.bbox(pajaro)[2] > canvas.bbox(
                tubo_abajo)[0]:
            if canvas.bbox(pajaro)[1] < canvas.bbox(tubo_arriba)[3] or canvas.bbox(pajaro)[3] > canvas.bbox(
                    tubo_abajo)[1]:
                fin_del_juego()
    if not fin_juego:
        game.after(50, mover_tubo)


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
    lbl_fin_juego.place_forget()
    bt_reiniciar.place_forget()
    mover_pajaro()
    mover_tubo()


def fin_del_juego():
    global fin_juego
    fin_juego = True
    lbl_fin_juego.place(relx=0.5, rely=0.5, anchor='center')
    bt_reiniciar.place(relx=0.5, rely=0.7, anchor='center')

    query = "SELECT nombre FROM Jugador WHERE nombre='{0}'".format(nombre)
    res = conexionBD(query)

    if len(res) == 0:
        insert = "INSERT INTO Jugador (nombre, puntaje) VALUES ('{0}', '{1}')".format(nombre, puntuacion)
        conexionBD(insert)
    else:
        query = "SELECT puntaje FROM Jugador WHERE nombre='{0}'".format(nombre)
        res_query = conexionBD(query)
        res = res_query[0]
        if res[0] > puntuacion:
            tk.messagebox.showwarning("Advertencia", "El puntaje anterior era mas alto")
        else:        
            update = "UPDATE Jugador SET puntaje='{0}' WHERE nombre='{1}'".format(puntuacion, nombre)
            conexionBD(update)

    while canvas.coords(pajaro):
        if canvas.bbox(pajaro)[0] < canvas.bbox(tubo_abajo)[2] and canvas.bbox(pajaro)[2] > canvas.bbox(tubo_abajo)[
            0]:
            if canvas.bbox(pajaro)[1] < canvas.bbox(tubo_arriba)[3] or canvas.bbox(pajaro)[3] > canvas.bbox(
                    tubo_abajo)[1]:
                break
    lbl_fin_juego.place(relx=0.5, rely=0.5, anchor='center')
    bt_reiniciar.place(relx=0.5, rely=0.7, anchor='center')


query_top1 = "SELECT MAX(puntaje) as puntaje, nombre FROM Jugador"
res_top1 = conexionBD(query_top1)
res_top1 = res_top1[0]

jugador_top1 = res_top1[1]
puntaje_top1 = res_top1[0]

tabla_frame = tk.Frame(game, bg='#B8B8B8', padx=10, pady=10)
tabla_frame.place(relx=0.005, rely=0.1, relwidth=0.15, relheight=0.15)

lbl_top1 = tk.Label(tabla_frame, text="Jugador Top 1", font=('D3 Egoistism outline', 16), bg='#B8B8B8', fg='white')
lbl_top1.pack()

lbl_nombre_top1 = tk.Label(tabla_frame, text=f"Nombre: {jugador_top1}", font=('D3 Egoistism outline', 12), bg='#B8B8B8', fg='white')
lbl_nombre_top1.pack()

lbl_puntaje_top1 = tk.Label(tabla_frame, text=f"Puntaje: {puntaje_top1}", font=('D3 Egoistism outline', 12), bg='#B8B8B8', fg='white')
lbl_puntaje_top1.pack()

texto_puntuacion = canvas.create_text(50, 40, text='0', fill='white', font=('D3 Egoistism outline', 30))


lbl_fin_juego = tk.Label(game, text='Juego Terminado!', font=('D3 Egoistism outline', 30), fg='white', bg='#00bfff')
bt_reiniciar = tk.Button(game, border=0, image=img_reiniciar, activebackground='#00bfff', bg='#00bfff', command=reiniciar_juego)

game.after(50, mover_pajaro)
game.after(50, mover_tubo)

game.call('wm', 'iconphoto', game._w, img_pajaro)
game.mainloop()


import tkinter as tk
from tkinter import messagebox
import sqlite3

nombre = ""
contrasena = ""

def conexionBD(consulta, parametros=None):
    with sqlite3.connect("Flappy-Bird.db") as conexion:
        cursor = conexion.cursor()
        if parametros:
            cursor.execute(consulta, parametros)
        else:
            cursor.execute(consulta)
        res = cursor.fetchall()
        conexion.commit()
        return res


def iniciar_sesion():
    global nombre, contrasena
    nombre = entry_usuario.get()
    contrasena = entry_contrasena.get()

    consulta = "SELECT * FROM Jugador WHERE nombre = {0} AND contrasena = {1}".format(nombre, contrasena)
    resultado = conexionBD(consulta)

    if resultado:
        messagebox.showinfo("Inicio de Sesión", "BUENO VAMO A JUGAR")
        login.destroy()
    else:
        messagebox.showerror("Error", "Usuario o Contraseña incorrectas")

    

login = tk.Tk()
login.title("Inicio de Sesión")
login.geometry("1000x600")

label_usuario = tk.Label(login, text="Usuario:")
label_contrasena = tk.Label(login, text="Contraseña:")
entry_usuario = tk.Entry(login)
entry_contrasena = tk.Entry(login, show="*")
boton_iniciar_sesion = tk.Button(login, text="Iniciar Sesión", command=iniciar_sesion)

label_usuario.pack()
entry_usuario.pack()

label_contrasena.pack()
entry_contrasena.pack()

boton_iniciar_sesion.pack()

login.mainloop()

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

    # Consulta para verificar las credenciales en la base de datos
    consulta = "SELECT * FROM Jugador WHERE nombre = ? AND contrasena = ?"
    parametros = (nombre, contrasena)
    resultado = conexionBD(consulta, parametros)

    if resultado:
        messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso")
        #Ejecutar el archivo main.py
        #main_function()  # Asegúrate de que esta función exista en main.py
        game()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

def game():
    ventana.destroy()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Inicio de Sesión")
ventana.geometry("1000x600")

# Crear widgets
label_usuario = tk.Label(ventana, text="Usuario:")
label_contrasena = tk.Label(ventana, text="Contraseña:")
entry_usuario = tk.Entry(ventana)
entry_contrasena = tk.Entry(ventana, show="*")
boton_iniciar_sesion = tk.Button(ventana, text="Iniciar Sesión", command=iniciar_sesion)

# Colocar widgets en la ventana
label_usuario.pack()
entry_usuario.pack()

label_contrasena.pack()
entry_contrasena.pack()

boton_iniciar_sesion.pack()

# Iniciar el bucle de la interfaz gráfica
ventana.mainloop()

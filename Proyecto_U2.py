import tkinter as tk
from tkinter import messagebox, Toplevel, Label
from PIL import Image, ImageTk
import math
from graphviz import Digraph
import pygame
pygame.mixer.init()
# ─── Funcion de la Alarma ───────────────────────────────────────────────────────────
def reproducir_error():
    pygame.mixer.music.load("sound/sinacceso.mp3")
    pygame.mixer.music.play()

# ─── Ventana de Carga ───────────────────────────────────────────────────────────
def mostrar_cargando(mensaje="Generando diagrama..."):
    cargando = Toplevel(ventana)
    cargando.title("Por favor, espere")
    cargando.geometry("300x100")
    cargando.configure(bg="#f0f0f0")
    cargando.resizable(False, False)
    cargando.transient(ventana) 
    cargando.grab_set()


    cargando.update_idletasks()
    x = (cargando.winfo_screenwidth() - cargando.winfo_reqwidth()) // 2
    y = (cargando.winfo_screenheight() - cargando.winfo_reqheight()) // 2
    cargando.geometry(f"+{x}+{y}")

    frame = tk.Frame(cargando, bg="#ffffff", bd=2, relief="groove")
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    label = Label(frame, text=mensaje, font=("Segoe UI", 11, "italic"), bg="#ffffff", fg="#333")
    label.pack(pady=15)

    barra = tk.Canvas(frame, width=200, height=6, bg="#ccc", bd=0, highlightthickness=0)
    barra.pack()
    barra.create_rectangle(0, 0, 80, 6, fill="#4caf50", width=0) 

    cargando.update()
    return cargando


# ─── Variables globales ───────────────────────────────────────────────────────────
transiciones_realizadas = []

# ─── Función para dibujar autómata Mealy ────────────────────────────────
def draw_mealy(transiciones=None):
    dot = Digraph(comment="Mealy Machine - Turnstile")
    dot.attr(rankdir='LR')

    estados = {"LOCKED", "UNLOCKED"}
    for estado in estados:
        dot.node(estado)

    for estado_inicial, entrada, estado_siguiente in transiciones:
        if estado_inicial == "LOCKED" and estado_siguiente == "UNLOCKED":
            salida = "unlock"
        elif estado_inicial == "LOCKED":
            salida = "alarm"
        elif estado_inicial == "UNLOCKED" and estado_siguiente == "LOCKED":
            salida = "lock"
        elif estado_inicial == "UNLOCKED":
            salida = "thank you"
        else:
            salida = "?"

        dot.edge(estado_inicial, estado_siguiente, label=f"{entrada} / {salida}")

    dot.render("mealy_turnstile", format="png", cleanup=True)
    
# ─── Función para dibujar autómata Moore ────────────────────────────────
def draw_moore(transiciones=None):
    dot = Digraph(comment="Moore Machine - Turnstile")
    dot.attr(rankdir='LR')

    estados = {"LOCKED": "lock", "UNLOCKED": "unlock"}  # Salidas estilo simple

    for estado, salida in estados.items():
        dot.node(estado, label=f"{estado}\n[{salida}]")  # Estilo visual deseado

    for estado_inicial, entrada, estado_siguiente in transiciones:
        dot.edge(estado_inicial, estado_siguiente, label=entrada)

    dot.render("moore_turnstile", format="png", cleanup=True)
    print("✅ Diagrama Moore generado: moore_turnstile.png")
  

# ─── Interfaz Gráfica ───────────────────────────────────────────────────────────────
ventana = tk.Tk()
ventana.title("Torniquete - de Acceso")
ventana.state("zoomed")
ventana.configure(bg="#e8e8e8")

modo_actual = tk.StringVar(value="Ninguno")

def cambiar_modo(modo):
    modo_actual.set(modo)
    messagebox.showinfo("Modo seleccionado", f"Modo actual: Maquina {modo}")

menuboton = tk.Menubutton(ventana, textvariable=modo_actual,
                          relief=tk.RAISED, bg="#e8e8e8",
                          activebackground="#d0d0d0")
menu_opciones = tk.Menu(menuboton, tearoff=0)
menu_opciones.add_command(label="Maquina Moore", command=lambda: cambiar_modo("Moore"))
menu_opciones.add_command(label="Maquina Mealy", command=lambda: cambiar_modo("Mealy"))
menuboton["menu"] = menu_opciones
menuboton.place(x=10, y=10)

canvas = tk.Canvas(ventana, width=600, height=470, bg="#f5f5f5", highlightthickness=0)
canvas.pack()

centro_x, centro_y = 300, 240
longitud_brazo = 70
angulo_actual = 0
lector_color = "red"
pantalla_texto = "Insertar $5"
puertas_abiertas = False
brillo_led = False
cantidad_ingresada = 0

# ─── Dibujar fondo y torniquete ─────────────────────────────────────────────
def dibujar_fondo():
    canvas.create_polygon(50, 0, 550, 0, 600, 100, 0, 100, fill="#d0d4d8", outline="")
    canvas.create_polygon(0, 300, 600, 300, 550, 470, 50, 470, fill="#c0c4c8", outline="")
    canvas.create_polygon(0, 100, 50, 0, 50, 470, 0, 300, fill="#e0e4e8", outline="")
    canvas.create_polygon(550, 0, 600, 100, 600, 300, 550, 470, fill="#e0e4e8", outline="")
    canvas.create_line(0, 300, 300, 235, fill="#b0b0b0", width=2)
    canvas.create_line(600, 300, 300, 235, fill="#b0b0b0", width=2)

def calcular_brazo(angulo):
    rad = math.radians(angulo)
    x = centro_x + longitud_brazo * math.cos(rad)
    y = centro_y + longitud_brazo * math.sin(rad)
    return x, y

def dibujar_torniquete():
    canvas.delete("all")
    dibujar_fondo()
    canvas.create_oval(260, 360, 340, 370, fill="#ccc", outline="")
    canvas.create_rectangle(170, 110, 250, 190, fill="#a9a9a9", outline="#555", width=2)
    canvas.create_rectangle(190, 190, 230, 360, fill="#b0b0b0", outline="#444")
    canvas.create_rectangle(250, 110, 330, 190, fill="#c0c0c0", outline="#555", width=2)
    color_led = lector_color if not brillo_led else "white"
    canvas.create_oval(275, 125, 305, 155, fill=color_led, outline="black")
    canvas.create_rectangle(258, 160, 322, 175, fill="black", outline="#0f0", width=1)
    canvas.create_text(290, 167, text=pantalla_texto, fill="lime" if lector_color == "green" else "white", font=("Consolas", 8, "bold"))
    canvas.create_rectangle(270, 190, 310, 360, fill="#bcbcbc", outline="#444")
    canvas.create_line(250, 110, 330, 110)
    canvas.create_line(250, 190, 330, 190)
    for offset in [0, 120, 240]:
        ang = angulo_actual + offset
        x, y = calcular_brazo(ang)
        canvas.create_line(centro_x, centro_y, x, y, width=10, fill="black", capstyle=tk.ROUND)
    if puertas_abiertas:
        canvas.create_rectangle(190, 360, 210, 390, fill="green", outline="darkgreen")
        canvas.create_rectangle(310, 360, 330, 390, fill="green", outline="darkgreen")
    else:
        canvas.create_rectangle(190, 360, 210, 390, fill="gray", outline="black")
        canvas.create_rectangle(310, 360, 330, 390, fill="gray", outline="black")
    canvas.create_text(300, 30, text="SISTEMA DE CONTROL DE ACCESO", font=("Helvetica", 16, "bold"), fill="#222")

# ─── Acciones del sistema ───────────────────────────────────────────────────
def girar_brazos():
    global angulo_actual
    for _ in range(20):
        angulo_actual += 9
        dibujar_torniquete()
        ventana.update()
        canvas.after(20)

def parpadear_led(n=0):
    global brillo_led
    if n < 6:
        brillo_led = not brillo_led
        dibujar_torniquete()
        ventana.after(150, lambda: parpadear_led(n+1))

def reiniciar_lector():
    global lector_color, pantalla_texto, puertas_abiertas, cantidad_ingresada, transiciones_realizadas
    lector_color = "red"
    pantalla_texto = "Insertar $5"
    puertas_abiertas = False
    cantidad_ingresada = 0
    transiciones_realizadas = []
    dibujar_torniquete()

def mostrar_grafo():
    if modo_actual.get() == "Mealy":
        ventana_carga = mostrar_cargando("Generando diagrama Mealy...")
        ventana.update()
        draw_mealy(transiciones_realizadas)
        ventana_carga.destroy()
        nueva = Toplevel()
        nueva.title("Autómata Mealy")
        img = Image.open("mealy_turnstile.png")
        img = ImageTk.PhotoImage(img)
        lbl = Label(nueva, image=img)
        lbl.image = img
        lbl.pack()
    elif modo_actual.get() == "Moore":
        ventana_carga = mostrar_cargando("Generando diagrama Moore...")
        ventana.update()
        draw_moore(transiciones_realizadas)
        ventana_carga.destroy()
        nueva = Toplevel()
        nueva.title("Autómata Moore")
        img = Image.open("moore_turnstile.png")
        img = ImageTk.PhotoImage(img)
        lbl = Label(nueva, image=img)
        lbl.image = img
        lbl.pack()
    else:        
        messagebox.showinfo("Modo inactivo", "Por favor selecciona un modo válido.")

# ─── Entrada del usuario ──────────────────────────────────────────────────────────
def presionar_boton(n):
    global cantidad_ingresada, lector_color, pantalla_texto, puertas_abiertas, transiciones_realizadas

    if modo_actual.get() == "Ninguno":
        messagebox.showwarning("Advertencia", "Por favor, elija un modo de máquina antes de continuar.")
        return

    estado_anterior = "LOCKED" if cantidad_ingresada < 5 else "UNLOCKED"
    cantidad_ingresada += n
    pantalla_texto = f"Ingresado: ${cantidad_ingresada}"
    estado_actual = "UNLOCKED" if cantidad_ingresada >= 5 else "LOCKED"

    transiciones_realizadas.append((estado_anterior, str(n), estado_actual))

    dibujar_torniquete()

def presionar_push():
    global lector_color, pantalla_texto, puertas_abiertas

    if modo_actual.get() == "Ninguno":
        messagebox.showwarning("Advertencia", "Por favor, elija un modo de máquina antes de continuar.")
        return

    if cantidad_ingresada >= 5:
        transiciones_realizadas.append(("UNLOCKED", "push", "LOCKED"))
        pantalla_texto = "Acceso OK"
        puertas_abiertas = True
        lector_color = "green"
        parpadear_led()
        girar_brazos()
        dibujar_torniquete()
        mostrar_grafo()
        ventana.after(3000, reiniciar_lector)
    else:
        transiciones_realizadas.append(("LOCKED", "push", "LOCKED"))
        pantalla_texto = "No puedes pasar"
        parpadear_led()
        dibujar_torniquete()
        reproducir_error()

# ─── Botones numéricos ────────────────────────────────────────────────────────────
for i in range(9):
    tk.Button(ventana, text=str(i+1), width=4, height=2,
              font=("Arial", 10, "bold"),
              command=lambda n=i+1: presionar_boton(n),
              bg="#ffffff", activebackground="#dcdcdc",
              relief="raised").place(x=60 + (i % 3) * 60, y=475 + (i // 3) * 40)
    tk.Button(ventana, text="PUSH", width=10, height=2,
          font=("Arial", 10, "bold"),
          command=presionar_push,
          bg="#ffcccc", activebackground="#fbb",
          relief="raised").place(x=240, y=595)


# ─── Primer render ───────────────────────────────────────────────────────────
dibujar_torniquete()
ventana.mainloop()
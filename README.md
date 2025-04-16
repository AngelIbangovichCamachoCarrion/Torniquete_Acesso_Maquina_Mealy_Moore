# 🌀 Proyecto: Simulación de Torniquete con Máquina de Estados (Moore y Mealy)

Este proyecto es una simulación visual de un sistema de **torniquete de acceso** que utiliza autómatas de tipo **Mealy** y **Moore** para representar el comportamiento de entrada basado en el ingreso de dinero. Fue desarrollado con **Tkinter**, **Graphviz** y **Pygame** en Python.

## 🛠 Tecnologías utilizadas

- Python 3
- Tkinter (Interfaz gráfica)
- Graphviz (Visualización del autómata)
- PIL / Pillow (Carga de imágenes)
- Pygame (Reproducción de sonido)
- Math (Cálculos trigonométricos)

## 🚦 Descripción del sistema

- El torniquete requiere **$5** para desbloquearse.
- Se pueden ingresar cantidades del 1 al 9 presionando los botones numéricos.
- Una vez alcanzados los $5 o más, el sistema pasa al estado **UNLOCKED**.
- Al presionar el botón **PUSH**, se simula el giro del torniquete y el acceso.
- Si no se han ingresado $5 y se presiona PUSH, se activa una alarma.
- El modo puede cambiarse entre **Máquina de Moore** o **Mealy**, y se genera el autómata correspondiente.

## 🎮 Cómo usar

1. Ejecuta el archivo `Proyecto_U2.py`.
2. Selecciona el tipo de máquina en el menú desplegable (Mealy o Moore).
3. Ingresa monedas (1 al 9) haciendo clic en los botones numéricos.
4. Una vez que la cantidad ingresada sea ≥ $5, presiona **PUSH** para simular el acceso.
5. Se mostrará el grafo del autómata utilizado.
6. Si intentas acceder sin dinero suficiente, sonará una alarma.

## 📁 Estructura del proyecto

```
📁 Proyecto_U2
│
├── Proyecto_U2.py           # Código fuente principal
├── sound/
│   └── sinacceso.mp3        # Sonido de alarma al intentar acceso sin saldo
├── moore_turnstile.png      # Imagen generada del autómata Moore (se crea en ejecución)
├── mealy_turnstile.png      # Imagen generada del autómata Mealy (se crea en ejecución)
```

## 📸 Vista previa

🎥 Mira el video demostrativo: 
<video width="600" controls> <source src="evidencia.mp4" type="video/mp4"> Tu
navegador no soporta la reproducción de video. </video>


## 🧠 Conceptos aplicados

- Máquinas de estados finitos (FSM)
- Máquina de Moore
- Máquina de Mealy
- Transiciones autoapuntadas
- Acumulación y validación de entradas
- Visualización dinámica y retroalimentación audiovisual

## ✅ Requisitos

- Python 3.7+
- Librerías:
  ```bash
  pip install pygame pillow graphviz
  ```

> Asegúrate de tener Graphviz instalado en tu sistema para renderizar los diagramas correctamente.
## 🧪 Instalación paso a paso

1. **Instala las dependencias necesarias:**
   ```bash
   pip install pygame pillow graphviz
   ```

2. **Instala Graphviz (dependencia del sistema):**
   - En Windows: [Descargar Graphviz](https://graphviz.org/download/)
   - En macOS (con Homebrew):
     ```bash
     brew install graphviz
     ```
   - En Linux (Debian/Ubuntu):
     ```bash
     sudo apt install graphviz
     ```

3. **Verifica la instalación ejecutando el programa:**
   ```bash
   python Proyecto_U2.py
   ```
4. **Verifica la instalacion de graphviz en tu sistema:**
    ```bash
    dot -V
    ```
> Asegúrate de tener el archivo de sonido `sinacceso.mp3` en la carpeta `sound/` para una experiencia completa.
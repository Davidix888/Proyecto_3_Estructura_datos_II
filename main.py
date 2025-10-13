# main.py
import tkinter as tk
from interfaz_grafica import InterfazCompresion

def main():
    """
    Función principal que inicia la aplicación de compresión de datos
    """
    try:
        root = tk.Tk()
        app = InterfazCompresion(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")

if __name__ == "__main__":
    main()
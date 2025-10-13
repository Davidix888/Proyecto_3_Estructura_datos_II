# interfaz_grafica.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import font as tkfont
import os
from PIL import Image, ImageTk
import base64
from compresor_texto import CompresorTexto
from compresor_imagenes import CompresorImagenes
from compresor_audio import CompresorAudio
from utilidades import obtener_tamano_archivo, formatear_tamano

class InterfazCompresion:
    def __init__(self, root):
        self.root = root
        self.root.title("🔧 Sistema de Compresión de Datos - Proyecto 3")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f8ff')
        self.root.resizable(True, True)
        
        # Configurar estilo moderno
        self.configurar_estilos()
        
        # Inicializar compresores
        self.compresor_texto = CompresorTexto()
        self.compresor_imagenes = CompresorImagenes()
        self.compresor_audio = CompresorAudio()
        
        self.configurar_interfaz()
        
    def configurar_estilos(self):
        """Configura estilos modernos para la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores modernos
        style.configure('Titulo.TLabel', 
                       background='#2c3e50', 
                       foreground='white', 
                       font=('Arial', 18, 'bold'),
                       padding=20)
        
        style.configure('Card.TFrame', 
                       background='white', 
                       relief='raised', 
                       borderwidth=2)
        
        style.configure('Moderno.TButton',
                       font=('Arial', 11, 'bold'),
                       padding=(20, 10),
                       background='#3498db',
                       foreground='white')
        
        style.map('Moderno.TButton',
                 background=[('active', '#2980b9'),
                           ('pressed', '#21618c')])
        
        style.configure('Success.TLabel',
                       background='#d4edda',
                       foreground='#155724',
                       font=('Arial', 10),
                       padding=10)
        
        style.configure('Info.TLabel',
                       background='#d1ecf1',
                       foreground='#0c5460',
                       font=('Arial', 9),
                       padding=8)
        
    def configurar_interfaz(self):
        """Configura los elementos de la interfaz gráfica principal"""
        # Frame principal con gradiente
        frame_principal = tk.Frame(self.root, bg='#f0f8ff')
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header con título
        header_frame = tk.Frame(frame_principal, bg='#2c3e50', relief='raised', bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        titulo = tk.Label(header_frame, 
                         text="🔧 SISTEMA DE COMPRESIÓN DE DATOS", 
                         font=('Arial', 20, 'bold'),
                         bg='#2c3e50',
                         fg='white',
                         pady=20)
        titulo.pack()
        
        subtitulo = tk.Label(header_frame,
                            text="Proyecto 3 - Estructuras de Datos II",
                            font=('Arial', 12),
                            bg='#2c3e50',
                            fg='#bdc3c7',
                            pady=5)
        subtitulo.pack()
        
        # Frame para tarjetas de opciones
        opciones_frame = tk.Frame(frame_principal, bg='#f0f8ff')
        opciones_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tarjeta de Texto
        self.crear_tarjeta_opcion(opciones_frame, 
                                 "📝 Compresión de Texto", 
                                 "Algoritmo Huffman\nComprime archivos .txt", 
                                 "#e8f4f8",
                                 self.abrir_ventana_texto,
                                 0, 0)
        
        # Tarjeta de Imágenes
        self.crear_tarjeta_opcion(opciones_frame, 
                                 "🖼️ Compresión de Imágenes", 
                                 "Algoritmo RLE\nComprime .png y .bmp", 
                                 "#f8e8f4",
                                 self.abrir_ventana_imagenes,
                                 0, 1)
        
        # Tarjeta de Audio
        self.crear_tarjeta_opcion(opciones_frame, 
                                 "🎵 Compresión de Audio", 
                                 "Técnica de reducción\nComprime .wav y .mp3", 
                                 "#f4f8e8",
                                 self.abrir_ventana_audio,
                                 1, 0)
        
        # Información del proyecto
        info_frame = tk.Frame(frame_principal, bg='#34495e', relief='sunken', bd=1)
        info_frame.pack(fill=tk.X, pady=(20, 0))
        
        info_texto = "💡 Selecciona el tipo de archivo que deseas comprimir. Cada opción utiliza algoritmos especializados para máxima eficiencia."
        info_label = tk.Label(info_frame, 
                             text=info_texto,
                             font=('Arial', 10),
                             bg='#34495e',
                             fg='#ecf0f1',
                             wraplength=700,
                             justify=tk.CENTER,
                             pady=10)
        info_label.pack()
        
    def crear_tarjeta_opcion(self, parent, titulo, descripcion, color, comando, fila, columna):
        """Crea una tarjeta moderna para cada opción de compresión"""
        tarjeta_frame = tk.Frame(parent, 
                                bg=color, 
                                relief='raised', 
                                bd=2,
                                cursor='hand2')
        tarjeta_frame.grid(row=fila, column=columna, padx=10, pady=10, sticky='nsew')
        tarjeta_frame.bind("<Button-1>", lambda e: comando())
        
        # Configurar grid weights para responsividad
        parent.grid_rowconfigure(fila, weight=1)
        parent.grid_columnconfigure(columna, weight=1)
        
        # Icono y título
        titulo_label = tk.Label(tarjeta_frame,
                               text=titulo,
                               font=('Arial', 14, 'bold'),
                               bg=color,
                               fg='#2c3e50',
                               pady=10)
        titulo_label.pack()
        
        # Descripción
        desc_label = tk.Label(tarjeta_frame,
                             text=descripcion,
                             font=('Arial', 11),
                             bg=color,
                             fg='#34495e',
                             wraplength=200,
                             justify=tk.CENTER)
        desc_label.pack(pady=5)
        
        # Botón
        boton = ttk.Button(tarjeta_frame,
                          text="Abrir",
                          command=comando,
                          style='Moderno.TButton')
        boton.pack(pady=15)
        
        # Efecto hover
        def on_enter(e):
            tarjeta_frame.configure(bg=self.clarificar_color(color))
            titulo_label.configure(bg=self.clarificar_color(color))
            desc_label.configure(bg=self.clarificar_color(color))
            
        def on_leave(e):
            tarjeta_frame.configure(bg=color)
            titulo_label.configure(bg=color)
            desc_label.configure(bg=color)
            
        tarjeta_frame.bind("<Enter>", on_enter)
        tarjeta_frame.bind("<Leave>", on_leave)
        
    def clarificar_color(self, hex_color, factor=0.1):
        """Aclara un color hexadecimal"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
        
    def abrir_ventana_texto(self):
        """Abre la ventana para compresión de texto"""
        VentanaCompresionTexto(self.root, self.compresor_texto)
        
    def abrir_ventana_imagenes(self):
        """Abre la ventana para compresión de imágenes"""
        VentanaCompresionImagenes(self.root, self.compresor_imagenes)
        
    def abrir_ventana_audio(self):
        """Abre la ventana para compresión de audio"""
        VentanaCompresionAudio(self.root, self.compresor_audio)

class VentanaCompresionBase:
    """Clase base para ventanas de compresión con diseño moderno"""
    def __init__(self, parent, compresor, titulo, icono):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"{icono} {titulo}")
        self.ventana.geometry("600x500")
        self.ventana.configure(bg='#ecf0f1')
        self.ventana.resizable(True, True)
        
        # Centrar ventana
        self.centrar_ventana()
        
        self.compresor = compresor
        self.archivo_original = ""
        self.archivo_comprimido = ""
        
        self.configurar_interfaz()
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        ancho = self.ventana.winfo_width()
        alto = self.ventana.winfo_height()
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'+{x}+{y}')
        
    def configurar_interfaz(self):
        """Método abstracto para configurar la interfaz"""
        pass
        
    def seleccionar_archivo(self, tipos_archivo, titulo_dialogo):
        """Selecciona un archivo para comprimir con diálogo mejorado"""
        try:
            archivo = filedialog.askopenfilename(
                title=titulo_dialogo,
                filetypes=tipos_archivo
            )
            if archivo:
                self.archivo_original = archivo
                tamano = obtener_tamano_archivo(archivo)
                
                # Actualizar interfaz con información del archivo
                nombre_archivo = os.path.basename(archivo)
                self.label_archivo.config(
                    text=f"📄 Archivo seleccionado: {nombre_archivo}",
                    style='Info.TLabel'
                )
                self.label_tamano_original.config(
                    text=f"📊 Tamaño original: {formatear_tamano(tamano)}"
                )
                
                # Habilitar botón de compresión
                self.boton_comprimir.config(state='normal')
                return True
            return False
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo cargar el archivo: {e}")
            return False
            
    def mostrar_resultados(self, tamano_original, tamano_comprimido, archivo_comprimido):
        """Muestra los resultados de la compresión con diseño mejorado"""
        try:
            if tamano_original > 0:
                ratio = (tamano_comprimido / tamano_original) * 100
                ahorro = 100 - ratio
            else:
                ratio = 0
                ahorro = 0
                
            self.archivo_comprimido = archivo_comprimido
            
            resultado_texto = (f"✅ Compresión completada exitosamente!\n\n"
                             f"📊 Tamaño original: {formatear_tamano(tamano_original)}\n"
                             f"📦 Tamaño comprimido: {formatear_tamano(tamano_comprimido)}\n"
                             f"📈 Ratio de compresión: {ratio:.2f}%\n"
                             f"💰 Ahorro de espacio: {ahorro:.2f}%")
            
            self.label_resultados.config(text=resultado_texto, style='Success.TLabel')
            self.boton_descomprimir.config(state='normal')
            
            messagebox.showinfo("Éxito", "🎉 Compresión realizada correctamente!")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudieron calcular los resultados: {e}")

class VentanaCompresionTexto(VentanaCompresionBase):
    def __init__(self, parent, compresor):
        super().__init__(parent, compresor, "Compresión de Texto", "📝")
        
    def configurar_interfaz(self):
        # Frame principal
        main_frame = tk.Frame(self.ventana, bg='#ecf0f1', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#3498db', relief='raised', bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        titulo = tk.Label(header_frame,
                         text="📝 Compresión de Texto - Algoritmo Huffman",
                         font=('Arial', 16, 'bold'),
                         bg='#3498db',
                         fg='white',
                         pady=15)
        titulo.pack()
        
        # Frame de contenido
        content_frame = tk.Frame(main_frame, bg='white', relief='sunken', bd=1, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botón seleccionar archivo
        boton_seleccionar = ttk.Button(content_frame,
                                      text="📁 Seleccionar Archivo .txt",
                                      command=lambda: self.seleccionar_archivo(
                                          [("Archivos de texto", "*.txt")],
                                          "Seleccionar archivo de texto"
                                      ),
                                      style='Moderno.TButton')
        boton_seleccionar.pack(pady=15)
        
        # Información del archivo
        info_frame = tk.Frame(content_frame, bg='#f8f9fa', relief='ridge', bd=1, padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.label_archivo = ttk.Label(info_frame, text="📄 No se ha seleccionado archivo")
        self.label_archivo.pack(pady=5)
        
        self.label_tamano_original = ttk.Label(info_frame, text="📊 Tamaño original: --")
        self.label_tamano_original.pack(pady=5)
        
        # Frame de botones de acción
        action_frame = tk.Frame(content_frame, bg='white')
        action_frame.pack(pady=20)
        
        self.boton_comprimir = ttk.Button(action_frame,
                                         text="🗜️ Comprimir",
                                         command=self.comprimir,
                                         state='disabled',
                                         style='Moderno.TButton')
        self.boton_comprimir.grid(row=0, column=0, padx=10)
        
        self.boton_descomprimir = ttk.Button(action_frame,
                                            text="📤 Descomprimir",
                                            command=self.descomprimir,
                                            state='disabled',
                                            style='Moderno.TButton')
        self.boton_descomprimir.grid(row=0, column=1, padx=10)
        
        # Resultados
        resultados_frame = tk.Frame(content_frame, bg='white')
        resultados_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.label_resultados = ttk.Label(resultados_frame,
                                         text="ℹ️ Los resultados aparecerán aquí después de la compresión",
                                         justify=tk.LEFT,
                                         style='Info.TLabel')
        self.label_resultados.pack(fill=tk.BOTH, expand=True)
        
    def comprimir(self):
        if not self.archivo_original:
            messagebox.showwarning("Advertencia", "⚠️ Por favor seleccione un archivo primero")
            return
            
        try:
            # Mostrar progreso
            self.label_resultados.config(text="⏳ Comprimiendo archivo... Por favor espere.")
            self.ventana.update()
            
            archivo_comprimido = self.compresor.comprimir(self.archivo_original)
            tamano_original = obtener_tamano_archivo(self.archivo_original)
            tamano_comprimido = obtener_tamano_archivo(archivo_comprimido)
            
            self.mostrar_resultados(tamano_original, tamano_comprimido, archivo_comprimido)
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo comprimir el archivo: {e}")
            self.label_resultados.config(text="❌ Error en la compresión")
            
    def descomprimir(self):
        if not self.archivo_comprimido:
            messagebox.showwarning("Advertencia", "⚠️ No hay archivo comprimido para descomprimir")
            return
            
        try:
            self.label_resultados.config(text="⏳ Descomprimiendo archivo... Por favor espere.")
            self.ventana.update()
            
            archivo_descomprimido = self.compresor.descomprimir(self.archivo_comprimido)
            messagebox.showinfo("Éxito", f"✅ Archivo descomprimido:\n{archivo_descomprimido}")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo descomprimir el archivo: {e}")

class VentanaCompresionImagenes(VentanaCompresionBase):
    def __init__(self, parent, compresor):
        super().__init__(parent, compresor, "Compresión de Imágenes", "🖼️")
        
    def configurar_interfaz(self):
        main_frame = tk.Frame(self.ventana, bg='#ecf0f1', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#9b59b6', relief='raised', bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        titulo = tk.Label(header_frame,
                         text="🖼️ Compresión de Imágenes - Algoritmo RLE",
                         font=('Arial', 16, 'bold'),
                         bg='#9b59b6',
                         fg='white',
                         pady=15)
        titulo.pack()
        
        content_frame = tk.Frame(main_frame, bg='white', relief='sunken', bd=1, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        boton_seleccionar = ttk.Button(content_frame,
                                      text="🖼️ Seleccionar Imagen (.png, .bmp)",
                                      command=lambda: self.seleccionar_archivo([
                                          ("Imágenes PNG", "*.png"),
                                          ("Imágenes BMP", "*.bmp")
                                      ], "Seleccionar imagen"),
                                      style='Moderno.TButton')
        boton_seleccionar.pack(pady=15)
        
        info_frame = tk.Frame(content_frame, bg='#f8f9fa', relief='ridge', bd=1, padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.label_archivo = ttk.Label(info_frame, text="🖼️ No se ha seleccionado archivo")
        self.label_archivo.pack(pady=5)
        
        self.label_tamano_original = ttk.Label(info_frame, text="📊 Tamaño original: --")
        self.label_tamano_original.pack(pady=5)
        
        action_frame = tk.Frame(content_frame, bg='white')
        action_frame.pack(pady=20)
        
        self.boton_comprimir = ttk.Button(action_frame,
                                         text="🗜️ Comprimir",
                                         command=self.comprimir,
                                         state='disabled',
                                         style='Moderno.TButton')
        self.boton_comprimir.grid(row=0, column=0, padx=10)
        
        self.boton_descomprimir = ttk.Button(action_frame,
                                            text="📤 Descomprimir",
                                            command=self.descomprimir,
                                            state='disabled',
                                            style='Moderno.TButton')
        self.boton_descomprimir.grid(row=0, column=1, padx=10)
        
        resultados_frame = tk.Frame(content_frame, bg='white')
        resultados_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.label_resultados = ttk.Label(resultados_frame,
                                         text="ℹ️ Los resultados aparecerán aquí después de la compresión",
                                         justify=tk.LEFT,
                                         style='Info.TLabel')
        self.label_resultados.pack(fill=tk.BOTH, expand=True)
        
    def comprimir(self):
        if not self.archivo_original:
            messagebox.showwarning("Advertencia", "⚠️ Por favor seleccione un archivo primero")
            return
            
        try:
            self.label_resultados.config(text="⏳ Comprimiendo imagen... Por favor espere.")
            self.ventana.update()
            
            archivo_comprimido = self.compresor.comprimir(self.archivo_original)
            tamano_original = obtener_tamano_archivo(self.archivo_original)
            tamano_comprimido = obtener_tamano_archivo(archivo_comprimido)
            
            self.mostrar_resultados(tamano_original, tamano_comprimido, archivo_comprimido)
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo comprimir la imagen: {e}")
            self.label_resultados.config(text="❌ Error en la compresión")
            
    def descomprimir(self):
        if not self.archivo_comprimido:
            messagebox.showwarning("Advertencia", "⚠️ No hay archivo comprimido para descomprimir")
            return
            
        try:
            self.label_resultados.config(text="⏳ Descomprimiendo imagen... Por favor espere.")
            self.ventana.update()
            
            archivo_descomprimido = self.compresor.descomprimir(self.archivo_comprimido)
            messagebox.showinfo("Éxito", f"✅ Imagen descomprimida:\n{archivo_descomprimido}")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo descomprimir la imagen: {e}")

class VentanaCompresionAudio(VentanaCompresionBase):
    def __init__(self, parent, compresor):
        super().__init__(parent, compresor, "Compresión de Audio", "🎵")
        
    def configurar_interfaz(self):
        main_frame = tk.Frame(self.ventana, bg='#ecf0f1', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = tk.Frame(main_frame, bg='#e74c3c', relief='raised', bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        titulo = tk.Label(header_frame,
                         text="🎵 Compresión de Audio",
                         font=('Arial', 16, 'bold'),
                         bg='#e74c3c',
                         fg='white',
                         pady=15)
        titulo.pack()
        
        content_frame = tk.Frame(main_frame, bg='white', relief='sunken', bd=1, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        boton_seleccionar = ttk.Button(content_frame,
                                      text="🎵 Seleccionar Audio (.wav, .mp3)",
                                      command=lambda: self.seleccionar_archivo([
                                          ("Audio WAV", "*.wav"),
                                          ("Audio MP3", "*.mp3")
                                      ], "Seleccionar archivo de audio"),
                                      style='Moderno.TButton')
        boton_seleccionar.pack(pady=15)
        
        info_frame = tk.Frame(content_frame, bg='#f8f9fa', relief='ridge', bd=1, padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.label_archivo = ttk.Label(info_frame, text="🎵 No se ha seleccionado archivo")
        self.label_archivo.pack(pady=5)
        
        self.label_tamano_original = ttk.Label(info_frame, text="📊 Tamaño original: --")
        self.label_tamano_original.pack(pady=5)
        
        action_frame = tk.Frame(content_frame, bg='white')
        action_frame.pack(pady=20)
        
        self.boton_comprimir = ttk.Button(action_frame,
                                         text="🗜️ Comprimir",
                                         command=self.comprimir,
                                         state='disabled',
                                         style='Moderno.TButton')
        self.boton_comprimir.grid(row=0, column=0, padx=10)
        
        self.boton_descomprimir = ttk.Button(action_frame,
                                            text="📤 Descomprimir",
                                            command=self.descomprimir,
                                            state='disabled',
                                            style='Moderno.TButton')
        self.boton_descomprimir.grid(row=0, column=1, padx=10)
        
        resultados_frame = tk.Frame(content_frame, bg='white')
        resultados_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.label_resultados = ttk.Label(resultados_frame,
                                         text="ℹ️ Los resultados aparecerán aquí después de la compresión",
                                         justify=tk.LEFT,
                                         style='Info.TLabel')
        self.label_resultados.pack(fill=tk.BOTH, expand=True)
        
    def comprimir(self):
        if not self.archivo_original:
            messagebox.showwarning("Advertencia", "⚠️ Por favor seleccione un archivo primero")
            return
            
        try:
            self.label_resultados.config(text="⏳ Comprimiendo audio... Por favor espere.")
            self.ventana.update()
            
            archivo_comprimido = self.compresor.comprimir(self.archivo_original)
            tamano_original = obtener_tamano_archivo(self.archivo_original)
            tamano_comprimido = obtener_tamano_archivo(archivo_comprimido)
            
            self.mostrar_resultados(tamano_original, tamano_comprimido, archivo_comprimido)
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo comprimir el audio: {e}")
            self.label_resultados.config(text="❌ Error en la compresión")
            
    def descomprimir(self):
        if not self.archivo_comprimido:
            messagebox.showwarning("Advertencia", "⚠️ No hay archivo comprimido para descomprimir")
            return
            
        try:
            self.label_resultados.config(text="⏳ Descomprimiendo audio... Por favor espere.")
            self.ventana.update()
            
            archivo_descomprimido = self.compresor.descomprimir(self.archivo_comprimido)
            messagebox.showinfo("Éxito", f"✅ Audio descomprimido:\n{archivo_descomprimido}")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo descomprimir el audio: {e}")
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
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
        
        style.configure('Titulo.TLabel', 
                       background='#2c3e50', 
                       foreground='white', 
                       font=('Arial', 18, 'bold'),
                       padding=20)
        
        style.configure('Moderno.TButton',
                       font=('Arial', 11, 'bold'),
                       padding=(20, 10),
                       background='#3498db',
                       foreground='white')
        
        style.map('Moderno.TButton',
                 background=[('active', '#2980b9'),
                           ('pressed', '#21618c')])
        
    def configurar_interfaz(self):
        """Configura los elementos de la interfaz gráfica principal"""
        # Frame principal
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
                            text="Proyecto 3 - Estructuras de Datos II - Solo Compresión",
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
                                 "Algoritmo Huffman\nComprime archivos .txt a .bin", 
                                 "#e8f4f8",
                                 self.abrir_ventana_texto,
                                 0, 0)
        
        # Tarjeta de Imágenes
        self.crear_tarjeta_opcion(opciones_frame, 
                                 "🖼️ Compresión de Imágenes", 
                                 "Algoritmo RLE\nComprime .png y .bmp a .rle", 
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
        
    def crear_tarjeta_opcion(self, parent, titulo, descripcion, color, comando, fila, columna):
        """Crea una tarjeta moderna para cada opción de compresión"""
        tarjeta_frame = tk.Frame(parent, 
                                bg=color, 
                                relief='raised', 
                                bd=2,
                                cursor='hand2')
        tarjeta_frame.grid(row=fila, column=columna, padx=10, pady=10, sticky='nsew')
        
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
                          text="Comprimir",
                          command=comando,
                          style='Moderno.TButton')
        boton.pack(pady=15)
        
    def abrir_ventana_texto(self):
        """Abre la ventana para compresión de texto"""
        ventana = VentanaCompresionTexto(self.root, self.compresor_texto)
        self._configurar_ventana_secundaria(ventana.ventana)
        
    def abrir_ventana_imagenes(self):
        """Abre la ventana para compresión de imágenes"""
        ventana = VentanaCompresionImagenes(self.root, self.compresor_imagenes)
        self._configurar_ventana_secundaria(ventana.ventana)
        
    def abrir_ventana_audio(self):
        """Abre la ventana para compresión de audio"""
        ventana = VentanaCompresionAudio(self.root, self.compresor_audio)
        self._configurar_ventana_secundaria(ventana.ventana)
    
    def _configurar_ventana_secundaria(self, ventana):
        """Configura el comportamiento de las ventanas secundarias"""
        ventana.transient(self.root)  # Mantiene relación con la ventana principal
        ventana.focus_set()  # Da foco a la ventana secundaria

class VentanaCompresionBase:
    """Clase base para ventanas de compresión"""
    def __init__(self, parent, compresor, titulo, icono):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title(f"{icono} {titulo}")
        self.ventana.geometry("500x500")
        self.ventana.configure(bg='#ecf0f1')
        self.ventana.resizable(True, True)
        
        # Centrar ventana
        self.centrar_ventana()
        
        self.compresor = compresor
        self.archivo_original = ""
        
        self.configurar_interfaz()
        
        # Configurar comportamiento al cerrar
        self.ventana.protocol("WM_DELETE_WINDOW", self._al_cerrar)
        
    def _al_cerrar(self):
        """Comportamiento cuando se cierra la ventana"""
        self.ventana.destroy()
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.ventana.update_idletasks()
        ancho = 500
        alto = 500
        x = (self.ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (alto // 2)
        self.ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
        
    def configurar_interfaz(self):
        """Método abstracto para configurar la interfaz"""
        pass
        
    def seleccionar_archivo(self, tipos_archivo, titulo_dialogo):
        """Selecciona un archivo para comprimir"""
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
                self.label_archivo.config(text=f"📄 Archivo: {nombre_archivo}")
                self.label_tamano_original.config(text=f"📊 Tamaño original: {formatear_tamano(tamano)}")
                
                # Habilitar botón de compresión
                self.boton_comprimir.config(state='normal')
                
                return True
            return False
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo cargar el archivo: {e}")
            return False
            
    def mostrar_resultados(self, tamano_original, tamano_comprimido, archivo_comprimido):
        """Muestra los resultados de la compresión"""
        try:
            if tamano_original > 0:
                ratio = (tamano_comprimido / tamano_original) * 100
                ahorro = 100 - ratio
            else:
                ratio = 0
                ahorro = 0
                
            resultado_texto = (f"✅ Compresión completada!\n\n"
                             f"📊 Tamaño original: {formatear_tamano(tamano_original)}\n"
                             f"📦 Tamaño comprimido: {formatear_tamano(tamano_comprimido)}\n"
                             f"📈 Ratio de compresión: {ratio:.2f}%\n"
                             f"💰 Ahorro de espacio: {ahorro:.2f}%\n\n"
                             f"📁 Archivo generado:\n{archivo_comprimido}")
            
            self.label_resultados.config(text=resultado_texto)
            messagebox.showinfo("Éxito", "🎉 Compresión realizada correctamente!")
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudieron calcular los resultados: {e}")

class VentanaCompresionTexto(VentanaCompresionBase):
    def __init__(self, parent, compresor):
        super().__init__(parent, compresor, "Compresión de Texto", "📝")
        
    def configurar_interfaz(self):
        main_frame = tk.Frame(self.ventana, bg='#ecf0f1', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#3498db', relief='raised', bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        titulo = tk.Label(header_frame,
                         text="📝 Compresión de Texto - Algoritmo Huffman",
                         font=('Arial', 14, 'bold'),
                         bg='#3498db',
                         fg='white',
                         pady=10)
        titulo.pack()
        
        # Frame de contenido
        content_frame = tk.Frame(main_frame, bg='white', relief='sunken', bd=1, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botón seleccionar archivo
        boton_seleccionar = ttk.Button(content_frame,
                                      text="📁 Seleccionar Archivo .txt",
                                      command=lambda: self.seleccionar_archivo(
                                          [("Archivos de texto", "*.txt")],
                                          "Seleccionar archivo .txt para comprimir"
                                      ),
                                      style='Moderno.TButton')
        boton_seleccionar.pack(pady=15)
        
        # Información del archivo
        info_frame = tk.Frame(content_frame, bg='#f8f9fa', relief='ridge', bd=1, padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.label_archivo = tk.Label(info_frame, text="📄 No se ha seleccionado archivo", bg='#f8f9fa')
        self.label_archivo.pack(pady=5)
        
        self.label_tamano_original = tk.Label(info_frame, text="📊 Tamaño original: --", bg='#f8f9fa')
        self.label_tamano_original.pack(pady=5)
        
        # Botón comprimir (inicialmente deshabilitado)
        self.boton_comprimir = ttk.Button(content_frame,
                                         text="🗜️ Comprimir a .bin",
                                         command=self.comprimir,
                                         style='Moderno.TButton',
                                         state='disabled')
        self.boton_comprimir.pack(pady=20)
        
        # Resultados
        self.label_resultados = tk.Label(content_frame, text="", bg='white', justify=tk.LEFT, wraplength=400)
        self.label_resultados.pack(pady=10, fill=tk.BOTH, expand=True)
        
    def comprimir(self):
        if not self.archivo_original:
            messagebox.showwarning("Advertencia", "⚠️ Por favor seleccione un archivo .txt primero")
            return
            
        try:
            self.label_resultados.config(text="⏳ Comprimiendo archivo... Por favor espere.")
            self.ventana.update()
            
            archivo_comprimido = self.compresor.comprimir(self.archivo_original)
            tamano_original = obtener_tamano_archivo(self.archivo_original)
            tamano_comprimido = obtener_tamano_archivo(archivo_comprimido)
            
            self.mostrar_resultados(tamano_original, tamano_comprimido, archivo_comprimido)
            
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo comprimir el archivo: {e}")
            self.label_resultados.config(text="❌ Error en la compresión")


class VentanaCompresionImagenes(VentanaCompresionBase):
    def __init__(self, parent, compresor):
        super().__init__(parent, compresor, "Compresión de Imágenes", "🖼️")

    def configurar_interfaz(self):
        main_frame = tk.Frame(self.ventana, bg='#ecf0f1', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = tk.Frame(main_frame, bg='#9b59b6', relief='raised', bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 20))

        titulo = tk.Label(header_frame,
                          text="🖼️ Compresión de Imágenes - Algoritmo RLE",
                          font=('Arial', 14, 'bold'),
                          bg='#9b59b6',
                          fg='white',
                          pady=10)
        titulo.pack()

        # Frame de contenido
        content_frame = tk.Frame(main_frame, bg='white', relief='sunken', bd=1, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Botón seleccionar archivo
        boton_seleccionar = ttk.Button(content_frame,
                                       text="🖼️ Seleccionar Imagen",
                                       command=lambda: self.seleccionar_archivo([
                                           ("Imágenes PNG", "*.png"),
                                           ("Imágenes BMP", "*.bmp")
                                       ], "Seleccionar imagen para comprimir"),
                                       style='Moderno.TButton')
        boton_seleccionar.pack(pady=15)

        # Información del archivo
        info_frame = tk.Frame(content_frame, bg='#f8f9fa', relief='ridge', bd=1, padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=10)

        self.label_archivo = tk.Label(info_frame, text="🖼️ No se ha seleccionado archivo", bg='#f8f9fa')
        self.label_archivo.pack(pady=5)

        self.label_tamano_original = tk.Label(info_frame, text="📊 Tamaño original: --", bg='#f8f9fa')
        self.label_tamano_original.pack(pady=5)

        # Botón comprimir (inicialmente deshabilitado)
        self.boton_comprimir = ttk.Button(content_frame,
                                          text="🗜️ Comprimir a .rle",
                                          command=self.comprimir,
                                          style='Moderno.TButton',
                                          state='disabled')
        self.boton_comprimir.pack(pady=10)

        # Botón descomprimir (.rle)
        self.boton_descomprimir = ttk.Button(content_frame,
                                             text="🔓 Descomprimir .rle",
                                             command=self.descomprimir,
                                             style='Moderno.TButton')
        self.boton_descomprimir.pack(pady=10)

        # Botón visualizar reconstruida
        self.boton_visualizar = ttk.Button(content_frame,
                                           text="👁️ Visualizar imagen reconstruida",
                                           command=self.visualizar_imagen,
                                           style='Moderno.TButton')
        self.boton_visualizar.pack(pady=10)

        # Resultados
        self.label_resultados = tk.Label(content_frame, text="", bg='white', justify=tk.LEFT, wraplength=400)
        self.label_resultados.pack(pady=10, fill=tk.BOTH, expand=True)

    def comprimir(self):
        if not self.archivo_original:
            messagebox.showwarning("Advertencia", "⚠️ Por favor seleccione una imagen primero")
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

    # -------------------- NUEVOS MÉTODOS --------------------
    def descomprimir(self):
        """Permite seleccionar un .rle y reconstruir la imagen."""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo .rle para descomprimir",
            filetypes=[("Archivo RLE", "*.rle")]
        )
        if not archivo:
            return

        try:
            self.label_resultados.config(text="⏳ Descomprimiendo imagen... Por favor espere.")
            self.ventana.update()

            archivo_reconstruido = self.compresor.descomprimir(archivo)
            # Actualizamos ultima salida y mostramos info
            self.label_resultados.config(text=f"✅ Imagen reconstruida: {os.path.basename(archivo_reconstruido)}")
            messagebox.showinfo("Éxito", f"🎉 Imagen reconstruida:\n{archivo_reconstruido}")

        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo descomprimir la imagen: {e}")
            self.label_resultados.config(text="❌ Error en la descompresión")

    def visualizar_imagen(self):
        """Abre la última imagen reconstruida en el visor del sistema."""
        try:
            from PIL import Image
            ruta = getattr(self.compresor, "ultima_salida", None)
            if ruta and os.path.exists(ruta):
                Image.open(ruta).show()
            else:
                messagebox.showwarning("Atención",
                                       "⚠️ No hay imagen disponible para visualizar. Puedes descomprimir primero.")
        except Exception as e:
            messagebox.showerror("Error", f"❌ No se pudo abrir la imagen: {e}")


class VentanaCompresionAudio(VentanaCompresionBase):
    def __init__(self, parent, compresor):
        super().__init__(parent, compresor, "Compresión de Audio", "🎵")
        
    def configurar_interfaz(self):
        main_frame = tk.Frame(self.ventana, bg='#ecf0f1', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#e74c3c', relief='raised', bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        titulo = tk.Label(header_frame,
                         text="🎵 Compresión de Audio",
                         font=('Arial', 14, 'bold'),
                         bg='#e74c3c',
                         fg='white',
                         pady=10)
        titulo.pack()
        
        # Frame de contenido
        content_frame = tk.Frame(main_frame, bg='white', relief='sunken', bd=1, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Botón seleccionar archivo
        boton_seleccionar = ttk.Button(content_frame,
                                      text="🎵 Seleccionar Audio",
                                      command=lambda: self.seleccionar_archivo([
                                          ("Audio WAV", "*.wav"),
                                          ("Audio MP3", "*.mp3")
                                      ], "Seleccionar archivo de audio para comprimir"),
                                      style='Moderno.TButton')
        boton_seleccionar.pack(pady=15)
        
        # Información del archivo
        info_frame = tk.Frame(content_frame, bg='#f8f9fa', relief='ridge', bd=1, padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=10)
        
        self.label_archivo = tk.Label(info_frame, text="🎵 No se ha seleccionado archivo", bg='#f8f9fa')
        self.label_archivo.pack(pady=5)
        
        self.label_tamano_original = tk.Label(info_frame, text="📊 Tamaño original: --", bg='#f8f9fa')
        self.label_tamano_original.pack(pady=5)
        
        # Botón comprimir (inicialmente deshabilitado)
        self.boton_comprimir = ttk.Button(content_frame,
                                         text="🗜️ Comprimir Audio",
                                         command=self.comprimir,
                                         style='Moderno.TButton',
                                         state='disabled')
        self.boton_comprimir.pack(pady=20)
        
        # Resultados
        self.label_resultados = tk.Label(content_frame, text="", bg='white', justify=tk.LEFT, wraplength=400)
        self.label_resultados.pack(pady=10, fill=tk.BOTH, expand=True)
        
    def comprimir(self):
        if not self.archivo_original:
            messagebox.showwarning("Advertencia", "⚠️ Por favor seleccione un archivo de audio primero")
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
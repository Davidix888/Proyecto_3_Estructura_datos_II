# compresor_imagenes.py
from PIL import Image
import os
import struct

class CompresorImagenes:
    def __init__(self):
        pass
    
    def comprimir(self, archivo_imagen):
        """
        Comprime una imagen usando Run-Length Encoding (RLE)
        """
        try:
            # Abrir y procesar la imagen
            imagen = Image.open(archivo_imagen)
            ancho, alto = imagen.size
            modo = imagen.mode
            pixeles = list(imagen.getdata())
            
            # Aplicar RLE
            pixeles_comprimidos = self._aplicar_rle(pixeles)
            
            # Guardar datos comprimidos
            nombre_base = os.path.splitext(archivo_imagen)[0]
            archivo_salida = nombre_base + "_comprimido.rle"
            
            # Guardar en formato binario limpio
            self._guardar_comprimido(archivo_salida, pixeles_comprimidos, ancho, alto, modo)
            
            return archivo_salida
            
        except Exception as e:
            raise Exception(f"Error en compresión de imagen: {e}")
    
    def descomprimir(self, archivo_comprimido):
        """
        Descomprime una imagen comprimida con RLE
        """
        try:
            # Cargar datos comprimidos
            pixeles_comprimidos, ancho, alto, modo = self._cargar_comprimido(archivo_comprimido)
            
            # Reconstruir pixeles
            pixeles = self._aplicar_descompresion_rle(pixeles_comprimidos)
            
            # Reconstruir imagen
            imagen = Image.new(modo, (ancho, alto))
            imagen.putdata(pixeles)
            
            # Guardar imagen reconstruida
            nombre_base = os.path.splitext(archivo_comprimido)[0]
            archivo_salida = nombre_base + "_reconstruida.png"
            
            imagen.save(archivo_salida)
            return archivo_salida
            
        except Exception as e:
            raise Exception(f"Error en descompresión de imagen: {e}")
    
    def _aplicar_rle(self, pixeles):
        """
        Aplica Run-Length Encoding a la lista de pixeles
        """
        if not pixeles:
            return []
        
        comprimido = []
        actual = pixeles[0]
        contador = 1
        
        for pixel in pixeles[1:]:
            if pixel == actual:
                contador += 1
            else:
                comprimido.append((actual, contador))
                actual = pixel
                contador = 1
        
        comprimido.append((actual, contador))
        return comprimido
    
    def _aplicar_descompresion_rle(self, pixeles_comprimidos):
        """
        Descomprime datos RLE a lista de pixeles
        """
        pixeles = []
        for pixel, contador in pixeles_comprimidos:
            pixeles.extend([pixel] * contador)
        return pixeles
    
    def _guardar_comprimido(self, archivo_salida, pixeles_comprimidos, ancho, alto, modo):
        """
        Guarda los datos RLE en formato binario limpio
        """
        with open(archivo_salida, 'wb') as archivo:
            # Guardar dimensiones y modo
            archivo.write(ancho.to_bytes(4, byteorder='big'))
            archivo.write(alto.to_bytes(4, byteorder='big'))
            
            # Guardar modo de color
            modo_bytes = modo.encode('utf-8')
            archivo.write(len(modo_bytes).to_bytes(2, byteorder='big'))
            archivo.write(modo_bytes)
            
            # Guardar cantidad de secuencias RLE
            archivo.write(len(pixeles_comprimidos).to_bytes(4, byteorder='big'))
            
            # Guardar secuencias RLE
            for pixel, contador in pixeles_comprimidos:
                # Guardar pixel
                if isinstance(pixel, int):
                    # Escala de grises
                    archivo.write(pixel.to_bytes(1, byteorder='big'))
                elif isinstance(pixel, tuple):
                    # RGB/RGBA
                    for componente in pixel:
                        archivo.write(componente.to_bytes(1, byteorder='big'))
                
                # Guardar contador
                archivo.write(contador.to_bytes(4, byteorder='big'))
    
    def _cargar_comprimido(self, archivo_comprimido):
        """
        Carga los datos RLE desde archivo binario
        """
        with open(archivo_comprimido, 'rb') as archivo:
            # Leer dimensiones
            ancho = int.from_bytes(archivo.read(4), byteorder='big')
            alto = int.from_bytes(archivo.read(4), byteorder='big')
            
            # Leer modo
            long_modo = int.from_bytes(archivo.read(2), byteorder='big')
            modo_bytes = archivo.read(long_modo)
            modo = modo_bytes.decode('utf-8')
            
            # Leer cantidad de secuencias
            num_secuencias = int.from_bytes(archivo.read(4), byteorder='big')
            
            pixeles_comprimidos = []
            
            # Determinar tamaño del pixel basado en el modo
            if modo == 'L':
                componentes_por_pixel = 1
            elif modo == 'RGB':
                componentes_por_pixel = 3
            elif modo == 'RGBA':
                componentes_por_pixel = 4
            else:
                componentes_por_pixel = 3  # Por defecto
            
            for _ in range(num_secuencias):
                # Leer pixel
                if componentes_por_pixel == 1:
                    pixel = int.from_bytes(archivo.read(1), byteorder='big')
                else:
                    pixel = tuple(int.from_bytes(archivo.read(1), byteorder='big') 
                                for _ in range(componentes_por_pixel))
                
                # Leer contador
                contador = int.from_bytes(archivo.read(4), byteorder='big')
                
                pixeles_comprimidos.append((pixel, contador))
            
            return pixeles_comprimidos, ancho, alto, modo
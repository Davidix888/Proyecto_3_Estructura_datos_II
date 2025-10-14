# compresor_imagenes.py
from PIL import Image
import os

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
            
            # Guardar datos comprimidos en formato .rle
            nombre_base = os.path.splitext(archivo_imagen)[0]
            archivo_salida = nombre_base + "_comprimido.rle"
            
            # Guardar en formato texto legible
            self._guardar_comprimido(archivo_salida, pixeles_comprimidos, ancho, alto, modo)
            
            return archivo_salida
            
        except Exception as e:
            raise Exception(f"Error en compresión de imagen: {e}")
    
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
    
    def _guardar_comprimido(self, archivo_salida, pixeles_comprimidos, ancho, alto, modo):
        """
        Guarda los datos RLE en formato .rle legible
        """
        with open(archivo_salida, 'w', encoding='utf-8') as archivo:
            # Guardar información básica
            archivo.write(f"ANCHO:{ancho}\n")
            archivo.write(f"ALTO:{alto}\n")
            archivo.write(f"MODO:{modo}\n")
            archivo.write("DATOS_RLE:\n")
            
            # Guardar secuencias RLE
            for i, (pixel, contador) in enumerate(pixeles_comprimidos):
                if isinstance(pixel, int):
                    # Escala de grises
                    archivo.write(f"{pixel}:{contador}")
                else:
                    # RGB/RGBA - convertir tupla a string
                    pixel_str = ','.join(map(str, pixel))
                    archivo.write(f"({pixel_str}):{contador}")
                
                # Nueva línea cada 5 secuencias para mejor legibilidad
                if (i + 1) % 5 == 0:
                    archivo.write("\n")
                else:
                    archivo.write(" ")
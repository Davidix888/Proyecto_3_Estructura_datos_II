# compresor_imagenes.py
from PIL import Image
import os

class CompresorImagenes:
    def __init__(self):
        self.ultima_salida = None  # Guarda el último archivo generado (comprimido o reconstruido)

    # ======================================================
    # COMPRESIÓN
    # ======================================================
    def comprimir(self, archivo_imagen):
        """
        Comprime una imagen usando Run-Length Encoding (RLE)
        """
        try:
            imagen = Image.open(archivo_imagen)
            imagen = imagen.convert("RGB")  # Asegura modo RGB
            ancho, alto = imagen.size
            modo = imagen.mode
            pixeles = list(imagen.getdata())

            # Aplicar RLE
            pixeles_comprimidos = self._aplicar_rle(pixeles)

            # Guardar datos comprimidos en formato .rle
            nombre_base = os.path.splitext(archivo_imagen)[0]
            archivo_salida = nombre_base + "_comprimido.rle"

            self._guardar_comprimido(archivo_salida, pixeles_comprimidos, ancho, alto, modo)
            self.ultima_salida = archivo_salida
            return archivo_salida

        except Exception as e:
            raise Exception(f"Error en compresión de imagen: {e}")

    def _aplicar_rle(self, pixeles):
        """Aplica Run-Length Encoding a la lista de píxeles"""
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
        """Guarda los datos RLE en formato .rle legible"""
        with open(archivo_salida, 'w', encoding='utf-8') as archivo:
            archivo.write(f"ANCHO:{ancho}\n")
            archivo.write(f"ALTO:{alto}\n")
            archivo.write(f"MODO:{modo}\n")
            archivo.write("DATOS_RLE:\n")
            for (pixel, contador) in pixeles_comprimidos:
                pixel_str = ','.join(map(str, pixel))
                archivo.write(f"({pixel_str}):{contador}\n")

    # ======================================================
    # DESCOMPRESIÓN
    # ======================================================
    def descomprimir(self, archivo_rle):
        try:
            with open(archivo_rle, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()

            # Extraer metadatos
            ancho = int(lineas[0].split(':')[1])
            alto = int(lineas[1].split(':')[1])
            modo = lineas[2].split(':')[1].strip()

            # Saltar encabezados y quedarse con los datos RLE
            datos_rle = []
            for linea in lineas[4:]:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(" ")
                for parte in partes:
                    if not parte:
                        continue
                    pixel_str, contador_str = parte.split(':')
                    contador = int(contador_str)

                    # Determinar si es RGB o escala de grises
                    if pixel_str.startswith("(") and pixel_str.endswith(")"):
                        # RGB: quitar paréntesis y convertir a tupla
                        valores = tuple(map(int, pixel_str[1:-1].split(',')))
                        datos_rle.append((valores, contador))
                    else:
                        # Escala de grises
                        datos_rle.append((int(pixel_str), contador))

            # Reconstruir lista de píxeles
            pixeles = []
            for pixel, repeticiones in datos_rle:
                pixeles.extend([pixel] * repeticiones)

            # Validar cantidad de píxeles
            if len(pixeles) != ancho * alto:
                raise Exception(
                    f"La cantidad de píxeles ({len(pixeles)}) no coincide con el tamaño de la imagen ({ancho * alto}).")

            # Crear imagen y guardarla
            imagen = Image.new(modo, (ancho, alto))
            imagen.putdata(pixeles)

            nombre_base = os.path.splitext(archivo_rle)[0]
            archivo_salida = nombre_base + "_reconstruida.png"
            imagen.save(archivo_salida)

            # Guardar ruta para visualizar
            self.ultima_salida = archivo_salida

            return archivo_salida

        except Exception as e:
            raise Exception(f"Error en descompresión: {e}")
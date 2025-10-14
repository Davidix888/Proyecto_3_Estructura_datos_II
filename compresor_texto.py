# compresor_texto.py
import heapq
import os
from collections import Counter

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None
        
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

class CompresorTexto:
    def __init__(self):
        self.codigos = {}
        
    def comprimir(self, archivo_entrada):
        """
        Comprime un archivo de texto usando el algoritmo de Huffman
        """
        try:
            # Leer el archivo de texto
            with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
                texto = archivo.read()
            
            if not texto:
                raise ValueError("El archivo está vacío")
            
            # Generar árbol de Huffman y códigos
            arbol = self._construir_arbol_huffman(texto)
            self.codigos = {}
            self._generar_codigos(arbol, "")
            
            # Codificar el texto
            texto_codificado = "".join(self.codigos[caracter] for caracter in texto)
            
            # Crear archivo comprimido .bin
            nombre_base = os.path.splitext(archivo_entrada)[0]
            archivo_salida = nombre_base + "_comprimido.bin"
            
            # Guardar solo los bits en archivo .bin
            with open(archivo_salida, 'w', encoding='utf-8') as archivo:
                archivo.write(texto_codificado)
            
            return archivo_salida
            
        except Exception as e:
            raise Exception(f"Error en compresión de texto: {e}")
    
    def _construir_arbol_huffman(self, texto):
        """
        Construye el árbol de Huffman a partir del texto
        """
        frecuencia = Counter(texto)
        monticulo = [NodoHuffman(caracter, freq) for caracter, freq in frecuencia.items()]
        heapq.heapify(monticulo)
        
        while len(monticulo) > 1:
            izquierda = heapq.heappop(monticulo)
            derecha = heapq.heappop(monticulo)
            
            nodo_combinado = NodoHuffman(None, izquierda.frecuencia + derecha.frecuencia)
            nodo_combinado.izquierda = izquierda
            nodo_combinado.derecha = derecha
            
            heapq.heappush(monticulo, nodo_combinado)
        
        return monticulo[0]
    
    def _generar_codigos(self, nodo, codigo_actual):
        """
        Genera los códigos Huffman recursivamente
        """
        if nodo is None:
            return
        
        if nodo.caracter is not None:
            self.codigos[nodo.caracter] = codigo_actual
            return
        
        self._generar_codigos(nodo.izquierda, codigo_actual + "0")
        self._generar_codigos(nodo.derecha, codigo_actual + "1")
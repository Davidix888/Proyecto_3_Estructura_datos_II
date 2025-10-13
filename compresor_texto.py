# compresor_texto.py
import heapq
import os
import json
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
            # Verificar que sea archivo .txt
            if not archivo_entrada.lower().endswith('.txt'):
                raise ValueError("Solo se permiten archivos .txt")
            
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
            
            # Crear archivo comprimido .txt
            nombre_base = os.path.splitext(archivo_entrada)[0]
            archivo_salida = nombre_base + "_comprimido.txt"
            
            # Guardar SOLO los bits comprimidos
            with open(archivo_salida, 'w', encoding='utf-8') as archivo:
                archivo.write(texto_codificado)
            
            # Guardar los códigos en un archivo separado para la descompresión
            archivo_codigos = nombre_base + "_codigos.json"
            with open(archivo_codigos, 'w', encoding='utf-8') as archivo:
                # Convertir caracteres especiales para JSON
                codigos_serializables = {}
                for char, code in self.codigos.items():
                    if char == '\n':
                        codigos_serializables["\\n"] = code
                    elif char == '\t':
                        codigos_serializables["\\t"] = code
                    elif char == '\r':
                        codigos_serializables["\\r"] = code
                    elif char == ' ':
                        codigos_serializables["space"] = code
                    else:
                        codigos_serializables[char] = code
                json.dump(codigos_serializables, archivo)
            
            return archivo_salida
            
        except Exception as e:
            raise Exception(f"Error en compresión de texto: {e}")
    
    def descomprimir(self, archivo_comprimido):
        """
        Descomprime un archivo comprimido con Huffman
        """
        try:
            # Verificar que sea archivo .txt
            if not archivo_comprimido.lower().endswith('.txt'):
                raise ValueError("Solo se permiten archivos .txt")
            
            # Leer los bits del archivo comprimido
            with open(archivo_comprimido, 'r', encoding='utf-8') as archivo:
                texto_codificado = archivo.read().strip()
            
            # Buscar el archivo de códigos
            if "_comprimido.txt" in archivo_comprimido:
                archivo_codigos = archivo_comprimido.replace("_comprimido.txt", "_codigos.json")
            else:
                nombre_base = os.path.splitext(archivo_comprimido)[0]
                archivo_codigos = nombre_base + "_codigos.json"
            
            if not os.path.exists(archivo_codigos):
                raise FileNotFoundError(f"No se encontró el archivo de códigos: {archivo_codigos}")
            
            # Cargar los códigos
            with open(archivo_codigos, 'r', encoding='utf-8') as archivo:
                codigos_serializables = json.load(archivo)
            
            # Convertir códigos de vuelta
            codigos = {}
            for char_repr, code in codigos_serializables.items():
                if char_repr == "\\n":
                    codigos['\n'] = code
                elif char_repr == "\\t":
                    codigos['\t'] = code
                elif char_repr == "\\r":
                    codigos['\r'] = code
                elif char_repr == "space":
                    codigos[' '] = code
                else:
                    codigos[char_repr] = code
            
            # Reconstruir el árbol de Huffman
            arbol = self._reconstruir_arbol(codigos)
            
            # Decodificar el texto
            texto_decodificado = self._decodificar_texto(texto_codificado, arbol)
            
            # Guardar texto descomprimido
            if "_comprimido.txt" in archivo_comprimido:
                archivo_salida = archivo_comprimido.replace("_comprimido.txt", "_descomprimido.txt")
            else:
                nombre_base = os.path.splitext(archivo_comprimido)[0]
                archivo_salida = nombre_base + "_descomprimido.txt"
            
            with open(archivo_salida, 'w', encoding='utf-8') as archivo:
                archivo.write(texto_decodificado)
            
            return archivo_salida
            
        except Exception as e:
            raise Exception(f"Error en descompresión de texto: {e}")
    
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
    
    def _reconstruir_arbol(self, codigos):
        """
        Reconstruye el árbol de Huffman a partir de los códigos
        """
        arbol = NodoHuffman(None, 0)
        
        for caracter, codigo in codigos.items():
            nodo_actual = arbol
            for bit in codigo:
                if bit == '0':
                    if not nodo_actual.izquierda:
                        nodo_actual.izquierda = NodoHuffman(None, 0)
                    nodo_actual = nodo_actual.izquierda
                else:
                    if not nodo_actual.derecha:
                        nodo_actual.derecha = NodoHuffman(None, 0)
                    nodo_actual = nodo_actual.derecha
            nodo_actual.caracter = caracter
        
        return arbol
    
    def _decodificar_texto(self, texto_codificado, arbol):
        """
        Decodifica el texto usando el árbol de Huffman
        """
        texto_decodificado = []
        nodo_actual = arbol
        
        for bit in texto_codificado:
            if bit == '0':
                nodo_actual = nodo_actual.izquierda
            else:
                nodo_actual = nodo_actual.derecha
            
            if nodo_actual.caracter is not None:
                texto_decodificado.append(nodo_actual.caracter)
                nodo_actual = arbol
        
        return "".join(texto_decodificado)
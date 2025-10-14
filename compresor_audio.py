# compresor_audio.py
import wave
import struct
import os

class CompresorAudio:
    def __init__(self):
        pass
    
    def comprimir(self, archivo_audio):
        """
        Comprime audio usando una técnica simple de compresión
        """
        try:
            # Para WAV - compresión real con reducción de calidad
            if archivo_audio.lower().endswith('.wav'):
                return self._comprimir_wav(archivo_audio)
            
            # Para MP3 - no podemos comprimir MP3, entonces hacemos una "simulación"
            elif archivo_audio.lower().endswith('.mp3'):
                return self._simular_compresion_mp3(archivo_audio)
            
            else:
                raise ValueError("Formato de audio no soportado. Use .wav o .mp3")
            
        except Exception as e:
            raise Exception(f"Error en compresión de audio: {e}")
    
    def _comprimir_wav(self, archivo_audio):
        """Comprime archivo WAV real reduciendo la calidad"""
        try:
            with wave.open(archivo_audio, 'rb') as audio:
                params = audio.getparams()
                frames = audio.readframes(params.nframes)
            
            # Convertir frames a lista de muestras
            muestras = self._frames_a_muestras(frames, params.sampwidth)
            
            # Aplicar compresión reduciendo la resolución
            muestras_comprimidas = self._comprimir_muestras(muestras)
            
            # Crear archivo WAV comprimido (REPRODUCIBLE)
            nombre_base = os.path.splitext(archivo_audio)[0]
            archivo_salida = nombre_base + "_comprimido.wav"
            
            # Guardar como WAV reproducible
            self._guardar_wav_comprimido(archivo_salida, muestras_comprimidas, params)
            
            return archivo_salida
            
        except Exception as e:
            raise Exception(f"Error comprimiendo WAV: {e}")
    
    def _simular_compresion_mp3(self, archivo_audio):
        """Simula compresión MP3 (no podemos comprimir MP3 realmente)"""
        try:
            nombre_base = os.path.splitext(archivo_audio)[0]
            archivo_salida = nombre_base + "_info_compresion.txt"
            
            # Crear archivo de información sobre la compresión
            tamano_original = obtener_tamano_archivo(archivo_audio)
            
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write("INFORMACIÓN DE COMPRESIÓN DE AUDIO MP3\n")
                f.write("=" * 50 + "\n")
                f.write(f"Archivo original: {os.path.basename(archivo_audio)}\n")
                f.write(f"Tamaño original: {formatear_tamano(tamano_original)}\n")
                f.write(f"Formato: MP3\n")
                f.write("\nNOTA: Los archivos MP3 ya están comprimidos.\n")
                f.write("Esta es una simulación de compresión.\n")
                f.write("El archivo MP3 original se mantiene intacto.\n")
            
            return archivo_salida
            
        except Exception as e:
            raise Exception(f"Error en simulación MP3: {e}")
    
    def _frames_a_muestras(self, frames, sampwidth):
        """Convierte frames de audio a lista de muestras"""
        if sampwidth == 1:
            formato = 'B'
            offset = 128
        elif sampwidth == 2:
            formato = 'h'
            offset = 0
        else:
            formato = 'i'
            offset = 0
        
        muestras = []
        for i in range(0, len(frames), sampwidth):
            muestra = struct.unpack(formato, frames[i:i+sampwidth])[0]
            if sampwidth == 1:
                muestra -= offset
            muestras.append(muestra)
        
        return muestras
    
    def _muestras_a_frames(self, muestras, sampwidth):
        """Convierte lista de muestras a frames de audio"""
        frames = b''
        if sampwidth == 1:
            formato = 'B'
            offset = 128
        elif sampwidth == 2:
            formato = 'h'
            offset = 0
        else:
            formato = 'i'
            offset = 0
        
        for muestra in muestras:
            if sampwidth == 1:
                muestra += offset
            frames += struct.pack(formato, muestra)
        
        return frames
    
    def _comprimir_muestras(self, muestras, factor=2):
        """Comprime muestras reduciendo la resolución (pérdida de calidad)"""
        return [muestra // factor * factor for muestra in muestras]
    
    def _guardar_wav_comprimido(self, archivo_salida, muestras_comprimidas, params_original):
        """
        Guarda las muestras comprimidas como un archivo WAV reproducible
        """
        # Convertir muestras a frames
        frames_comprimidos = self._muestras_a_frames(muestras_comprimidas, params_original.sampwidth)
        
        # Crear nuevo archivo WAV
        with wave.open(archivo_salida, 'wb') as audio:
            # Usar los mismos parámetros pero ajustar nframes
            audio.setnchannels(params_original.nchannels)
            audio.setsampwidth(params_original.sampwidth)
            audio.setframerate(params_original.framerate)
            audio.setnframes(len(muestras_comprimidas) // params_original.nchannels)
            audio.writeframes(frames_comprimidos)

# Necesitamos importar estas funciones desde utilidades
def obtener_tamano_archivo(ruta_archivo):
    """Obtiene el tamaño de un archivo en bytes"""
    try:
        return os.path.getsize(ruta_archivo)
    except OSError:
        return 0

def formatear_tamano(tamano_bytes):
    """Formatea el tamaño en bytes a una representación legible"""
    if tamano_bytes == 0:
        return "0 B"
    
    unidades = ['B', 'KB', 'MB', 'GB']
    tamano = float(tamano_bytes)
    
    for unidad in unidades:
        if tamano < 1024.0 or unidad == unidades[-1]:
            return f"{tamano:.2f} {unidad}"
        tamano /= 1024.0
    
    return f"{tamano_bytes} B"
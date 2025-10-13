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
            # Solo funciona con archivos WAV por simplicidad
            if not archivo_audio.lower().endswith('.wav'):
                raise ValueError("Solo se soportan archivos WAV para compresión")
            
            with wave.open(archivo_audio, 'rb') as audio:
                params = audio.getparams()
                frames = audio.readframes(params.nframes)
            
            # Convertir frames a lista de muestras
            muestras = self._frames_a_muestras(frames, params.sampwidth)
            
            # Aplicar compresión simple (reducción de resolución)
            muestras_comprimidas = self._comprimir_muestras(muestras)
            
            # Guardar audio comprimido
            nombre_base = os.path.splitext(archivo_audio)[0]
            archivo_salida = nombre_base + "_comprimido.awc"
            
            # Guardar en formato binario limpio
            self._guardar_comprimido(archivo_salida, muestras_comprimidas, params)
            
            return archivo_salida
            
        except Exception as e:
            raise Exception(f"Error en compresión de audio: {e}")
    
    def descomprimir(self, archivo_comprimido):
        """
        Descomprime audio comprimido
        """
        try:
            # Cargar datos comprimidos
            muestras_comprimidas, params = self._cargar_comprimido(archivo_comprimido)
            
            # Convertir muestras a frames
            frames = self._muestras_a_frames(muestras_comprimidas, params.sampwidth)
            
            # Guardar audio descomprimido
            nombre_base = os.path.splitext(archivo_comprimido)[0]
            archivo_salida = nombre_base + "_reconstruido.wav"
            
            with wave.open(archivo_salida, 'wb') as audio:
                audio.setparams(params)
                audio.writeframes(frames)
            
            return archivo_salida
            
        except Exception as e:
            raise Exception(f"Error en descompresión de audio: {e}")
    
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
    
    def _comprimir_muestras(self, muestras, factor=4):
        """Comprime muestras reduciendo la resolución"""
        return [muestra // factor * factor for muestra in muestras]
    
    def _guardar_comprimido(self, archivo_salida, muestras_comprimidas, params):
        """
        Guarda muestras comprimidas en formato binario limpio
        """
        with open(archivo_salida, 'wb') as archivo:
            # Guardar parámetros del audio
            archivo.write(params.nchannels.to_bytes(2, byteorder='big'))
            archivo.write(params.sampwidth.to_bytes(2, byteorder='big'))
            archivo.write(params.framerate.to_bytes(4, byteorder='big'))
            archivo.write(params.nframes.to_bytes(4, byteorder='big'))
            archivo.write(params.comptype.encode('utf-8'))
            archivo.write(params.compname.encode('utf-8'))
            
            # Guardar cantidad de muestras
            archivo.write(len(muestras_comprimidas).to_bytes(4, byteorder='big'))
            
            # Guardar muestras
            for muestra in muestras_comprimidas:
                archivo.write(muestra.to_bytes(4, byteorder='big', signed=True))
    
    def _cargar_comprimido(self, archivo_comprimido):
        """
        Carga muestras comprimidas desde archivo binario
        """
        with open(archivo_comprimido, 'rb') as archivo:
            # Leer parámetros
            nchannels = int.from_bytes(archivo.read(2), byteorder='big')
            sampwidth = int.from_bytes(archivo.read(2), byteorder='big')
            framerate = int.from_bytes(archivo.read(4), byteorder='big')
            nframes = int.from_bytes(archivo.read(4), byteorder='big')
            comptype = archivo.read(4).decode('utf-8')
            compname = archivo.read(4).decode('utf-8')
            
            params = wave._wave_params(nchannels, sampwidth, framerate, nframes, comptype, compname)
            
            # Leer cantidad de muestras
            num_muestras = int.from_bytes(archivo.read(4), byteorder='big')
            
            # Leer muestras
            muestras_comprimidas = []
            for _ in range(num_muestras):
                muestra = int.from_bytes(archivo.read(4), byteorder='big', signed=True)
                muestras_comprimidas.append(muestra)
            
            return muestras_comprimidas, params
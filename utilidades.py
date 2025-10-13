# utilidades.py
import os

def obtener_tamano_archivo(ruta_archivo):
    """
    Obtiene el tamaño de un archivo en bytes
    """
    try:
        return os.path.getsize(ruta_archivo)
    except OSError:
        return 0

def formatear_tamano(tamano_bytes):
    """
    Formatea el tamaño en bytes a una representación legible
    """
    if tamano_bytes == 0:
        return "0 B"
    
    unidades = ['B', 'KB', 'MB', 'GB']
    tamano = float(tamano_bytes)
    
    for unidad in unidades:
        if tamano < 1024.0 or unidad == unidades[-1]:
            return f"{tamano:.2f} {unidad}"
        tamano /= 1024.0
    
    return f"{tamano_bytes} B"

def verificar_extension(archivo, extensiones_permitidas):
    """
    Verifica si un archivo tiene una extensión permitida
    """
    extension = os.path.splitext(archivo)[1].lower()
    return extension in extensiones_permitidas

def crear_directorio_si_no_existe(ruta):
    """
    Crea un directorio si no existe
    """
    if not os.path.exists(ruta):
        os.makedirs(ruta)
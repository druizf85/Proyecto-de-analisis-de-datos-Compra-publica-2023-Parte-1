import os
import pandas as pd
import re

# -------------------------------------------- FUNCIONES ------------------------------------------------------ #

def delete_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)
        print("Archivo eliminado con éxito.")
    else:
        print("El archivo no existe.")

# -------------------------------------------------------------------------------------------- #    
        
def limpiar_texto(texto):
    texto_limpio = re.sub(r'[^a-zA-Z0-9\s]', '', texto)
    return texto_limpio

# -------------------------------------------------------------------------------------------- # 
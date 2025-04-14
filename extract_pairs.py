import csv
import re
import os
import sys

def process_chunk(chunk, encoding):
    """
    Procesa un fragmento (chunk) del archivo para encontrar pares de Item Name y Alias.
    
    Args:
        chunk: Fragmento de datos binarios del archivo
        encoding: Codificación del archivo (utf-16, utf-8, etc.)
    
    Returns:
        Lista de pares encontrados en el fragmento
    """
    try:
        # Convertimos los datos binarios a texto usando la codificación especificada
        content = chunk.decode(encoding)
        
        # Definimos diferentes patrones de búsqueda para encontrar los pares
        # Cada patrón busca diferentes formatos de comillas y espacios
        patterns = [
            r'Item Name=""([^"]+)""\s+Alias=""([^"]+)""',  # Comillas dobles
            r'Item Name="([^"]+)"\s+Alias="([^"]+)"',      # Comillas simples
            r'Item Name=([^"\s]+)\s+Alias=([^"\s]+)',      # Sin comillas
            r'Item Name=([^"\s]+)\s+Alias=""([^"]+)""',    # Mezcla de formatos
            r'Item Name=""([^"]+)""\s+Alias=([^"\s]+)'     # Mezcla de formatos
        ]
        
        # Lista para almacenar todos los pares encontrados
        all_pairs = []
        
        # Probamos cada patrón de búsqueda
        for pattern in patterns:
            try:
                # Buscamos todas las coincidencias del patrón en el contenido
                pairs = re.finditer(pattern, content)
                # Convertimos el resultado a lista y lo añadimos a all_pairs
                all_pairs.extend(list(pairs))
            except Exception as e:
                # Si hay un error con un patrón, lo mostramos y continuamos con el siguiente
                print(f"Error al procesar el patrón {pattern}: {str(e)}")
                continue
            
        return all_pairs
    except UnicodeDecodeError:
        # Si hay error al decodificar, devolvemos lista vacía
        return []
    except Exception as e:
        # Si hay cualquier otro error, lo mostramos y devolvemos lista vacía
        print(f"Error al decodificar el chunk: {str(e)}")
        return []

def extract_pairs(input_file, output_file, chunk_size=1000000):
    """
    Extrae los pares de Item Name y Alias de un archivo y los guarda en un CSV.
    
    Args:
        input_file: Ruta del archivo de entrada
        output_file: Ruta del archivo de salida CSV
        chunk_size: Tamaño de los fragmentos en que se divide el archivo (por defecto 1MB)
    """
    print(f"\nIniciando procesamiento del archivo: {input_file}")
    print(f"Tamaño del archivo: {os.path.getsize(input_file)} bytes")
    
    try:
        # Abrimos el archivo en modo binario
        with open(input_file, 'rb') as f:
            # Leemos los primeros 2 bytes para determinar la codificación
            bom = f.read(2)
            if bom == b'\xff\xfe':
                encoding = 'utf-16-le'  # UTF-16 Little Endian
            elif bom == b'\xfe\xff':
                encoding = 'utf-16-be'  # UTF-16 Big Endian
            else:
                encoding = 'utf-16'     # UTF-16 por defecto
            
            print(f"Usando codificación: {encoding}")
            
            # Leemos todo el contenido después del BOM
            content = f.read()
            try:
                # Decodificamos el contenido
                decoded_content = content.decode(encoding)
                print("\nBuscando pares en el contenido...")
                
                # Buscamos todos los pares en el contenido completo
                pairs = process_chunk(content, encoding)
                if pairs:
                    print(f"\nTotal de pares encontrados: {len(pairs)}")
                    
                    # Creamos el archivo CSV de salida
                    with open(output_file, 'w', encoding='utf-8', newline='') as out_file:
                        # Escribimos la cabecera
                        out_file.write('Alias,"Item Name"\n')
                        
                        # Procesamos cada par encontrado
                        for i, pair in enumerate(pairs, 1):
                            # Extraemos el Item Name y el Alias del par
                            item_name = pair.group(1)
                            alias = pair.group(2)
                            # Escribimos la fila directamente
                            out_file.write(f'{alias},"{item_name}"\n')
                        
                        print(f'\nSe exportaron exitosamente {len(pairs)} pares al archivo {output_file}')
                        return True
                else:
                    print("\nNo se encontraron pares en el archivo")
                    return False
                    
            except UnicodeDecodeError as e:
                print(f"Error al decodificar el contenido: {str(e)}")
                return False
                
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")
        return False

def show_file_sample(input_file, sample_size=1000):
    print(f"\nMostrando una muestra del archivo {input_file}:")
    try:
        with open(input_file, 'rb') as f:
            # Leer una muestra del archivo
            sample = f.read(sample_size)
            # Intentar diferentes codificaciones
            for encoding in ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']:
                try:
                    decoded_sample = sample.decode(encoding)
                    print(f"\nMuestra decodificada con {encoding}:")
                    print(decoded_sample)
                    return True
                except UnicodeDecodeError:
                    continue
            print("No se pudo decodificar la muestra con ninguna codificación")
            return False
    except Exception as e:
        print(f"Error al leer el archivo: {str(e)}")
        return False

# Este bloque se ejecuta solo si el script se ejecuta directamente
if __name__ == '__main__':
    try:
        # Definimos los archivos de entrada y salida
        input_file = 'pru.txt'
        output_file = 'item_alias_pairs.csv'
        
        # Verificamos que el archivo de entrada existe
        if not os.path.exists(input_file):
            print(f"Error: El archivo {input_file} no existe")
            sys.exit(1)
            
        # Ejecutamos la función principal
        extract_pairs(input_file, output_file)
    except Exception as e:
        # Si hay algún error general, lo mostramos y terminamos el programa
        print(f"Error general: {str(e)}")
        sys.exit(1) 
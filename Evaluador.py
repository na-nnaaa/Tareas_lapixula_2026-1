import re

    # ELEMENTOS DEL EBNF
# Estructuras basicas
digito = r"[0-9]"
letra_min = r"[a-z]"
letra_may = r"[A-Z]"
letra = rf"({letra_min}|{letra_may})"
palabra = rf"({letra}({letra}|{digito})*)"

# Tipos de dato y operaciones
operacion = r"(\+|-|/|\*|==|=|<|>)"
booleano = r"(true|false)"
cadena_texto = rf"\"{palabra}\""
caracter = rf"\'{letra}\'"
valor = rf"({digito}+|{booleano}|{cadena_texto}|{caracter})"
tipo_dato = r"(int|bool|char|string|void)"

# Estilos de Nomenclatura
snake_case = rf"(_{letra_min}+(_{letra_min}*)*)|({letra_min}+_({letra_min}*_)+)|({letra_min}+(_{letra_min}*)+)" 
camelCase = rf"{letra_min}+({letra_may}+{letra_min}*)+"
PascalCase = rf"{letra_may}+{letra_min}*({letra_may}+{letra_min}*)*"
nombre_cualquiera = rf"{letra}({letra}|{digito}|_)*"
nombre_valido = rf"({snake_case}|{camelCase}|{PascalCase})"

# Estructuras avanzadas
condicion = rf"\(\s*{nombre_cualquiera}\s*{operacion}\s*{valor}\s*\)"
estructura_control = rf"(if|while)\s*{condicion}\s*\{{"
cierre_bloque = r"\}"
parametro = rf"({tipo_dato}\s+{nombre_cualquiera})"
lista_parametros = rf"({parametro}(\s*,\s*{parametro})*)?"
declaracion_funcion = rf"({tipo_dato})\s+({nombre_cualquiera})\s*\(\s*{lista_parametros}\s*\)\s*\{{?"
declaracion_variable = rf"({tipo_dato})\s+({nombre_cualquiera})\s*{operacion}\s*{valor}\s*;"
retorno = rf"return\s+{nombre_cualquiera}\s*;"
comentario_one_line = rf"\s*//.*"
comentario_multi_line = r"/\*[\s\S]*?\*/"

# Errores de sintaxis
# 1. Falta punto y coma al final
error_punto_coma = rf"({tipo_dato}\s+{nombre_cualquiera}\s*{operacion}\s*{valor}\s*$)|(return\s+{nombre_cualquiera}\s*$)"
# 2. Falta el tipo
error_tipo = rf"(\s*{nombre_cualquiera}\s*{operacion}\s*{valor}\s*;)"
# 3. Falta el nombre
error_nombre = rf"({tipo_dato}\s*{operacion}\s*{valor}\s*;)"
# 4. Asignacion vacia
error_valor = rf"({tipo_dato}\s+{nombre_cualquiera}\s*{operacion}\s*;)"
# Combinacion de las 3 ultimas, no meto punto y coma aqui porque se pide distinguir este error en la pauta de la tarea
declaracion_variable_erronea = rf"({error_tipo}|{error_nombre}|{error_valor})"


def procesar_bloque(bloque, autor, stats, nombre_funcion):
    """
    ***
    Parametros: bloque->string, autor->string, stats->diccionario, nombre_funcion->string
    ***
    Retorno: None
    ***
    Analiza el numero de llaves de una funcion.
    Escribe el bloque en el archivo del practicante correspondiente
    Detecta errores de estilo y sintaxis linea por linea.
    """
    stats[autor]["funciones"] += 1

    llaves_abiertas = len(re.findall(r"\{", bloque))
    llaves_cerradas = len(re.findall(r"\}", bloque))
    diferencia = llaves_abiertas - llaves_cerradas
    
    if diferencia > 0:
        stats[autor]["errores"].append(f"Error en '{nombre_funcion}': Bloque sin cerrar. Faltan {diferencia} llaves '}}' de cierre.")
    elif diferencia < 0:
        faltan_apertura = abs(diferencia)
        stats[autor]["errores"].append(f"Error en '{nombre_funcion}': Faltan {faltan_apertura} llaves '{{' de apertura.")

    with open(f"{autor}.txt", "a") as resultante:
        resultante.write(bloque + "\n")

        for linea in bloque.splitlines():

            match_variable = re.search(declaracion_variable, linea)

            if match_variable:
                stats[autor]["variables"] += 1
                nombre_variable = match_variable.group(3)

                if autor == "Snake" and not re.fullmatch(snake_case, nombre_variable):
                    stats[autor]["diferencias"] += 1
                elif autor == "Camel" and not re.fullmatch(camelCase, nombre_variable):
                    stats[autor]["diferencias"] += 1
                elif autor == "Pascal" and not re.fullmatch(PascalCase, nombre_variable):
                    stats[autor]["diferencias"] += 1
            
            elif re.search(error_punto_coma, linea):
                stats[autor]["errores"].append(f"Error en '{nombre_funcion}': Falta ';' en la linea {linea}")
            elif re.search(declaracion_variable_erronea, linea):
                stats[autor]["errores"].append(f"Error en '{nombre_funcion}': Variable mal construida en {linea}")
    return


def identificar_autor(nombre):
    """
    ***
    Parametros: nombre->string
    ***
    Retorno: string
    ***
    Clasifica una funcion como Snake, Camel, Pascal o Desconocido basandose en las expresiones 
    regulares de las nomenclauturas definidas
    """
    if re.fullmatch(snake_case, nombre):
        return "Snake"
    elif re.fullmatch(camelCase, nombre):
        return "Camel"
    elif re.fullmatch(PascalCase, nombre):
        return "Pascal"
    else:
        return "Desconocido"

def imprimir_reporte(stats):
    """
    ***
    Parametros: stats->diccionario
    ***
    Retorno: None
    ***
    Imprime el reporte final
    """
    print("=== REPORTE DE EVALUACIÓN DE PRACTICANTES ===")
    autores = ["Snake", "Camel", "Pascal", "Desconocido"]
    
    for autor in autores:
        datos = stats[autor]
        
        # Solo imprime si el practicante tiene algo en el archivo
        if datos["funciones"] > 0:
            print(f"\nPRACTICANTE: {autor}")
            print(f"Funciones creadas: {datos['funciones']}")
            print(f"Variables declaradas: {datos['variables']}")
            print(f"Diferencias de Estilo: {datos['diferencias']}")
            print(f"Errores de Sintaxis: {len(datos['errores'])}")
            
            # Imprime mensajes de error si es que hay
            for error in datos['errores']:
                print(error)

def procesar_archivo():
    """
    ***
    Parametros: None
    ***
    Retorno: None
    ***
    Es el main()
    Lee el archivo fuente, segmenta las funciones encontradas en bloques individuales, gatilla el analisis e impresion del mensaje final
    """
    try:
        with open("programa.txt", "r") as codigo_fuente:
            contenido = codigo_fuente.read()
    except FileNotFoundError:
        print("Error al leer el archivo, no se encontró en el directorio del programa")
        return

    stats = {"Snake": {"funciones": 0, "variables": 0, "diferencias": 0, "errores": []}, "Camel": {"funciones": 0, "variables": 0, "diferencias": 0, "errores": []}, "Pascal": {"funciones": 0, "variables": 0, "diferencias": 0, "errores": []}, "Desconocido": {"funciones": 0, "variables": 0, "diferencias": 0, "errores": []}}
    matches = list(re.finditer(declaracion_funcion, contenido))
    
    for nombre in ["Snake", "Camel", "Pascal", "Desconocido"]:
        open(f"{nombre}.txt", "w").close() # Para reiniciar el contenido de archivos existentes previo a esta ejecucion

    for i in range(len(matches)):
        inicio_funcion = matches[i].start()
        nombre_funcion = matches[i].group(3)

        autor = identificar_autor(nombre_funcion)
        if i+1 < len(matches):
            limite_funcion = matches[i+1].start() # Guardo el indice del inicio de la sig funcion, en otras palabras, (el fin de la actual)+1
        else:
            limite_funcion = len(contenido) # Esto para el caso de la ultima funcion del documento

        bloque = contenido[inicio_funcion:limite_funcion] # Concatena hasta la linea anterior al inicio de la funcion

        procesar_bloque(bloque, autor, stats, nombre_funcion)

    imprimir_reporte(stats)

    return

if __name__ == "__main__":
    procesar_archivo()
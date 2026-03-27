Nombre: Iker Renato Ortiz Labraña
Rol: 202473562-4

Caracteristicas del sistema utilizado:
- OS: CachyOS
- Editor de codigo: Visual Studio Code
- Python 3.14.3
- No se requieren librerías externas (solo se utiliza el módulo 're' nativo).

Pasos para ejecutar:
1. Abrir la terminal y navegar hasta el directorio raíz del proyecto donde se encuentra el script.
2. Asegurarse de que el archivo con el código fuente a analizar se llame exactamente "programa.txt" y se encuentre en el mismo directorio que "Evaluador.py".
3. Ejecutar el script mediante el comando:
        python Evaluador.py 
4. El programa imprimirá el reporte de evaluación por la salida estándar (consola) y generará/sobreescribirá automáticamente los archivos snake.txt, camel.txt, pascal.txt y desconocido.txt en el mismo directorio.

SUPUESTOS Y CONSIDERACIONES DE DISEÑO
Para el desarrollo de este analizador léxico y con el fin de respetar la gramática EBNF proporcionada en el enunciado, de la manera que se puede apreciar en respuestas al foro de consultas de la tarea, se han asumido las siguientes consideraciones:

1. DEFINICIÓN DE ERRORES CRÍTICOS (SINTAXIS)
El evaluador detecta y reporta los siguientes casos como errores de sintaxis críticos que interrumpen la correcta estructura de una declaración:
- Falta de punto y coma (';') al final de una asignación o de una instrucción 'return'.
- Omisión del tipo de dato en una declaración (Ej: 'variable = 10;').
- Omisión del identificador/nombre de la variable (Ej: 'int = 10;').
- Asignación vacía o falta de valor post-operador (Ej: 'int x = ;').
- Desbalanceo de llaves '{' y '}'. Se reporta la cantidad exacta de llaves faltantes de apertura o cierre por bloque de función.

2. ELEMENTOS FUERA DEL ALCANCE (NO SOPORTADOS POR EL EBNF)
Dado que el linter se ciñe a la gramática EBNF base, los siguientes elementos de C++ legítimos se consideran "fuera de alcance" o "mal construidos", y el programa los tratará como errores o los ignorará, según corresponda:
- Operaciones complejas en asignaciones: El EBNF define <valor> estrictamente como un dígito, booleano, cadena o carácter. Por ende, expresiones aritméticas (Ej: 'int a = b + c;') o asignaciones de variables a otras variables exceden la gramática de <valor> y serán ignoradas por el linter.
- Tipos de datos no especificados: El EBNF limita <tipo_dato> a (int|bool|char|string|void). Tipos como 'float', 'double' o punteros serán ignorados o clasificados como errores sintácticos.
- Operadores de incremento/decremento: Estructuras como 'i++' o 'i--' no están definidas en la gramática.
- Las variables si pueden llevar digitos, sin embargo, se consideraran de estilo "Desconocido". El resto solamente llevan letras de la "a" a la "z", considerando las reglas de cada nomenclatura.
- Formato de una sola línea: El analizador procesa el código interior de las funciones asumiendo saltos de línea para el reporte de errores (splitlines). No se soporta código "minificado" donde múltiples instrucciones compartan la misma línea física.

3. EVALUACIÓN DE ESTILOS DE NOMENCLATURA
Se considera "Diferencia de Estilo" cualquier identificador que no posea los rasgos gramaticales explícitos del estilo asignado. 
- En snake_Case, se exige la presencia de al menos un guion bajo ('_') y solamente minusculas.
- En camelCase, se exige empezar con minuscula (no solo una) y tener al menos una mayúscula intermedia (no inicial).
- En PascalCase, se exige empezar con mayuscula (no solo una).
- Cualquier variable que no se adhiera a esos criterios, se considera un estilo "Desconocido"
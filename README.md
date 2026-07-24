# aed-tp2-tratamientos
Procesamiento de registros médicos en Python - TP2 AED, UTN-FRC
# TP2 - Procesamiento de Tratamientos Médicos

Programa en Python que procesa un archivo de registros médicos de ancho fijo (`tratamientos.txt`) y calcula distintas estadísticas: cantidad de tratamientos por categoría ICD10, promedios, montos totales y el paciente con mayor gasto.

## Contexto
Trabajo Práctico N°2 de la materia Algoritmos y Estructuras de Datos (AED) - UTN-FRC.

## Restricción del enunciado
No se permite el uso de métodos built-in de strings (como `round()`), por lo que se implementó una función propia `redondear()`.

## Qué calcula
- Cantidad total de tratamientos cargados
- Cantidad de tratamientos por letra de código ICD10 (A, B, C, E, P)
- Promedio de importe final para el capítulo 19
- Paciente con mayor importe pagado
- Porcentaje de tratamientos de alta complejidad por encima del promedio

## Cómo correrlo
1. Colocar el archivo `tratamientos.txt` en la misma carpeta que el script.
2. Ejecutar `python tp2_tratamientos.py`.

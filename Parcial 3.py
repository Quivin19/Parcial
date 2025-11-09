import pandas as pd
import numpy as np


# 1. Lectura de datos
print("="*80)
print("1. Lectura de datos")
print("="*80)

# Cargar el archivo CSV
df = pd.read_csv('notas_alumnos_utf8_sig.csv')

# Mostrar las primeras 10 filas
print("\n Primeras 10 filas del DataFrame:")
print(df.head(10))

# Información general del dataset
print("\n\n Información del DataFrame:")
print(df.info())

print("\n\nDimensiones del DataFrame:")
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

# 2. Análisis de notas
print("\n" + "="*80)
print("2. Análisis de notas")
print("="*80)

# Nota promedio general
promedio_general = df['nota'].mean()
print(f"\n Nota promedio general de todos los alumnos: {promedio_general:.2f}")

# Nota promedio por materia
print("\n Nota promedio por materia:")
promedio_por_materia = df.groupby('materia')['nota'].mean().sort_values(ascending=False)
for materia, promedio in promedio_por_materia.items():
    print(f"   {materia:15s}: {promedio:.2f}")

# Nota promedio por trimestre
print("\n Nota promedio por trimestre:")
promedio_por_trimestre = df.groupby('trimestre')['nota'].mean()
for trimestre, promedio in promedio_por_trimestre.items():
    print(f"   Trimestre {trimestre}: {promedio:.2f}")

# Alumno con promedio más alto
promedio_por_alumno = df.groupby(['id_alumno', 'nombre'])['nota'].mean()
alumno_top = promedio_por_alumno.idxmax()
nota_top = promedio_por_alumno.max()
print(f"\n Alumno con el promedio más alto:")
print(f"   {alumno_top[1]} (ID: {alumno_top[0]}): {nota_top:.2f}")

# Materia con mayor cantidad de calificaciones bajas
df['es_baja'] = df['nota'] < 60
calificaciones_bajas = df.groupby('materia')['es_baja'].sum().sort_values(ascending=False)
materia_mas_bajas = calificaciones_bajas.idxmax()
cantidad_bajas = calificaciones_bajas.max()
print(f"\n Materia con mayor cantidad de calificaciones bajas (< 60):")
print(f"   {materia_mas_bajas}: {cantidad_bajas} calificaciones bajas")

print("\n   Detalle de calificaciones bajas por materia:")
for materia, cantidad in calificaciones_bajas.items():
    print(f"   {materia:15s}: {cantidad} calificaciones")


# 3. Análisis por alumno
print("\n" + "="*80)
print("3. Análisis por alumno")
print("="*80)

# Alumnos con promedio >= 90
alumnos_excelentes = promedio_por_alumno[promedio_por_alumno >= 90]
print(f"\n Alumnos con promedio general mayor o igual a 90:")
if len(alumnos_excelentes) > 0:
    for (id_alumno, nombre), promedio in alumnos_excelentes.items():
        print(f"   {nombre} (ID: {id_alumno}): {promedio:.2f}")
else:
    print("No hay alumnos con promedio >= 90")

# Materia más difícil por alumno (menor promedio)
print(f"\n Materia más difícil (menor promedio) para cada alumno:")
materia_dificil = df.groupby(['id_alumno', 'nombre', 'materia'])['nota'].mean().reset_index()
materia_dificil_por_alumno = materia_dificil.loc[materia_dificil.groupby(['id_alumno', 'nombre'])['nota'].idxmin()]

for _, row in materia_dificil_por_alumno.iterrows():
    print(f"   {row['nombre']:20s}: {row['materia']:15s} (promedio: {row['nota']:.2f})")

# 4. Bonus - Tabla promedio por alumno y materia
# 
print("\n" + "="*80)
print("4. Bonus - Tabla promedio por alumno y materia")
print("="*80)

# Crear tabla pivote con promedio por alumno y materia
tabla_promedio = df.groupby(['nombre', 'materia'])['nota'].mean().unstack(fill_value=0)

# Añadir columna con promedio general de cada alumno
tabla_promedio['Promedio_General'] = tabla_promedio.mean(axis=1)

# Ordenar por promedio general descendente
tabla_promedio = tabla_promedio.sort_values('Promedio_General', ascending=False)

print("\n Tabla de promedios por alumno y materia:")
tabla_promedio = tabla_promedio.round(2)

# Guardar la tabla en un archivo CSV
tabla_promedio.to_csv('tabla_promedios_por_alumno_materia.csv')
print("\n Tabla guardada en: tabla_promedios_por_alumno_materia.csv")


# Estadísticas adicionales
print("\n" + "="*80)
print("Estadísticas adicionales")
print("="*80)

print("\n Estadísticas descriptivas de las notas:")
print(df['nota'].describe())

print("\n Distribución de notas por rango:")
rangos = pd.cut(df['nota'], bins=[0, 60, 70, 80, 90, 100], 
                labels=['0-59 (Reprobado)', '60-69 (Regular)', '70-79 (Bueno)', 
                        '80-89 (Muy Bueno)', '90-100 (Excelente)'])
print(rangos.value_counts().sort_index())

print("\n" + "="*80)
print("Análisis completado")
print("="*80)
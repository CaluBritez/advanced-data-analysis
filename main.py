import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

# Conexión a la base de datos
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='CompanyData'
)

cursor = conn.cursor()

# Consulta para obtener datos de la tabla EmployeePerformance
query = "SELECT * FROM EmployeePerformance"
cursor.execute(query)

# Obtener los nombres de las columnas
column_names = [i[0] for i in cursor.description]

# Obtener todos los datos de la consulta
data = cursor.fetchall()

# Crear el DataFrame
df = pd.DataFrame(data, columns=column_names)

# Cerrar el cursor y la conexión
cursor.close()
conn.close()

#print(df)

# Convertir las columnas performance_score y salary a float
df['performance_score'] = df['performance_score'].astype(float)
df['salary'] = df['salary'].astype(float)

# Estadísticas por departamento
print("Según Puntaje")
stats_score = df.groupby('department')['performance_score'].agg(['mean', 'median', 'std'])
print(stats_score)

print("Según Salario")
stats_salary = df.groupby('department')['salary'].agg(['mean', 'median', 'std'])
print(stats_salary)

print("Total de empleados por departamento")
print(df.groupby('department').size())

# Correlación entre years_with_company y performance_score
correlacion = df[['years_with_company', 'performance_score']].corr()
print("\nCorrelación entre years_with_company y performance_score:")
print(correlacion)

# Correlación entre salary y performance_score
correlacion_s = df[['salary', 'performance_score']].corr()
print("\nCorrelación entre salary y performance_score:")
print(correlacion_s)


# Histograma del departamento Games según su performance_score
df_games = df[df['department'] == 'Games']
plt.figure(figsize=(10, 6))  # Ajustar el tamaño de la figura
plt.hist(df_games['performance_score'], bins=10, edgecolor='black', alpha=0.7)
plt.title('Histograma del Performance Score del Departamento Games')
plt.xlabel('Performance Score')
plt.ylabel('Frecuencia')
plt.grid(axis='y', alpha=0.75)  # Añadir una cuadrícula para facilitar la lectura
plt.xticks(np.arange(min(df_games['performance_score']), max(df_games['performance_score']) + 1, 1))  # Ajustar las etiquetas del eje x
plt.show()

# Dispersión de years_with_company vs. performance_score
plt.figure(figsize=(10, 6))
plt.scatter(df['years_with_company'], df['performance_score'], alpha=0.5)
plt.title('Gráfico de Dispersión: Years with Company vs. Performance Score')
plt.xlabel('Years with Company')
plt.ylabel('Performance Score')
plt.grid(True)
plt.show()

# Dispersión de salary vs. performance_score
plt.figure(figsize=(10, 6))
plt.scatter(df['salary'], df['performance_score'], alpha=0.5, color='red')
plt.title('Gráfico de Dispersión: Salary vs. Performance Score')
plt.xlabel('Salary')
plt.ylabel('Performance Score')
plt.grid(True)
plt.show()
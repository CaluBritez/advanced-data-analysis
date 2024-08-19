import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def fetch_data(self, query):
        self.cursor.execute(query)
        columns = [i[0] for i in self.cursor.description]
        data = self.cursor.fetchall()
        return pd.DataFrame(data, columns=columns)
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

class EmployeePerformanceAnalysis:
    def __init__(self, dataframe):
        self.df = dataframe
        self.df['performance_score'] = self.df['performance_score'].astype(float)
        self.df['salary'] = self.df['salary'].astype(float)
    
    def calculate_statistics(self):
        print("Según Puntaje")
        stats_score = self.df.groupby('department')['performance_score'].agg(['mean', 'median', 'std'])
        print(stats_score)

        print("Según Salario")
        stats_salary = self.df.groupby('department')['salary'].agg(['mean', 'median', 'std'])
        print(stats_salary)

        print("Total de empleados por departamento")
        print(self.df.groupby('department').size())
    
    def calculate_correlations(self):
        correlacion = self.df[['years_with_company', 'performance_score']].corr()
        print("\nCorrelación entre years_with_company y performance_score:")
        print(correlacion)

        correlacion_s = self.df[['salary', 'performance_score']].corr()
        print("\nCorrelación entre salary y performance_score:")
        print(correlacion_s)
    
    def plot_histogram(self, department):
        df_department = self.df[self.df['department'] == department]
        plt.figure(figsize=(10, 6))
        plt.hist(df_department['performance_score'], bins=10, edgecolor='black', alpha=0.7)
        plt.title(f'Histograma del Performance Score del Departamento {department}')
        plt.xlabel('Performance Score')
        plt.ylabel('Frecuencia')
        plt.grid(axis='y', alpha=0.75)
        plt.xticks(np.arange(min(df_department['performance_score']), max(df_department['performance_score']) + 1, 1))
        plt.show()

    def plot_scatter(self, x_column, y_column, color='blue'):
        plt.figure(figsize=(10, 6))
        plt.scatter(self.df[x_column], self.df[y_column], alpha=0.5, color=color)
        plt.title(f'Gráfico de Dispersión: {x_column} vs. {y_column}')
        plt.xlabel(x_column)
        plt.ylabel(y_column)
        plt.grid(True)
        plt.show()

# Uso de las clases
if __name__ == "__main__":
    db_manager = DatabaseManager(host='localhost', user='root', password='', database='CompanyData')
    db_manager.connect()
    df = db_manager.fetch_data("SELECT * FROM EmployeePerformance")
    db_manager.close()

    analysis = EmployeePerformanceAnalysis(df)
    analysis.calculate_statistics()
    analysis.calculate_correlations()
    analysis.plot_histogram('Games')
    analysis.plot_scatter('years_with_company', 'performance_score')
    analysis.plot_scatter('salary', 'performance_score', color='red')

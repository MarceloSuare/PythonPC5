import pandas as pd
from collections import defaultdict

# Leer el archivo CSV
df_wine = pd.read_csv("/workspaces/PythonPC5/SOLUCIONARIO/data/winemag-data-130k-v2.csv")

# Explorar el DataFrame
print(df_wine.head())
print(df_wine.info())

# Renombrar columnas
df_wine.rename(columns={
    'country': 'pais',
    'designation': 'denominacion',
    'points': 'puntos',
    'price': 'precio'
}, inplace=True)

# Crear nuevas columnas
# Etiquetar continentes
continents = defaultdict(lambda: 'Otros', {
    'France': 'Europa',
    'Italy': 'Europa',
    'US': 'América',
    'Spain': 'Europa',
    'Portugal': 'Europa',
    'Chile': 'América',
    'Argentina': 'América',
    'Australia': 'Oceanía',
    'Austria': 'Europa',
    'Germany': 'Europa',
    # Añade más países según sea necesario
})

df_wine['continente'] = df_wine['pais'].map(continents)

# Crear una columna que indique si el vino es caro o barato (por encima de la mediana)
median_price = df_wine['precio'].median()
df_wine['categoria_precio'] = df_wine['precio'].apply(lambda x: 'Caro' if x > median_price else 'Barato')

# Crear una columna que indique si el vino tiene una puntuación excelente (>90)
df_wine['puntuacion_excelente'] = df_wine['puntos'].apply(lambda x: 'Excelente' if x > 90 else 'Normal')

# Generar reportes por agrupamiento de datos
# 1. Promedio de precio y cantidad de reviews por país
reporte_pais = df_wine.groupby('pais').agg({
    'precio': 'mean',
    'puntos': 'count'
}).sort_values(by='precio', ascending=False)
print(reporte_pais.head())

# 2. Vinos mejor puntuados por continente
reporte_continente = df_wine.groupby('continente').agg({
    'puntos': 'max'
}).sort_values(by='puntos', ascending=False)
print(reporte_continente.head())

# 3. Promedio de precio y cantidad de reviews por continente
reporte_precio_continente = df_wine.groupby('continente').agg({
    'precio': 'mean',
    'puntos': 'count'
}).sort_values(by='precio', ascending=False)
print(reporte_precio_continente.head())

# 4. Cantidad de vinos por categoría de precio
reporte_categoria_precio = df_wine['categoria_precio'].value_counts()
print(reporte_categoria_precio)

# Almacenar uno de los reportes en un archivo Excel
reporte_pais.to_excel("reporte_pais.xlsx")

# Almacenar otro reporte en un archivo CSV
reporte_continente.to_csv("reporte_continente.csv")

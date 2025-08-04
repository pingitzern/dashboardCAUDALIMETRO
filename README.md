# 💧 Dashboard de Análisis de Producción para Equipos de Ósmosis Inversa

Esta es una aplicación web interactiva creada con Streamlit para analizar y visualizar los datos de producción de un equipo de ósmosis inversa a partir de los registros de un caudalímetro.

## 🚀 Características Principales

- **Carga de Datos Flexible**: Soporta la carga de archivos en formato `.csv` y `.xlsx`.
- **Reportes por Rango de Fechas**: Permite al usuario seleccionar un período específico para el análisis.
- **Detección Automática de Ciclos**: Identifica de forma inteligente los ciclos de producción, considerando como una pausa cualquier interrupción mayor a 10 minutos.
- **Cálculo de Volumen**: Calcula con precisión el volumen de agua producido en cada ciclo, el total diario y el total para el período seleccionado.
- **Visualización Interactiva**: Muestra los resultados en un reporte claro y fácil de entender, además de un gráfico de barras que resume la producción diaria.

## 🛠️ Cómo Utilizar la Aplicación

1.  **Ejecutar la Aplicación**: Para iniciar el dashboard, ejecuta el siguiente comando en tu terminal:
    ```bash
    streamlit run analisis_osmosis.py
    ```
2.  **Subir el Archivo**: Haz clic en el botón "Elige tu archivo de datos" y selecciona el archivo Excel o CSV que contiene los registros del caudalímetro. El archivo debe tener obligatoriamente dos columnas:
    - `fecha_hora`: La fecha y hora de la medición.
    - `L/MIN`: El caudal medido en litros por minuto.
3.  **Seleccionar Fechas**: En la barra lateral, elige la fecha de inicio y fin para el período que deseas analizar.
4.  **Generar Reporte**: Haz clic en el botón "Generar Reporte". La aplicación procesará los datos y mostrará un resumen detallado de la producción.

## ⚙️ Lógica de Negocio

El núcleo del análisis es la detección de ciclos. La aplicación considera que un nuevo ciclo de producción comienza cuando detecta una pausa en el registro de datos superior a **10 minutos**. Además, para que un registro sea considerado como "producción real", el caudal (`flowRate`) debe ser de al menos **1.0 L/min**. Los registros por debajo de este umbral son ignorados para el cálculo del volumen.
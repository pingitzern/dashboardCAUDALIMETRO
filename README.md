# dashboardCAUDALIMETRO

Este proyecto es un dashboard interactivo construido con Streamlit para analizar los datos de producción de un equipo de ósmosis inversa. La aplicación permite a los usuarios subir un archivo de datos (CSV o Excel) y genera un reporte detallado de los ciclos de producción y el volumen total de agua producida en un período seleccionado.

## 📜 Descripción

La herramienta está diseñada para procesar datos crudos de caudalímetros, identificar automáticamente los ciclos de operación y presentar un resumen claro y fácil de entender, tanto a nivel diario como para un período completo.

## ✨ Características Principales

- **Carga de datos flexible**: Soporta archivos en formato `.csv` y `.xlsx`.
- **Análisis de ciclos de producción**: Detecta automáticamente los ciclos de trabajo basándose en interrupciones de tiempo (10 minutos o más).
- **Cálculo de volumen**: Calcula el volumen de agua producida en cada ciclo y el total acumulado.
- **Reportes detallados**: Muestra un desglose de los ciclos por día, con horas de inicio/fin y el volumen de cada uno.
- **Visualización gráfica**: Incluye un gráfico de barras que resume la producción total por día.
- **Interfaz interactiva**: Permite al usuario seleccionar el rango de fechas para el análisis.

## ⚙️ Lógica de Análisis

El script aplica la siguiente lógica de negocio:
1.  **Detección de Ciclos**: Un ciclo de producción se considera nuevo si hay un intervalo de **más de 10 minutos** desde el último registro de datos.
2.  **Umbral de Producción**: La producción real se contabiliza solo cuando el caudal (`L/MIN`) es de **1.0 o superior**. Los registros con un caudal inferior se ignoran para el cálculo de volumen.

## 📊 Formato de Datos de Entrada

Para que el análisis funcione correctamente, el archivo subido debe contener al menos las siguientes dos columnas:

- `fecha_hora`: La fecha y hora de la medición.
- `L/MIN`: El caudal medido en litros por minuto. (También se acepta el nombre de columna `flowRate`).

## 🚀 Instalación y Uso

Para ejecutar este dashboard en tu máquina local, sigue estos pasos:

1.  **Clona este repositorio:**
    ```bash
    git clone <URL-DEL-REPOSITORIO>
    cd dashboardCAUDALIMETRO
    ```

2.  **Crea y activa un entorno virtual (recomendado):**
    ```bash
    # Para Windows
    python -m venv venv
    venv\Scripts\activate

    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecuta la aplicación Streamlit:**
    ```bash
    streamlit run analisis_osmosis.py
    ```

5.  Abre tu navegador y ve a la dirección URL que se muestra en la terminal.

## 🛠️ Tecnologías Utilizadas

- Python
- Streamlit
- Pandas
- Numpy
- Openpyxl

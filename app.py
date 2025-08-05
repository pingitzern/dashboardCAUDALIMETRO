from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import io

app = Flask(__name__)

# --- Funciones Principales de Análisis ---

def procesar_datos(df):
    """Limpia y prepara el DataFrame para el análisis."""
    if 'L/MIN' in df.columns:
        df.rename(columns={'L/MIN': 'flowRate'}, inplace=True)
    
    if 'flowRate' not in df.columns or 'fecha_hora' not in df.columns:
        return None, "El archivo debe contener las columnas 'fecha_hora' y 'L/MIN' (o 'flowRate')."

    df['fecha_hora'] = pd.to_datetime(df['fecha_hora'], errors='coerce')
    df.dropna(subset=['fecha_hora', 'flowRate'], inplace=True)
    df.sort_values(by='fecha_hora', inplace=True, ascending=True)
    return df, None

def analizar_periodo(df, fecha_inicio, fecha_fin):
    """Aplica la lógica de negocio para analizar los datos en el rango de fechas seleccionado."""
    
    mask = (df['fecha_hora'].dt.date >= fecha_inicio) & (df['fecha_hora'].dt.date <= fecha_fin)
    df_periodo = df.loc[mask].copy()

    if df_periodo.empty:
        return None, 0, "No hay datos para el rango de fechas seleccionado."

    df_periodo['time_since_last'] = df_periodo['fecha_hora'].diff()
    time_gap_threshold = pd.Timedelta('10 minutes')
    df_periodo['cycle_id'] = (df_periodo['time_since_last'] > time_gap_threshold).cumsum()

    all_cycles_data = []

    for cycle_id, cycle_data in df_periodo.groupby('cycle_id'):
        if cycle_data.empty:
            continue

        production_data = cycle_data[cycle_data['flowRate'] >= 1.0].copy()
        if production_data.empty:
            continue

        start_time = production_data['fecha_hora'].min()
        end_time = production_data['fecha_hora'].max()
        
        production_data['time_diff_mins'] = production_data['fecha_hora'].diff().dt.total_seconds().div(60)
        production_data['volume'] = production_data['flowRate'] * production_data['time_diff_mins']
        cycle_volume = production_data['volume'].sum()

        all_cycles_data.append({
            'start_date': start_time.date(),
            'start_time': start_time,
            'end_time': end_time,
            'cycle_volume': cycle_volume
        })
    
    if not all_cycles_data:
        return None, 0, "No se detectaron ciclos de producción en este período."

    results_df = pd.DataFrame(all_cycles_data)
    period_total_volume = results_df['cycle_volume'].sum()
    
    return results_df, period_total_volume, None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            try:
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                
                df_procesado, error = procesar_datos(df)

                if error:
                    return render_template('index.html', error=error)

                min_date = df_procesado['fecha_hora'].min().date()
                max_date = df_procesado['fecha_hora'].max().date()

                fecha_inicio_str = request.form.get('fecha_inicio')
                fecha_fin_str = request.form.get('fecha_fin')

                if fecha_inicio_str and fecha_fin_str:
                    fecha_inicio = pd.to_datetime(fecha_inicio_str).date()
                    fecha_fin = pd.to_datetime(fecha_fin_str).date()

                    if fecha_inicio > fecha_fin:
                        return render_template('index.html', error="La fecha de inicio no puede ser posterior a la fecha de fin.", min_date=min_date.strftime('%Y-%m-%d'), max_date=max_date.strftime('%Y-%m-%d'))

                    reporte_df, volumen_total, error = analizar_periodo(df_procesado, fecha_inicio, fecha_fin)

                    if error:
                        return render_template('index.html', error=error, min_date=min_date.strftime('%Y-%m-%d'), max_date=max_date.strftime('%Y-%m-%d'))
                    
                    # Agrupar por día
                    reporte_diario = {}
                    if reporte_df is not None:
                        for day in sorted(reporte_df['start_date'].unique()):
                            day_str = day.strftime('%d de %B de %Y')
                            day_cycles_data = reporte_df[reporte_df['start_date'] == day]
                            daily_total_volume = day_cycles_data['cycle_volume'].sum()
                            reporte_diario[day_str] = {
                                'cycles': day_cycles_data.to_dict('records'),
                                'total_volume': daily_total_volume
                            }


                    return render_template('index.html', reporte_diario=reporte_diario, volumen_total=volumen_total, min_date=min_date.strftime('%Y-%m-%d'), max_date=max_date.strftime('%Y-%m-%d'), fecha_inicio=fecha_inicio_str, fecha_fin=fecha_fin_str)

                return render_template('index.html', min_date=min_date.strftime('%Y-%m-%d'), max_date=max_date.strftime('%Y-%m-%d'))

            except Exception as e:
                return render_template('index.html', error=f"Ocurrió un error al procesar el archivo: {e}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

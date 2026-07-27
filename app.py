import streamlit as st
import pandas as pd

#configuracion de la pagina principal
st.set_page_config(page_title="Automatización", page_icon=":smiley:", layout="wide")

@st.cache_data
def load_data():
    # Cargar datos desde un archivo CSV
    url="https://docs.google.com/spreadsheets/d/e/2PACX-1vQCnu5XfJ_Bh45m11u9AncRJFhgs-Wz-V5b_hs1F6UomL8or0hu5X-tlAL8SSzREo0Sgh9Vs0ka38_1/pub?gid=1473418694&single=true&output=csv"
    data = pd.read_csv(url)
    data = data[data["Sede"]=="San Felipe"]
    data['Fecha del Turno'] = pd.to_datetime(data['Fecha del Turno'], format='%d/%m/%Y', dayfirst=True, errors='coerce')
    # Eliminar filas donde la fecha es inválida (NaT), ya que no se pueden pivotar correctamente
    data.dropna(subset=['Fecha del Turno'], inplace=True)

    # Realizar el pivoteo para crear 'Hora de Inicio' y 'Hora de Termino'
    df_pivot_final = data.pivot_table(
        index=['Nombre Fiscalizador', 'Fecha del Turno', 'Sede'], # Columnas para agrupar
        columns='Selección de Jornada',
        values='Hora del turno',
        aggfunc='first' # Toma el primer valor si hay duplicados para una misma fecha y tipo de jornada
    ).reset_index()

    # Renombrar las columnas resultantes del pivoteo
    df_pivot_final = df_pivot_final.rename(columns={
        'Inicio': 'Hora de Inicio',
        'Termino': 'Hora de Termino'
    })

    # Definir el orden deseado de las columnas
    nuevo_orden_columnas = ["Sede", "Nombre Fiscalizador", "Fecha del Turno", "Hora de Inicio", "Hora de Termino"]

    # Reordenar las columnas del DataFrame
    df_pivot_final = df_pivot_final[nuevo_orden_columnas]

    # Rellenar los valores NaN en las columnas de hora con espacios vacíos
    df_pivot_final[['Hora de Inicio', 'Hora de Termino']] = df_pivot_final[['Hora de Inicio', 'Hora de Termino']].fillna('')

    # Ordenar el DataFrame según la fecha y el nombre del fiscalizador
    df_pivot_final = df_pivot_final.sort_values(by=['Fecha del Turno', 'Nombre Fiscalizador']).reset_index(drop=True)
    
    return df_pivot_final

def main():
    st.title("Automatización de procesos con Streamlit")
    st.dataframe(load_data())



if __name__ == "__main__":
    main()
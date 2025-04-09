import streamlit as st
import pandas as pd
import urllib
import pyodbc
# ,sdjhcbzsd
# -------------------------------
# Configuración de la conexión
# -------------------------------
who_is = "Cris2"
users = {
    "Cris1": ["test_access", "CBARRERA29N7\\SQLEXPRESS"],
    "Cris2": ["test_access", "NB-CD-DEE2"]
}
user = users[who_is]

DB_NAME = user[0]
SERVER_NAME = user[1]

# -------------------------------
# Función para cargar datos
# -------------------------------
def cargar_datos():
    try:
        conn = pyodbc.connect(
            f"Driver={{ODBC Driver 17 for SQL Server}};"
            f"Server={SERVER_NAME};"
            f"Database={DB_NAME};"
            f"Trusted_Connection=yes;"
        )
        query = "SELECT * FROM ComponentT"
        df = pd.read_sql(query, con=conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {e}")
        return pd.DataFrame()

# -------------------------------
# Interfaz Streamlit
# -------------------------------
st.set_page_config(page_title="ComponentT Viewer", layout="wide")
st.title("📋 Visualizador de la tabla ComponentT")

# Cargar datos
df = cargar_datos()

if not df.empty:
    st.success("Datos cargados correctamente.")

    with st.expander("🔎 Filtros por columna"):
        for col in df.select_dtypes(include=['object', 'category', 'string']):
            valores = df[col].dropna().unique()
            if len(valores) < 100:
                seleccion = st.multiselect(f"Filtrar por '{col}'", valores)
                if seleccion:
                    df = df[df[col].isin(seleccion)]

    st.dataframe(df, use_container_width=True)

    # Botón para exportar
    st.download_button(
        label="📥 Exportar a Excel",
        data=df.to_excel(index=False, engine='openpyxl'),
        file_name="ComponentT_export.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("No se encontraron datos en la tabla o hubo un error de conexión.")
import streamlit as st
import pandas as pd
import urllib
import pyodbc


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
# Función para correr querys
# -------------------------------
    
def QuerysExcecute(query):
    try:
        conn = pyodbc.connect(
            f"Driver={{ODBC Driver 17 for SQL Server}};"
            f"Server={SERVER_NAME};"
            f"Database={DB_NAME};"
            f"Trusted_Connection=yes;"
        )
        df = pd.read_sql(query, con=conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Error al ejecutar query: {e}")
        return pd.DataFrame()
    
# -------------------------------
# Configuración de querys
# -------------------------------

# ENAPLetter = """SELECT ReceivedLetterT.Correlativo
#         FROM CompanyT INNER JOIN ReceivedLetterT ON CompanyT.CompanyID = ReceivedLetterT.CompanyID
#         WHERE (((CompanyT.CompanyName)="ENAP REFINERÍAS S.A."));"""
# Company = """SELECT CompanyT.CompanyName
#             FROM ReceivedLetterT
#             INNER JOIN CompanyT ON ReceivedLetterT.CompanyID = CompanyT.CompanyID;"""

# GetAllComponents = """SELECT ComponentT.ComponentName, PowerStationT.PowerStationName, CompanyT.CompanyName 
#                    FROM CompanyT INNER JOIN (PowerStationT INNER JOIN ComponentT ON PowerStationT.PowerStationID = ComponentT.PowerStationID) ON CompanyT.CompanyID = PowerStationT.MarketParticipantID
#                    ORDER BY ComponentT.ComponentID;"""
# GetAllGenerators = """SELECT ComponentT.ComponentName, PowerStationT.PowerStationName, CompanyT.CompanyName
#                     FROM CompanyT INNER JOIN (PowerStationT INNER JOIN ComponentT ON PowerStationT.PowerStationID = ComponentT.PowerStationID) ON CompanyT.CompanyID = PowerStationT.MarketParticipantID
#                     WHERE (((ComponentT.ComponentTypeID)=1))
#                     ORDER BY ComponentT.ComponentID;"""
# ReceivedLetter = """SELECT SentLetterT.Correlativo
#                 FROM ReceivedLetterT INNER JOIN (SentLetterT INNER JOIN SentLetterAnswersToT ON SentLetterT.SentLetterID = SentLetterAnswersToT.SentLetterID) ON ReceivedLetterT.ReceivedLetterID = SentLetterAnswersToT.AnswersToID;"""
# SentLetter = """SELECT ReceivedLetterT.Correlativo
#                 FROM SentLetterT INNER JOIN (ReceivedLetterT INNER JOIN ReceivedLetterAnswersToT ON ReceivedLetterT.ReceivedLetterID = ReceivedLetterAnswersToT.ReceivedLetterID) ON SentLetterT.SentLetterID = ReceivedLetterAnswersToT.AnswersToID;
#                 """
# date = """SELECT ReceivedLetterT.LetterDate
#             FROM ReceivedLetterT;"""
# next_company = """
#                 SELECT 
#                     c.CompanyName,
#                     r.Correlativo,
#                     CAST(r.LetterDate AS DATE) AS LetterDate
#                 FROM 
#                     ReceivedLetterT r
#                 INNER JOIN 
#                     CompanyT c ON r.CompanyID = c.CompanyID
#                 ORDER BY 
#                     r.Correlativo
#                 """

GetCmponents = """SELECT ComponentT.ComponentName, PowerStationT.PowerStationName, CompanyT.CompanyName, ComponentT.ComponentID
FROM CompanyT INNER JOIN (PowerStationT INNER JOIN ComponentT ON PowerStationT.PowerStationID = ComponentT.PowerStationID) ON CompanyT.CompanyID = PowerStationT.MarketParticipantID
ORDER BY ComponentT.ComponentID;
"""
GetCommitments = """SELECT CompanyT.CompanyName AS Empresa, ComponentT.ComponentName AS Componente, EMTPModelT.EMTPModelTypeName AS ModeloEMTP, CommitmentInLetterT.CommittedDate AS FechaPropuesta
FROM (((CommitmentInLetterT INNER JOIN ComponentT ON CommitmentInLetterT.ComponentID = ComponentT.ComponentID) INNER JOIN EMTPModelT ON CommitmentInLetterT.EMTPModelID = EMTPModelT.EMTPModelID) INNER JOIN ReceivedLetterT ON CommitmentInLetterT.ReceivedLetterID = ReceivedLetterT.ReceivedLetterID) INNER JOIN CompanyT ON ReceivedLetterT.CompanyID = CompanyT.CompanyID
WHERE CommitmentInLetterT.CommittedDate IS NOT NULL;
"""
MissingModels = """SELECT Nz(Base.CompanyName, 'Empresa no encontrada') AS Empresa, Base.ComponentName AS Componente, EMTPModelT.EMTPModelTypeName AS EMTPModelFaltante
FROM (SELECT ComponentT.ComponentID, ComponentT.ComponentName, CompanyT.CompanyName FROM ComponentT LEFT JOIN CompanyT ON ComponentT.MarketParticipantID = CompanyT.CompanyID)  AS Base, EMTPModelT
WHERE NOT EXISTS (         SELECT 1         FROM ComponentInReceivedLetterT         WHERE              ComponentInReceivedLetterT.ComponentID = Base.ComponentID             AND ComponentInReceivedLetterT.EMTPModelID = EMTPModelT.EMTPModelID     );
"""
ReceivedComponents = """SELECT Nz(CompanyT.CompanyName, 'Empresa no encontrada') AS Empresa, ComponentT.ComponentName AS Componente, EMTPModelT.EMTPModelTypeName AS ModeloEMTP
FROM ((ComponentInReceivedLetterT INNER JOIN ComponentT ON ComponentInReceivedLetterT.ComponentID = ComponentT.ComponentID) INNER JOIN EMTPModelT ON ComponentInReceivedLetterT.EMTPModelID = EMTPModelT.EMTPModelID) LEFT JOIN CompanyT ON ComponentT.MarketParticipantID = CompanyT.CompanyID;
"""
ReceivedModel = """SELECT Nz(CompanyT.CompanyName, 'Empresa no encontrada') AS Empresa, ComponentT.ComponentName AS Componente, EMTPModelT.EMTPModelTypeName AS ModeloEMTP, ReceivedLetterT.LetterDate AS FechaRecepcion
FROM (((ComponentInReceivedLetterT INNER JOIN ComponentT ON ComponentInReceivedLetterT.ComponentID = ComponentT.ComponentID) INNER JOIN EMTPModelT ON ComponentInReceivedLetterT.EMTPModelID = EMTPModelT.EMTPModelID) INNER JOIN ReceivedLetterT ON ComponentInReceivedLetterT.ReceivedLetterID = ReceivedLetterT.ReceivedLetterID) LEFT JOIN CompanyT ON ComponentT.MarketParticipantID = CompanyT.CompanyID;
"""
ReceivedLetterAnswered = """SELECT SentLetterT.Correlativo
FROM ReceivedLetterT INNER JOIN (SentLetterT INNER JOIN SentLetterAnswersToT ON SentLetterT.SentLetterID = SentLetterAnswersToT.SentLetterID) ON ReceivedLetterT.ReceivedLetterID = SentLetterAnswersToT.AnswersToID
WHERE (((ReceivedLetterT.Correlativo)=[Forms]![ReceivedLetterF]![txtBoxCorrelativo]));
"""
SentLetterAnswered = """SELECT ReceivedLetterT.Correlativo, CompanyT.CompanyName
FROM CompanyT INNER JOIN (SentLetterT INNER JOIN (ReceivedLetterT INNER JOIN ReceivedLetterAnswersToT ON ReceivedLetterT.ReceivedLetterID = ReceivedLetterAnswersToT.ReceivedLetterID) ON SentLetterT.SentLetterID = ReceivedLetterAnswersToT.AnswersToID) ON CompanyT.CompanyID = ReceivedLetterT.CompanyID
WHERE (((SentLetterT.Correlativo)=[Forms]![SentLetterF]![txtCorrelativo]));
"""






# WHERE (((ReceivedLetterT.Correlativo)=[Forms]![ReceivedLetterF]![txtBoxCorrelativo]))
# WHERE (((SentLetterT.Correlativo)=Forms!SentLetterF![txtCorrelativo]))
# -------------------------------S
# Interfaz Streamlit
# -------------------------------
st.set_page_config(page_title="Data Viewer", layout="wide")
st.title("RESUMEN DE REVISIÓN DE MODELOS DLAB")

# Cargar datos
# df = QuerysExcecute(GetAllComponents)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Received Letter")
    df = QuerysExcecute(next_company)
    corr = df['Correlativo']
    Cname = df['CompanyName']
    date = df['LetterDate']
    if "index_actual" not in st.session_state:
        st.session_state.index_actual = 0
    # Botones para navegar
    col11, col12, col13 = st.columns([7, 1, 1])

    with col12:
        if st.button("⬅️ Anterior") and st.session_state.index_actual > 0:
            st.session_state.index_actual -= 1

    with col13:
        if st.button("➡️ Siguiente") and st.session_state.index_actual < len(df) - 1:
            st.session_state.index_actual += 1

    with col11:
        # Mostrar la fila actual
        fila = corr.iloc[st.session_state.index_actual]
        fila_2 = Cname.iloc[st.session_state.index_actual]
        fila_3 = date.iloc[st.session_state.index_actual]
        st.write(f"**Registro {st.session_state.index_actual + 1} de {len(df)}**")
        st.write(f"Correlativo: **{list(fila.to_dict().values())[0]}**")
        st.write(f"Empresa: **{list(fila_2.to_dict().values())[0]}**")
        st.write(f"Fecha recepción: **{list(fila_3.to_dict().values())[0]}**")



with col2:
    st.subheader("Sent Letter")
    df = QuerysExcecute(GetAllGenerators)
    st.dataframe(df)

























    # if not df.empty:
    #     with st.expander("🔎 Busque la carta"):
    #         for col in df.select_dtypes(include=['object', 'category', 'string']):
    #             valores = df[col].dropna().unique()
    #             if len(valores) < 10000:
    #                 seleccion = st.multiselect(f"Filtrar por '{col}'", valores)
    #                 if seleccion:
    #                     df = df[df[col].isin(seleccion)]
    #                     st.dataframe(df.style.set_properties(**{'width': '150px'}), use_container_width=True)




# with col3:
#     # if st.button("Eliminar componentes prueba"):
#     #     try:
#     #         cursor = conn.cursor()
#     #         cursor.execute("DELETE FROM ComponentT WHERE Nombre = 'Componente Prueba'")
#     #         conn.commit()
#     #         st.success("🗑️ Registros eliminados.")
#     #     except Exception as e:
#     #         st.error(f"❌ Error: {e}")
#     if st.button("Cartas Recibidas"):
#         result = QuerysExcecute(ReceivedLetter)
#         # st.metric("Total componentes", result['total'][0])
#         st.dataframe(result)



# if not df.empty:
#     st.success("Datos cargados correctamente.")

#     with st.expander("🔎 Filtros por columna"):
#         for col in df.select_dtypes(include=['object', 'category', 'string']):
#             valores = df[col].dropna().unique()
#             if len(valores) < 100:
#                 seleccion = st.multiselect(f"Filtrar por '{col}'", valores)
#                 if seleccion:
#                     df = df[df[col].isin(seleccion)]

#     st.dataframe(df, use_container_width=True)

#     # Botón para exportar
# #     st.download_button(
# #         label="📥 Exportar a Excel",
# #         data=df.to_excel(index=False, engine='openpyxl'),
# #         file_name="ComponentT_export.xlsx",
# #         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
# #     )
# else:
#     st.warning("No se encontraron datos en la tabla o hubo un error de conexión.")



# import pyodbc

# DB_NAME = "test_access"
# SERVER_NAME = "10.5.54.108\\NB-CD-DEE2"  # O solo "192.168.1.100" si es instancia por defecto
# usuario = "Fabi.fabi"
# contrasena = "Fabino123_#"

# try:
#     conn = pyodbc.connect(
#         f"Driver={{ODBC Driver 17 for SQL Server}};"
#         f"Server={SERVER_NAME};"
#         f"Database={DB_NAME};"
#         f"UID={usuario};"
#         f"PWD={contrasena};"
#     )
#     print("✅ Conectado correctamente.")
# except Exception as e:
#     print(f"❌ Error al conectar: {e}")

# import urllib
# from sqlalchemy import create_engine

# DB_NAME = "test_access"
# SERVER_NAME = "10.5.54.108\\NB-CD-DEE2"
# usuario = "Fabi.fabi"
# contrasena = "Fabino123_#"

# params = urllib.parse.quote_plus(
#     f"Driver={{ODBC Driver 17 for SQL Server}};"
#     f"Server={SERVER_NAME};"
#     f"Database={DB_NAME};"
#     f"UID={usuario};"
#     f"PWD={contrasena};"
# )
# connection_string = f"mssql+pyodbc:///?odbc_connect={params}"

# engine = create_engine(connection_string, echo=True)
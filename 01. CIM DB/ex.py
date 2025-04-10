import pandas as pd 
# import urllib
# from sqlalchemy import create_engine
# who_is = "Cris2"
# users = {"Hayter": ["NEWCIM", "localhost"], "Cris1": ["NEWCIM", "CBARRERA29N7\SQLEXPRESS"], "Cris2": ["SCADA_2", "NB-CD-DEE2"]}
# user = users[who_is]

# usuario = "Fabi.fabi"
# contrasena = "Fabifabiño123_-@sjk,chba<siclawr83746rq3efdqwl.kjsh!!!!"
 
# DB_NAME = user[0]
# SERVER_NAME = user[1]
# params = urllib.parse.quote_plus(
#     f"Driver={{ODBC Driver 17 for SQL Server}};"
#     f"Server={SERVER_NAME};"
#     f"Database={DB_NAME};"
#     f"UID={usuario};"
#     f"PWD={contrasena};"
# )
# connection_string = f"mssql+pyodbc:///?odbc_connect={params}"
# engine = create_engine(connection_string, echo=True)


usuarios = {
    "Nombre": ["Juan", "María", "Carlos", "Ana", "Luis"],
    "Apellido": ["Gómez", "López", "Rodríguez", "Pérez", "Martínez"],
    "Email": ["juan@example.com", "maria@example.com", "carlos@example.com", "ana@example.com", "luis@example.com"],
    "Telefono": ["123-123-4567", "456-987-6543", "789-567-8901", "654-234-5678", "963-678-9012"],
    "Edad": [12, 27, 22, 30, 16]
}

usuarios_df = pd.DataFrame(usuarios)
usuarios_df["Nombre Completo"] = usuarios_df["Nombre"] + " " + usuarios_df["Apellido"]

print(usuarios_df)
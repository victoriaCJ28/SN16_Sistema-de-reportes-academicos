import gspread
from oauth2client.service_account import ServiceAccountCredentials

def main():
    # Scope para Google Sheets API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # Cargar credenciales desde archivo JSON
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials/service_account.json", scope
    )
    client = gspread.authorize(creds)

    # Abrir Google Sheet por ID o nombre
    SHEET_ID = "1siSQmTX87HkddO5m4EkhbRKogPHK8-_WO97hK2_pq34"
    sheet = client.open_by_key(SHEET_ID).sheet1

    # Obtener todos los registros como lista de diccionarios
    records = sheet.get_all_records()

    print("Listado de alumnos:\n")
    for r in records:
        print(
            f"Id: {r.get('Id')} | "
            f"Nombre: {r.get('Nombre')} | "
            f"Email: {r.get('Email')} | "
            f"Período: {r.get('Período')} | "
            f"Materia: {r.get('Materia')} | "
            f"Nota: {r.get('Nota')}"
        )

if __name__ == "__main__":
    main()
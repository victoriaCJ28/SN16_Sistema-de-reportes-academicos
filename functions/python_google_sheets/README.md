# Proyecto Python - Imprimir Google Sheets

Este proyecto lee datos desde una hoja de **Google Sheets** y los imprime en consola.

## Campos esperados en la hoja
- Carnet
- Nombre
- Apellido
- Materia
- Nota

Los encabezados deben estar exactamente con esos nombres en la primera fila.

## Requisitos
- Python 3.9+
- Cuenta de Google
- Acceso a Google Sheets API

## Instalación (requerimientos)
```bash
##pip install -r requirements.txt
python -m pip install gspread oauth2client
```

## Configuración
1. Crear un proyecto en Google Cloud.
2. Habilitar **Google Sheets API** y **Google Drive API**.
3. Crear una **Service Account**.
4. Descargar el archivo JSON de credenciales.
5. Guardarlo en:
   ```
   credentials/service_account.json
   ```
6. Compartir la hoja de Google Sheets con el email de la Service Account.
7. Colocar el ID de la hoja en `main.py`.

## Ejecución
```bash
python main.py
```
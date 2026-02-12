import os
import smtplib
import pandas as pd
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
import google.auth

# --- FUNCIÓN ADICIONAL PARA LA BITÁCORA ---
def registrar_log(service, spreadsheet_id, evento, destinatarios, status):
    fecha_actual = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    valores = [[fecha_actual, evento, destinatarios, status]]
    body = {'values': valores}
    
    # Registra en la pestaña Log_Envios al final de la lista
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="Log_Envios!A:D",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()

def hello_http(request):
    # --- CONFIGURACIÓN ---
    SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
    RANGE_NAME = 'resumen_estudiantes!A:H' 
    mi_correo = os.environ.get('MI_CORREO')
    llave_seguridad = os.environ.get('LLAVE_SEGURIDAD')
    correos_str = os.environ.get('CORREOS_GRUPO', '')
    correos_grupo = [c.strip() for c in correos_str.split(',') if c]
    todos_str = ", ".join([mi_correo] + correos_grupo)

    # --- ESTILOS PARA LA RESPUESTA EN EL NAVEGADOR ---
    CSS_NAVEGADOR = """
   <style>
        .container { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 500px; margin: 40px auto; text-align: center; }
        .card { padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 1px solid #eee; }
        .success { background: #f0fff4; border-top: 5px solid #48bb78; }
        .error { background: #fff5f5; border-top: 5px solid #f56565; }
        .btn { display: inline-block; margin-top: 20px; padding: 10px 20px; background: #2d3748; color: white; text-decoration: none; border-radius: 8px; }
    </style>
    """

    try:
        # 1. OBTENCIÓN DE DATOS (Con permisos de escritura para logs)
        credentials, project = google.auth.default(scopes=['https://www.googleapis.com/auth/spreadsheets'])
        service = build('sheets', 'v4', credentials=credentials)
        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            return "No hay datos.", 404

        df = pd.DataFrame(values[1:], columns=values[0])
        df.columns = df.columns.str.strip()

        # 2. GENERACIÓN DE FILAS 
        filas_html = ""
        for _, row in df.iterrows():
            try:
               # Normalizamos la nota para la comparación
                nota = float(row['promedio_CUM'].replace(',', '.'))
                color_cum = "#2e7d32" if nota >= 7.0 else "#d32f2f" # Verde oscuro / Rojo DAC
            except:
                color_cum = "#37474f"
                
            # ---  Color para el Estado ---
            estado_texto = row['estado'].strip()
            # Si el estado es "En Riesgo", usamos rojo; de lo contrario, un color neutro
            color_estado_texto = "#d32f2f" if estado_texto == "En Riesgo" else "#4a5568"
            # También podemos cambiar el fondo si prefieres que resalte más
            fondo_estado = "#fff5f5" if estado_texto == "En Riesgo" else "#edf2f7"

            filas_html += f"""
            <tr style="border-bottom: 1px solid #edf2f7;">
                <td style="padding: 12px; font-size: 14px; color: #2d3748;">{row['nombre_estudiante']}</td>
                <td style="padding: 12px; text-align: center; color: #4a5568;">{row['asistencia']}</td>
                <td style="padding: 12px; text-align: center; font-weight: bold; color: {color_cum};">{row['promedio_CUM']}</td>
                <td style="padding: 12px; text-align: center;"><span style="background: {fondo_estado}; color: {color_estado_texto}; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{row['estado']}</span></td>
            </tr>
            """

        # 3. CONSTRUCCIÓN DEL CORREO 
        msg = MIMEMultipart()
        msg['From'] = mi_correo
        msg['To'] = mi_correo
        msg['Cc'] = ", ".join(correos_grupo)
        msg['Subject'] = "REPORTE ACADÉMICO - DAC"

        html_correo = f"""
        <div style="background-color: #f7fafc; padding: 30px; font-family: Arial, sans-serif;">
            <div style="max-width: 650px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <div style="background-color: #ffffff; padding: 25px; border-bottom: 2px solid #edf2f7;">
                    <h2 style="color: #2d3748; margin: 0; font-size: 22px;">📊 Consolidado de rendimiento estudiantil</h2> 
                </div>
                <div style="padding: 25px;">
                    <p style="color: #4a5568;">Estimados miembros de la <b>DAC</b>,</p>
                    <p style="color: #4a5568;">Se presenta el informe de indicadores académicos procesado automáticamente por la Unidad de Proyectos ESIT:</p>
                    <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                        <thead>
                            <tr style="background-color: #f8fafc; border-bottom: 2px solid #e2e8f0;">
                                <th style="padding: 12px; text-align: left; color: #64748b; font-size: 11px; text-transform: uppercase;">Estudiante</th>
                                <th style="padding: 12px; color: #64748b; font-size: 11px; text-transform: uppercase;">Asistencia</th>
                                <th style="padding: 12px; color: #64748b; font-size: 11px; text-transform: uppercase;">CUM</th>
                                <th style="padding: 12px; color: #64748b; font-size: 11px; text-transform: uppercase;">Estado</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filas_html}
                        </tbody>
                    </table>
                </div>
                <div style="background: #f8fafc; padding: 15px; text-align: center; font-size: 12px; color: #94a3b8; border-top: 1px solid #edf2f7;">
                    Este reporte es generado por el sistema de automatización Serverless. No responder a este correo.
                </div>
            </div>
        </div>
        """
        msg.attach(MIMEText(html_correo, 'html'))

        # 4. ENVÍO
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(mi_correo, llave_seguridad)
        server.sendmail(mi_correo, [mi_correo] + correos_grupo, msg.as_string())
        server.quit()

        # 5. REGISTRO AUTOMÁTICO DE LOG
        registrar_log(service, SPREADSHEET_ID, "Reporte DAC Enviado", todos_str, "200 OK")

        return f"{CSS_NAVEGADOR}<div class='container'><div class='card success'><h2>✅ Reporte Enviado</h2><p>La DAC ha recibido el reporte y se ha registrado en la bitácora.</p></div></div>", 200

    except Exception as e:
        # Intento de registrar el error en los logs si la conexión con Sheets está viva
        try: registrar_log(service, SPREADSHEET_ID, "ERROR DE ENVÍO", todos_str, str(e))
        except: pass
        return f"{CSS_NAVEGADOR}<div class='container'><div class='card error'><h2>❌ Error Crítico</h2><p>{str(e)}</p></div></div>", 500
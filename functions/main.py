import os
import smtplib
import pandas as pd
import pytz
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
import google.auth

# --- FUNCIÓN DE BITÁCORA (USA APPEND PARA CONSERVAR ANTERIORES) ---
def registrar_log(service, spreadsheet_id, evento, destinatarios, status):
    try:
        tz = pytz.timezone('America/El_Salvador')
        # Agregamos un apóstrofe (') al inicio para forzar el formato de texto en Sheets
        fecha_actual = "'" + datetime.now(tz).strftime('%d/%m/%Y %H:%M:%S')
    except:
        fecha_actual = "'" + datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    valores = [[fecha_actual, evento, destinatarios, status]]
    body = {'values': valores}
    
    # Se usa el rango "Log_Envios!A:A" para asegurar que empiece en la primera columna
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="Log_Envios!A:D", 
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

def limpiar_y_validar(valor, tipo="cum"):
    if pd.isna(valor) or str(valor).strip() == "":
        raise ValueError("Campo vacío")
    
    s = str(valor).replace('%', '').replace(',', '.').strip()
    
    try:
        num = float(s)
    except:
        raise ValueError(f"Dato no numérico: '{valor}'")
    
    if num < 0:
        raise ValueError(f"Valor negativo no permitido: {num}")
    
    if tipo == "asistencia" and num > 100:
        raise ValueError(f"Asistencia excede el 100%: {num}%")
        
    return num

def hello_http(request):
    # --- CONFIGURACIÓN ---
    SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
    mi_correo = os.environ.get('MI_CORREO')
    llave_seguridad = os.environ.get('LLAVE_SEGURIDAD')
    correos_str = os.environ.get('CORREOS_GRUPO', '')
    correos_grupo = [c.strip() for c in correos_str.split(',') if c]
    todos_str = ", ".join([mi_correo] + correos_grupo)

    # --- ESTILOS ORIGINALES ---
    CSS_NAVEGADOR = """
   <style>
        .container { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 500px; margin: 40px auto; text-align: center; }
        .card { padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border: 1px solid #eee; }
        .success { background: #f0fff4; border-top: 5px solid #48bb78; }
        .error { background: #fff5f5; border-top: 5px solid #f56565; }
    </style>
    """

    try:
        credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/spreadsheets'])
        service = build('sheets', 'v4', credentials=credentials)
        
        # Lectura de datos
        res_resumen = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="resumen_estudiantes!A:H").execute()
        res_asis = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="asistencia_detalle!A:L").execute()
        res_eval = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range="evaluaciones_detalle!A:K").execute()

        df = pd.DataFrame(res_resumen.get('values', [])[1:], columns=res_resumen.get('values', [])[0])
        df_asis = pd.DataFrame(res_asis.get('values', [])[1:], columns=res_asis.get('values', [])[0])
        df_eval = pd.DataFrame(res_eval.get('values', [])[1:], columns=res_eval.get('values', [])[0])

        df.columns = df.columns.str.strip()
        df_asis.columns = df_asis.columns.str.strip()
        df_eval.columns = df_eval.columns.str.strip()

        filas_html = ""
        observaciones_lista = []
        estados_validos = ["Activo", "Retirado", "En Riesgo"]
        
        for _, row in df.iterrows():
            email_est = str(row['email_estudiante']).strip()
            nombre_est = row['nombre_estudiante']
            
            try:
                # 1. VALIDAR ESTADO ACTUAL DEL SHEET
                estado_sheet = str(row['estado']).strip()
                if estado_sheet not in estados_validos:
                    raise ValueError(f"Estado inválido en Sheet: '{estado_sheet}'")

                # 2. PROCESAR ASISTENCIA
                det_asis = df_asis[df_asis['email_estudiante'].str.strip() == email_est].copy()
                if det_asis.empty: raise ValueError("Sin registros de asistencia")
                asis_nums = det_asis['porcentaje_asistencia'].apply(lambda x: limpiar_y_validar(x, "asistencia"))
                promedio_asis = asis_nums.mean()
                
                # 3. PROCESAR CUM
                det_eval = df_eval[df_eval['email_estudiante'].str.strip() == email_est].copy()
                if det_eval.empty: raise ValueError("Sin registros de evaluaciones")
                notas_validadas = det_eval['nota_ponderada'].apply(lambda x: limpiar_y_validar(x, "cum"))
                cum_calculado = notas_validadas.sum()

                # 4. LÓGICA DE ESTADO SEGÚN FÓRMULA (IF AND...)
                # IF(AND(cum<=5; asis<=0.5); "Retirado"; IF(AND(cum>=6; asis>=0.8); "Activo"; "En Riesgo"))
                asis_decimal = promedio_asis / 100
                
                if cum_calculado <= 5.0 and asis_decimal <= 0.5:
                    nuevo_estado = "Retirado"
                elif cum_calculado >= 6.0 and asis_decimal >= 0.8:
                    nuevo_estado = "Activo"
                else:
                    nuevo_estado = "En Riesgo"

                # 5. COLORES Y ESTILOS
                color_cum = "#2e7d32" if cum_calculado >= 7.0 else "#d32f2f"
                color_txt_estado = "#d32f2f" if nuevo_estado == "En Riesgo" else "#4a5568"
                fondo_estado = "#fff5f5" if nuevo_estado == "En Riesgo" else "#edf2f7"

                filas_html += f"""
                <tr style="border-bottom: 1px solid #edf2f7;">
                    <td style="padding: 12px; font-size: 14px; color: #2d3748;">{nombre_est}</td>
                    <td style="padding: 12px; text-align: center; color: #4a5568;">{promedio_asis:.2f}%</td>
                    <td style="padding: 12px; text-align: center; font-weight: bold; color: {color_cum};">{cum_calculado:.2f}</td>
                    <td style="padding: 12px; text-align: center;"><span style="background: {fondo_estado}; color: {color_txt_estado}; padding: 4px 8px; border-radius: 4px; font-size: 12px;">{nuevo_estado}</span></td>
                </tr>
                """
            except Exception as e:
                msg_err = f"Inconsistencia en {nombre_est}: {str(e)}"
                observaciones_lista.append(f"<li>{msg_err}</li>")
                # REGISTRO DE ERROR EN LOG (CADA UNO EN SU FILA)
                registrar_log(service, SPREADSHEET_ID, "ERROR_DATO", email_est, str(e))

        # 6. CONSTRUCCIÓN DEL CORREO
        html_obs = ""
        if observaciones_lista:
            html_obs = f"""
            <div style="margin-top: 20px; padding: 15px; background: #fff5f5; border: 1px solid #feb2b2; border-radius: 8px;">
                <p style="color: #c53030; font-weight: bold; margin: 0 0 5px 0;">Atención - Inconsistencias:</p>
                <ul style="color: #742a2a; font-size: 12px; margin: 0;">{''.join(observaciones_lista)}</ul>
            </div>"""

        msg = MIMEMultipart()
        msg['Subject'] = "REPORTE ACADÉMICO - DAC"
        msg['From'] = mi_correo
        msg['To'] = mi_correo
        msg['Cc'] = ", ".join(correos_grupo)

        html_correo = f"""
        <div style="background-color: #f7fafc; padding: 30px; font-family: Arial, sans-serif;">
            <div style="max-width: 650px; margin: 0 auto; background: white; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0;">
                <div style="padding: 25px; border-bottom: 2px solid #edf2f7;">
                    <h2 style="color: #2d3748; margin: 0; font-size: 22px;">📊 Consolidado de rendimiento estudiantil</h2> 
                </div>
                <div style="padding: 25px;">
                    <p>Estimados miembros de la <b>DAC</b>.</p>
                    <p>Se presenta el informe de indicadores académicos procesado automáticamente por la Unidad de Proyectos ESIT:</p>
                    <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                        <thead>
                            <tr style="background-color: #f8fafc; border-bottom: 2px solid #e2e8f0;">
                                <th style="padding: 12px; text-align: left; font-size: 11px;">ESTUDIANTE</th>
                                <th style="padding: 12px; color: #64748b; font-size: 11px;">ASISTENCIA</th>
                                <th style="padding: 12px; color: #64748b; font-size: 11px;">CUM</th>
                                <th style="padding: 12px; color: #64748b; font-size: 11px;">ESTADO</th>
                            </tr>
                        </thead>
                        <tbody>{filas_html}</tbody>
                    </table>
                    {html_obs}
                </div>
                <div style="background: #f8fafc; padding: 15px; text-align: center; font-size: 12px; color: #94a3b8;">
                    Generado automáticamente por sistema serverless. No responder a este correo.
                </div>
            </div>
        </div>"""
        
        msg.attach(MIMEText(html_correo, 'html'))
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(mi_correo, llave_seguridad)
        server.sendmail(mi_correo, [mi_correo] + correos_grupo, msg.as_string())
        server.quit()

        registrar_log(service, SPREADSHEET_ID, "Reporte DAC Enviado", todos_str, "200 OK")
        return f"{CSS_NAVEGADOR}<div class='container'><div class='card success'><h2>✅ Reporte Enviado</h2><p>Logs actualizados correctamente.</p></div></div>", 200

    except Exception as e:
        try: registrar_log(service, SPREADSHEET_ID, "ERROR CRÍTICO", todos_str, str(e))
        except: pass
        return f"{CSS_NAVEGADOR}<div class='container'><div class='card error'><h2>❌ Error Crítico</h2><p>{str(e)}</p></div></div>", 500
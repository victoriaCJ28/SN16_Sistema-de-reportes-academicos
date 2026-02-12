# SN16: Sistema de Reportes Académicos Serverless
## Dirección General de Escuelas Rurales (DAC)

Este proyecto desarrolla una solución automatizada para la consolidación de datos académicos, eliminando procesos manuales mediante el uso de **Google Cloud Functions** y la integración de servicios en la nube.

---

### 👥 Equipo SN-16 - Roles y Responsabilidades
* **Andrea Victoria Castro Jiménez**: Líder de Proyecto Jr. & Ingeniera de Integración Serverless Jr.
* **Bryan Stephan Madriz Arteaga**: Analista de Datos Académicos Jr.
* **Rafael Ignacio Funes Duarte**: Desarrollador Backend Jr. (Funcional)
* **Elmer Geovany Quijano Hernández**: QA / Documentador Técnico Jr.

---

### 🏗️ Arquitectura Conceptual
El sistema sigue un flujo asincrónico diseñado para la eficiencia operativa.
1. **Origen:** Datos en Google Sheets (Asistencia, Notas, Evaluaciones).
2. **Procesamiento:** Google Cloud Functions (Node.js/Python).
3. **Salida:** Reportes automáticos en PDF o HTML.
4. **Notificación:** Envío vía Gmail API.
5. **Control:** Registro de actividad en Hoja de Logs.

---

### 📂 Estructura del Repositorio
* `/functions`: Lógica de las Cloud Functions y archivos de despliegue
* `/docs`: Documentación oficial dividida por fases (0 a 4)
* `/tests`: Matriz de pruebas y validación de escenarios

---

### 🚀 Instrucciones de Despliegue y Configuración

#### 1️⃣ Configuración en Google Cloud
* Crear una **Cloud Function** con entorno de ejecución **Python 3.11**.
* Definir el **Entry Point** como `hello_http`.
* Asignar una **Service Account** con permisos para leer la Google Sheet.

#### 2️⃣ Gestión de Seguridad (Variables de Entorno)
Para evitar el hardcoding y proteger credenciales en GitHub, el sistema utiliza variables de entorno mediante el módulo `os`.

Agregar en **Variables & Secrets**:

* `MI_CORREO`: Dirección de correo electrónico del remitente.
* `LLAVE_SEGURIDAD`: Contraseña de aplicación de 16 caracteres de Google.
* `SPREADSHEET_ID`: ID de la Google Sheet de origen.
* `CORREOS_GRUPO`: Lista de correos separados por coma.

---

### 🎨 Lógica de Alerta y Formato Condicional
* **Resaltado de Riesgo:** Los estudiantes con estado "En Riesgo" se muestran en color rojo (`#d32f2f`) con fondo destacado.
* **Alerta de CUM:** Promedios menores a **7.0** cambian automáticamente a color rojo.
* **Interfaz Web:** Respuesta visual en navegador tras envío exitoso.

---
*Proyecto desarrollado para la Unidad de Proyectos ESIT - Línea de Automatización Serverless.*

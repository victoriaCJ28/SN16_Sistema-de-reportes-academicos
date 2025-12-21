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
*Proyecto desarrollado para la Unidad de Proyectos ESIT - Línea de Automatización Serverless.*

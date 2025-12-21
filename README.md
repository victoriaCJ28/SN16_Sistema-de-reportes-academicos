# SN16: Sistema de Reportes Académicos Serverless
## Dirección General de Escuelas Rurales (DAC)

[cite_start]Este proyecto desarrolla una solución automatizada para la consolidación de datos académicos, eliminando procesos manuales mediante el uso de **Google Cloud Functions** y la integración de servicios en la nube[cite: 3, 39, 45].

---

### 👥 Equipo SN-16 - Roles y Responsabilidades
* [cite_start]**Andrea Victoria Castro Jiménez**: Líder de Proyecto Jr. & Ingeniera de Integración Serverless Jr.[cite: 95].
* [cite_start]**Bryan Stephan Madriz Arteaga**: Analista de Datos Académicos Jr.[cite: 95].
* [cite_start]**Rafael Ignacio Funes Duarte**: Desarrollador Backend Jr. (Funcional)[cite: 95].
* [cite_start]**Elmer Geovany Quijano Hernández**: QA / Documentador Técnico Jr.[cite: 95].

---

### 🏗️ Arquitectura Conceptual
[cite_start]El sistema sigue un flujo asincrónico diseñado para la eficiencia operativa[cite: 16, 98]:
1. [cite_start]**Origen:** Datos en Google Sheets (Asistencia, Notas, Evaluaciones)[cite: 17, 37].
2. [cite_start]**Procesamiento:** Google Cloud Functions (Node.js/Python)[cite: 29, 110].
3. [cite_start]**Salida:** Reportes automáticos en PDF o HTML[cite: 19, 101].
4. [cite_start]**Notificación:** Envío vía Gmail API[cite: 20, 102].
5. [cite_start]**Control:** Registro de actividad en Hoja de Logs[cite: 21, 103].

---

### 📂 Estructura del Repositorio
* [cite_start]`/functions`: Lógica de las Cloud Functions y archivos de despliegue[cite: 139, 186].
* [cite_start]`/docs`: Documentación oficial dividida por fases (0 a 4)[cite: 121, 186].
* [cite_start]`/tests`: Matriz de pruebas y validación de escenarios[cite: 121, 194].

---
[cite_start]*Proyecto desarrollado para la Unidad de Proyectos ESIT - Línea de Automatización Serverless.*[cite: 48].
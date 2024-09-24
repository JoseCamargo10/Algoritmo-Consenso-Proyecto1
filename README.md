# ST0263 | Tópicos Especiales en Telemática

### Estudiantes
- José Manuel Camargo Hoyos | jmcamargoh@eafit.edu.co
- Jose David Valencia Calle | jdvalenci2@eafit.edu.co

### Profesor:
- Juan Carlos Montoya Mendoza | jcmontoy@eafit.edu.co

## 1. Descripción del Proyecto

### 1.1. Entendimiento del Problema

![Diagrama de Descripción](https://github.com/user-attachments/assets/5fcee5a9-04bf-48ad-b142-ee4cc205f94a)

El diagrama representa un sistema distribuido típico, donde las operaciones de lectura y escritura se distribuyen a través de múltiples nodos para mejorar la disponibilidad y el rendimiento. Dentro de este sistema, se pueden evidenciar los siguientes componentes: 
- **Cliente:** Es el punto de entrada del usuario al sistema. Realiza solicitudes de lectura y escritura de datos.
- **Proxy:** Actúa como intermediario entre el cliente y los servidores. Enruta las solicitudes de lectura a los servidores esclavos (slaves) y las solicitudes de escritura al servidor maestro (master). 
- **Maestro (Master):** Es el nodo principal responsable de procesar todas las solicitudes de escritura. Una vez procesada la escritura, replica los datos a los esclavos. 
- **Esclavos (Slaves):** Son nodos secundarios que contienen réplicas de los datos del maestro. Se utilizan únicamente para servir solicitudes de lectura, lo que distribuye la carga y mejora el rendimiento. 

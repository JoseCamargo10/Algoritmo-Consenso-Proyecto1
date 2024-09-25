# ST0263 | Tópicos Especiales en Telemática

## Estudiantes
- José Manuel Camargo Hoyos | jmcamargoh@eafit.edu.co
- Jose David Valencia Calle | jdvalenci2@eafit.edu.co

## Profesor:
- Juan Carlos Montoya Mendoza | jcmontoy@eafit.edu.co

## Proyecto 1 | Implementación de Algoritmo de Consenso para Elección de Líder

### 1. Descripción del Proyecto

#### 1.1. Entendimiento del Problema

![Diagrama de Descripción](https://github.com/user-attachments/assets/5fcee5a9-04bf-48ad-b142-ee4cc205f94a)

El diagrama representa un sistema distribuido típico, donde las operaciones de lectura y escritura se distribuyen a través de múltiples nodos para mejorar la disponibilidad y el rendimiento. Dentro de este sistema, se pueden evidenciar los siguientes componentes: 
- **Cliente:** Es el punto de entrada del usuario al sistema. Realiza solicitudes de lectura y escritura de datos.
- **Proxy:** Actúa como intermediario entre el cliente y los servidores. Enruta las solicitudes de lectura a los servidores esclavos (slaves) y las solicitudes de escritura al servidor maestro (master). 
- **Maestro (Master):** Es el nodo principal responsable de procesar todas las solicitudes de escritura. Una vez procesada la escritura, replica los datos a los esclavos. 
- **Esclavos (Slaves):** Son nodos secundarios que contienen réplicas de los datos del maestro. Se utilizan únicamente para servir solicitudes de lectura, lo que distribuye la carga y mejora el rendimiento.

Una vez establecidos los componentes, el flujo del sistema ha de funcionar de la siguiente manera: 
1. El cliente envía una solicitud de lectura o escritura al proxy.
2. El proxy identifica a qué clase de solicitud se refiere (escritura o lectura) y la reenvía al nodo correspondiente al tipo de solicitud (al tratarse de una solicitud de lectura, el proxy debe implementar un algoritmo que permita una distribución óptima de las cargas de peticiones).
3. Una vez el proxy redirige la petición, el nodo correspondiente se encarga de su procesamiento:
    1. **Escritura:** El maestro o nodo principal se encarga de escribir los datos, y una vez escritos, debe replicarlos a los esclavos o los secundarios para así garantizar la consistencia. 
    2. **Lectura:** El esclavo o nodo secundario procesa la petición y devuelve los datos al cliente a través del proxy.

Finalmente, e identificadas las cuestiones principales del proyecto, hay que tener en cuenta un par de consideraciones al momento de llevarlo a cabo: 
- Si el maestro falla, los esclavos deben estar en la capacidad de elegir un nuevo maestro y continuar con el sistema en línea. Para esto, se ha de optar por la implementación de algoritmos de consenso como Paxos o Raft en la elección de un nuevo maestro.
- En caso de que ese fallo se dé, el proxy debe estar en la capacidad de manejar las peticiones entrantes y llevarlas a cabo una vez los nodos estén listos para continuar, así como estar consciente del estado de los nodos.
- Si un esclavo falla, el sistema debe seguir funcionando sin problemas, siempre y cuando haya nodos que puedan sustentar las peticiones.
- En lugar de manejar bases de datos directamente, el manejo de los datos se hará a través de archivos planos, para trabajar en línea con los protocolos de comunicación estudiados recientemente.

### 2. Información General de Diseño de Alto Nivel | Arquitectura | Patrones 

### 3. Descripción del Ambiente de Desarrollo y Técnico

### 4. Descripcion del Ambiente de Ejecución (En Producción)

### 5. Información Relevante Adicional

### 6. Referencias

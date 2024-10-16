# ST0263 | Tópicos Especiales en Telemática

# Estudiantes
- José Manuel Camargo Hoyos | jmcamargoh@eafit.edu.co
- Jose David Valencia Calle | jdvalenci2@eafit.edu.co

# Profesor
- Juan Carlos Montoya Mendoza | jcmontoy@eafit.edu.co

# Proyecto 1 | Implementación de Algoritmo de Consenso para Elección de Líder

## 1. Descripción del Proyecto

En el contexto de los sistemas distribuidos, la coordinación y la consistencia entre los distintos procesos son aspectos fundamentales para el correcto funcionamiento de una aplicación. En este sentido, cuando múltiples procesos colaboran para almacenar, procesar y replicar datos, es necesario que uno de ellos actúe como líder para coordinar las operaciones entre ellos. El líder es responsable de recibir y aplicar las solicitudes de los clientes, garantizar la consistencia de los datos replicados y coordinar a los procesos que actúan como seguidores o followers.

Sin embargo, los sistemas distribuidos están expuestos a fallos de red, caídas de procesos y otros tipos de errores, lo que puede causar la indisponibilidad del líder. En estos casos, la elección de un nuevo líder de manera rápida y segura es fundamental para asegurar la tolerancia a fallos y la disponibilidad continua del sistema. Esta elección debe ser realizada de forma consensuada por todos los procesos restantes, garantizando que solo un proceso asuma el rol de líder en cualquier momento.

Algoritmos de consenso como Raft y Paxos han sido diseñados específicamente para resolver este problema. Estos algoritmos aseguran que, a pesar de fallos en uno o varios procesos, el sistema pueda continuar operando correctamente sin perder datos ni comprometer su consistencia. En sistemas modernos, estos algoritmos son esenciales para garantizar la robustez y disponibilidad de aplicaciones distribuidas, como bases de datos, sistemas de archivos distribuidos y entre otros tipos de servicios.

Este proyecto tiene como objetivo que los estudiantes implementen uno de estos algoritmos o propongan una solución propia para manejar la elección de líder en un entorno distribuido de base de datos, proporcionando una experiencia práctica en el diseño de sistemas tolerantes a fallos.

### 1.1. Entendimiento del Problema

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

### 1.2. Marco Teórico (Paxos VS Raft)
En los sistemas distribuidos, es crucial que varios nodos lleguen a un acuerdo sobre el estado del sistema, incluso si algunos de los nodos fallan. Los algoritmos de consenso son fundamentales para la consistencia, y dos de los más destacados son Paxos y Raft.

#### 1.2.1. Paxos
El algoritmo Paxos fue desarrollado por Leslie Lamport, Robert Shostak y Marshall Pease en 1988, es conocido por ser uno de los más difíciles de entender debido a su complejidad, aunque es un estándar en sistemas de alto rendimiento. Paxos es un algoritmo de consenso distribuido para sistemas descentralizados. Su función es garantizar que un grupo de nodos, que pueden estar ubicados en diferentes lugares y tener diferentes puntos de vista, lleguen a un acuerdo sobre el estado del sistema. Esto es especialmente útil en aplicaciones que requieren tolerancia a fallas, como redes de almacenamiento distribuidas o sistemas de monederos electrónicos. 
- **Objetivo:** Paxos tiene como objetivo lograr consenso en un sistema donde los mensajes pueden perderse o duplicarse, y algunos nodos pueden fallar, pero sin comprometer la consistencia. 
- **Fases Principales:**
    1. **Proposición:** Un nodo (el proponente) propone un valor para ser acordado.
    2. **Promesas:** Los nodos participantes (aceptadores) pueden prometer aceptar propuestas.
    3. **Aceptación:** Si se alcanza un quórum, se acepta la propuesta y el valor se acuerda.

- **Elección del Líder:** Paxos no tiene un líder fijo, pero se pueden hacer optimizaciones, como Multi-Paxos, donde se selecciona un líder para manejar múltiples rondas de consenso, lo que mejora el rendimiento al reducir la comunicación.
- **Ventajas:** Alta tolerancia a fallos y muy utilizado en entornos críticos como Google Chubby.
- **Desventajas:** La implementación de Paxos es notoriamente compleja, y su rendimiento puede verse afectado si hay fallos frecuentes o gran latencia de red.

Es un algoritmo de consenso que cuenta con cierto grado de tolerancia a fallos. Funciona con el modelo de paso de mensajes asincrónicos y con menos de n/2 fallos (pero no con fallos bizantinos), garantizando que se llegará a un acuerdo y a la finalización, si hay un tiempo suficientemente largo sin que ningún proceso reinicie el protocolo. 

#### 1.2.2. Raft
Raft fue diseñado en 2014 por Diego Ongaro y John Ousterhout como una alternativa a Paxos. Es más fácil de entender y también resuelve el problema del consenso distribuido. Es un protocolo de consenso descentralizado utilizado en sistemas distribuidos. El algoritmo es utilizado para asegurar la consistencia y seguridad de los datos en un sistema distribuido y garantizar que solo haya un líder válido en un momento dado. El algoritmo de raft es ampliamente utilizado en sistemas de bases de datos y clusters de servidores. Es conocido por ser escalable, resistente a fallos y fácil de implementar. 
- **Objetivo:** Raft también busca alcanzar el consenso de manera distribuida, pero prioriza la simplicidad y claridad en su diseño.
- **Fases Principales:**
    1. **Elección de Líder:** Se elige un líder a través de elecciones cuando no hay un líder activo o cuando el líder actual falla. Este líder coordina la replicación de logs entre los seguidores.
    2. **Replicación de Logs:** El líder recibe las entradas de logs y las distribuye a los seguidores, garantizando la coherencia.
 
- **Elección del Líder:** En Raft, los nodos periódicamente realizan elecciones para elegir un líder. Si un nodo no recibe mensajes de corazón (heartbeats) del líder actual, puede asumir que el líder ha fallado y solicitar una nueva elección.
- **Ventajas:** Fácil de implementar y de entender, tiene buen rendimiento en condiciones normales y maneja la elección de líder de manera explícita. 
- **Desventajas:** Si bien es más sencillo que Paxos, no tiene el mismo nivel de optimización que Paxos en escenarios de alta carga o fallos constantes.

Es un algoritmo de consenso, con el que se busca lograr consistencia en un grupo de nodos los cuales comparten información. Trabaja seleccionando un nodo líder sobre el que se realizan las solicitudes y coordinación del resto de los nodos para implementarlas. El clúster de nodos de raft, trabaja mientras que exista una mayoría (51%) de nodos en línea. 

Los nodos participantes pueden estar en tres estados:
- **Líder:** Todos los cambios que se realicen en el cluster pasan por él primero.
- **Seguidor:** Nodo pasivo cuya responsabilidad es responder a las peticiones del nodo líder.
- **Candidato:** Nodo que no ha encontrado líder y solicita su elección.

#### 1.2.3. Resumen
La elección de un líder es una parte fundamental en los algoritmos de consenso. El líder es responsable de coordinar las operaciones en el sistema, manteniendo la consistencia entre los nodos. Ambos algoritmos tienen diferentes enfoques para la elección de un líder:
- En Raft, el líder es esencial para la operación, y la pérdida del líder implica una pausa en el procesamiento hasta que se elige uno nuevo.
- En Paxos, el proceso de elección de líder no es tan evidente, pero Multi-Paxos permite que un líder coordine múltiples rondas de consenso, optimizando el rendimiento. 

### 1.3. Requerimientos Funcionales y No Funcionales ALCANZADOS

#### 1.3.1. Requerimientos Funcionales
- El Cliente debe permitir a la aplicación cliente realizar consultas (lecturas) y modificaciones (escrituras) en la base de datos.
- Las operaciones de escritura deben ser manejadas por el Líder, mientras que las de lectura deben ser manejadas por los Seguidores.
- El Proxy debe interceptar las solicitudes del cliente y redirigirlas al proceso adecuado para su manejo (escrituras al Líder, lecturas a los Seguidores).
- El Líder debe coordinar las operaciones de escritura para garantizar la consistencia de los datos.
- Los Seguidores deben replicar las actualizaciones que les envía el líder. 
- Se debe permitir la simulación de fallos del Líder y de uno o más Seguidores.
- El sistema debe seguir funcionando con una mayoría de procesos operativos.
- Los procesos que fallaron deben poder reincorporarse al sistema como Seguidores, sin comprometer la consistencia de los datos.
- El sistema debe manejar de forma independiente las operaciones de manejo de datos (consultas y replicación) y la coordinación de la elección del Líder.
- El sistema debe detectar automáticamente la caída del Líder.
- En caso de falla del Líder, uno de los Seguidores debe asumir el rol de Líder para asegurar la continuidad del servicio.

#### 1.3.2. Requerimientos No Funcionales
- El sistema debe ser altamente disponible, garantizando que los Clientes puedan realizar operaciones incluso si alguno de los procesos (Líder o Seguidores) falla.
- El sistema debe mantener la consistencia de los datos en todos los Seguidores durante las operaciones de escritura y replicación, así como durante la transición de un nuevo Líder.
- El sistema debe gestionar de forma eficiente las operaciones de lectura y escritura, minimizando el tiempo de respuesta para las consultas del Cliente.
- El sistema debe poder escalar con la adición de más Seguidores para manejar un mayor número de consultas de lectura sin comprometer la consistencia y disponibilidad.
- El sistema debe ser capaz de recuperar su funcionamiento normal tras la caída de procesos y la elección de un nuevo Líder, sin pérdida de datos ni de solicitudes en curso.
- El plano de control y el plano de datos deben estar desacoplados, asegurando que la coordinación del liderazgo no interfiera con las operaciones de consulta y modificación de datos.
- El sistema debe permitir la simulación de fallos de forma controlada para verificar el comportamiento de la elección de Líder y la consistencia de datos en condiciones de fallo.
- El proceso de elección de un nuevo Líder debe ser rápido y coordinado, para minimizar el tiempo en que el sistema opera sin un Líder activo.

### 1.4. Requerimientos Funcionales y No Funcionales NO ALCANZADOS

#### 1.4.1. Requerimientos Funcionales
- Durante la simulación de fallos, el sistema debe garantizar que no se pierdan solicitudes de la aplicación Cliente y que la consistencia de los datos se mantenga.

#### 1.4.2. Requerimientos No Funcionales
- Todos los requisitos fueron alcanzados.

## 2. Información General de Diseño de Alto Nivel | Arquitectura | Patrones 

### 2.1. Diseño del Sistema

#### 2.1.1. Componentes del Sistema y sus Acciones
- **Cliente (Proceso 1):**
    - Realiza solicitudes de lectura y escritura a través del proxy.
- **Proxy (Proceso 2):**
    - Redirige las solicitudes de lectura y escritura a los nodos correctos.
    - Mantiene información actualizada sobre el líder y los seguidores para dirigir las peticiones adecuadamente. 
- **Líder (Proceso 3):**
    - Coordina las operaciones de escritura.
    - Administra la replicación de los logs de transacciones hacia los seguidores.
    - Envía heartbeats a los seguidores para mantener la relación de liderazgo.
    - Si falla, los seguidores inician una elección de nuevo líder. 
- **Seguidores (Procesos 4 y 5):**
    - Replican las operaciones de escritura.
    - Responden a las solicitudes de lectura.
    - Participan en el proceso de elección de líder en caso de fallo.

#### 2.1.2. Flujo de Trabajo de Raft
1. **Operación de Escritura**
    - El cliente envía una solicitud de escritura al proxy.
    - El proxy redirige la solicitud al líder.
    - El líder agrega la operación al log de replicación.
    - El líder replica el log a los seguidores y espera confirmaciones (quórum).
    - Una vez confirmado, el líder aplica la operación a la base de datos y envía la respuesta al cliente.
2. **Operación de Lectura**
    - El cliente envía una solicitud de lectura al proxy.
    - El proxy redirige la solicitud a uno de los seguidores.
    - El seguidor responde con los datos solicitados.
3. **Elección de Nuevo Líder**
    - Si el líder falla (falta de heartbeats), los seguidores inician una elección.
    - Cada seguidor solicita votos a los otros nodos.
    - El nodo que obtiene la mayoría de votos se convierte en el nuevo líder.
    - El nuevo líder notifica al proxy para redirigir las futuras solicitudes.

#### 2.1.3. Simulación de Fallos
- **Fallo del líder:** Se simula la desconexión del líder. Los seguidores detectan la ausencia de heartbeats e inician el proceso de elección de un nuevo líder.
- **Fallo de seguidores:** Si un seguidor falla, los otros siguen funcionando mientras haya una mayoría activa.
- **Reincorporación:** Cuando un proceso se reincorpora, actualiza su estado replicando las entradas del log del líder actual (entra como seguidor y se actualiza).

**DIAGRAMA DE FLUJO DEL ALGORITMO RAFT**

![Raft](https://github.com/user-attachments/assets/672361a3-414e-4eba-96b6-34d7ea0cb29a)

### 2.2. Especificaciones de Comunicación
La comunicación en el sistema distribuido se gestionará a través de gRPC, que es eficiente y adecuado para sistemas distribuidos debido a sus características como el uso de HTTP/2 y soporte para múltiples lenguajes.

#### 2.2.1 Roles de los Procesos y la Comunicación
- **Cliente (Proceso 1):** Realiza consultas y modificaciones en la base de datos.
    - **Comunicación con el Proxy:** El cliente se comunica con el proxy para enviar solicitudes de lectura/escritura.
    - **Operación de Lectura:** El proxy redirige las solicitudes de lectura a los seguidores.
    - **Operación de Escritura:** El proxy redirige las solicitudes de escritura al líder.
- **Proxy (Proceso 2):** Actúa como intermediario entre el cliente y los nodos de la base de datos.
    - **Comunicación con Líder y Seguidores** El proxy envía las solicitudes de escritura al líder y las de lectura a los seguidores. Además, recibe notificaciones sobre la elección de un nuevo líder y ajusta las solicitudes en consecuencia.
- **Líder (Proceso 3):** Coordina las operaciones de escritura y la replicación de los datos.
    - **Comunicación con Seguidores:** El líder envía las actualizaciones de los logs de replicación a los seguidores. Este proceso es crítico para mantener la consistencia del sistema.
- **Seguidores (Procesos 4 y 5):** Replican el estado de la base de datos y pueden asumir el rol de líder en caso de fallo.
    - **Comunicación entre Seguidores:** Los seguidores se comunican entre sí para coordinar la elección de un nuevo líder cuando sea necesario.
    - **Heartbeats:** El líder envía regularmente "heartbeats" para informar a los seguidores que sigue activo.

#### 2.2.2. Interfaces de gRPC
- **Cliente a Proxy**
    - Request(message): Envía solicitudes de lectura/escritura. 
    - Response(message): Recibe la respuesta de la base de datos.
- **Proxy a Líder/Seguidores**
    - WriteRequest(data): Solicitud de escritura, enviada al líder.
    - WriteResponse(message): Notificación sobre la escritura realizada. 
    - ReadRequest(key): Solicitud de lectura, enviada a los followers.
    - ReadResponse(data): Respuesta del seguidor con los datos esperados. 
    - LeaderInfo(leaderId): Notifica al proxy sobre el nuevo líder.
- **Líder a Seguidores**
    - AppendEntries(logs): Solicita a los followers replicar entradas de logs.
    - Heartbeat(): Envía heartbeats periódicos a los followers.
- **Entre Seguidores**
    - VoteRequest(candidateId): Solicitud de votos para elegir un nuevo líder.
    - VoteResponse(granted): Respuesta de aceptación o rechazo del voto.

**DIAGRAMA DE COMUNICACIÓN**
![Diagrama_Comunicación](https://github.com/user-attachments/assets/e134319b-f27a-411f-8b72-9e77570c3a0d)

## 3. Descripción del Ambiente de Desarrollo y Técnico

### 3.1. ¿Cómo se compila y se ejecuta?
EL proyecto solo necesita compilar el archivo *"Communication.proto"*, que es el encargado de definir los servicios de mensajería y los mensajes vía gRPC. Este archivo solo será necesario compilarlo si se le hacen cambios al mismo, ubicando a la terminal en la carpeta *"/Project"*:

    $ python3 -m grpc_tools.protoc -I protos --python_out=. --grpc_python_out=. protos/Communication.proto

Para ejecutar el código, hay que ubicarse en la carpeta *"/Project"* y aquí ejecutar los comandos ya conocidos de Python (con los archivos *"Client.py"*, *"Node.py"*, *"Proxy.py"*):

    $ python3 Nombre_del_Archivo.py

### 3.2. Detalles del Desarrollo
- El programa fue desarrollado en una máquina Windows, pero los comandos compartidos en este documento son de máquina Linux, dado que para ver la funcionalidad completa debe hacerse uso de varias máquinas comunicadas entre sí (el código utiliza unos comandos para definir la dirección IP de la máquina, por lo que al ejecutar todo en la misma, se darían unos problemas de comunicación al confundir los nodos entre sí).
- El programa sigue la secuencia en la que el Cliente hace una petición que recepciona el Proxy, y el Proxy la redirige al Nodo más adecuado para resolverla (sea el Leader para escritura y alguno de los Followers para lectura).
- Los Nodos crean un archivo .csv que es el encargado de conservar la data necesaria y allí se hacen todas las operaciones.
- El Proxy hace uso del algoritmo Round-Robin para distribuir las peticiones de lectura entre los nodos Follower.
- La explicación del Algoritmo de Consenso está adjuntada en el vídeo de la sección 4.

### 3.3. Detalles Técnicos
**Lenguajes de Programación:**
- Python 3.12.6: https://www.python.org/downloads/release/python-3126/

**Librerías:**

Estas librerías se descargan haciendo uso de Pip 24.2:
- grpcio 1.66.2
- grpcio-tools 1.66.2
- protobuf 5.28.2

**Instalación de Python:**

    $ sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git
    $ cd /usr/src
    $ sudo wget https://www.python.org/ftp/python/3.12.6/Python-3.12.6.tgz
    $ sudo tar xzf Python-3.12.6.tgz
    $ cd Python-3.12.6
    $ sudo ./configure --enable-optimizations
    $ sudo make altinstall

**Instalación de Librerías:**

    $ sudo apt install -y python3-pip
    $ python3.12 -m ensurepip --upgrade
    $ python3.12 -m pip install --upgrade pip==24.2
    $ python3.12 -m pip install grpcio==1.66.2 grpcio-tools==1.66.2 protobuf==5.28.2
    $ python3.12 -m pip show grpcio grpcio-tools protobuf

### 3.4. ¿Cómo se configuran los parámetros del proyecto?
Al estar ubicado en la carpeta del proyecto, en caso de estar usando una máquina virtual Linux, se le deben entregar permisos a la carpeta para que así pueda escribir y leer los archivos necesarios:

    $ sudo chown ubuntu:ubuntu /usr/Algoritmo-Consenso-Proyecto1/Project/
    $ sudo chmod 775 /usr/Algoritmo-Consenso-Proyecto1/Project/

### 3.5. Guía de Uso para Usuario
1. Descargar el lenguaje de programación y las librerías en las máquinas a utilizar.
2. Para las máquinas destinadas para los Nodos y para el Cliente, definir la dirección IP del Proxy en las secciones donde diga *"localhost"* (solo es necesario cambiar eso, porque a través de la comunicación los Nodos y el Cliente notifican al Proxy sobre sus direcciones IP).
3. Ejecutar *"Proxy.py"* en una máquina.
4. Ejecutar *"Node.py"* en una máquina, donde ese primer nodo se defina como "leader" (línea 172).
5. Ejecutar *"Node.py"* en el número de máquinas que se desee, donde los nodos sean definidos como "follower" (línea 172). Para que el sistema pueda hacer consultas, por lo menos un follower debe estar en línea.
6. Ejecutar *"Client.py"* en una máquina. Al ejecutar este archivo, se le darán instrucciones al usuario de como insertar datos y como consultarlos.

## 4. Información Relevante Adicional
Enlace del video explicativo y la demostración de pruebas: https://youtu.be/RQrZ-UKKK2I

## 5. Referencias
- https://medium.com/@dappsar/algor%C3%ADtmos-de-consenso-raft-y-paxos-b252e51e911a
- https://oa.upm.es/71285/
- https://www.natapuntes.es/algoritmo-paxos/ 
- https://www.researchgate.net/figure/Leader-election-and-opposition-process-in-the-Raft-PLUS-flow-chart_fig3_360971616
- https://www.youtube.com/watch?v=sVROxQdFgs4&ab_channel=NataliaBarra
- https://grpc.io/docs/languages/python/basics/
- https://www.youtube.com/watch?v=WB37L7PjI5k&ab_channel=MissCoding
- https://www.w3schools.com/sql/sql_insert.asp
- https://www.w3schools.com/sql/sql_select.asp
- https://realpython.com/python-sleep/
- https://www.youtube.com/watch?v=9-LECe6YoiQ&ab_channel=AgustinOlivares-Ingenier%C3%ADa
- https://www.youtube.com/watch?v=JSLaNX8j7WY&ab_channel=Genbit
- https://raft.github.io/
- https://aeron.io/docs/cluster-quickstart/raft-consensus/
- https://zeromq.org/get-started/?language=python#
- https://github.com/nikwl/raft-lite/tree/master
- https://github.com/lynix94/pyraft/tree/master/pyraft
- https://www.youtube.com/watch?v=IujMVjKvWP4&ab_channel=CoreDump
- https://protobuf.dev/reference/python/python-generated/#invocation
- https://www.geeksforgeeks.org/python-program-find-ip-address/
- https://www.datacamp.com/es/tutorial/guide-to-python-hashmaps
- https://sparkbyexamples.com/python/create-array-of-strings-in-python/
- https://groups.google.com/g/protobuf/c/15cQIumEVtI?pli=1
- https://webdebe.com/python/55/recorrer-un-array-vector-o-lista-con-python
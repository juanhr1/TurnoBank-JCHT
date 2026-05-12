# Laboratorio: Sistema que aprende a fallar
### Juan Camilo Herrera Torres

# FASE 1 – OBSERVAR (sin modificar código)
- Apagar el servicio de mascotas

<img width="2048" height="1224" alt="unnamed" src="https://github.com/user-attachments/assets/5c584249-3ac7-4588-86bb-79d5952b214d" />

- Hacer varias peticiones al gateway

<img width="2048" height="1221" alt="unnamed (1)" src="https://github.com/user-attachments/assets/c59ddddf-e299-4e74-9461-c3014bf5fae9" />

- Revisar logs

<img width="1728" height="916" alt="fase1" src="https://github.com/user-attachments/assets/76c29ebf-6f1c-4fc6-b50b-ef8e8618f7be" />

Responder:

¿Qué hace el sistema actualmente?

- Cada vez que llega una petición, el gateway intenta conectarse al servicio aunque esté caído, espera el timeout (3 segundos) y devuelve error.

¿Se protege o insiste?

- El sistema inicialmente insiste en conectarse al servicio aunque esté caído, realizando varios intentos consecutivos. Después de alcanzar el límite de fallos configurado, activa el Circuit Breaker y se protege dejando de enviar solicitudes al backend. Sin embargo, el circuito no tiene recuperación automática, por lo que permanece abierto hasta reiniciar el gateway.

# FASE 2 – APLICAR (Extensión del Circuit Breaker)

Aplicando circuit breaker a /usuarios

<img width="443" height="306" alt="Cbreakerusuarios" src="https://github.com/user-attachments/assets/ad780a7b-ebc3-486e-a70c-8ecdfc68dec8" />

Aplicando circuit breaker a /resumen

<img width="1028" height="809" alt="image" src="https://github.com/user-attachments/assets/c99a7798-682a-40ef-b3eb-9a35b55753f0" />

### ¿Cada servicio debe tener su propio contador de fallos?

Sí. Cada servicio debe manejar su propio contador de fallos porque en la arquitectura de microservicios, cada servicio puede fallar de manera independiente sin afectar a otra parte del sistema. En la implementación realizada se utilizaron variables separadas para mascotas y usuarios, permitiendo controlar los errores de cada servicio individualmente.

### ¿El circuito debe abrirse de forma independiente por servicio?

Sí. El circuito debe abrirse de manera independiente para evitar que el fallo de un servicio afecte a los demás. De esta forma, si el servicio de mascotas presenta múltiples errores, únicamente se bloquean las solicitudes relacionadas con mascotas, mientras que usuarios continúa funcionando normalmente y visceversa.

### ¿Qué pasa si falla un servicio pero el otro sigue funcionando?

El sistema continúa respondiendo parcialmente. Por ejemplo, si el servicio de mascotas falla pero el de usuarios sigue activo, el endpoint /usuarios continúa funcionando y /resumen puede seguir mostrando la información de usuarios mientras reporta un error únicamente en la sección de mascotas. Esto mejora la tolerancia a fallos y evita que todo el sistema deje de funcionar por un solo servicio caído.

# FASE 3 – INVESTIGAR (Half-Open)

### ¿Qué significa “half-open”?

El estado “half-open” es una etapa intermedia del Circuit Breaker. Se utiliza después de que el circuito ha permanecido abierto durante un tiempo determinado. Es en este estado el sistema permite realizar una nueva solicitud de prueba al servicio para verificar si ya se recuperó.

### ¿Cuándo se vuelve a intentar una llamada?

La llamada se vuelve a intentar después de un tiempo de espera configurado por el sistema. Este tiempo evita realizar intentos constantes mientras el servicio continúa caído.

### ¿Qué pasa si el servicio vuelve a fallar?

Si el servicio vuelve a fallar durante el estado half-open, el circuito se abre nuevamente y se bloquean otra vez las solicitudes al servicio. Si la petición funciona correctamente, el circuito se cierra y el sistema vuelve a operar normalmente.

# FASE 4 – IMPLEMENTAR (Recuperación)

Se implementa tiempo de espera definido y validaciones por mediante if y cambios en los endpoints

## Para el endpoint de mascotas:

Importar tiempo

<img width="1019" height="577" alt="Captura de pantalla 2026-05-10 220230" src="https://github.com/user-attachments/assets/de987bc8-ba65-43bd-af91-f0335c2ed2e4" />

Se importan más variables globales necesarias

<img width="524" height="54" alt="Captura de pantalla 2026-05-10 220508" src="https://github.com/user-attachments/assets/c7507093-1b3a-483d-892a-940901f84d2a" />

Se hace la validación inicial del endpoint /mascotas. Cuando el circuito se encuentra abierto con un circuito_abierto = True, el sistema verifica cuánto tiempo ha pasado desde que ocurrió la apertura utilizando time.time() y la variable tiempo_apertura_mascotas.

Si todavía no se cumple el tiempo de espera configurado, el gateway bloquea inmediatamente la solicitud y responde con el mensaje "Circuito abierto" evitando seguir intentando conexiones innecesarias al servicio caído.

<img width="499" height="158" alt="Captura de pantalla 2026-05-10 223302" src="https://github.com/user-attachments/assets/8c1ee1aa-ec13-4a1b-9744-e5cede05d5cd" />

Aquí está un try, donde el gateway intenta conectarse nuevamente al servicio de mascotas.
Donde si la petición funciona correctamente:

El contador de fallos se reinicia, el circuito vuelve al estado CLOSED y el sistema imprime "Circuito cerrado" indicando que el servicio se recuperó exitosamente.

Esta es la creación del proceso de recuperación automática después del estado HALF-OPEN.

<img width="432" height="145" alt="Captura de pantalla 2026-05-10 223329" src="https://github.com/user-attachments/assets/ff89725d-4761-4a25-bd91-1bbe99aca63f" />

Vemos aquí el bloque except, seguido del try, encargado de manejar los errores cuando el servicio de mascotas falla.

El sistema incrementa el contador de fallos y verifica si el circuito se encontraba en estado HALF-OPEN.

Entramos al manejo de errores y reapertura del circuito donde: Si la prueba de recuperación falla:

El circuito vuelve al estado OPEN, se guarda nuevamente el tiempo de apertura y se imprime el mensaje "HALF-OPEN falló por tanto se abre el circuito".

Además, cuando el número de fallos alcanza el límite configurado, el Circuit Breaker abre nuevamente el circuito para proteger el sistema y evitar seguir enviando solicitudes al servicio caído.

<img width="426" height="206" alt="image" src="https://github.com/user-attachments/assets/30cfc4c6-3120-4492-8dbc-66826f068a1c" />

Pruebas funcionales

<img width="526" height="239" alt="Captura de pantalla 2026-05-10 222206" src="https://github.com/user-attachments/assets/f2aa66f9-3096-4d38-8aff-fc049677e305" />

## Para el endpoint de usuarios:

En esta parte se implementaron nuevas variables globales para el endpoint /usuarios, permitiendo manejar de forma independiente el Circuit Breaker del servicio de usuarios.

Se agregó un estado inicial llamado CLOSED, el cual representa el funcionamiento normal del servicio, y una variable encargada de almacenar el tiempo en el que el circuito se abre. Estas variables fueron necesarias para poder implementar posteriormente la lógica de recuperación automática mediante el estado HALF-OPEN.

<img width="198" height="38" alt="Captura de pantalla 2026-05-11 211735" src="https://github.com/user-attachments/assets/27c987eb-de8b-4e44-8048-61f1b54bf675" />

Importar más variables globales necesarias

<img width="518" height="49" alt="Captura de pantalla 2026-05-11 211816" src="https://github.com/user-attachments/assets/72df90f6-8a26-4f0c-b342-adcef784b03f" />

En esta sección se implementó la lógica encargada de verificar si el circuito del servicio de usuarios se encuentra abierto.

También se agregó un tiempo de espera utilizando time.time(), permitiendo que el sistema pueda calcular cuándo debe volver a intentar una conexión al servicio.

Cuando el tiempo configurado se cumple, el circuito cambia temporalmente al estado HALF-OPEN y el gateway permite realizar una nueva petición de prueba para comprobar si el servicio ya se recuperó.

Si el tiempo aún no se cumple, el sistema mantiene el circuito abierto y responde inmediatamente con un error controlado.

<img width="514" height="166" alt="Captura de pantalla 2026-05-11 213917" src="https://github.com/user-attachments/assets/e3346007-d478-4378-94e6-8486c8144727" />

En esta parte se implementó la lógica principal de recuperación automática y manejo de errores para el servicio de usuarios.

Dentro del bloque try, se configuró el sistema para que, cuando la petición al servicio funciona correctamente, el contador de fallos vuelva a cero y el circuito regrese nuevamente al estado CLOSED, indicando que el servicio ya se recuperó.

Por otro lado, dentro del bloque except, se implementó el incremento del contador de fallos y la validación del estado HALF-OPEN.

Si la prueba realizada en HALF-OPEN falla, el sistema vuelve automáticamente al estado OPEN, guarda nuevamente el tiempo de apertura y bloquea temporalmente las solicitudes al servicio para proteger el gateway de intentos innecesarios.

<img width="438" height="255" alt="Captura de pantalla 2026-05-11 212304" src="https://github.com/user-attachments/assets/5576de79-30f4-4e58-bcdb-12b51e53bd93" />

<img width="362" height="82" alt="Captura de pantalla 2026-05-11 212455" src="https://github.com/user-attachments/assets/033e55f9-7277-49a4-afa8-c00698d815e8" />

Pruebas funcionales

<img width="472" height="185" alt="Captura de pantalla 2026-05-11 213002" src="https://github.com/user-attachments/assets/91b9ec12-6dc1-47df-b809-cf7e0040ec6c" />

# FASE 5 – VALIDAR

## Escenario 1 – Servicios funcionando

Se realizaron peticiones a los endpoints /mascotas y /usuarios con ambos servicios activos. El sistema respondió correctamente y los circuitos permanecieron en estado CLOSED.

<img width="949" height="539" alt="image" src="https://github.com/user-attachments/assets/25dd74be-0f98-45e5-859a-1a9863105a04" />

<img width="374" height="281" alt="image" src="https://github.com/user-attachments/assets/d5ca8f12-38bc-43a5-bb59-dfa603a01e83" />

<img width="374" height="206" alt="image" src="https://github.com/user-attachments/assets/7eb84004-06a6-4b53-8764-54732f9f1b58" />

<img width="481" height="28" alt="image" src="https://github.com/user-attachments/assets/5921f5e1-0478-4b0a-a350-3eb0b660aefd" />

<img width="479" height="43" alt="image" src="https://github.com/user-attachments/assets/c183a579-530f-47e4-99d1-3d9858f66572" />

## Escenario 2 – Servicio caído

Se apagó cada servicio individualmente para verificar el comportamiento del Circuit Breaker.

<img width="322" height="319" alt="image" src="https://github.com/user-attachments/assets/70bc3814-183b-4413-b5c7-59aee7515c3f" />

Después de varios fallos consecutivos:

El circuito de mascotas pasó a OPEN

<img width="485" height="156" alt="image" src="https://github.com/user-attachments/assets/807faf00-16eb-4537-ae58-ef405a6e2b5e" />

Posteriormente se realizó la misma validación para usuarios.

<img width="479" height="164" alt="image" src="https://github.com/user-attachments/assets/32782841-f76b-4ab4-858d-deb88e189461" />

Una vez abierto el circuito, el gateway dejó de enviar solicitudes al servicio caído y respondió inmediatamente con mensajes de error controlados, evitando tiempos de espera innecesarios.

## Escenario 4 – Recuperación del servicio

Después del tiempo de espera configurado, ambos servicios pasaron al estado HALF-OPEN y realizaron nuevas pruebas de conexión.

Mascotas

<img width="474" height="201" alt="image" src="https://github.com/user-attachments/assets/4d794a0f-663d-4228-84af-1085ea2eebb0" />

Usuarios

<img width="481" height="183" alt="image" src="https://github.com/user-attachments/assets/154691ca-8d85-4d17-87ce-21a191b2560e" />

Cuando los servicios volvieron a estar disponibles:

los circuitos regresaron automáticamente al estado CLOSED,
y el sistema volvió a responder normalmente.

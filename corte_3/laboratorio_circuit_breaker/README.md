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

Importar más variables globales necesarias

<img width="524" height="54" alt="Captura de pantalla 2026-05-10 220508" src="https://github.com/user-attachments/assets/c7507093-1b3a-483d-892a-940901f84d2a" />

<img width="499" height="158" alt="Captura de pantalla 2026-05-10 223302" src="https://github.com/user-attachments/assets/8c1ee1aa-ec13-4a1b-9744-e5cede05d5cd" />

<img width="432" height="145" alt="Captura de pantalla 2026-05-10 223329" src="https://github.com/user-attachments/assets/ff89725d-4761-4a25-bd91-1bbe99aca63f" />

<img width="426" height="206" alt="image" src="https://github.com/user-attachments/assets/30cfc4c6-3120-4492-8dbc-66826f068a1c" />

Pruebas funcionales

<img width="526" height="239" alt="Captura de pantalla 2026-05-10 222206" src="https://github.com/user-attachments/assets/f2aa66f9-3096-4d38-8aff-fc049677e305" />

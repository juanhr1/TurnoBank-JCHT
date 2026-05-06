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



### ¿Cuándo se vuelve a intentar una llamada?



### ¿Qué pasa si el servicio vuelve a fallar?


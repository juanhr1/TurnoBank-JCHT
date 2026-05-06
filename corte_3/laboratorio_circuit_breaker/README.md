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


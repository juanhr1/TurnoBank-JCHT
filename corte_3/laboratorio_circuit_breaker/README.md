# Laboratorio: Sistema que aprende a fallar
## Juan Camilo Herrera Torres

# FASE 1 – OBSERVAR (sin modificar código)
- Apagar el servicio de mascotas

- Hacer varias peticiones al gateway

- Revisar logs

### Evidencias en carpeta evidencias/fase1.png ✅

Responder:

¿Qué hace el sistema actualmente?

- Cada vez que llega una petición, el gateway intenta conectarse al servicio aunque esté caído, espera el timeout (3 segundos) y devuelve error.

¿Se protege o insiste?

- No tiene memoria de fallos anteriores, cada request sufre el timeout completo. 


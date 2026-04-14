# Sistema de Gestión de Turnos basado en Microservicios

## Descripción del proyecto

El presente proyecto implementa un sistema de gestión de turnos utilizando una arquitectura de microservicios, en la cual cada componente del sistema funciona de manera independiente y se comunica con los demás a través de protocolos de red.

El sistema permite el registro de usuarios, la asignación de turnos y el envío de notificaciones. Cada una de estas funcionalidades está desacoplada en servicios independientes, lo que facilita la escalabilidad, mantenibilidad y despliegue del sistema.

Se implementa una comunicación síncrona entre microservicios mediante el uso de HTTP, donde cada servicio realiza solicitudes a otros y espera una respuesta para continuar con su ejecución. Adicionalmente, se utiliza una base de datos relacional (PostgreSQL) para garantizar la persistencia de la información, junto con volúmenes en Docker para evitar la pérdida de datos.

El sistema está contenerizado mediante Docker y orquestado con Docker Compose, lo que permite su ejecución en diferentes entornos de manera consistente.

## Instrucciones para la ejecución

1. Clonar el repositorio:

    git clone <URL_DEL_REPOSITORIO>
    cd gestor-turnos-py

2. Crear el archivo de configuración `.env` en la raíz del proyecto:

    env
        DB_HOST=db
        DB_NAME=turnos_db
        DB_USER=admin
        DB_PASSWORD=admin

3. Construir y ejecutar los contenedores:

    docker-compose up --build


4. Verificar el funcionamiento de los servicios en:

* http://localhost:5001/users
* http://localhost:5002/turns
* http://localhost:5003/notifications

## Descripción de endpoints

### Servicio de Usuarios

* **POST /users**
  Permite registrar un nuevo usuario en el sistema.

json
    {
    "identificacion": "123",
    "telefono": "3001234567"
    }


* **GET /users**
  Retorna la lista de usuarios registrados.

### Servicio de Turnos

* **POST /turn**
  Permite crear un turno para un usuario existente. Este endpoint realiza una comunicación síncrona con el servicio de usuarios para validar la existencia del usuario antes de registrar el turno.

json
    {
    "identificacion": "123"
    }

* **GET /turns**
  Permite consultar los turnos almacenados en la base de datos.


### Servicio de Notificaciones

* **POST /notify**
  Recibe solicitudes desde el servicio de turnos para simular el envío de notificaciones. Este servicio representa un comportamiento desacoplado dentro del sistema.

## Consideraciones técnicas

* Arquitectura basada en microservicios.
* Comunicación síncrona mediante HTTP.
* Persistencia de datos con PostgreSQL.
* Uso de volúmenes en Docker para almacenamiento persistente.
* Configuración mediante variables de entorno.
* Contenerización con Docker y orquestación con Docker Compose.

## Conclusión

El sistema desarrollado evidencia la aplicación de conceptos fundamentales de sistemas distribuidos, tales como la separación de responsabilidades, comunicación entre servicios, persistencia de datos y despliegue en contenedores. Esta arquitectura permite la escalabilidad del sistema y facilita su mantenimiento y evolución.

# ApiTaskManager

Desarrollo de una API RESTful para un sistema de gestión de tareas.

---

## Tecnologías Usadas

- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework para construir APIs rápidas y modernas con Python.
- **[SQLModel](https://sqlmodel.tiangolo.com/)**: Biblioteca para trabajar con bases de datos SQL y modelos Pydantic.
- **[PostgreSQL](https://www.postgresql.org/)**: Base de datos relacional robusta y escalable.
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI para ejecutar la aplicación FastAPI.
- **[Python-JOSE](https://python-jose.readthedocs.io/)**: Biblioteca para manejar JWT.
- **[Bcrypt](https://pypi.org/project/bcrypt/)**: Biblioteca para hashear y verificar contraseñas.
- **[Redis](https://redis.io/docs/latest/develop/clients/redis-py/)**: Almacén de datos en memoria para gestionar tokens JWT revocados.

## Estructura de Carpetas

```
app/
├── auth/
│   ├── dependencies.py   # Dependencias para autenticación y roles
│   ├── hashing.py        # Funciones para hashear y verificar contraseñas
│   └── jwt.py            # Funciones para manejo de JWT
├── crud/
│   ├── task_status.py    # Operaciones CRUD para TaskStatus
│   ├── task.py           # Operaciones CRUD para Task
│   ├── todo_list.py      # Operaciones CRUD para TodoList
│   └── user.py           # Operaciones CRUD para User
├── db/
│   ├── database.py       # Configuración de la base de datos postgres
│   └── redis.py          # Configuración de la base de datos redis
├── models/
│   ├── task_status.py    # Modelo TaskStatus con SQLModel
│   ├── task.py           # Modelo Task con SQLModel
│   ├── todo_list.py      # Modelo TodoList con SQLModel
│   └── user.py           # Modelo User con SQLModel
├── routes/
│   ├── auth.py           # Endpoints relacionados con autenticación
│   ├── task_status.py    # Endpoints relacionados con TaskStatus
│   ├── task.py           # Endpoints relacionados con Task
│   ├── todo_list.py      # Endpoints relacionados con TodoList
│   └── user.py           # Endpoints relacionados con User
├── .env                  # Variables de entorno para configuración local y Docker
├── .gitignore            # Lista de archivos y carpetas que Git debe ignorar
├── docker-compose.yml    # Archivo Docker Compose para orquestar los servicios
├── Dockerfile            # Archivo Docker para construir la imagen de la aplicación
├── logging.conf          # Configuración del sistema de logging de la aplicación
├── main.py               # Punto de entrada principal de la aplicación
├── seeder.py             # Script para poblar la base de datos con datos iniciales
├── requirements.txt      # Lista de dependencias necesarias para la aplicación
└── README.md             # Documentación del proyecto
```

## Configuración del Proyecto

### Variables de Entorno

El proyecto utiliza un único archivo `.env` para configuraciones tanto locales como en Docker.

Ejemplo de `.env`:

```properties
# ========================
# DATABASE CONFIGURATION
# ========================
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
DB_NAME=mydatabase

# ========================
# REDIS CONFIGURATION
# ========================
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# ========================
# JWT CONFIGURATION
# ========================
SECRET_KEY=your_secret_key_here
REFRESH_SECRET_KEY=your_refresh_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
REVOKED_TOKENS_FILE=/app/revoked_tokens.json
```

### Cómo Ejecutar el Proyecto

#### 1. **Ejecutar Localmente**

1. **Crear un entorno virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la base de datos**:
   Asegúrate de que PostgreSQL esté instalado y ejecutándose. Crea la base de datos especificada en el archivo `.env`.

4. **Ejecutar el seeder**:
   Si deseas poblar la base de datos con datos iniciales, ejecuta:

   ```bash
   python seeder.py
   ```

5. **Ejecutar la aplicación**:

   ```bash
   python main.py
   ```

6. **Abrir la documentación interactiva**:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

#### 2. **Ejecución con Docker**

### Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Pasos para Ejecutar

1. **Construir y levantar los servicios**:

   ```bash
   docker-compose up --build -d
   ```

2. **Acceder a la aplicación**:

   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

3. **Parar los servicios**:
   ```bash
   docker-compose down
   ```

### Cómo Ejecutar el Seeder

Si deseas poblar la base de datos con datos iniciales, puedes ejecutar el script `seeder.py` de las siguientes maneras:

#### Localmente

1. Asegúrate de que la base de datos esté configurada y en ejecución.
2. Ejecuta el siguiente comando:
   ```bash
   python seeder.py
   ```

#### Con Docker

1. Asegúrate de que los servicios estén levantados con Docker Compose:

   ```bash
   docker-compose up -d
   ```

2. Ejecuta el seeder dentro del contenedor de la aplicación:
   ```bash
   docker-compose exec app python seeder.py
   ```

Esto poblará la base de datos con los datos iniciales definidos en el script `seeder.py`.

### Notas

- Los datos de la base de datos se almacenan en un volumen llamado `postgres_data`, por lo que no se perderán al reiniciar los contenedores.
- Puedes modificar las variables de entorno en el archivo `.env` según sea necesario.

## Funcionalidades

### Sistema de Roles y Autenticación con JWT

Este proyecto incluye un sistema de autenticación basado en JWT (JSON Web Tokens) y roles (`admin`, `user` y `viewer`). A continuación, se explica cómo usarlo:

#### Roles

1. **Admin**

   - Permisos: Acceso completo a todos los endpoints (`GET`, `POST`, `PUT`, `DELETE`).

2. **User**

   - Permisos: Acceso restringido a endpoints que devuelvan datos del mismo usuario (`GET`, `POST`, `PUT`, `DELETE`) en `/users`, `/todo_lists` y `/tasks`. Acceso `GET` de `/status`.

3. **Viewer**
   - Permisos: Acceso restringido sólo a endpoints de lectura (`GET`) de las tablas `todo_lists`y `tasks`
     - Podrá hacer todas las operaciones(`GET`, `POST`, `PUT`, `DELETE`) sobre los endpoints del propio usuario en `/users`.

#### Protección de Rutas

- Todas las rutas `GET`, `POST`, `PUT` y `DELETE` de los módulos `task_status`, `task`, `todo_list` y `user` están protegidas con JWT. Solo los usuarios con rol de `admin`, `user` o `viewer` pueden acceder a estas rutas.

#### Registro de Usuarios

Para registrar un nuevo usuario, utiliza el endpoint `/api/auth/register`. Este endpoint espera un objeto JSON con los campos `username`, `email`, `password` y opcionalmente `role` (por defecto es `user`).

#### Inicio de Sesión

Para iniciar sesión y obtener un token JWT, utiliza el endpoint `/api/auth/login`. Este endpoint espera los campos `username` y `password`.

- Tiempo de expiración del token:
  - **Admin**: 60 minutos.
  - **User**: 30 minutos.
  - **Viewer**: 15 minutos.

#### Renovación de Tokens

El endpoint `/api/auth/refresh` permite obtener un nuevo `access_token` utilizando un `refresh_token` válido.

#### Cierre de Sesión

El endpoint `/api/auth/logout` permite cerrar sesión y revocar el token de acceso. Los tokens revocados se almacenan en Redis y adicionalmente en un archivo llamado `revoked_tokens.txt` para evitar su reutilización. Este archivo se encuentra en la raíz del proyecto y se carga al iniciar la aplicación.

---

### Recuperación de Contraseña

El proyecto incluye un flujo para la recuperación de contraseñas:

1. **Solicitar recuperación**:

   - Endpoint: `/api/auth/forgot-password`
   - Método: `POST`
   - Envía un token de recuperación al cliente.
   - Tiempo de expiración del token: 15 minutos.

2. **Restablecer contraseña**:
   - Endpoint: `/api/auth/reset-password`
   - Método: `POST`
   - Permite al usuario establecer una nueva contraseña utilizando el token de recuperación.

---

### Operaciones CRUD

### **Listas de Tareas (`/todo_lists`)**

- `admin` tiene permisos completos
- `user` tiene permisos completos sobre sus propias listas
- `viewer` tiene permisos GET de cualquier lista

---

### **Tareas (`/tasks`)**

- `admin` tiene permisos completos
- `user` tiene permisos completos sobre sus propias tareas
- `viewer` tiene permisos GET de cualquier tarea

---

### **Estados de Tareas (`/task_status`)**

- `admin` tiene permisos completos
- `user` tiene permisos GET de los estados
- `viewer` no tiene permisos

---

### **Users (`/users`)**

- `admin` tiene permisos completos
- `user` tiene permisos completos sobre su propio usuario
- `viewer` tiene permisos GET de cualquier usuario

---

### Notas Adicionales

- **Excepciones**:
  - Manejo global de excepciones para errores inesperados.

---

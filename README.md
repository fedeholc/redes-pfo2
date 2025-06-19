# Programación sobre Redes - 3°B

# PFO2 - Sistema de Gestión de Tareas con API y Base de Datos

**Estudiante: Federico Holc**

## Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/fedeholc/redes-pfo2.git
cd redes-pfo2
```

2. **Crear y activar un entorno virtual (recomendado):**

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

3. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

## Ejecución

### Iniciar el servidor

```bash
python servidor.py
```

El servidor estará disponible en: `http://localhost:5000`

### Usar el cliente de consola

En otra terminal:

```bash
python cliente.py
```

## API Endpoints

### Autenticación

#### Registrar Usuario

- **URL:** `POST /registro`
- **Body:**

```json
{
  "usuario": "mi_usuario",
  "contraseña": "mi_contraseña"
}
```

- **Respuesta exitosa (201):**

```json
{
  "mensaje": "Usuario registrado exitosamente",
  "usuario_id": 1,
  "usuario": "mi_usuario"
}
```

#### Iniciar Sesión

- **URL:** `POST /login`
- **Body:**

```json
{
  "usuario": "mi_usuario",
  "contraseña": "mi_contraseña"
}
```

- **Respuesta exitosa (200):**

```json
{
  "mensaje": "Inicio de sesión exitoso",
  "usuario": "mi_usuario",
  "usuario_id": 1
}
```

#### Cerrar Sesión

- **URL:** `POST /logout`
- **Respuesta exitosa (200):**

```json
{
  "mensaje": "Sesión cerrada exitosamente"
}
```

### Gestión de Tareas

**Nota:** Todos los endpoints de tareas requieren autenticación previa.

#### Obtener Todas las Tareas

- **URL:** `GET /api/tareas`
- **Respuesta exitosa (200):**

```json
{
  "tareas": [
    {
      "id": 1,
      "titulo": "Mi primera tarea",
      "descripcion": "Descripción de la tarea",
      "completada": false,
      "fecha_creacion": "2025-06-19 10:30:00"
    }
  ],
  "total": 1
}
```

#### Crear Nueva Tarea

- **URL:** `POST /api/tareas`
- **Body:**

```json
{
  "titulo": "Nueva tarea",
  "descripcion": "Descripción opcional"
}
```

- **Respuesta exitosa (201):**

```json
{
  "mensaje": "Tarea creada exitosamente",
  "tarea_id": 2,
  "titulo": "Nueva tarea",
  "descripcion": "Descripción opcional"
}
```

#### Actualizar Tarea

- **URL:** `PUT /api/tareas/<id>`
- **Body (campos opcionales):**

```json
{
  "titulo": "Título actualizado",
  "descripcion": "Nueva descripción",
  "completada": true
}
```

- **Respuesta exitosa (200):**

```json
{
  "mensaje": "Tarea actualizada exitosamente"
}
```

#### Eliminar Tarea

- **URL:** `DELETE /api/tareas/<id>`
- **Respuesta exitosa (200):**

```json
{
  "mensaje": "Tarea eliminada exitosamente"
}
```

### Páginas Web

#### Página de Inicio

- **URL:** `GET /`
- Muestra la página principal con información sobre la API

#### Página de Tareas

- **URL:** `GET /tareas`
- Página de bienvenida para usuarios autenticados
- **Requiere:** Sesión activa

## Tests

```bash
# Ejecutar todas las pruebas con curl y generar documentación
./test_curl.sh

# Suite completa de pruebas automatizadas
python test_completo.py

# Ver resultados detallados
ls api-tests/
```

#Resumen de Pruebas API - Sistema de Gestión de Tareas

**Fecha:** 2025-06-19 08:26:12
**URL Base:** http://localhost:5000
**Total de pruebas:** 24

## Lista de Pruebas Ejecutadas

- **01_home:** Home
- **02_registro_valido:** Registro Valido
- **03_registro_invalido:** Registro Invalido
- **04_registro_sin_datos:** Registro Sin Datos
- **05_login_valido:** Login Valido
- **06_login_invalido:** Login Invalido
- **07_tareas_sin_auth:** Tareas Sin Auth
- **08_obtener_tareas:** Obtener Tareas
- **09_crear_tarea:** Crear Tarea
- **10_crear_tarea_sin_titulo:** Crear Tarea Sin Titulo
- **11_crear_segunda_tarea:** Crear Segunda Tarea
- **12_actualizar_tarea:** Actualizar Tarea
- **13_actualizar_tarea_inexistente:** Actualizar Tarea Inexistente
- **14_obtener_tareas_actualizadas:** Obtener Tareas Actualizadas
- **15_eliminar_tarea:** Eliminar Tarea
- **16_eliminar_tarea_inexistente:** Eliminar Tarea Inexistente
- **17_pagina_tareas_auth:** Pagina Tareas Auth
- **18_pagina_tareas_sin_auth:** Pagina Tareas Sin Auth
- **19_logout:** Logout
- **20_tareas_despues_logout:** Tareas Despues Logout
- **21_endpoint_inexistente:** Endpoint Inexistente
- **22_metodo_no_permitido:** Metodo No Permitido
- **23_json_malformado:** Json Malformado
- **24_usuario_duplicado:** Usuario Duplicado

## 🔍 Cómo usar estos resultados

1. Cada archivo `.txt` contiene:
   - Descripción de la prueba
   - Comando curl utilizado
   - Respuesta completa del servidor
   - Código de estado HTTP
   - Tiempo de respuesta

2. Los archivos están numerados en orden de ejecución
3. Puedes usar estos ejemplos para:
   - Documentar la API
   - Crear tutoriales
   - Verificar el comportamiento esperado
   - Depurar problemas

## Comandos curl de ejemplo

### Registro de usuario
```bash
curl -X POST http://localhost:5000/registro \
  -H 'Content-Type: application/json' \
  -d '{"usuario": "mi_usuario", "contraseña": "mi_password"}'
```

### Login y guardar cookies
```bash
curl -X POST http://localhost:5000/login \
  -H 'Content-Type: application/json' \
  -d '{"usuario": "mi_usuario", "contraseña": "mi_password"}' \
  -c cookies.txt
```

### Crear tarea
```bash
curl -X POST http://localhost:5000/api/tareas \
  -H 'Content-Type: application/json' \
  -d '{"titulo": "Mi tarea", "descripcion": "Descripción"}' \
  -b cookies.txt
```

### Obtener tareas
```bash
curl http://localhost:5000/api/tareas -b cookies.txt
```

---

**Generado automáticamente por:** test_curl.sh

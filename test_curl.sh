#!/bin/bash

# Programación sobre Redes - 3°B
# PFO2 - Sistema de Gestión de Tareas con API y Base de Datos
# Estudiante: Federico Holc
# Script de pruebas con curl 

echo "PRUEBAS DE API CON CURL - SISTEMA DE GESTIÓN DE TAREAS"
echo "=========================================================="
echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Configuración
BASE_URL="http://localhost:5000"
OUTPUT_DIR="api-tests"
COOKIE_FILE="test_cookies.txt"

# Crear directorio de salida
mkdir -p "$OUTPUT_DIR"

# Función para ejecutar curl y guardar salida
run_curl_test() {
    local test_name="$1"
    local description="$2"
    local curl_command="$3"
    local output_file="$OUTPUT_DIR/${test_name}.txt"
    
    echo "Test: $test_name"
    echo "$description"
    echo "Comando: $curl_command"
    echo ""
    
    # Guardar información del test
    {
        echo "=== $test_name ==="
        echo "Descripción: $description"
        echo "Comando: $curl_command"
        echo "Fecha: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        echo "--- RESPUESTA ---"
    } > "$output_file"
    
    # Ejecutar comando y capturar salida
    eval "$curl_command" >> "$output_file" 2>&1
    local exit_code=$?
    
    echo "" >> "$output_file"
    echo "--- STATUS ---" >> "$output_file"
    echo "Exit code: $exit_code" >> "$output_file"
    
    if [ $exit_code -eq 0 ]; then
        echo "OK Completado"
    else
        echo "Error (código: $exit_code)"
    fi
    echo ""
    
    return $exit_code
}

# Verificar que el servidor esté funcionando
echo "Verificando conectividad con el servidor..."
if ! curl -s "$BASE_URL" > /dev/null; then
    echo "Error: No se puede conectar al servidor en $BASE_URL"
    echo "Asegúrarse de ejecutar: python servidor.py"
    exit 1
fi
echo "Servidor funcionando correctamente"
echo ""

# Limpiar archivos de cookies previos
rm -f "$COOKIE_FILE"

echo "INICIANDO PRUEBAS DE ENDPOINTS"
echo "================================="
echo ""

# Test 1: Página de inicio
run_curl_test "01_home" \
    "Obtener página de inicio del sistema" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' '$BASE_URL/'"

# Test 2: Registro de usuario válido
run_curl_test "02_registro_valido" \
    "Registrar un nuevo usuario con datos válidos" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X POST '$BASE_URL/registro' \
    -H 'Content-Type: application/json' \
    -d '{\"usuario\": \"test_user_$(date +%s)\", \"contraseña\": \"test123456\"}'"

# Test 3: Registro con datos inválidos
run_curl_test "03_registro_invalido" \
    "Intentar registrar usuario con contraseña muy corta" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X POST '$BASE_URL/registro' \
    -H 'Content-Type: application/json' \
    -d '{\"usuario\": \"user_invalid\", \"contraseña\": \"123\"}'"

# Test 4: Registro sin datos
run_curl_test "04_registro_sin_datos" \
    "Intentar registrar usuario sin proporcionar datos" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X POST '$BASE_URL/registro' \
    -H 'Content-Type: application/json' \
    -d '{}'"

# Test 5: Login con credenciales correctas
TIMESTAMP=$(date +%s)
USER_NAME="demo_user_$TIMESTAMP"

# Primero registrar el usuario para el login
curl -s -X POST "$BASE_URL/registro" \
    -H 'Content-Type: application/json' \
    -d "{\"usuario\": \"$USER_NAME\", \"contraseña\": \"demo123456\"}" > /dev/null

run_curl_test "05_login_valido" \
    "Iniciar sesión con credenciales válidas y guardar cookies" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X POST '$BASE_URL/login' \
    -H 'Content-Type: application/json' \
    -d '{\"usuario\": \"$USER_NAME\", \"contraseña\": \"demo123456\"}' \
    -c '$COOKIE_FILE'"

# Test 6: Login con credenciales incorrectas
run_curl_test "06_login_invalido" \
    "Intentar login con contraseña incorrecta" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X POST '$BASE_URL/login' \
    -H 'Content-Type: application/json' \
    -d '{\"usuario\": \"$USER_NAME\", \"contraseña\": \"password_incorrecta\"}'"

# Test 7: Acceso a tareas sin autenticación
run_curl_test "07_tareas_sin_auth" \
    "Intentar acceder a tareas sin estar autenticado" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    '$BASE_URL/api/tareas'"

# Test 8: Obtener tareas (con autenticación)
run_curl_test "08_obtener_tareas" \
    "Obtener lista de tareas del usuario autenticado" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    '$BASE_URL/api/tareas' \
    -b '$COOKIE_FILE'"

# Test 9: Crear nueva tarea
run_curl_test "09_crear_tarea" \
    "Crear una nueva tarea con título y descripción" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X POST '$BASE_URL/api/tareas' \
    -H 'Content-Type: application/json' \
    -d '{\"titulo\": \"Tarea de prueba con curl\", \"descripcion\": \"Esta tarea fue creada usando curl para probar la API\"}' \
    -b '$COOKIE_FILE'"

# Test 10: Crear tarea sin título
run_curl_test "10_crear_tarea_sin_titulo" \
    "Intentar crear tarea sin proporcionar título" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X POST '$BASE_URL/api/tareas' \
    -H 'Content-Type: application/json' \
    -d '{\"descripcion\": \"Tarea sin título\"}' \
    -b '$COOKIE_FILE'"

# Test 11: Crear otra tarea para tests de actualización
run_curl_test "11_crear_segunda_tarea" \
    "Crear segunda tarea para pruebas de actualización" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X POST '$BASE_URL/api/tareas' \
    -H 'Content-Type: application/json' \
    -d '{\"titulo\": \"Tarea para actualizar\", \"descripcion\": \"Esta tarea será actualizada en las pruebas\"}' \
    -b '$COOKIE_FILE'"

# Test 12: Actualizar tarea (marcar como completada)
run_curl_test "12_actualizar_tarea" \
    "Actualizar tarea - marcar como completada y cambiar descripción" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X PUT '$BASE_URL/api/tareas/1' \
    -H 'Content-Type: application/json' \
    -d '{\"completada\": true, \"descripcion\": \"Tarea completada usando curl\"}' \
    -b '$COOKIE_FILE'"

# Test 13: Actualizar tarea inexistente
run_curl_test "13_actualizar_tarea_inexistente" \
    "Intentar actualizar una tarea que no existe" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X PUT '$BASE_URL/api/tareas/999' \
    -H 'Content-Type: application/json' \
    -d '{\"completada\": true}' \
    -b '$COOKIE_FILE'"

# Test 14: Obtener tareas después de actualizaciones
run_curl_test "14_obtener_tareas_actualizadas" \
    "Obtener lista actualizada de tareas después de los cambios" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    '$BASE_URL/api/tareas' \
    -b '$COOKIE_FILE'"

# Test 15: Eliminar tarea
run_curl_test "15_eliminar_tarea" \
    "Eliminar una tarea específica" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X DELETE '$BASE_URL/api/tareas/2' \
    -b '$COOKIE_FILE'"

# Test 16: Eliminar tarea inexistente
run_curl_test "16_eliminar_tarea_inexistente" \
    "Intentar eliminar una tarea que no existe" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X DELETE '$BASE_URL/api/tareas/999' \
    -b '$COOKIE_FILE'"

# Test 17: Página de tareas (HTML) con autenticación
run_curl_test "17_pagina_tareas_auth" \
    "Acceder a la página HTML de tareas (autenticado)" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    '$BASE_URL/tareas' \
    -b '$COOKIE_FILE'"

# Test 18: Página de tareas sin autenticación
run_curl_test "18_pagina_tareas_sin_auth" \
    "Intentar acceder a la página de tareas sin autenticación" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    '$BASE_URL/tareas'"

# Test 19: Cerrar sesión
run_curl_test "19_logout" \
    "Cerrar sesión del usuario actual" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X POST '$BASE_URL/logout' \
    -b '$COOKIE_FILE'"

# Test 20: Verificar que las tareas no son accesibles después del logout
run_curl_test "20_tareas_despues_logout" \
    "Verificar que no se puede acceder a tareas después del logout" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    '$BASE_URL/api/tareas' \
    -b '$COOKIE_FILE'"

# Test 21: Endpoint inexistente
run_curl_test "21_endpoint_inexistente" \
    "Probar acceso a un endpoint que no existe" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    '$BASE_URL/endpoint/que/no/existe'"

# Test 22: Método HTTP no permitido
run_curl_test "22_metodo_no_permitido" \
    "Usar método HTTP no permitido en un endpoint" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X PATCH '$BASE_URL/registro'"

# Test 23: JSON malformado
run_curl_test "23_json_malformado" \
    "Enviar JSON malformado al endpoint de registro" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X POST '$BASE_URL/registro' \
    -H 'Content-Type: application/json' \
    -d '{\"usuario\": \"test\", \"contraseña\":}'"

# Test 24: Registro de usuario duplicado
run_curl_test "24_usuario_duplicado" \
    "Intentar registrar un usuario que ya existe" \
    "curl -s -w '\nHTTP Status: %{http_code}\nTiempo total: %{time_total}s\n' \
    -X POST '$BASE_URL/registro' \
    -H 'Content-Type: application/json' \
    -d '{\"usuario\": \"$USER_NAME\", \"contraseña\": \"otra_password\"}'"

# Limpiar archivos temporales
rm -f "$COOKIE_FILE"

echo ""
echo "PRUEBAS COMPLETADAS"
echo "======================"
echo ""
echo "Resultados guardados en: $OUTPUT_DIR/"
echo "Archivos generados:"
ls -la "$OUTPUT_DIR/"
echo ""

# Generar resumen de resultados
RESUMEN_FILE="$OUTPUT_DIR/00_resumen.md"
{
    echo "#Resumen de Pruebas API - Sistema de Gestión de Tareas"
    echo ""
    echo "**Fecha:** $(date '+%Y-%m-%d %H:%M:%S')"
    echo "**URL Base:** $BASE_URL"
    echo "**Total de pruebas:** $(ls -1 "$OUTPUT_DIR"/*.txt | wc -l)"
    echo ""
    echo "## Lista de Pruebas Ejecutadas"
    echo ""
    for file in "$OUTPUT_DIR"/*.txt; do
        if [ -f "$file" ]; then
            filename=$(basename "$file" .txt)
            test_name=$(echo "$filename" | sed 's/^[0-9]*_//' | tr '_' ' ' | sed 's/\b\w/\u&/g')
            echo "- **$filename:** $test_name"
        fi
    done
    echo ""
    echo "## 🔍 Cómo usar estos resultados"
    echo ""
    echo "1. Cada archivo \`.txt\` contiene:"
    echo "   - Descripción de la prueba"
    echo "   - Comando curl utilizado"
    echo "   - Respuesta completa del servidor"
    echo "   - Código de estado HTTP"
    echo "   - Tiempo de respuesta"
    echo ""
    echo "2. Los archivos están numerados en orden de ejecución"
    echo "3. Puedes usar estos ejemplos para:"
    echo "   - Documentar la API"
    echo "   - Crear tutoriales"
    echo "   - Verificar el comportamiento esperado"
    echo "   - Depurar problemas"
    echo ""
    echo "## Comandos curl de ejemplo"
    echo ""
    echo "### Registro de usuario"
    echo "\`\`\`bash"
    echo "curl -X POST http://localhost:5000/registro \\"
    echo "  -H 'Content-Type: application/json' \\"
    echo "  -d '{\"usuario\": \"mi_usuario\", \"contraseña\": \"mi_password\"}'"
    echo "\`\`\`"
    echo ""
    echo "### Login y guardar cookies"
    echo "\`\`\`bash"
    echo "curl -X POST http://localhost:5000/login \\"
    echo "  -H 'Content-Type: application/json' \\"
    echo "  -d '{\"usuario\": \"mi_usuario\", \"contraseña\": \"mi_password\"}' \\"
    echo "  -c cookies.txt"
    echo "\`\`\`"
    echo ""
    echo "### Crear tarea"
    echo "\`\`\`bash"
    echo "curl -X POST http://localhost:5000/api/tareas \\"
    echo "  -H 'Content-Type: application/json' \\"
    echo "  -d '{\"titulo\": \"Mi tarea\", \"descripcion\": \"Descripción\"}' \\"
    echo "  -b cookies.txt"
    echo "\`\`\`"
    echo ""
    echo "### Obtener tareas"
    echo "\`\`\`bash"
    echo "curl http://localhost:5000/api/tareas -b cookies.txt"
    echo "\`\`\`"
    echo ""
    echo "---"
    echo ""
    echo "**Generado automáticamente por:** test_curl.sh"
} > "$RESUMEN_FILE"

echo "Resumen generado: $RESUMEN_FILE"
echo ""
echo "¡Pruebas completadas exitosamente!"

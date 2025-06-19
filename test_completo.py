#!/usr/bin/env python3
"""
Script de pruebas completas para el Sistema de Gestión de Tareas
Incluye pruebas de integración, validación y casos extremos
"""

import requests
import json
import time
import threading
from concurrent.futures import ThreadPoolExecutor

class TestRunner:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def assert_status(self, response, expected_status, test_name):
        """Valida el código de estado HTTP"""
        if response.status_code == expected_status:
            self.passed += 1
            self.results.append(f"✅ {test_name}")
            return True
        else:
            self.failed += 1
            self.results.append(f"❌ {test_name} - Expected: {expected_status}, Got: {response.status_code}")
            return False
    
    def assert_contains(self, response_data, key, test_name):
        """Valida que la respuesta contenga una clave específica"""
        if key in response_data:
            self.passed += 1
            self.results.append(f"✅ {test_name}")
            return True
        else:
            self.failed += 1
            self.results.append(f"❌ {test_name} - Key '{key}' not found in response")
            return False
    
    def test_server_connection(self):
        """Test 1: Verificar conectividad con el servidor"""
        print("🔍 Test 1: Conectividad del servidor")
        try:
            response = requests.get(self.base_url, timeout=5)
            self.assert_status(response, 200, "Conectividad del servidor")
        except requests.exceptions.ConnectionError:
            self.failed += 1
            self.results.append("❌ Conectividad del servidor - No se puede conectar")
    
    def test_registration_validation(self):
        """Test 2: Validación de registro de usuarios"""
        print("🔍 Test 2: Validación de registro")
        
        # Test con datos vacíos
        response = requests.post(f"{self.base_url}/registro", json={})
        self.assert_status(response, 400, "Registro con datos vacíos")
        
        # Test con usuario muy corto
        response = requests.post(f"{self.base_url}/registro", 
                               json={"usuario": "ab", "contraseña": "test123"})
        self.assert_status(response, 400, "Usuario muy corto")
        
        # Test con contraseña muy corta
        response = requests.post(f"{self.base_url}/registro", 
                               json={"usuario": "testuser", "contraseña": "123"})
        self.assert_status(response, 400, "Contraseña muy corta")
        
        # Test registro válido
        response = requests.post(f"{self.base_url}/registro", 
                               json={"usuario": "test_valid", "contraseña": "valid123"})
        if response.status_code == 201:
            self.assert_status(response, 201, "Registro válido")
            data = response.json()
            self.assert_contains(data, 'usuario_id', "ID de usuario en respuesta")
        elif response.status_code == 409:
            self.passed += 1
            self.results.append("✅ Usuario ya existe (comportamiento esperado)")
    
    def test_authentication(self):
        """Test 3: Autenticación de usuarios"""
        print("🔍 Test 3: Autenticación")
        
        # Registrar usuario para pruebas
        requests.post(f"{self.base_url}/registro", 
                     json={"usuario": "auth_test", "contraseña": "auth123"})
        
        # Test login con credenciales incorrectas
        response = requests.post(f"{self.base_url}/login", 
                               json={"usuario": "auth_test", "contraseña": "wrong_password"})
        self.assert_status(response, 401, "Login con credenciales incorrectas")
        
        # Test login con usuario inexistente
        response = requests.post(f"{self.base_url}/login", 
                               json={"usuario": "nonexistent", "contraseña": "password"})
        self.assert_status(response, 401, "Login con usuario inexistente")
        
        # Test login válido
        session = requests.Session()
        response = session.post(f"{self.base_url}/login", 
                              json={"usuario": "auth_test", "contraseña": "auth123"})
        self.assert_status(response, 200, "Login válido")
        
        return session
    
    def test_task_crud(self, authenticated_session):
        """Test 4: CRUD de tareas"""
        print("🔍 Test 4: CRUD de tareas")
        
        if not authenticated_session:
            self.failed += 4
            self.results.extend([
                "❌ Creación de tarea - Sin sesión autenticada",
                "❌ Lectura de tareas - Sin sesión autenticada", 
                "❌ Actualización de tarea - Sin sesión autenticada",
                "❌ Eliminación de tarea - Sin sesión autenticada"
            ])
            return
        
        # Test crear tarea
        response = authenticated_session.post(f"{self.base_url}/api/tareas",
                                            json={"titulo": "Tarea de prueba", 
                                                 "descripcion": "Descripción de prueba"})
        if self.assert_status(response, 201, "Creación de tarea"):
            task_id = response.json().get('tarea_id')
        else:
            return
        
        # Test obtener tareas
        response = authenticated_session.get(f"{self.base_url}/api/tareas")
        if self.assert_status(response, 200, "Obtener tareas"):
            data = response.json()
            self.assert_contains(data, 'tareas', "Lista de tareas en respuesta")
        
        # Test actualizar tarea
        response = authenticated_session.put(f"{self.base_url}/api/tareas/{task_id}",
                                           json={"completada": True})
        self.assert_status(response, 200, "Actualización de tarea")
        
        # Test eliminar tarea
        response = authenticated_session.delete(f"{self.base_url}/api/tareas/{task_id}")
        self.assert_status(response, 200, "Eliminación de tarea")
    
    def test_authorization(self):
        """Test 5: Autorización - acceso sin autenticación"""
        print("🔍 Test 5: Control de autorización")
        
        # Test acceso a tareas sin autenticación
        response = requests.get(f"{self.base_url}/api/tareas")
        self.assert_status(response, 401, "Acceso a tareas sin autenticación")
        
        # Test crear tarea sin autenticación
        response = requests.post(f"{self.base_url}/api/tareas",
                               json={"titulo": "Tarea no autorizada"})
        self.assert_status(response, 401, "Crear tarea sin autenticación")
        
        # Test página de tareas sin autenticación
        response = requests.get(f"{self.base_url}/tareas")
        self.assert_status(response, 401, "Página de tareas sin autenticación")
    
    def test_error_handling(self):
        """Test 6: Manejo de errores"""
        print("🔍 Test 6: Manejo de errores")
        
        # Test endpoint inexistente
        response = requests.get(f"{self.base_url}/nonexistent")
        self.assert_status(response, 404, "Endpoint inexistente")
        
        # Test método HTTP incorrecto
        response = requests.patch(f"{self.base_url}/registro")
        self.assert_status(response, 405, "Método HTTP incorrecto")
        
        # Test datos JSON malformados
        try:
            response = requests.post(f"{self.base_url}/registro",
                                   data="invalid json",
                                   headers={'Content-Type': 'application/json'})
            # Debería dar 400 o 500
            if response.status_code in [400, 500]:
                self.passed += 1
                self.results.append("✅ JSON malformado manejado correctamente")
            else:
                self.failed += 1
                self.results.append(f"❌ JSON malformado - Status inesperado: {response.status_code}")
        except Exception:
            self.passed += 1
            self.results.append("✅ JSON malformado manejado con excepción")
    
    def test_concurrent_access(self):
        """Test 7: Acceso concurrente"""
        print("🔍 Test 7: Acceso concurrente")
        
        def register_user(user_id):
            try:
                response = requests.post(f"{self.base_url}/registro",
                                       json={"usuario": f"concurrent_{user_id}", 
                                            "contraseña": "concurrent123"})
                return response.status_code in [201, 409]  # 201 = creado, 409 = ya existe
            except:
                return False
        
        # Probar 5 registros concurrentes
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(register_user, i) for i in range(5)]
            results = [future.result() for future in futures]
        
        if all(results):
            self.passed += 1
            self.results.append("✅ Acceso concurrente manejado correctamente")
        else:
            self.failed += 1
            self.results.append("❌ Problemas con acceso concurrente")
    
    def test_data_persistence(self):
        """Test 8: Persistencia de datos"""
        print("🔍 Test 8: Persistencia de datos")
        
        # Crear usuario y tarea
        session = requests.Session()
        session.post(f"{self.base_url}/registro",
                    json={"usuario": "persistence_test", "contraseña": "persist123"})
        session.post(f"{self.base_url}/login",
                    json={"usuario": "persistence_test", "contraseña": "persist123"})
        
        # Crear tarea
        response = session.post(f"{self.base_url}/api/tareas",
                              json={"titulo": "Tarea persistente"})
        
        if response.status_code == 201:
            # Cerrar sesión y volver a iniciar
            session.post(f"{self.base_url}/logout")
            session.post(f"{self.base_url}/login",
                        json={"usuario": "persistence_test", "contraseña": "persist123"})
            
            # Verificar que la tarea aún existe
            response = session.get(f"{self.base_url}/api/tareas")
            if response.status_code == 200:
                data = response.json()
                tasks = data.get('tareas', [])
                if any(task['titulo'] == 'Tarea persistente' for task in tasks):
                    self.passed += 1
                    self.results.append("✅ Persistencia de datos funcionando")
                else:
                    self.failed += 1
                    self.results.append("❌ Datos no persisten correctamente")
            else:
                self.failed += 1
                self.results.append("❌ Error verificando persistencia")
        else:
            self.failed += 1
            self.results.append("❌ No se pudo crear tarea para test de persistencia")
    
    def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        print("🧪 EJECUTANDO SUITE COMPLETA DE PRUEBAS")
        print("=" * 50)
        
        start_time = time.time()
        
        # Ejecutar pruebas en orden
        self.test_server_connection()
        self.test_registration_validation()
        authenticated_session = self.test_authentication()
        self.test_task_crud(authenticated_session)
        self.test_authorization()
        self.test_error_handling()
        self.test_concurrent_access()
        self.test_data_persistence()
        
        end_time = time.time()
        
        # Mostrar resultados
        print("\n" + "=" * 50)
        print("📊 RESULTADOS DE LAS PRUEBAS")
        print("=" * 50)
        
        for result in self.results:
            print(result)
        
        print("\n" + "=" * 50)
        print(f"✅ Pruebas exitosas: {self.passed}")
        print(f"❌ Pruebas fallidas: {self.failed}")
        print(f"⏱️  Tiempo total: {end_time - start_time:.2f} segundos")
        
        success_rate = (self.passed / (self.passed + self.failed)) * 100 if (self.passed + self.failed) > 0 else 0
        print(f"📈 Tasa de éxito: {success_rate:.1f}%")
        
        if self.failed == 0:
            print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        else:
            print(f"\n⚠️  {self.failed} pruebas fallaron. Revisar implementación.")
        
        print("=" * 50)

def main():
    """Función principal"""
    print("🚀 Iniciando suite de pruebas completa...")
    
    # Verificar que el servidor esté funcionando
    try:
        response = requests.get('http://localhost:5000', timeout=2)
        print("✅ Servidor detectado, iniciando pruebas...")
    except requests.exceptions.ConnectionError:
        print("❌ Error: El servidor no está ejecutándose.")
        print("💡 Ejecuta 'python servidor.py' en otra terminal primero.")
        return
    
    # Ejecutar pruebas
    test_runner = TestRunner()
    test_runner.run_all_tests()

if __name__ == '__main__':
    main()

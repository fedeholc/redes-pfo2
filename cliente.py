#!/usr/bin/env python3
"""
Cliente de consola para el Sistema de Gestión de Tareas
Autor: GitHub Copilot
Fecha: Junio 2025
"""

import requests
import json
import getpass
import sys
from datetime import datetime

class ClienteTareas:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
        self.usuario_actual = None
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        print("\n" + "="*50)
        print("🚀 SISTEMA DE GESTIÓN DE TAREAS")
        print("="*50)
        print("1. 📝 Registrar nuevo usuario")
        print("2. 🔐 Iniciar sesión")
        print("3. ❌ Salir")
        print("="*50)
    
    def mostrar_menu_tareas(self):
        """Muestra el menú de gestión de tareas"""
        print(f"\n🏠 Bienvenido, {self.usuario_actual}!")
        print("="*50)
        print("📋 GESTIÓN DE TAREAS")
        print("="*50)
        print("1. 📋 Ver todas las tareas")
        print("2. ➕ Crear nueva tarea")
        print("3. ✏️  Actualizar tarea")
        print("4. ❌ Eliminar tarea")
        print("5. 🚪 Cerrar sesión")
        print("="*50)
    
    def registrar_usuario(self):
        """Registra un nuevo usuario"""
        print("\n📝 REGISTRO DE USUARIO")
        print("-" * 30)
        
        usuario = input("👤 Usuario: ").strip()
        if not usuario:
            print("❌ El usuario no puede estar vacío")
            return False
        
        contraseña = getpass.getpass("🔒 Contraseña: ")
        if not contraseña:
            print("❌ La contraseña no puede estar vacía")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/registro",
                json={"usuario": usuario, "contraseña": contraseña},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                data = response.json()
                print(f"✅ {data['mensaje']}")
                print(f"🎉 Usuario '{data['usuario']}' registrado con ID: {data['usuario_id']}")
                return True
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('error', 'Error desconocido')}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se puede conectar al servidor. ¿Está ejecutándose?")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def iniciar_sesion(self):
        """Inicia sesión con un usuario existente"""
        print("\n🔐 INICIO DE SESIÓN")
        print("-" * 25)
        
        usuario = input("👤 Usuario: ").strip()
        if not usuario:
            print("❌ El usuario no puede estar vacío")
            return False
        
        contraseña = getpass.getpass("🔒 Contraseña: ")
        if not contraseña:
            print("❌ La contraseña no puede estar vacía")
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/login",
                json={"usuario": usuario, "contraseña": contraseña},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.usuario_actual = data['usuario']
                print(f"✅ {data['mensaje']}")
                print(f"🎉 Bienvenido, {self.usuario_actual}!")
                return True
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('error', 'Error desconocido')}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se puede conectar al servidor. ¿Está ejecutándose?")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
    
    def ver_tareas(self):
        """Muestra todas las tareas del usuario"""
        try:
            response = self.session.get(f"{self.base_url}/api/tareas")
            
            if response.status_code == 200:
                data = response.json()
                tareas = data['tareas']
                
                if not tareas:
                    print("\n📋 No tienes tareas registradas")
                    return
                
                print(f"\n📋 TUS TAREAS ({data['total']} total)")
                print("=" * 70)
                
                for tarea in tareas:
                    estado = "✅" if tarea['completada'] else "⏳"
                    fecha = datetime.fromisoformat(tarea['fecha_creacion']).strftime("%d/%m/%Y %H:%M")
                    
                    print(f"ID: {tarea['id']} | {estado} | {tarea['titulo']}")
                    if tarea['descripcion']:
                        print(f"    📝 {tarea['descripcion']}")
                    print(f"    🕒 Creada: {fecha}")
                    print("-" * 70)
                    
            elif response.status_code == 401:
                print("❌ Sesión expirada. Por favor, inicia sesión nuevamente.")
                self.usuario_actual = None
                return False
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('error', 'Error desconocido')}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se puede conectar al servidor.")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def crear_tarea(self):
        """Crea una nueva tarea"""
        print("\n➕ CREAR NUEVA TAREA")
        print("-" * 25)
        
        titulo = input("📝 Título de la tarea: ").strip()
        if not titulo:
            print("❌ El título no puede estar vacío")
            return
        
        descripcion = input("📄 Descripción (opcional): ").strip()
        
        try:
            data = {"titulo": titulo}
            if descripcion:
                data["descripcion"] = descripcion
            
            response = self.session.post(
                f"{self.base_url}/api/tareas",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ {result['mensaje']}")
                print(f"🎉 Tarea '{result['titulo']}' creada con ID: {result['tarea_id']}")
            elif response.status_code == 401:
                print("❌ Sesión expirada. Por favor, inicia sesión nuevamente.")
                self.usuario_actual = None
                return False
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('error', 'Error desconocido')}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se puede conectar al servidor.")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def actualizar_tarea(self):
        """Actualiza una tarea existente"""
        print("\n✏️ ACTUALIZAR TAREA")
        print("-" * 20)
        
        try:
            tarea_id = int(input("🔢 ID de la tarea a actualizar: "))
        except ValueError:
            print("❌ Por favor, ingresa un ID válido")
            return
        
        print("\n¿Qué deseas actualizar?")
        print("1. Título")
        print("2. Descripción")
        print("3. Marcar como completada/pendiente")
        print("4. Todo lo anterior")
        
        try:
            opcion = int(input("Selecciona una opción (1-4): "))
        except ValueError:
            print("❌ Opción inválida")
            return
        
        data = {}
        
        if opcion in [1, 4]:
            nuevo_titulo = input("📝 Nuevo título (Enter para mantener actual): ").strip()
            if nuevo_titulo:
                data["titulo"] = nuevo_titulo
        
        if opcion in [2, 4]:
            nueva_descripcion = input("📄 Nueva descripción (Enter para mantener actual): ").strip()
            if nueva_descripcion:
                data["descripcion"] = nueva_descripcion
        
        if opcion in [3, 4]:
            completada_input = input("✅ ¿Completada? (s/n, Enter para mantener actual): ").strip().lower()
            if completada_input in ['s', 'si', 'sí', 'y', 'yes']:
                data["completada"] = True
            elif completada_input in ['n', 'no']:
                data["completada"] = False
        
        if not data:
            print("❌ No se proporcionaron cambios")
            return
        
        try:
            response = self.session.put(
                f"{self.base_url}/api/tareas/{tarea_id}",
                json=data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {result['mensaje']}")
            elif response.status_code == 404:
                print("❌ Tarea no encontrada")
            elif response.status_code == 401:
                print("❌ Sesión expirada. Por favor, inicia sesión nuevamente.")
                self.usuario_actual = None
                return False
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('error', 'Error desconocido')}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se puede conectar al servidor.")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def eliminar_tarea(self):
        """Elimina una tarea"""
        print("\n❌ ELIMINAR TAREA")
        print("-" * 18)
        
        try:
            tarea_id = int(input("🔢 ID de la tarea a eliminar: "))
        except ValueError:
            print("❌ Por favor, ingresa un ID válido")
            return
        
        confirmacion = input("⚠️  ¿Estás seguro? Esta acción no se puede deshacer (s/n): ").strip().lower()
        if confirmacion not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Operación cancelada")
            return
        
        try:
            response = self.session.delete(f"{self.base_url}/api/tareas/{tarea_id}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {result['mensaje']}")
            elif response.status_code == 404:
                print("❌ Tarea no encontrada")
            elif response.status_code == 401:
                print("❌ Sesión expirada. Por favor, inicia sesión nuevamente.")
                self.usuario_actual = None
                return False
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('error', 'Error desconocido')}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se puede conectar al servidor.")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
    
    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        try:
            response = self.session.post(f"{self.base_url}/logout")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {result['mensaje']}")
            
            self.usuario_actual = None
            return True
            
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se puede conectar al servidor.")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
        
        # Limpiar sesión local de todos modos
        self.usuario_actual = None
        return True
    
    def ejecutar(self):
        """Método principal que ejecuta el cliente"""
        print("🚀 Conectando con el servidor...")
        
        # Verificar conexión con el servidor
        try:
            response = self.session.get(self.base_url)
            if response.status_code != 200:
                print("❌ El servidor no responde correctamente")
                return
        except requests.exceptions.ConnectionError:
            print("❌ No se puede conectar al servidor.")
            print("💡 Asegúrate de que el servidor esté ejecutándose en http://localhost:5000")
            return
        
        print("✅ Conexión establecida")
        
        while True:
            if not self.usuario_actual:
                # Menú principal (sin autenticar)
                self.mostrar_menu_principal()
                
                try:
                    opcion = input("Selecciona una opción (1-3): ").strip()
                except KeyboardInterrupt:
                    print("\n👋 ¡Hasta luego!")
                    break
                
                if opcion == '1':
                    self.registrar_usuario()
                elif opcion == '2':
                    self.iniciar_sesion()
                elif opcion == '3':
                    print("👋 ¡Hasta luego!")
                    break
                else:
                    print("❌ Opción inválida. Por favor, selecciona 1, 2 o 3.")
            
            else:
                # Menú de tareas (autenticado)
                self.mostrar_menu_tareas()
                
                try:
                    opcion = input("Selecciona una opción (1-5): ").strip()
                except KeyboardInterrupt:
                    print("\n👋 ¡Hasta luego!")
                    break
                
                if opcion == '1':
                    self.ver_tareas()
                elif opcion == '2':
                    self.crear_tarea()
                elif opcion == '3':
                    self.actualizar_tarea()
                elif opcion == '4':
                    self.eliminar_tarea()
                elif opcion == '5':
                    if self.cerrar_sesion():
                        continue
                else:
                    print("❌ Opción inválida. Por favor, selecciona 1, 2, 3, 4 o 5.")
                
                # Pausa para que el usuario pueda leer los mensajes
                input("\n⏸️  Presiona Enter para continuar...")

def main():
    """Función principal"""
    print("🔧 Iniciando cliente de gestión de tareas...")
    
    # Permitir configurar la URL del servidor
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
        print(f"🌐 Usando servidor personalizado: {base_url}")
    else:
        base_url = 'http://localhost:5000'
        print(f"🌐 Usando servidor por defecto: {base_url}")
    
    cliente = ClienteTareas(base_url)
    cliente.ejecutar()

if __name__ == '__main__':
    main()

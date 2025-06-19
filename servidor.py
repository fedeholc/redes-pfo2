#!/usr/bin/env python3
"""
Programación sobre Redes - 3°B
PFO2 - Sistema de Gestión de Tareas con API y Base de Datos
Estudiante: Federico Holc
"""

import sqlite3
import bcrypt
from flask import Flask, request, jsonify, render_template_string, session
from flask_cors import CORS
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = 'clave_secreta'  # En prod hay que usar variable de entorno
CORS(app)

# Configuración de la base de datos
DATABASE = 'tareas.db'

def init_db():
    """Inicializa la base de datos con las tablas necesarias"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de tareas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            completada BOOLEAN DEFAULT FALSE,
            usuario_id INTEGER,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Obtiene una conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Hashea una contraseña usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    """Verifica una contraseña contra su hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def login_required(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return jsonify({'error': 'Debe iniciar sesión primero'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    """Página de inicio"""
    html_template = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sistema de Gestión de Tareas</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 600px;
                width: 90%;
            }
            h1 {
                color: #333;
                margin-bottom: 1rem;
                font-size: 2.5rem;
            }
            .subtitle {
                color: #666;
                font-size: 1.2rem;
                margin-bottom: 2rem;
            }
            .endpoints {
                text-align: left;
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 2rem 0;
            }
            .endpoint {
                margin: 1rem 0;
                padding: 0.5rem;
                border-left: 4px solid #667eea;
                padding-left: 1rem;
            }
            .method {
                font-weight: bold;
                color: #667eea;
            }
            .footer {
                margin-top: 2rem;
                color: #999;
                font-size: 0.9rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Sistema de Gestión de Tareas</h1>
            <p class="subtitle">API REST con Flask y SQLite</p>
            
            <div class="endpoints">
                <h3>Endpoints disponibles:</h3>
                
                <div class="endpoint">
                    <span class="method">POST</span> /registro<br>
                    <small>Registrar un nuevo usuario</small>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> /login<br>
                    <small>Iniciar sesión</small>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> /logout<br>
                    <small>Cerrar sesión</small>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> /tareas<br>
                    <small>Ver página de bienvenida de tareas (requiere login)</small>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> /api/tareas<br>
                    <small>Obtener todas las tareas (requiere login)</small>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> /api/tareas<br>
                    <small>Crear una nueva tarea (requiere login)</small>
                </div>
            </div>
            
            <div class="footer">
                <p>Las contraseñas están protegidas con hash bcrypt</p>
                <p>Los datos se almacenan en SQLite</p>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_template)

@app.route('/registro', methods=['POST'])
def registro():
    """Endpoint para registrar nuevos usuarios"""
    try:
        data = request.get_json()
        
        if not data or 'usuario' not in data or 'contraseña' not in data:
            return jsonify({'error': 'Debe proporcionar usuario y contraseña'}), 400
        
        usuario = data['usuario'].strip()
        contraseña = data['contraseña']
        
        if len(usuario) < 3:
            return jsonify({'error': 'El usuario debe tener al menos 3 caracteres'}), 400
        
        if len(contraseña) < 4:
            return jsonify({'error': 'La contraseña debe tener al menos 4 caracteres'}), 400
        
        # Hashear la contraseña
        password_hash = hash_password(contraseña)
        
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO usuarios (usuario, password_hash) VALUES (?, ?)',
                (usuario, password_hash)
            )
            conn.commit()
            usuario_id = cursor.lastrowid
            
            return jsonify({
                'mensaje': 'Usuario registrado exitosamente',
                'usuario_id': usuario_id,
                'usuario': usuario
            }), 201
            
        except sqlite3.IntegrityError:
            return jsonify({'error': 'El usuario ya existe'}), 409
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
def login():
    """Endpoint para iniciar sesión"""
    try:
        data = request.get_json()
        
        if not data or 'usuario' not in data or 'contraseña' not in data:
            return jsonify({'error': 'Debe proporcionar usuario y contraseña'}), 400
        
        usuario = data['usuario'].strip()
        contraseña = data['contraseña']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM usuarios WHERE usuario = ?', (usuario,))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data and check_password(contraseña, user_data['password_hash']):
            session['usuario_id'] = user_data['id']
            session['usuario'] = usuario
            
            return jsonify({
                'mensaje': 'Inicio de sesión exitoso',
                'usuario': usuario,
                'usuario_id': user_data['id']
            }), 200
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401
            
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@app.route('/logout', methods=['POST'])
def logout():
    """Endpoint para cerrar sesión"""
    session.clear()
    return jsonify({'mensaje': 'Sesión cerrada exitosamente'}), 200

@app.route('/tareas')
@login_required
def tareas_html():
    """Página de bienvenida para tareas (requiere autenticación)"""
    usuario = session.get('usuario', 'Usuario')
    
    html_template = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Mis Tareas - Sistema de Gestión</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 800px;
                width: 90%;
            }
            h1 {
                color: #333;
                margin-bottom: 1rem;
                font-size: 2.5rem;
            }
            .welcome {
                color: #667eea;
                font-size: 1.4rem;
                margin-bottom: 2rem;
            }
            .info-box {
                background: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 2rem 0;
                text-align: left;
            }
            .api-info {
                margin: 1rem 0;
                padding: 0.5rem;
                border-left: 4px solid #28a745;
                padding-left: 1rem;
            }
            .method {
                font-weight: bold;
                color: #28a745;
            }
            .logout-btn {
                background: #dc3545;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 1rem;
                margin-top: 1rem;
            }
            .logout-btn:hover {
                background: #c82333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Gestión de Tareas</h1>
            <p class="welcome">¡Bienvenido, <strong>{{ usuario }}</strong>!</p>
            
            <div class="info-box">
                <h3>API de Tareas disponible:</h3>
                
                <div class="api-info">
                    <span class="method">GET</span> /api/tareas<br>
                    <small>Obtener todas tus tareas</small>
                </div>
                
                <div class="api-info">
                    <span class="method">POST</span> /api/tareas<br>
                    <small>Crear una nueva tarea<br>
                    Body: {"titulo": "Mi tarea", "descripcion": "Descripción opcional"}</small>
                </div>
                
                <div class="api-info">
                    <span class="method">PUT</span> /api/tareas/&lt;id&gt;<br>
                    <small>Actualizar una tarea existente</small>
                </div>
                
                <div class="api-info">
                    <span class="method">DELETE</span> /api/tareas/&lt;id&gt;<br>
                    <small>Eliminar una tarea</small>
                </div>
            </div>
            
            <button class="logout-btn" onclick="logout()">Cerrar Sesión</button>
        </div>
        
        <script>
            function logout() {
                fetch('/logout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.mensaje);
                    window.location.href = '/';
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_template, usuario=usuario)

@app.route('/api/tareas', methods=['GET'])
@login_required
def obtener_tareas():
    """Obtiene todas las tareas del usuario autenticado"""
    try:
        usuario_id = session['usuario_id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, titulo, descripcion, completada, fecha_creacion 
            FROM tareas 
            WHERE usuario_id = ? 
            ORDER BY fecha_creacion DESC
        ''', (usuario_id,))
        
        tareas = []
        for row in cursor.fetchall():
            tareas.append({
                'id': row['id'],
                'titulo': row['titulo'],
                'descripcion': row['descripcion'],
                'completada': bool(row['completada']),
                'fecha_creacion': row['fecha_creacion']
            })
        
        conn.close()
        
        return jsonify({
            'tareas': tareas,
            'total': len(tareas)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@app.route('/api/tareas', methods=['POST'])
@login_required
def crear_tarea():
    """Crea una nueva tarea para el usuario autenticado"""
    try:
        data = request.get_json()
        
        if not data or 'titulo' not in data:
            return jsonify({'error': 'Debe proporcionar un título para la tarea'}), 400
        
        titulo = data['titulo'].strip()
        descripcion = data.get('descripcion', '').strip()
        usuario_id = session['usuario_id']
        
        if len(titulo) < 1:
            return jsonify({'error': 'El título no puede estar vacío'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tareas (titulo, descripcion, usuario_id) 
            VALUES (?, ?, ?)
        ''', (titulo, descripcion, usuario_id))
        
        tarea_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'mensaje': 'Tarea creada exitosamente',
            'tarea_id': tarea_id,
            'titulo': titulo,
            'descripcion': descripcion
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@app.route('/api/tareas/<int:tarea_id>', methods=['PUT'])
@login_required
def actualizar_tarea(tarea_id):
    """Actualiza una tarea del usuario autenticado"""
    try:
        data = request.get_json()
        usuario_id = session['usuario_id']
        
        if not data:
            return jsonify({'error': 'Debe proporcionar datos para actualizar'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar que la tarea pertenece al usuario
        cursor.execute('SELECT id FROM tareas WHERE id = ? AND usuario_id = ?', (tarea_id, usuario_id))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        # Actualizar campos proporcionados
        updates = []
        values = []
        
        if 'titulo' in data:
            updates.append('titulo = ?')
            values.append(data['titulo'].strip())
        
        if 'descripcion' in data:
            updates.append('descripcion = ?')
            values.append(data['descripcion'].strip())
        
        if 'completada' in data:
            updates.append('completada = ?')
            values.append(bool(data['completada']))
        
        if not updates:
            conn.close()
            return jsonify({'error': 'No hay campos para actualizar'}), 400
        
        values.append(tarea_id)
        query = f'UPDATE tareas SET {", ".join(updates)} WHERE id = ?'
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        return jsonify({'mensaje': 'Tarea actualizada exitosamente'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@app.route('/api/tareas/<int:tarea_id>', methods=['DELETE'])
@login_required
def eliminar_tarea(tarea_id):
    """Elimina una tarea del usuario autenticado"""
    try:
        usuario_id = session['usuario_id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Verificar que la tarea pertenece al usuario
        cursor.execute('SELECT id FROM tareas WHERE id = ? AND usuario_id = ?', (tarea_id, usuario_id))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Tarea no encontrada'}), 404
        
        # Eliminar la tarea
        cursor.execute('DELETE FROM tareas WHERE id = ?', (tarea_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'mensaje': 'Tarea eliminada exitosamente'}), 200
        
    except Exception as e:
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    """Maneja errores 404"""
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Maneja errores 500"""
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    # Inicializar la base de datos
    init_db()
    print("Iniciando servidor de gestión de tareas...")
    print("Base de datos SQLite inicializada")
    print("Servidor disponible en: http://localhost:5000")
    
    # Ejecutar la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)

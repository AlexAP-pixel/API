from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# Crear la aplicación Flask
app = Flask(__name__) # Crea la aplicación Flask
CORS(app)  # Permitir peticiones desde otros dominios

# Datos de ejemplo (en una aplicación real usarías una base de datos)
usuarios = [
    {"id": 1, "nombre": "Juan", "email": "juan@ejemplo.com"},
    {"id": 2, "nombre": "María", "email": "maria@ejemplo.com"},
    {"id": 3, "nombre": "Carlos", "email": "carlos@ejemplo.com"}
]
"""
---------Conectarlo a la base de datos sql server-------------------------
import pyodbc
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:servidor-sql.database.windows.net,1433;Database=mydatabase;Uid=myusername;Pwd=mypassword;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
cursor = conn.cursor()
cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()
conn.close()
"""

# Ruta principal - GET
@app.route('/', methods=['GET'])
def inicio():
    return jsonify({
        "mensaje": "¡Bienvenido a mi API!",
        "version": "1.0",
        "endpoints": {
            "usuarios": "/usuarios",
            "usuario_por_id": "/usuarios/<id>",
            "crear_usuario": "/usuarios (POST)"
        }
    })

# Obtener todos los usuarios - GET
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify({
        "usuarios": usuarios,
        "total": len(usuarios)
    })

# Obtener un usuario por ID - GET
@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    usuario = next((u for u in usuarios if u["id"] == usuario_id), None) # 
    if usuario:
        return jsonify(usuario)
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

# Crear un nuevo usuario - POST
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    try:
        datos = request.get_json() 
        
        # Validar que los datos necesarios estén presentes
        if not datos or 'nombre' not in datos or 'email' not in datos:
            return jsonify({"error": "Se requieren nombre y email"}), 400
        
        # Crear nuevo usuario
        nuevo_id = max(u["id"] for u in usuarios) + 1 if usuarios else 1
        nuevo_usuario = {
            "id": nuevo_id,
            "nombre": datos["nombre"],
            "email": datos["email"]
        }
        
        usuarios.append(nuevo_usuario)
        
        return jsonify({
            "mensaje": "Usuario creado exitosamente",
            "usuario": nuevo_usuario
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Error al crear usuario: {str(e)}"}), 500

# Actualizar un usuario - PUT
@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    try:
        datos = request.get_json()
        usuario = next((u for u in usuarios if u["id"] == usuario_id), None)
        
        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        # Actualizar datos
        if 'nombre' in datos:
            usuario["nombre"] = datos["nombre"]
        if 'email' in datos:
            usuario["email"] = datos["email"]
        
        return jsonify({
            "mensaje": "Usuario actualizado exitosamente",
            "usuario": usuario
        })
        
    except Exception as e:
        return jsonify({"error": f"Error al actualizar usuario: {str(e)}"}), 500

# Eliminar un usuario - DELETE
@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    usuario = next((u for u in usuarios if u["id"] == usuario_id), None)
    
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    usuarios.remove(usuario)
    
    return jsonify({
        "mensaje": "Usuario eliminado exitosamente",
        "usuario_eliminado": usuario
    })

# Endpoint de prueba con parámetros de consulta
@app.route('/buscar', methods=['GET'])
def buscar():
    nombre = request.args.get('nombre', '')
    if nombre:
        resultados = [u for u in usuarios if nombre.lower() in u["nombre"].lower()]
        return jsonify({
            "busqueda": nombre,
            "resultados": resultados,
            "total_encontrados": len(resultados)
        })
    else:
        return jsonify({"error": "Se requiere el parámetro 'nombre'"}), 400

# Manejo de errores
@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({"error": "Endpoint no encontrado"}), 404

@app.errorhandler(500)
def error_servidor(error):
    return jsonify({"error": "Error interno del servidor"}), 500

# Ejecutar la aplicación
if __name__ == '__main__':
    print("Iniciando API...")
    print("Servidor disponible en: http://localhost:5000")
    print("Documentación de endpoints:")
    print("   GET  / - Información de la API")
    print("   GET  /usuarios - Obtener todos los usuarios")
    print("   GET  /usuarios/<id> - Obtener usuario por ID")
    print("   POST /usuarios - Crear nuevo usuario")
    print("   PUT  /usuarios/<id> - Actualizar usuario")
    print("   DELETE /usuarios/<id> - Eliminar usuario")
    print("   GET  /buscar?nombre=<nombre> - Buscar usuarios por nombre")
    print("\n Ejemplos de uso:")
    print("   curl http://localhost:5000/usuarios")
    print("   curl -X POST http://localhost:5000/usuarios -H 'Content-Type: application/json' -d '{\"nombre\":\"Ana\",\"email\":\"ana@ejemplo.com\"}'")
    app.run(debug=True, host='0.0.0.0', port=5000)

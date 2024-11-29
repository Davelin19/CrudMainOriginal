# Importamos las librerías necesarias para el funcionamiento de la API
from flask import Flask
from flask_cors import CORS # CORS es necesario para permitir el acceso desde aplicaciones web de otros dominios.
from flask import jsonify, request  # jsonify se usa para enviar respuestas en formato JSON, request para leer los datos enviados por el cliente. 
import pymysql  # pymysql es el conector que usamos para interactuar con la base de datos MySQL.

# Creamos la instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de CORS, que permite que nuestra API sea consumida desde otros orígenes (dominios)
CORS(app)

# Función para conectarnos a la base de datos MySQL
def conectar(vhost, vuser, vpass, vdb):
    """
    Función para realizar la conexión con la base de datos MySQL.
    Recibe los siguientes parámetros:
    - vhost: El host de la base de datos.
    - vuser: El usuario para autenticarse en la base de datos.
    - vpass: La contraseña del usuario.
    - vdb: El nombre de la base de datos.
    """
    conn = pymysql.connect(host=vhost, user=vuser, passwd=vpass, db=vdb, charset='utf8mb4')
    return conn

# Ruta para obtener todos los registros del "baúl de contraseñas"
@app.route("/")
def consulta_general():
    """
    Esta ruta devuelve todos los registros de la tabla COFRE en la base de datos
    """
    try:
        # Nos conectamos a la base de datos
        conn = conectar('localhost', 'root', 'root', 'gestor_contrasena')
        cur = conn.cursor()  # Creamos un cursor para ejecutar las consultas SQL.
        
        # Ejecutamos la consulta para seleccionar todos los registros de la tabla COFRE.
        cur.execute("""SELECT * FROM COFRE""")
        datos = cur.fetchall()  # Obtenemos todos los resultados de la consulta.

        # Preparamos la lista de datos para devolverlos como respuesta en formato JSON
        data = []
        for row in datos:
            dato = {
                'id_COFRE': row[0],
                'Plataforma': row[1],
                'usuario': row[2],
                'clave': row[3],
            }
            data.append(dato)  # Añadimos cada registro a la lista 'data'
        
        cur.close()  # Cerramos el cursor
        conn.close()  # Cerramos la conexión a la base de datos
        
        # Devolvemos los resultados como respuesta en formato JSON
        return jsonify({'COFRE': data, 'mensaje': 'COFRE de contrasenas'})
    
    except Exception as ex:
        # Si ocurre un error, devolvemos un mensaje de error.
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Ruta para obtener un solo registro del "baúl de contraseñas" por su ID
@app.route("/consulta_individual/<codigo>", methods=['GET'])
def consulta_individual(codigo):
    """
    Esta ruta devuelve un solo registro de la tabla COFRE según el ID proporcionado en la URL.
    """
    try:
        conn = conectar('localhost', 'root', 'root', 'gestor_contrasena')
        cur = conn.cursor()
        
        # Buscamos el registro con el ID dado
        cur.execute("""SELECT * FROM COFRE WHERE id_COFRE='{0}'""".format(codigo))
        datos = cur.fetchone()  # Obtenemos un solo registro.

        cur.close()  # Cerramos el cursor
        conn.close()  # Cerramos la conexión
        
        if datos:
            # Si el registro es encontrado, lo devolvemos en formato JSON
            dato = {
                'id_COFRE': datos[0],
                'Plataforma': datos[1],
                'usuario': datos[2],
                'clave': datos[3]
            }
            return jsonify({'COFRE': dato, 'mensaje': 'Registro encontrado'})
        else:
            # Si no se encuentra el registro, devolvemos un mensaje de error
            return jsonify({'mensaje': 'Registro no encontrado'})
    
    except Exception as ex:
        # Si ocurre un error, devolvemos un mensaje genérico de error
        return jsonify({'mensaje': 'Error'})

# Ruta para registrar un nuevo "baúl de contraseñas"
@app.route("/registro/", methods=['POST'])
def registro():
    """
    Esta ruta permite agregar un nuevo registro a la tabla COFRE.
    Los datos deben enviarse en formato JSON en el cuerpo de la solicitud.
    """
    try:
        # Conectamos a la base de datos
        conn = conectar('localhost', 'root', 'root', 'gestor_contrasena')
        cur = conn.cursor()

        # Insertamos un nuevo registro en la tabla COFRE con los datos enviados en la solicitud
        x = cur.execute("""
            INSERT INTO COFRE (Plataforma, usuario, clave) 
            VALUES ('{0}', '{1}', '{2}')
        """.format(request.json['Plataforma'], request.json['usuario'], request.json['clave']))

        # Confirmamos la inserción en la base de datos
        conn.commit()
        cur.close()  # Cerramos el cursor
        conn.close()  # Cerramos la conexión

        # Devolvemos un mensaje indicando que el registro fue agregado correctamente
        return jsonify({'mensaje': 'Registro agregado'})
    
    except Exception as ex:
        # Si ocurre un error, devolvemos un mensaje de error
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Ruta para eliminar un registro del "baúl de contraseñas"
@app.route("/eliminar/<codigo>", methods=['DELETE'])
def eliminar(codigo):
    """
    Esta ruta permite eliminar un registro específico de la tabla COFRE
    según el ID proporcionado en la URL.
    """
    try:
        # Conectamos a la base de datos
        conn = conectar('localhost', 'root', 'root', 'gestor_contrasena')
        cur = conn.cursor()

        # Eliminamos el registro con el ID proporcionado
        x = cur.execute("""DELETE FROM COFRE WHERE id_COFRE={0}""".format(codigo))

        # Confirmamos la eliminación en la base de datos
        conn.commit()
        cur.close()  # Cerramos el cursor
        conn.close()  # Cerramos la conexión

        # Devolvemos un mensaje indicando que el registro fue eliminado
        return jsonify({'mensaje': 'Eliminado'})
    
    except Exception as ex:
        # Si ocurre un error, devolvemos un mensaje de error
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Ruta para actualizar un registro del "baúl de contraseñas"
@app.route("/actualizar/<codigo>", methods=['PUT'])
def actualizar(codigo):
    """
    Esta ruta permite actualizar un registro específico de la tabla COFRE
    según el ID proporcionado en la URL. Los nuevos datos deben enviarse
    en formato JSON en el cuerpo de la solicitud.
    """
    try:
        # Conectamos a la base de datos
        conn = conectar('localhost', 'root', 'root', 'gestor_contrasena')
        cur = conn.cursor()

        # Actualizamos el registro con el ID proporcionado
        x = cur.execute("""
            UPDATE COFRE SET Plataforma='{0}', usuario='{1}', clave='{2}'
            WHERE id_COFRE={3}
        """.format(request.json['Plataforma'], request.json['usuario'], request.json['clave'], codigo))

        # Confirmamos la actualización en la base de datos
        conn.commit()
        cur.close()  # Cerramos el cursor
        conn.close()  # Cerramos la conexión
                # Devolvemos un mensaje indicando que el registro fue actualizado
        return jsonify({'mensaje': 'Registro actualizado'})
    
    except Exception as ex:
        # Si ocurre un error, devolvemos un mensaje de error
        print(ex)
        return jsonify({'mensaje': 'Error'})

# Bloque principal para ejecutar la aplicación Flask
if __name__ == '__main__':
    # Ejecutamos la aplicación en modo de desarrollo (con depuración activada)
    app.run(debug=True)
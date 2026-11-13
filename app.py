"""!
@file app.py
@brief API de gestión de alumnos "Sistema Alumnos" (actividad OCY1102).
"""
import os

from flask import Flask, jsonify, request

## Aplicación Flask principal.
app = Flask(__name__)

## Base de datos en memoria con los registros iniciales de alumnos (solo para fines de la actividad).
ALUMNOS = [
    {"id": 1, "nombre": "Ana Pérez", "carrera": "Ingeniería en Informática", "promedio": 6.1},
    {"id": 2, "nombre": "Benjamín Rojas", "carrera": "Ingeniería en Ciberseguridad", "promedio": 5.4},
    {"id": 3, "nombre": "Camila Soto", "carrera": "Analista Programador", "promedio": 6.8},
]

## Versión de la aplicación inyectada por el pipeline (ver Jenkinsfile) para trazabilidad.
VERSION = os.environ.get("APP_VERSION", "dev")


@app.route('/hello')
def hello():
    """!
    @brief Devuelve un saludo personalizado usando el parámetro 'name' recibido en la URL.

    @return Cadena de texto con el mensaje de saludo.
    """
    name = request.args.get('name')
    return f"Hello, {name}!"


@app.route('/health')
def health():
    """!
    @brief Verifica el estado de salud del servicio.

    @return JSON indicando que el estado de la aplicación es correcto.
    """
    return jsonify({"estado": "ok"})


@app.route('/version')
def version():
    """!
    @brief Consulta la información y versión actual de la aplicación.

    @return JSON con el nombre de la aplicación y su versión desplegada.
    """
    return jsonify({"aplicacion": "Sistema Alumnos", "version": VERSION})


@app.route('/alumnos')
def listar_alumnos():
    """!
    @brief Lista todos los alumnos registrados en memoria.

    @return JSON con la lista completa de alumnos.
    """
    return jsonify(ALUMNOS)


@app.route('/alumnos/<int:alumno_id>')
def obtener_alumno(alumno_id):
    """!
    @brief Obtiene un alumno por su identificador.

    @param alumno_id Identificador numérico del alumno.
    @return JSON con el alumno, o error 404 si no existe.
    """
    for alumno in ALUMNOS:
        if alumno["id"] == alumno_id:
            return jsonify(alumno)
    return jsonify({"error": "Alumno no encontrado"}), 404


@app.route('/alumnos', methods=['POST'])
def crear_alumno():
    """!
    @brief Crea y registra un nuevo alumno a partir de los datos JSON recibidos en la petición.

    @return JSON con los datos del alumno creado y código 201, o error 400 si los datos son inválidos.
    """
    datos = request.get_json(silent=True) or {}
    nombre = str(datos.get("nombre", "")).strip()
    promedio = datos.get("promedio")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400
    if not isinstance(promedio, (int, float)) or not 1.0 <= promedio <= 7.0:
        return jsonify({"error": "El 'promedio' debe ser un número entre 1.0 y 7.0"}), 400

    nuevo = {
        "id": max(a["id"] for a in ALUMNOS) + 1,
        "nombre": nombre,
        "carrera": str(datos.get("carrera", "Sin carrera")),
        "promedio": promedio,
    }
    ALUMNOS.append(nuevo)
    return jsonify(nuevo), 201


def main():
    """!
    @brief Inicia el servidor de desarrollo de Flask en modo depuración.
    """
    app.run(debug=True)


if __name__ == '__main__':
    main()
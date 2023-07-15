import pymysql
from datetime import datetime


def conexion() -> pymysql.connect | None:
    """
    Establece una conexión a la base de datos utilizando pymysql

    :return: pymysql.connect Objeto de conexión a la base de datos
    :raises pymysql.err.OperationalError: Si ocurre un error al conectarse a la base de datos
    """
    try:
        conn = pymysql.connect(host='localhost',
                               user='root',
                               passwd='',
                               db='cumisystem',
                               charset='utf8mb4')
        return conn
    except pymysql.err.OperationalError as error:
        print(f'Ocurrió un error mientras de conectaba a la base de datos {error}')
        return None

def last_attendance(id_empleado: int, dia: datetime) -> any:
    """
    Función encargada de extraer el registro de la última entrada
    para un usuario en específico.

    :param id_empleado: Id del usuario.
    :param dia: Fecha de trabajo en formato 'YYYY-MM-DD'.
    :return: Una tuple que contiene la información del último registro de asistencia correspondiente,
    o None si no se encuentra ningún registro.
    :raises errorhandler: Error relacionado con la consulta a la BD.
    """
    cursor = conexion().cursor()
    try:
        cursor.execute(f""" 
                    SELECT * FROM attendances
                    WHERE attendances.employe_id = {id_empleado}
                    AND attendances.workday = '{dia}'
                    ORDER BY employe_id DESC;
                        """)
        if cursor:
            return cursor.fetchone()
        else:
            return None
    except pymysql.err.OperationalError as e:
        raise Exception(f'Ocurrió un error {e}')
    finally:
        cursor.close()

def attendance_exists(dia: datetime, hora: datetime.time, id_empleado: int) -> bool:
    """
    Verifica si existe un registro de asistencia para un empleado en una fecha y hora específicas.

    :param dia: Fecha de trabajo.
    :param hora: Hora de entrada.
    :param id_empleado: ID del empleado.
    :return: True si existe un registro de asistencia que cumple con los criterios especificados
             False de lo contrario.
    """
    cursor = conexion().cursor()
    try:
        cursor.execute(f"""
                            SELECT * FROM attendances
                            WHERE attendances.workday = '{dia}'
                            AND attendances.aentry_time = '{hora}'
                            AND attendances.employe_id = {id_empleado}
                            """)
        if cursor:
            return True
        else:
            return False
    except Exception as e:
        raise Exception(f'Ocurrio un error {e}')
    finally:
        cursor.close()


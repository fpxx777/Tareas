from config.db import connectToMySQL


class Profesor:
    def __init__(self, data):
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.id_colegio = data["id_colegio"]
        self.id = data["id"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM profesores"
        results = connectToMySQL("sist_educativo").query_db(query)
        profesores = []
        for profesor in results:
            profesores.append(cls(profesor))
        return profesores

    @classmethod
    def insert_profesor(cls, nombre, apellido, colegio):
        query = f"INSERT INTO profesores (nombre, apellido, id_colegio) VALUES ('{nombre}', '{apellido}', {colegio})"
        connectToMySQL("sist_educativo").query_db(query)

    @classmethod
    def select_one(cls, id_profesor):
        query = f"SELECT * FROM profesores WHERE id = {id_profesor}"
        try:
            resutls = connectToMySQL("sist_educativo").query_db(query)
            return resutls
        except:
            return False

    @classmethod
    def update(cls, id, nombre, apellido, id_colegio):
        query = f"UPDATE profesores SET nombre = '{nombre}', apellido = '{apellido}', id_colegio={id_colegio} WHERE id = {id}"
        result = connectToMySQL("sist_educativo").query_db(query)
        return result

    @classmethod
    def deleted(cls, id):
        query = f"DELETE FROM profesores WHERE id = {id}"
        result = connectToMySQL("sist_educativo").query_db(query)
        return result

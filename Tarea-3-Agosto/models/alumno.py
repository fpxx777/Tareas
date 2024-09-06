from config.db import connectToMySQL

class Alumno:
    def __init__(self, data):
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.id_curso = data["id_curso"]
        self.id = data["id"]
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM alumnos"
        results = connectToMySQL('sist_educativo').query_db(query)
        profesores = []
        for profesor in results:
            profesores.append(cls(profesor))
        return profesores
    @classmethod
    def insert_alumno(cls, nombre, apellido, curso):
        query = f"INSERT INTO alumnos (nombre, apellido, id_curso) VALUES ('{nombre}', '{apellido}', {curso})"
        connectToMySQL('sist_educativo').query_db(query)
        
    @classmethod
    def select_one(cls, id_alumno):
        query = f"SELECT * FROM alumnos WHERE id = {id_alumno}"
        try:
            resutls = connectToMySQL('sist_educativo').query_db(query)
            return resutls
        except:
            return False
    @classmethod
    def update(cls, id, nombre, apellido, id_curso):
        query = f"UPDATE alumnos SET nombre = '{nombre}', apellido = '{apellido}', id_curso={id_curso} WHERE id = {id}"
        result = connectToMySQL('sist_educativo').query_db(query)
        return result
    @classmethod
    def deleted(cls,id):
        query = f"DELETE FROM alumnos WHERE id = {id}"
        result = connectToMySQL('sist_educativo').query_db(query)
        return result
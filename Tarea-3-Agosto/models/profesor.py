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
        results = connectToMySQL('sist_educativo').query_db(query)
        profesores = []
        for profesor in results:
            profesores.append(cls(profesor))
        return profesores
    @classmethod
    def insert_profesor(cls, nombre, apellido, colegio):
        query = f"INSERT INTO profesores (nombre, apellido, id_colegio) VALUES ('{nombre}', '{apellido}', {colegio})"
        connectToMySQL('sist_educativo').query_db(query)
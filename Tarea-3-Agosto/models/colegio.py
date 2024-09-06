from config.db import connectToMySQL

class Colegio:
    def __init__(self, data):
        self.nombre = data["nombre"]
        self.id = data["id"]
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM colegios"
        results = connectToMySQL('sist_educativo').query_db(query)
        colegios = []
        for colegio in results:
            colegios.append(cls(colegio))
        return colegios
    @classmethod
    def insert_colegio(cls, name):
        query = f"INSERT INTO colegios (nombre) VALUES ('{name}')"
        try:
            resutls = connectToMySQL('sist_educativo').query_db(query)
            return resutls
        except:
            return False
    @classmethod
    def select_one(cls, id_colegio):
        query = f"SELECT * FROM colegios WHERE id = {id_colegio}"
        try:
            resutls = connectToMySQL('sist_educativo').query_db(query)
            return resutls
        except:
            return False
    @classmethod
    def update(cls, id_colegio, nombre):
        query = f"UPDATE colegios SET nombre = '{nombre}' WHERE id = {id_colegio}"
        result = connectToMySQL('sist_educativo').query_db(query)
        return result
    @classmethod
    @classmethod
    def deleted(cls,id):
        query = f"DELETE FROM colegios WHERE id = {id}"
        result = connectToMySQL('sist_educativo').query_db(query)
        return result
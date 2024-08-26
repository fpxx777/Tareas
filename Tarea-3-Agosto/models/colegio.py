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
            connectToMySQL('sist_educativo').query_db(query)
        except:
            return False
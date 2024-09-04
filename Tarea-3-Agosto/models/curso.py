from config.db import connectToMySQL

class Curso:
    def __init__(self, data):
        self.name = data["name"]
        self.id_colegio = data["id_colegio"]
        self.id = data["id"]
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cursos"
        results = connectToMySQL('sist_educativo').query_db(query)
        cursos = []
        for curso in results:
            cursos.append(cls(curso))
        return cursos
    @classmethod
    def insert_curso(cls, name, id_colegio):
        query = f"INSERT INTO cursos (name, id_colegio) VALUES ('{name}', {id_colegio})"
        try:
            connectToMySQL('sist_educativo').query_db(query)
        except:
            return False
    @classmethod
    def select_one(cls, id_curso):
        query = f"SELECT * FROM cursos WHERE id = {id_curso}"
        try:
            resutls = connectToMySQL('sist_educativo').query_db(query)
            return resutls
        except:
            return False
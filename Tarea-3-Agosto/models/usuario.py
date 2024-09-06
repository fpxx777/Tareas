from config.db import connectToMySQL


class Usuario:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.password = data["password"]

    @classmethod
    def insert_one(cls, nombre, apellido, email, password):
        query = f"""INSERT INTO usuarios 
            (nombre, apellido, email, password)
            VALUES ('{nombre}', '{apellido}', '{email}', '{password}');
            """
        result = connectToMySQL("sist_educativo").query_db(query)
        return result

    @classmethod
    def select_by_email(cls, email):
        query = f"SELECT * FROM usuarios WHERE email='{email}' "
        results = connectToMySQL("sist_educativo").query_db(query)
        usuarios = []
        for usuario in results:
            usuarios.append(cls(usuario))
        return usuarios

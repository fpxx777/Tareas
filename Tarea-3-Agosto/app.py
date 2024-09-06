from flask import Flask, render_template, request, redirect
from flask_bcrypt import Bcrypt

from models.colegio import Colegio
from models.profesor import Profesor
from models.curso import Curso
from models.alumno import Alumno
from models.usuario import Usuario

app = Flask(__name__)
bcrypt = Bcrypt(app)


def get_class(opcion):
    return {
        "colegios": Colegio,
        "profesores": Profesor,
        "cursos": Curso,
        "alumnos": Alumno,
    }[opcion]


# GENERAL ---------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/sesion", methods=["GET"])
def sesion():
    return render_template("sesion.html")


@app.route("/registro", methods=["POST"])
def register():
    nombre = request.form.get("first_name")
    apellido = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("pass")
    password2 = request.form.get("pass2")

    errors = []

    if not nombre or len(nombre) < 3:
        errors.append("Nombre invalido")

    if not apellido or len(apellido) < 3:
        errors.append("Apellido invalido")

    if not email or len(email) < 3:
        errors.append("email invalido")

    if password != password2:
        errors.append("Las constraseña no coinciden")

    users = Usuario.select_by_email(email)

    if len(users) > 0:
        errors.append("El usuario ya está registrado")

    if len(errors) > 0:
        return render_template("sesion.html", register_errors=errors)

    password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = Usuario.insert_one(nombre, apellido, email, password)
    return redirect("/sesion")


@app.route("/<opcion>/", methods=["post"])
def pre_select_one(opcion):
    search = request.form.get("response")
    print(opcion, search)
    return redirect(f"/{opcion}/{search}/")


@app.route("/<opcion>/<id>/", methods=["GET"])
def select_one(opcion, id):
    response = get_class(opcion).select_one(id)
    print(response[0])
    return render_template("select_one.html", response=response, opcion=opcion)


# COLEGIOS ---------------------------------------------
@app.route("/colegios/", methods=["GET"])
def colegios():
    colegio = Colegio.get_all()
    return render_template("colegio.html", colegios=colegio)


@app.route("/colegios/crear/", methods=["GET"])
def colegios_crear_ver():
    return render_template("crear-colegio.html")


@app.route("/colegios/crear/", methods=["POST"])
def colegios_crear():
    name = request.form.get("colegio")
    Colegio.insert_colegio(name)
    return redirect("/")


@app.route("/colegios/editar/<id>/", methods=["GET"])
def mostrar_colegios_editar(id):
    colegio = Colegio.select_one(id)
    return render_template("editar-colegio.html", colegio=colegio[0])


@app.route("/colegios/editar/<id>/", methods=["POST"])
def colegios_editar(id):
    id_colegio = request.form.get("id_colegio")
    nombre = request.form.get("nombre_colegio")
    Colegio.update(id_colegio, nombre)
    return redirect("/colegios")


@app.route("/colegios/eliminar/<id_colegio>/", methods=["POST"])
def eliminar_colegio(id_colegio):
    Colegio.deleted(id_colegio)
    return redirect("/colegios")


# PROFESORES --------------------------------------------
@app.route("/profesores", methods=["GET"])
def profesores():
    profesores = Profesor.get_all()
    return render_template("profesores.html", profesores=profesores)


@app.route("/profesores/crear/", methods=["GET"])
def profesores_crear_ver():
    colegios = Colegio.get_all()
    return render_template("crear-profesor.html", colegios=colegios)


@app.route("/profesores/crear/", methods=["POST"])
def profesores_crear():
    name = request.form.get("profesor_name")
    lastname = request.form.get("profesor_lastname")
    colegio_id = request.form.get("colegio")
    Profesor.insert_profesor(name, lastname, colegio_id)
    return redirect("/profesores")


@app.route(
    "/profesores/editar/<id_profesor>/",
    methods=[
        "GET",
    ],
)
def mostar_profesor_editar(id_profesor):
    profesor = Profesor.select_one(id_profesor)
    colegios = Colegio.get_all()
    return render_template(
        "profesor-editar.html", profesor=profesor[0], colegios=colegios
    )


@app.route(
    "/profesores/editar/<id_profesor>/",
    methods=[
        "POST",
    ],
)
def profesor_editar(id_profesor):
    id_profe = request.form["id_profe"]
    nombre = request.form["nombre_profesor"]
    apellido = request.form["apellido_profesor"]
    id_colegio = request.form["id_colegio"]
    Profesor.update(id_profe, nombre, apellido, id_colegio)
    return redirect("/profesores")


@app.route("/profesores/eliminar/<id>/", methods=["POST"])
def eliminar_profesor(id):
    Profesor.deleted(id)
    return redirect("/profesores")


# CURSOS --------------------------------------------
@app.route("/cursos", methods=["GET"])
def cursos():
    cursos = Curso.get_all()
    return render_template("cursos.html", cursos=cursos)


@app.route("/cursos/crear/", methods=["GET"])
def cursos_crear_ver():
    colegios = Colegio.get_all()
    return render_template("crear-curso.html", colegios=colegios)


@app.route("/cursos/crear/", methods=["POST"])
def cursos_crear():
    name = request.form.get("curso_name")
    colegio_id = request.form.get("colegio")
    Curso.insert_curso(name, colegio_id)
    return redirect("/cursos")


@app.route(
    "/cursos/editar/<id_curso>/",
    methods=[
        "GET",
    ],
)
def mostrar_cursos_editar(id_curso):
    curso = Curso.select_one(id_curso)
    return render_template("cursos-editar.html", curso=curso[0])


@app.route(
    "/cursos/editar/<id_curso>/",
    methods=[
        "POST",
    ],
)
def curso_editar(id_curso):
    nombre = request.form["nombre_curso"]
    id_curso = request.form["id_curso"]
    Curso.update(id_curso, nombre)
    return redirect("/cursos")


@app.route("/cursos/eliminar/<id>/", methods=["POST"])
def eliminar_curso(id):
    Curso.deleted(id)
    return redirect("/cursos")


# ALUMNOS ----------------------------------------------------------------
@app.route("/alumnos", methods=["GET"])
def alumnos():
    alumnos = Alumno.get_all()
    return render_template("alumnos.html", alumnos=alumnos)


@app.route("/alumnos/crear/", methods=["GET"])
def alumnos_crear_ver():
    cursos = Curso.get_all()
    return render_template("crear-alumno.html", cursos=cursos)


@app.route("/alumnos/crear/", methods=["POST"])
def alumnos_crear():
    name = request.form.get("alumno_name")
    lastname = request.form.get("alumno_lastname")
    curso_id = request.form.get("curso")
    Alumno.insert_alumno(name, lastname, curso_id)
    return redirect("/alumnos")


@app.route(
    "/alumnos/editar/<id_alumnos>/",
    methods=[
        "GET",
    ],
)
def mostrar_alumnos_editar(id_alumnos):
    alumno = Alumno.select_one(id_alumnos)
    cursos = Curso.get_all()
    return render_template("alumnos-editar.html", alumno=alumno[0], cursos=cursos)


@app.route(
    "/alumnos/editar/<id_alumnos>/",
    methods=[
        "POST",
    ],
)
def alumnos_ediar(id_alumnos):
    nombre = request.form["nombre_alumno"]
    apellido = request.form["apellido_alumno"]
    id_alumno = request.form["id_alumno"]
    id_curso = request.form["id_curso"]
    Alumno.update(id_alumno, nombre, apellido, id_curso)
    return redirect("/alumnos")


@app.route("/alumnos/eliminar/<id>/", methods=["POST"])
def eliminar_alumno(id):
    Alumno.deleted(id)
    return redirect("/alumnos")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

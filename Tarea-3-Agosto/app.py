from flask import Flask, render_template, request, redirect
from models.colegio import Colegio
from models.profesor import Profesor
from models.curso import Curso
from models.alumno import Alumno
app = Flask(__name__)


def get_class(opcion):
    return {
        "colegios": Colegio, 
    }[opcion]
#GENERAL ---------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/<opcion>/', methods=['post'])
def pre_select_one(opcion):
    search = request.form.get('response')
    print(opcion, search)
    return redirect(f'/{opcion}/{search}/')

@app.route('/<opcion>/<id>/', methods=['GET'])
def select_one(opcion, id):
    result = get_class(opcion).select_one(id)
    return render_template('select_one.html', result = result)
#COLEGIOS ---------------------------------------------
@app.route('/colegios', methods=['GET'])
def colegios():
    colegio = Colegio.get_all()
    return render_template('colegio.html', colegios=colegio)

@app.route('/colegios/crear/', methods=['GET'])
def colegios_crear_ver():
    return render_template('crear-colegio.html')

@app.route('/colegios/crear/', methods=['POST'])
def colegios_crear():
    name = request.form.get('colegio')
    Colegio.insert_colegio(name)
    return redirect('/')


#PROFESORES --------------------------------------------
@app.route('/profesores', methods=['GET'])
def profesores():
    profesores = Profesor.get_all()
    return render_template('profesores.html', profesores= profesores)

@app.route('/profesores/crear/', methods=['GET'])
def profesores_crear_ver():
    colegios = Colegio.get_all()
    return render_template('crear-profesor.html', colegios=colegios)

@app.route('/profesores/crear/', methods=['POST'])
def profesores_crear():
    name = request.form.get('profesor_name')
    lastname = request.form.get('profesor_lastname')
    colegio_id = request.form.get('colegio')
    Profesor.insert_profesor(name, lastname, colegio_id)
    return redirect('/profesores')

#CURSOS --------------------------------------------
@app.route('/cursos', methods=['GET'])
def cursos():
    cursos = Curso.get_all()
    return render_template('cursos.html', cursos=cursos)

@app.route('/cursos/crear/', methods=['GET'])
def cursos_crear_ver():
    colegios = Colegio.get_all()
    return render_template('crear-curso.html', colegios=colegios)

@app.route('/cursos/crear/', methods=['POST'])
def cursos_crear():
    name = request.form.get('curso_name')
    colegio_id = request.form.get('colegio')
    Curso.insert_curso(name, colegio_id)
    return redirect('/cursos')


#ALUMNOS ----------------------------------------------------------------
@app.route('/alumnos', methods=['GET'])
def alumnos():
    alumnos = Alumno.get_all()
    return render_template('alumnos.html', alumnos= alumnos)

@app.route('/alumnos/crear/', methods=['GET'])
def alumnos_crear_ver():
    cursos = Curso.get_all()
    return render_template('crear-alumno.html', cursos=cursos)

@app.route('/alumnos/crear/', methods=['POST'])
def alumnos_crear():
    name = request.form.get('alumno_name')
    lastname = request.form.get('alumno_lastname')
    curso_id = request.form.get('curso')
    Alumno.insert_alumno(name, lastname, curso_id)
    return redirect('/alumnos')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
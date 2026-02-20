from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

#realizar una interfaz con formulario y tabla para mostrar los usuarios que tenemos en la tabla de usuarios que tenemos arriba

API_URL = "http://127.0.0.1:8000/v1/usuarios/"

@app.route('/')
def inicio():
    #respuesta = requests.get(API_URL) nos ayuda a obtener los datos de la API y 
    # mostrarlos en la tabla de usuarios que tenemos en la interfaz de usuario que vamos a crear
    respuesta = requests.get(API_URL)
    #despues esta alinea nos ayuda a obtener los datos de la respuesta y mostrarlos en la
    # tabla de usuarios que tenemos en la interfaz de usuario que vamos a crear
    usuarios = respuesta.json().get("usuarios", [])
    #despues esta alinea nos ayuda a mostrar los datos de la tabla de usuarios que tenemos en la interfaz de usuario que vamos a crear
    return render_template('index.html', usuarios=usuarios)

#despues esta alinea nos ayuda a agregar un nuevo usuario a la tabla de usuarios que tenemos en la interfaz de usuario que vamos a crear
@app.route('/agregar', methods=['POST'])
#esta es la funcion que se encarga de agregar un nuevo usuario a la tabla de usuarios que tenemos en la interfaz de usuario que vamos a crear
def agregar():
    #despues esta alinea nos ayuda a obtener los datos del formulario que tenemos en la interfaz de usuario que vamos a crear
    nuevo_usuario = {
        "id": int(request.form["id"]),
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"])
    }
    
    #despues esta alinea nos ayuda a enviar los datos del nuevo usuario a la API para que se agregue a la tabla
    requests.post(API_URL, json=nuevo_usuario)
    #con esta linea solo tenemos 
    return redirect('/')

#esta linea nos ayuda a eliminar el usuario 
#lo que hace es que pide el id del usuario que queremos eliminar y luego envia una solicitud de eliminacion a la API para que se elimine el usuario de la tabla
@app.route('/eliminar/<int:id>', methods=['POST'])
#esta es la funcion que se encarga de eliminar el usuario
#la funcion es aliminar y dentro esta el id del usuario que queremos eliminar
def eliminar(id):
    #lo que haacemos aqui es mandar la solicitud de eliminar ala api 
    #la solicitud de eliminar es una solicitud de tipo delete y se envia a la url de la api con el id del usuario que queremos eliminar
    requests.delete(API_URL, json={"id": id})
    #despues simplemte volvemos a cargar la pagina 
    return redirect('/')


#actualizar un usuario
@app.route('/actualizar', methods=['POST'])

def actualizar():
    usuario_actualizado = {
        "id": int(request.form["id"]),
        "nombre": request.form["nombre"],
        "edad": int(request.form["edad"])
    }
    requests.put(API_URL, json=usuario_actualizado)
    return redirect('/')


 #Sección para configurar el puerto
if __name__ == '__main__':
    app.run(debug=True, port=5001)
    


    
    
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta_triseratops'

# --- SIMULACIÓN DE DATOS (MOCK DATA) ---
# Esta lista vive en la memoria del servidor mientras esté encendido
inventario = [
    {'id': 1, 'nombre': 'Placa de Video RTX 4060', 'precio': 450000, 'stock': 8},
    {'id': 2, 'nombre': 'Procesador Ryzen 7', 'precio': 320000, 'stock': 5},
    {'id': 3, 'nombre': 'Memoria RAM 16GB', 'precio': 85000, 'stock': 25}
]

@app.route('/')
def login():
    return render_template('auth/login.html')

@app.route('/verificar', methods=['POST'])
def verificar():
    user = request.form.get('usuario')
    pas = request.form.get('password')
    
    if user == 'admin' and pas == '123':
        session['rol'] = 'admin'
        return redirect(url_for('admin_panel'))
    elif user == 'cliente' and pas == '123':
        session['rol'] = 'cliente'
        return redirect(url_for('cliente_panel'))
    else:
        return redirect(url_for('login'))

# --- PANEL ADMINISTRADOR ---
@app.route('/admin')
def admin_panel():
    if 'rol' in session and session['rol'] == 'admin':
        # Le pasamos la lista de inventario al HTML
        return render_template('admin/dashboard.html', productos=inventario)
    return redirect(url_for('login'))

@app.route('/agregar', methods=['POST'])
def agregar():
    if 'rol' in session and session['rol'] == 'admin':
        # Creamos el nuevo diccionario con los datos del formulario
        nuevo_p = {
            'id': len(inventario) + 1, # Generamos un ID simple
            'nombre': request.form.get('nombre'),
            'precio': request.form.get('precio'),
            'stock': request.form.get('stock')
        }
        inventario.append(nuevo_p) # Lo sumamos a la lista global
    return redirect(url_for('admin_panel'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    if 'rol' in session and session['rol'] == 'admin':
        global inventario
        # Filtramos la lista para quitar el producto que coincida con el ID
        inventario = [p for p in inventario if p['id'] != id]
    return redirect(url_for('admin_panel'))

# --- PANEL CLIENTE ---
@app.route('/home')
def cliente_panel():
    if 'rol' in session and session['rol'] == 'cliente':
        # El cliente también ve la misma lista actualizada
        return render_template('client/home.html', productos=inventario)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
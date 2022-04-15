from flask import Blueprint, render_template, redirect, url_for
from models.inventario import Inventario  
from forms.inventarioForm import Nuevo_Producto
from flask_login import login_required, current_user
from utils.db import db

productos = Blueprint("productos", __name__, url_prefix="/products")

@productos.route("/")
@login_required
def home():
    lista_productos = Inventario.query.all()
    return render_template("inventario/home.html", items=lista_productos, user=current_user)

@productos.route("/new_product", methods=['GET', 'POST'])
@login_required
def NuevoProducto():
    form = Nuevo_Producto()
    if form.validate_on_submit():
        producto = form.producto.data
        existencia = form.existencia.data

        nuevoProducto = Inventario(producto, existencia)
        db.session.add(nuevoProducto)
        db.session.commit()
        return redirect(url_for("productos.home"))
    return render_template("inventario/nuevo.html", form=form, user=current_user)


@productos.route("/delete_product/<int:id_producto>")
@login_required
def EliminarProducto(id_producto):
    delete_producto = Inventario.query.get(id_producto)
    db.session.delete(delete_producto)
    db.session.commit()
    return redirect(url_for("productos.home"))
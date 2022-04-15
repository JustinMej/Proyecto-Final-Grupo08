from flask import Blueprint, render_template, redirect, url_for
from models.ventas import Venta
from models.inventario import Inventario
from forms.ventasForm import Nueva_Venta
from flask_login import login_required, current_user
from utils.db import db

ventas = Blueprint("ventas", __name__, url_prefix="/sales")

@ventas.route("/")
@login_required
def home():
    lista_ventas = Venta.query.all()
    return render_template("ventas/home.html", items=lista_ventas, user=current_user)



@ventas.route("/new_sale/<int:id_producto>", methods=['GET', 'POST'])
@login_required
def NuevaVenta(id_producto):
    nombre_producto = Inventario.query.get(id_producto)
    form = Nueva_Venta()
    if form.validate_on_submit():
        id_producto = id_producto
        cliente = form.cliente.data
        producto = nombre_producto.producto
        precio_unitario = form.precio_unitario.data
        cantidad = form.cantidad.data
        fecha = form.fecha.data
        total_venta = precio_unitario * cantidad

        nuevaVenta = Venta(id_producto, cliente, producto, precio_unitario, cantidad, fecha, total_venta)
        db.session.add(nuevaVenta)
        db.session.commit()
        return redirect(url_for("ventas.home"))
    return render_template("ventas/nuevo.html", form=form, user=current_user, id_producto=id_producto)


@ventas.route("/delete_sale/<int:id>")
@login_required
def EliminarVenta(id):
    delete_compra = Venta.query.get(id)
    db.session.delete(delete_compra)
    db.session.commit()
    return redirect(url_for("ventas.home"))
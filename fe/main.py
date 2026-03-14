import os

import httpx
from flask import Flask, flash, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


class RegistroForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(), Length(max=255)])
    email = StringField(
        "Correo electrónico", validators=[DataRequired(), Email(), Length(max=255)]
    )
    passw = PasswordField("Contraseña", validators=[DataRequired(), Length(max=255)])
    med_info = TextAreaField("Información médica (opcional)")
    submit = SubmitField("Crear cuenta")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        try:
            resp = httpx.post(
                f"{API_URL}/registro",
                json={
                    "name": form.name.data,
                    "email": form.email.data,
                    "passw": form.passw.data,
                    "med_info": form.med_info.data,
                },
                timeout=5,
            )
            if resp.status_code == 200:
                flash(
                    "¡Cuenta creada exitosamente! Redirigiendo al inicio de sesión...",
                    "success",
                )
                return render_template(
                    "registro.html", form=RegistroForm(), redirect_to=url_for("login")
                )
            else:
                try:
                    error = resp.json().get("detail", "Error al registrar.")
                except Exception:
                    error = "Error al registrar."
                flash(error, "error")
        except httpx.RequestError:
            flash("No se pudo conectar con el servidor. Inténtalo más tarde.", "error")
    return render_template("registro.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import httpx
from flask import Flask, flash, redirect, render_template, session, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


# ── Forms ────────────────────────────────────────────────────────────────────


class RegistroForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired(), Length(max=255)])
    email = StringField(
        "Correo electrónico", validators=[DataRequired(), Email(), Length(max=255)]
    )
    passw = PasswordField("Contraseña", validators=[DataRequired(), Length(max=255)])
    med_info = TextAreaField("Información médica (opcional)")
    submit = SubmitField("Crear cuenta")


class LoginForm(FlaskForm):
    email = StringField(
        "Correo electrónico", validators=[DataRequired(), Email(), Length(max=255)]
    )
    passw = PasswordField("Contraseña", validators=[DataRequired(), Length(max=255)])
    submit = SubmitField("Iniciar sesión")


# ── Auth helpers ─────────────────────────────────────────────────────────────


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = session.get("token")
        expires_at = session.get("expires_at")
        if not token:
            flash("Debes iniciar sesión para continuar.", "error")
            return redirect(url_for("login"))
        if expires_at:
            expiry = datetime.fromisoformat(expires_at)
            if datetime.now(timezone.utc) >= expiry:
                session.clear()
                flash("Tu sesión ha expirado. Inicia sesión nuevamente.", "error")
                return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated


# ── Routes ───────────────────────────────────────────────────────────────────


@app.route("/")
@login_required
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        name=session.get("name", "Usuario"),
        expires_at=session.get("expires_at"),
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("token"):
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            resp = httpx.post(
                f"{API_URL}/login",
                json={"email": form.email.data, "passw": form.passw.data},
                timeout=5,
            )
            if resp.status_code == 200:
                data = resp.json()
                expires_at = datetime.now(timezone.utc) + timedelta(
                    seconds=data["expires_in"]
                )
                session["token"] = data["access_token"]
                session["expires_at"] = expires_at.isoformat()
                session["name"] = data["name"]
                return redirect(url_for("dashboard"))
            else:
                try:
                    error = resp.json().get("detail", "Credenciales incorrectas.")
                except Exception:
                    error = "Credenciales incorrectas."
                flash(error, "error")
        except httpx.RequestError:
            flash("No se pudo conectar con el servidor. Inténtalo más tarde.", "error")
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión.", "success")
    return redirect(url_for("login"))


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
    # app.run(debug=True, port=5000)

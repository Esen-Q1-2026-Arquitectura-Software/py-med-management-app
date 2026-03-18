import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import httpx
from flask import Flask, flash, redirect, render_template, request, session, url_for
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


def parse_api_error(resp: httpx.Response, fallback: str) -> str:
    try:
        detail = resp.json().get("detail")
        if isinstance(detail, str) and detail.strip():
            return detail
    except Exception:
        pass
    return fallback


def auth_headers() -> dict[str, str]:
    token = session.get("token")
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


# ── Routes ───────────────────────────────────────────────────────────────────


@app.route("/")
@login_required
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    headers = auth_headers()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip()

        if action == "create_medico":
            payload = {
                "name": (request.form.get("name") or "").strip(),
                "email": (request.form.get("email") or "").strip(),
                "especialidad": (request.form.get("especialidad") or "").strip()
                or None,
            }
            if not payload["name"] or not payload["email"]:
                flash("Nombre y correo son obligatorios.", "error")
                return redirect(url_for("dashboard"))

            try:
                resp = httpx.post(
                    f"{API_URL}/medicos",
                    json=payload,
                    headers=headers,
                    timeout=5,
                )
                if resp.status_code == 200:
                    flash("Medico creado correctamente.", "success")
                else:
                    flash(parse_api_error(resp, "No se pudo crear el medico."), "error")
            except httpx.RequestError:
                flash("No se pudo conectar con el servidor. Intentalo mas tarde.", "error")
            return redirect(url_for("dashboard"))

        if action == "update_medico":
            medico_id = (request.form.get("medico_id") or "").strip()
            payload = {
                "name": (request.form.get("name") or "").strip(),
                "email": (request.form.get("email") or "").strip(),
                "especialidad": (request.form.get("especialidad") or "").strip()
                or None,
            }
            if not medico_id.isdigit():
                flash("El medico a actualizar es invalido.", "error")
                return redirect(url_for("dashboard"))
            if not payload["name"] or not payload["email"]:
                flash("Nombre y correo son obligatorios.", "error")
                return redirect(url_for("dashboard", edit=medico_id))

            try:
                resp = httpx.put(
                    f"{API_URL}/medicos/{medico_id}",
                    json=payload,
                    headers=headers,
                    timeout=5,
                )
                if resp.status_code == 200:
                    flash("Medico actualizado correctamente.", "success")
                else:
                    flash(
                        parse_api_error(resp, "No se pudo actualizar el medico."),
                        "error",
                    )
            except httpx.RequestError:
                flash("No se pudo conectar con el servidor. Intentalo mas tarde.", "error")
            return redirect(url_for("dashboard"))

        if action == "delete_medico":
            medico_id = (request.form.get("medico_id") or "").strip()
            if not medico_id.isdigit():
                flash("El medico a eliminar es invalido.", "error")
                return redirect(url_for("dashboard"))

            try:
                resp = httpx.delete(
                    f"{API_URL}/medicos/{medico_id}",
                    headers=headers,
                    timeout=5,
                )
                if resp.status_code == 200:
                    flash("Medico eliminado correctamente.", "success")
                else:
                    flash(parse_api_error(resp, "No se pudo eliminar el medico."), "error")
            except httpx.RequestError:
                flash("No se pudo conectar con el servidor. Intentalo mas tarde.", "error")
            return redirect(url_for("dashboard"))

        flash("Accion invalida.", "error")
        return redirect(url_for("dashboard"))

    medicos = []
    try:
        resp = httpx.get(f"{API_URL}/medicos", headers=headers, timeout=5)
        if resp.status_code == 200:
            medicos = resp.json()
        else:
            flash(parse_api_error(resp, "No se pudo cargar la lista de medicos."), "error")
    except httpx.RequestError:
        flash("No se pudo conectar con el servidor. Intentalo mas tarde.", "error")

    edit_id = request.args.get("edit", type=int)
    editing_medico = None
    if edit_id is not None:
        editing_medico = next((m for m in medicos if m.get("id") == edit_id), None)
        if editing_medico is None:
            flash("El medico que intentas editar no existe.", "error")

    return render_template(
        "dashboard.html",
        active_tab="medicos",
        name=session.get("name", "Usuario"),
        expires_at=session.get("expires_at"),
        medicos=medicos,
        editing_medico=editing_medico,
    )


@app.route("/citas", methods=["GET", "POST"])
@login_required
def citas():
    headers = auth_headers()

    if request.method == "POST":
        action = (request.form.get("action") or "").strip()

        if action == "create_cita":
            medico_id = (request.form.get("medico_id") or "").strip()
            fecha = (request.form.get("fecha") or "").strip()
            hora = (request.form.get("hora") or "").strip()
            motivo = (request.form.get("motivo") or "").strip() or None

            if not medico_id.isdigit() or not fecha or not hora:
                flash("Medico, fecha y hora son obligatorios.", "error")
                return redirect(url_for("citas", nueva="1"))

            try:
                resp = httpx.post(
                    f"{API_URL}/citas",
                    json={
                        "medicoId": int(medico_id),
                        "fecha": fecha,
                        "hora": hora,
                        "motivo": motivo,
                    },
                    headers=headers,
                    timeout=5,
                )
                if resp.status_code == 200:
                    flash("Cita creada correctamente.", "success")
                else:
                    flash(parse_api_error(resp, "No se pudo crear la cita."), "error")
            except httpx.RequestError:
                flash("No se pudo conectar con el servidor. Intentalo mas tarde.", "error")
            return redirect(url_for("citas"))

        flash("Accion invalida.", "error")
        return redirect(url_for("citas"))

    citas_list = []
    medicos = []
    try:
        resp = httpx.get(f"{API_URL}/citas", headers=headers, timeout=5)
        if resp.status_code == 200:
            citas_list = resp.json()
        else:
            flash(parse_api_error(resp, "No se pudo cargar las citas."), "error")

        resp_m = httpx.get(f"{API_URL}/medicos", headers=headers, timeout=5)
        if resp_m.status_code == 200:
            medicos = resp_m.json()
    except httpx.RequestError:
        flash("No se pudo conectar con el servidor. Intentalo mas tarde.", "error")

    show_nueva_cita = request.args.get("nueva") == "1"

    return render_template(
        "dashboard.html",
        active_tab="citas",
        name=session.get("name", "Usuario"),
        expires_at=session.get("expires_at"),
        citas=citas_list,
        medicos=medicos,
        show_nueva_cita=show_nueva_cita,
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

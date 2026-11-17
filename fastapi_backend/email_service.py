import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() == "true"


def send_password_reset_email(to_email: str, reset_url: str) -> None:
    """
    Envía el correo de recuperación de contraseña.

    Deliberadamente NO lanza excepciones hacia el llamador: se ejecuta
    en un BackgroundTask después de que la respuesta HTTP ya fue enviada,
    así que cualquier fallo de SMTP se registra en logs pero nunca
    revela al cliente si el envío tuvo éxito (evita filtrar si el
    email existe o no).
    """
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASSWORD:
        logger.error(
            "SMTP no configurado (faltan SMTP_HOST/SMTP_USER/SMTP_PASSWORD "
            "en el .env). No se pudo enviar el correo a %s", to_email
        )
        return

    subject = "Recupera tu contraseña"
    text_body = (
        "Recibimos una solicitud para restablecer tu contraseña.\n\n"
        f"Ingresa al siguiente enlace para continuar:\n{reset_url}\n\n"
        "Este enlace expira en 30 minutos. Si no solicitaste este cambio, "
        "puedes ignorar este correo."
    )
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 480px; margin: auto;">
        <h2>Recupera tu contraseña</h2>
        <p>Recibimos una solicitud para restablecer tu contraseña.</p>
        <p>
            <a href="{reset_url}"
               style="display:inline-block;padding:12px 20px;background:#1f6feb;
                      color:#fff;text-decoration:none;border-radius:8px;">
                Restablecer contraseña
            </a>
        </p>
        <p>Este enlace expira en 30 minutos. Si no solicitaste este cambio,
           puedes ignorar este correo.</p>
    </div>
    """

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SMTP_FROM
    message["To"] = to_email
    message.attach(MIMEText(text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            if SMTP_USE_TLS:
                server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM, [to_email], message.as_string())
        logger.info("Correo de recuperación enviado a %s", to_email)
    except Exception:
        logger.exception("Fallo al enviar correo de recuperación a %s", to_email)
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from api_client import ApiClient
from parser_ordenes import parse_orden


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ODOO_API_BASE_URL = os.getenv("ODOO_API_BASE_URL", "http://localhost:8070")

HELP_TEXT = (
    "Bot de socios EJ08. Ordenes soportadas:\n"
    "- Crear, nombre=\"nombre\",apellidos=\"apellidos\", num_socio=\"numerosocio\"\n"
    "- Modificar, nombre=\"nombre\",apellidos=\"apellidos\", num_socio=\"numerosocio\"\n"
    "- Consultar, num_socio=\"numerosocio\"\n"
    "- Borrar, num_socio=\"numerosocio\""
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    action, params, error = parse_orden(text)

    if action == "unsupported":
        await update.message.reply_text("Orden no soportada")
        return

    if action == "error":
        await update.message.reply_text(error)
        return

    client = ApiClient(ODOO_API_BASE_URL)

    if action == "crear":
        ok, msg, _ = client.crear_socio(
            params["nombre"], params["apellidos"], params["num_socio"]
        )
        await update.message.reply_text(msg)
        return

    if action == "modificar":
        ok, msg, _ = client.modificar_socio(
            params["nombre"], params["apellidos"], params["num_socio"]
        )
        await update.message.reply_text(msg)
        return

    if action == "borrar":
        ok, msg, _ = client.borrar_socio(params["num_socio"])
        await update.message.reply_text(msg)
        return

    if action == "consultar":
        ok, msg, data = client.consultar_socio(params["num_socio"])
        if not ok:
            await update.message.reply_text(msg)
            return

        record = data[0] if isinstance(data, list) and data else data
        num = record.get("num_socio", "")
        nombre = record.get("nombre", "")
        apellidos = record.get("apellidos", "")
        await update.message.reply_text(
            f"num_socio: {num}\nnombre: {nombre}\napellidos: {apellidos}"
        )


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("Falta TELEGRAM_BOT_TOKEN en variables de entorno")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()


if __name__ == "__main__":
    main()

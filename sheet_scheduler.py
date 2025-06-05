import os
import time
import smtplib
from email.mime.text import MIMEText

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule


# Path to the service account JSON file.
SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account_file.json")

# Spreadsheet ID or name.
SPREADSHEET_NAME = os.environ.get("GOOGLE_SPREADSHEET_NAME", "Stock de botellas")

# Email credentials for sending notifications.
EMAIL_USER = os.environ.get("NOTIFY_EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("NOTIFY_EMAIL_PASSWORD")
EMAIL_TO = os.environ.get("NOTIFY_EMAIL_TO")


def get_sheet():
    """Authenticate and return the first worksheet of the spreadsheet."""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open(SPREADSHEET_NAME)
    return spreadsheet.sheet1


def send_email_alert(subject: str, message: str) -> None:
    """Send an email notification."""
    if not (EMAIL_USER and EMAIL_PASSWORD and EMAIL_TO):
        print("Email credentials are not configured. Skipping notification.")
        return

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)


def check_stock_levels():
    """Check stock levels in the spreadsheet and send notifications."""
    worksheet = get_sheet()
    # Assumes the sheet has columns: SKU | Stock | Min | Max
    data = worksheet.get_all_records()

    for row in data:
        sku = row.get("SKU")
        stock = int(row.get("Stock", 0))
        min_stock = int(row.get("Min", 0))
        max_stock = int(row.get("Max", 0))
        if stock <= min_stock:
            send_email_alert(
                f"Stock bajo para {sku}",
                f"El stock actual es {stock} unidades, por debajo del mínimo de {min_stock}.",
            )
        elif stock >= max_stock:
            send_email_alert(
                f"Stock alto para {sku}",
                f"El stock actual es {stock} unidades, por encima del máximo de {max_stock}.",
            )


# Schedule the job every hour.
schedule.every().hour.do(check_stock_levels)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)

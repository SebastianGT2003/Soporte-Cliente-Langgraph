from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import base64
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from utils.state import Email


scopes = ['https://www.googleapis.com/auth/gmail.modify']

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def _get_header(headers, name):
    """Devuelve el valor de un encabezado (sin distinguir mayúsculas) o None."""
    return next(
        (h['value'] for h in headers if h.get('name', '').lower() == name.lower()),
        None,
    )


def _decode_body(data):
    """Decodifica el contenido base64url que entrega la API de Gmail."""
    if not data:
        return ''
    padded = data + '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded).decode('utf-8', errors='replace')


def _find_body(payload, mime_type):
    """Busca recursivamente la primera parte con el mime_type indicado."""
    if payload.get('mimeType') == mime_type:
        data = payload.get('body', {}).get('data')
        if data:
            return _decode_body(data)
    for part in payload.get('parts', []):
        body = _find_body(part, mime_type)
        if body:
            return body
    return ''


def _parse_date(headers, internal_date):
    """Convierte la fecha del correo a datetime.

    Usa el encabezado 'Date'; si falta o es inválido, usa 'internalDate'
    (milisegundos desde 1970, la hora en que Gmail recibió el correo).
    """
    raw = _get_header(headers, 'Date')
    if raw:
        try:
            return parsedate_to_datetime(raw)
        except (TypeError, ValueError):
            pass
    if internal_date:
        return datetime.fromtimestamp(int(internal_date) / 1000, tz=timezone.utc)
    return None


def parse_email(message) -> Email:
    payload = message.get('payload', {})
    headers = payload.get('headers', [])
    email_id = message.get('id')
    subject = _get_header(headers, 'Subject')
    sender = _get_header(headers, 'From')
    date = _parse_date(headers, message.get('internalDate'))

    # Prefiere texto plano; si el correo solo trae HTML, usa ese.
    body = _find_body(payload, 'text/plain') or _find_body(payload, 'text/html')
    if not body:
        body = _decode_body(payload.get('body', {}).get('data'))

    return Email(
        id=email_id,
        subject=subject or '',
        sender=sender or '',
        date=date.isoformat() if date else '',
        body=body or '',
    )


def get_most_recent_email() -> Email| None:
    service = get_gmail_service()
    today= datetime.now().date()
    query= f'after:{today.strftime("%Y/%m/%d")}'
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=1).execute()
        messages = results.get('messages', [])
        if not messages:
            return None
        message_id = messages[0]['id']
        message = service.users().messages().get(userId='me', id=message_id).execute()
        return parse_email(message)
    except Exception as e:
        print(f"Error occurred while fetching the most recent email: {e}")
        return None
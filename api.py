from fastapi import FastAPI
from fastapi.responses import Response
from urllib.parse import unquote
from utils import get_ical


app = FastAPI()

@app.get("/{prenom}")
def read_item(prenom):
    ical = get_ical(unquote(prenom))
    headers = {
        'Content-Disposition': f'attachment; filename="{prenom}.ics"'
    }
    return Response(ical, headers=headers)
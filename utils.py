import csv
import os
import requests
import vobject
import dateparser


def get_csv_url():
    DOCS_ID = os.environ.get('DOCS_ID')
    SHEET_ID = os.environ.get('SHEET_ID')
    return f'https://docs.google.com/spreadsheets/d/{DOCS_ID}/export?format=csv&gid={SHEET_ID}'



def get_ical(prenom):
    with requests.Session() as s:
        download = s.get(get_csv_url())
        decoded_content = download.content.decode('utf-8')

        cr = csv.DictReader(decoded_content.splitlines()[1:], delimiter=',')
        lignes = list(cr)

        if prenom not in lignes[0].keys():
            return None

        lignes = iter(lignes[2:])
        cal = vobject.iCalendar()
        cal.add('method').value = 'PUBLISH' # IE/Outlook needs this
        for ligne in lignes:
            if ligne[prenom]:
                emo, h_debut, h_fin = next(lignes)[prenom].replace('/ ', '').split(' ')
                debut = dateparser.parse(ligne[prenom] + h_debut)
                fin = dateparser.parse(ligne[prenom] + h_fin)
                vevent = cal.add('vevent')
                vevent.add('dtstart').value = debut
                vevent.add('dtend').value = fin
                vevent.add('summary').value = emo + 'Permanence Poupenn'
        icalstream = cal.serialize()

        return icalstream

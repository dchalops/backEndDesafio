import os, sys

# import telebot
# pip install python-telegram-bot
# import telegram

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pryinventario.settings')
application = get_wsgi_application()
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from django.db import transaction
from accounts.models import *

# TOKEN_TELEGRAM = '1239752846:AAE5DIDlCcUT5MFqHN339OV7G5UOK0rNhNM'
# tb = telegram.Bot(TOKEN_TELEGRAM)
# lista = ['1078235324',]

try:
    qsvotos = VotoPersonaPadron.objects.filter(persona__cab__id=2)
    total_empadronados = DetPersonaPadronElectoral.objects.filter(cab__id=2).count()
    total_validos = qsvotos.filter(tipo=1).count()
    total_blanco = qsvotos.filter(tipo=2).count()
    total_nulos = qsvotos.filter(tipo=3).count()
    total_ausentes = DetPersonaPadronElectoral.objects.filter(cab__id=2).exclude(id__in=qsvotos.values_list('persona__id', flat=True)).count()
    tab_ = TablaResultado(cab__id=2, empadronado=total_empadronados, ausentismo=total_ausentes, votovalido=total_validos, votoblanco=total_blanco, votonulo=total_nulos)
    tab_.save()
    listas_ = ListaElectoral.objects.filter(cab__id=2)
    for l in listas_:
        total_lista = qsvotos.filter(lista=l).count()
        subtab_ = SubTablaResultado(detallemesa=tab_, lista=l, totalvoto=total_lista)
        subtab_.save()
except Exception as ex:
    texto = 'ERROR AL GENERAR CORTE DE INVENTARIO\n {}\n Linea Error {}'.format(ex,sys.exc_info()[-1].tb_lineno)
    print(texto)

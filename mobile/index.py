import jwt
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from accounts.models import *


class IndexView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if 'action' in request.query_params:
            action = request.query_params['action']
            if action == 'vote':
                try:
                    userId = request.query_params.get('userId')
                    listaId = request.query_params.get('listaId')
                    detPer = DetPersonaPadronElectoral.objects.get(id=userId)
                    if VotoPersonaPadron.objects.filter(persona=detPer, cab=detPer.cab).exists():
                        raise NameError('Usted ya ejercio su derecho al voto')
                    else:
                        list_ = ListaElectoral.objects.get(id=listaId)
                        voto = VotoPersonaPadron(persona=detPer, tipo=list_.tipo, cab=detPer.cab, lista_id=listaId)
                        voto.save()
                    return Response({"success": True, "msg": "Voto registrado con éxito"}, status=status.HTTP_200_OK)
                except Exception as ex:
                    return Response({"success": False, "msg": str(ex)}, status=status.HTTP_200_OK)

            if action == 'loadListas':
                try:
                    cabid = request.query_params.get('cab')
                    listElectorales = ListaElectoral.objects.filter(cab__id=cabid).values('id', 'nombre', 'logo_file').order_by('nombre')
                    return Response({"success": True, "listElectorales": list(listElectorales)}, status=status.HTTP_200_OK)
                except Exception as ex:
                    return Response({"success": False, "msg": str(ex)}, status=status.HTTP_200_OK)

        return Response({"success": False, "msg": "Método no permitido"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

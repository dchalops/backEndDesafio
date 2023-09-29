from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import jwt
from django.conf import settings
from datetime import datetime, timedelta

from accounts.models import EventoElectoral, DetPersonaPadronElectoral, VotoPersonaPadron


class LoginView(APIView):
    permission_classes = [AllowAny]

    def generate_token(self, detpersona):
        payload = {
            'id': detpersona.id,
            'dni': detpersona.dni,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def post(self, request):
        try:
            data = request.data
            dni = data.get('dni')
            if EventoElectoral.objects.filter(fecha__lte=datetime.now().date()).exists():
                evento_ = EventoElectoral.objects.filter(fecha__lte=datetime.now().date()).first()
                if DetPersonaPadronElectoral.objects.filter(cab=evento_, dni__icontains=dni).exists():
                    detpersona_ = DetPersonaPadronElectoral.objects.filter(cab=evento_, dni__icontains=dni).first()
                    if VotoPersonaPadron.objects.filter(persona=detpersona_).exists():
                        raise NameError('Usted ya cuenta con un voto registrado')
                    token = self.generate_token(detpersona_)
                    user_data = {
                        'token': token,
                        'user': {
                            "id": detpersona_.id,
                            "cab": evento_.id,
                            "documento": detpersona_.dni,
                            "first_name": detpersona_.nombre,
                            "last_name": detpersona_.apellido,
                            "fullName": f"{detpersona_.nombre} {detpersona_.apellido}",
                            "canton": detpersona_.canton.nombre if detpersona_.canton else '',
                            "provincia": detpersona_.canton.provincia.nombre if detpersona_.canton else '',
                        }
                    }
                    return Response({"success": True, "data": user_data}, status=status.HTTP_200_OK)
                else:
                    raise NameError('Usted no forma parte del padron electoral')
            else:
                raise NameError('No existe evento electoral vigente')
        except Exception as ex:
            return Response({"success": False, "msg": str(ex)}, status=status.HTTP_200_OK)


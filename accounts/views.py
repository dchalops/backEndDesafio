from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import CustomUser, Canton, Provincia, VotoPersonaPadron,VotoPersonaPadron,TablaResultado,SubTablaResultado,ListaElectoral,EventoElectoral,DetPersonaPadronElectoral
from .serializers import UserSerializer, UserSerializerWithToken
from .serializers import CantonSerializer, ProvinciaSerializer, EventoSerializer
from django.db.models import Count, Sum
from django.http import JsonResponse
from .serializers import TablaResultadoSerializer
from django.shortcuts import get_object_or_404

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]
    authentication_classes = []

    def post(self, request):
        data = request.data
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        documento = data.get('documento')
        email = data.get('email')
        password = data.get('password')
        messages = {'errors': []}
        if first_name == None:
            messages['errors'].append('Nombre no puede estar vacío')
        if last_name == None:
            messages['errors'].append('Apellido no puede estar vacío')
        if documento == None:
            messages['errors'].append('Documento no puede estar vacío')
        if email == None:
            messages['errors'].append('El correo electrónico no puede estar vacío')
        if password == None:
            messages['errors'].append('La contraseña no puede estar vacía')
        if CustomUser.objects.filter(email=email).exists():
            messages['errors'].append(
                "La cuenta ya existe con esta identificación de correo electrónico.")
        if len(messages['errors']) > 0:
            return Response({"detail": messages['errors']}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.create(
                first_name=first_name,
                last_name=last_name,
                documento=documento,
                email=email,
                password=make_password(password)
            )
            current_site = get_current_site(request)
            mail_subject = 'El enlace de activación ha sido enviado a su id de correo electrónico'
            tokenSerializer = UserSerializerWithToken(user, many=False)

            # Next version will add a HTML template
            #message = "Confirme su email {}/api/v1/accounts/confirmation{}/{}/".format(current_site, tokenSerializer.data['refresh'], user.id)
            #to_email = email
            #send_mail(
            #        mail_subject, message, "d.chalops@gmail.com", [to_email]
            #)
            serializer = UserSerializerWithToken(user, many=False)
        except Exception as e:
            print(e)
            return Response({'detail': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

from django.http import HttpResponse
import datetime
import jwt
from config import settings

@api_view(['GET'])
def confirmation(request, pk, uid):
    user = CustomUser.objects.get(id=uid)
    token = jwt.decode(pk, settings.SECRET_KEY, algorithms=["HS256"])

    if user.isVerified == False and datetime.datetime.fromtimestamp(token['exp']) > datetime.datetime.now():
        user.isVerified = True
        user.save()
        return HttpResponse('Your account has been activated')

    elif (datetime.datetime.fromtimestamp(token['exp']) < datetime.datetime.now()):

        # For resending confirmation email use send_mail with the following encryption
        # print(jwt.encode({'user_id': user.user.id, 'exp': datetime.datetime.now() + datetime.timedelta(days=1)}, settings.SECRET_KEY, algorithm='HS256'))
        
        return HttpResponse('Your activation link has been expired')
    else:
        return HttpResponse('Your account has already been activated')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(ReadOnlyModelViewSet):
    throttle_classes = [UserRateThrottle]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]


@api_view(['GET'])
def cantones(request, provincia_id):
    if request.method == 'GET':
        try:
            
            cantones = Canton.objects.filter(provincia_id=provincia_id)
            
            serializer = CantonSerializer(cantones, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Canton.DoesNotExist:
            return Response({"message": "No se encontraron cantones para la provincia especificada."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def provincias(request):
    if request.method == 'GET':
        procincias = Provincia.objects.all()
        serializer = ProvinciaSerializer(procincias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def resultados_votos(request):
    evento_electoral_id = request.GET.get('evento_electoral_id', None)
    canton_name = request.GET.get('canton', None)

    queryset_resultados = TablaResultado.objects.all()

    if evento_electoral_id is not None:
        
        queryset_resultados = queryset_resultados.filter(cab_id=evento_electoral_id)

    eventos = EventoElectoral.objects.all()

    resultados_por_evento = []

    for evento in eventos:
        resultados_evento = queryset_resultados.filter(cab=evento)

        if canton_name is not None:
            #resultados_evento = resultados_evento.filter(canton__nombre=canton_name)
            resultados_evento = resultados_evento.filter(cab__detpersonapadronelectoral__canton__nombre=canton_name)

        totals = resultados_evento.aggregate(
            total_empadronado=Sum('empadronado'),
            total_ausentismo=Sum('ausentismo'),
            total_voto_valido=Sum('votovalido'),
            total_voto_nulo=Sum('votonulo'),
            total_voto_blanco=Sum('votoblanco')
        )

        # Filtrar los resultados por evento con valores no nulos en los campos deseados
        if all(value is not None for value in totals.values()):
            listas = ListaElectoral.objects.filter(cab=evento)

            votos_por_lista = []

            for lista in listas:
                total_votos_lista = SubTablaResultado.objects.filter(lista=lista, detallemesa__cab=evento).aggregate(total=Sum('totalvoto'))['total'] or 0

                votos_por_lista.append({
                    "lista": lista.nombre,
                    "total_votos": total_votos_lista,
                })

            resultado_evento = {
                "evento_electoral": evento.nombre,
                "total_empadronado": totals.get("total_empadronado", 0),
                "total_ausentismo": totals.get("total_ausentismo", 0),
                "total_voto_valido": totals.get("total_voto_valido", 0),
                "total_voto_nulo": totals.get("total_voto_nulo", 0),
                "total_voto_blanco": totals.get("total_voto_blanco", 0),
                "votos_por_lista": votos_por_lista
            }

            resultados_por_evento.append(resultado_evento)

    response_data = {
        "resultados_por_evento": resultados_por_evento
    }

    return JsonResponse(response_data)



@api_view(['GET'])
def eventos(request):
    if request.method == 'GET':
        procincias = EventoElectoral.objects.all()
        serializer = EventoSerializer(procincias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



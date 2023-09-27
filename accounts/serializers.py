from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Canton, Provincia, SubTablaResultado, TablaResultado, EventoElectoral

class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    avatarUrl = serializers.ImageField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    isVerified = serializers.BooleanField(read_only=True)
    status = serializers.CharField(read_only=True)
    documento = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    company = serializers.CharField(read_only=True)

    def get_name(self, obj):
        return str(obj.first_name + " " + obj.last_name)


class UserSerializerWithToken(UserSerializer):
    email = serializers.EmailField(read_only=True)
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)

    def get_access(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token)

class CantonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canton
        fields = '__all__'

class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoElectoral
        fields = '__all__'

class SubTablaResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTablaResultado
        fields = '__all__'

class TablaResultadoSerializer(serializers.ModelSerializer):
    sub_resultados = SubTablaResultadoSerializer(many=True, source="adicional")

    class Meta:
        model = TablaResultado
        fields = ['empadronado', 'ausentismo', 'votovalido', 'votonulo', 'votoblanco', 'sub_resultados']
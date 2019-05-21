# Nemo me impune lacessit
from rest_framework.serializers import ModelSerializer
from core.models import PontoTuristico

# Serializers cuidam da conversão de tipos ente valores do
# banco de dados para Python e para o formato de transmissão
# web a ser utilizado (ex.: JSON)

class PontoTuristicoSerializer(ModelSerializer):
    class Meta:
        model = PontoTuristico
        fields = ('id', 'nome', 'descricao', 'aprovado', 'foto')

    
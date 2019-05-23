# Nemo me impune lacessit
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from core.models import PontoTuristico
from atracoes.api.serializers import AtracaoSerializer
from enderecos.api.serializers import EnderecoSerializer

# Serializers cuidam da conversão de tipos ente valores do
# banco de dados para Python e para o formato de transmissão
# web a ser utilizado (ex.: JSON)

class PontoTuristicoSerializer(ModelSerializer):

    atracoes = AtracaoSerializer(many=True)
    endereco = EnderecoSerializer()
    # 'descricao_completa' é um campo somente-leitura definido
    # com SerializerMethodField. Ele não está definido no modelo
    # do banco de dados, mas é útil para reunir em um campo 
    # informações que podem ser calculadas/reunidas na requisição
    descricao_completa = SerializerMethodField()

    class Meta:
        model = PontoTuristico
        fields = (
            'id',
            'nome',
            'descricao',
            'aprovado',
            'foto',
            'atracoes',
            'comentarios',
            'endereco',
            'descricao_completa',
            'descricao_completa2',
        )

    def get_descricao_completa(self, objeto):
        return '%s - %s' % (objeto.nome, objeto.descricao)

# Nemo me impune lacessit
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from core.models import PontoTuristico, DocIdentificacao
from atracoes.models import Atracao
from enderecos.models import Endereco
from atracoes.api.serializers import AtracaoSerializer
from enderecos.api.serializers import EnderecoSerializer
from comentarios.api.serializers import ComentarioSerializer
from avaliacoes.api.serializers import AvaliacaoSerializer

# Serializers cuidam da conversão de tipos ente valores do
# banco de dados para Python e para o formato de transmissão
# web a ser utilizado (ex.: JSON)

class DocIdentificacaoSerializer(ModelSerializer):
    class Meta:
        model = DocIdentificacao
        fields = '__all__'


class PontoTuristicoSerializer(ModelSerializer):

    atracoes = AtracaoSerializer(many=True)
    endereco = EnderecoSerializer()
    doc_identificacao = DocIdentificacaoSerializer()
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
            'avaliacoes',
            'endereco',
            'descricao_completa', # SerializerMethodField
            'descricao_completa2', # @property em models.PontoTuristico
            'doc_identificacao',
        )
        read_only_fields = ('comentarios', 'avaliacoes',)

    def get_descricao_completa(self, objeto):
        return '%s - %s' % (objeto.nome, objeto.descricao)

    # Sobrescrevendo o método create do SERIALIZER para que ele suporte
    # a escrita de campos aninhados
    def create(self, validated_data):
        """
            Obtém os dados referentes aos relacionamentos many-to-many,
            one-to-one e one-to-many e os remove de validated_data.
            Cria então um objeto de Ponto Turístico sem nenhuma esses
            dados e os passa para funções auxiliares que vão criar os
            objetos correspondentes e associá-los ao ponto criado.
        """
        atracoes = validated_data['atracoes']
        del validated_data['atracoes']

        endereco = validated_data['endereco']
        del validated_data['endereco']

        doc_identificacao = validated_data['doc_identificacao']
        del validated_data['doc_identificacao']

        # Criando o ponto turístico e adicionando as atrações
        ponto = PontoTuristico.objects.create(**validated_data)
        self.cria_atracoes(atracoes, ponto)
        
        # Criando o registro de endereço e vinculando ao ponto
        end = Endereco.objects.create(**endereco)
        ponto.endereco = end

        # Criando o registro do documento de identificação e 
        # o vinculando ao ponto
        doc = DocIdentificacao.objects.create(**doc_identificacao)
        ponto.doc_identificacao = doc
        
        ponto.save()
        return ponto

    def cria_atracoes(self, atracoes, ponto):
        """
            Uma função auxiliar que recebe uma lista de dados de
            atrações, cria os objetos correspondentes e os associa
            ao ponto turístico que foi criado anteriormente.
        """
        for atracao in atracoes:
            at = Atracao.objects.create(**atracao)
            # adiciona a atração criada à tabela many-to-many,
            # vinculada ao ponto turístico dado
            ponto.atracoes.add(at)



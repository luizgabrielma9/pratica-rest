# Semper crescis aut decrescis

# Uma viewset é um agrupamento de views relacionadas
# a um recurso, por exemplo: listar, mostrar um objeto
# específico, apagar, substituir ou editar, etc.

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from core.models import PontoTuristico
from .serializers import PontoTuristicoSerializer
from django.shortcuts import get_object_or_404


class PontoTuristicoViewSet(ModelViewSet):
    """
        Uma viewset para gerenciar o banco de dados de
        pontos turísticos. 
    """
    # Permissão de acesso
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    permission_classes = (AllowAny,)
    authentication_classes = (TokenAuthentication,)

    # queryset = PontoTuristico.objects.all()
    serializer_class = PontoTuristicoSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('nome', 'descricao', 'endereco__linha1')
    # lookup_field = 'nome' # O padrão é o id do objeto

    # sobrescrito de ModelViewSet
    def get_queryset(self):
        # --- Filtrando a queryset devolvida com query strings ---
        # O get com opção None abaixo não levanta exceção
        # caso o usuário não tenha passado uma query_string

        # Obs.: Uma maneira de fazer isso automaticamente é com
        # o módulo externo DjangoFilterBackends, como descrito no
        # app atracoes

        id = self.request.query_params.get('id', None)
        nome = self.request.query_params.get('nome', None)
        descricao = self.request.query_params.get('descricao', None)
        aprovado = self.request.query_params.get('aprovado', None)
        queryset = PontoTuristico.objects.all()

        if id:
            queryset = PontoTuristico.objects.filter(pk=id)
        if nome:
            queryset = queryset.filter(nome__iexact=nome)
        if descricao:
            queryset = queryset.filter(descricao__iexact=descricao)
        if aprovado:
            queryset = queryset.filter(aprovado=aprovado)

        # return PontoTuristico.objects.filter(aprovado=True).order_by('id')
        return queryset

    # sobrescrito de ModelViewSet
    # HTTP GET geral
    def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
        
    #     if queryset.exists():
    #         serializer = PontoTuristicoSerializer(queryset, many=True)
    #         return Response(serializer.data)
    #     else:
    #         return Response(status=200, data=[])
        print('##### ' + str(request.user) + ' #####')
        return super(PontoTuristicoViewSet, self).list(request, *args, **kwargs)

    # HTTP POST
    # Assim como está, simula o comportamento padrão do
    # método create (não da melhor forma, provavelmente)
    def create(self, request, *args, **kwargs):
        # serializer = PontoTuristicoSerializer(data=request.data)
        
        # if serializer.is_valid():
        #     ponto_turistico = PontoTuristico.objects.create(**serializer.data)
        #     ponto_turistico.save()
        #     return Response(serializer.data, status=201)
        # else:
        #     return Response(serializer.errors, status=400)
        return super(PontoTuristicoViewSet, self).create(request, *args, **kwargs)

    # Comportamento alterado para apenas marcar o campo
    # 'aprovado' como False
    # HTTP DELETE
    def destroy(self, request, *args, **kwargs):
        # ponto_turistico = get_object_or_404(PontoTuristico, pk=kwargs['pk'])
        # ponto_turistico.aprovado = False
        # ponto_turistico.save()
        # return Response(status=204)
        return super(PontoTuristicoViewSet, self).destroy(request, *args, **kwargs)

    # HTTP GET específico
    def retrieve(self, request, *args, **kwargs):
        # ponto_turistico = self.get_queryset().filter(pk=pk)
        
        # if ponto_turistico.exists():
        #     serializer = PontoTuristicoSerializer(ponto_turistico.last())
        #     return Response(serializer.data)
        # else:
        #     return Response(status=404)
        return super(PontoTuristicoViewSet, self).retrieve(request, *args, **kwargs)
    
    # HTTP PUT
    def update(self, request, *args, **kwargs):
        # ponto_turistico = self.get_queryset().filter(pk=kwargs['pk'])

        # if ponto_turistico.exists():
        #     serializer = PontoTuristicoSerializer(data=request.data)

        #     if serializer.is_valid():
        #         PontoTuristico.objects.filter(pk=kwargs['pk']).update(**serializer.validated_data)
        #         return Response(status=200, data=serializer.validated_data)
        #     else:
        #         return Response(serializer.errors, status=400)
        # else:
        #     return Response(status=404)
        return super(PontoTuristicoViewSet, self).update(request, *args, **kwargs)

    # HTTP PATCH
    def partial_update(self, request, *args, **kwargs):
        # ponto_turistico = self.get_queryset().filter(pk=kwargs['pk'])
        
        # if ponto_turistico.exists():
        #     serializer = PontoTuristicoSerializer(data=request.data, partial=True)

        #     if serializer.is_valid():
        #         PontoTuristico.objects.filter(pk=kwargs['pk']).update(**serializer.validated_data)
        #         return Response(status=200, data=serializer.validated_data)
        #     else:
        #         return Response(serializer.errors, status=400)
        # else:
        #     return Response(status=404)
        return super(PontoTuristicoViewSet, self).partial_update(request, *args, **kwargs)

    # Actions personalizadas
    @action(methods=['get', 'post'], detail=True)
    def denunciar(self, request, pk=None):
        if request.method == 'POST':
            return Response(status=200, data=[
                'ALL THESE WORLDS ARE YOURS\n'
                'EXCEPT EUROPA\n'
                'ATTEMPT NO LANDING THERE'
            ])
        elif request.method == 'GET':
            return Response(status=200, data=[
                'The thing is hollow. It goes on forever, and '
                '- oh my God - it\'s full of stars!'
            ])

    @action(methods=['post'], detail=True)
    def associa_atracoes(self, request, pk):
        atracoes = request.data['ids']
        ponto = PontoTuristico.objects.get(id=pk)
        ponto.atracoes.set(atracoes)
        ponto.save()
        return Response(status=201, data=["OK"])
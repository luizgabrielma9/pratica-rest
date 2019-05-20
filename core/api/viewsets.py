# Semper crescis aut decrescis

# Uma viewset é um agrupamento de views relacionadas
# a um recurso, por exemplo: listar, mostrar um objeto
# específico, apagar, substituir ou editar, etc.

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from core.models import PontoTuristico
from .serializers import PontoTuristicoSerializer
from django.shortcuts import get_object_or_404

class PontoTuristicoViewSet(ModelViewSet):
    """
        Uma viewset para gerenciar o banco de dados de
        pontos turísticos. 
    """
    # queryset = PontoTuristico.objects.all()
    serializer_class = PontoTuristicoSerializer

    # sobrescrito de ModelViewSet
    def get_queryset(self):
        return PontoTuristico.objects.filter(aprovado=True)

    # sobrescrito de ModelViewSet
    # Aparentetemente, o método list tem prioridade sobre
    # o get_queryset acima
    # HTTP GET geral
    def list(self, request, *args, **kwargs):
    #     return Response({'de_quem_é': 'daquele que se foi'})
        queryset = PontoTuristico.objects.all().order_by('aprovado')
        serializer = PontoTuristicoSerializer(queryset, many=True)
        return Response(serializer.data)


    # HTTP POST
    def create(self, request, *args, **kwargs):
        # return Response({'de_quem_é': 'daquele que se foi'})
        ponto_turistico = PontoTuristico(
            nome=request.data['nome'],
            descricao=request.data['descricao'],
            aprovado=request.data['aprovado']
        )
        ponto_turistico.save()
        serializer = PontoTuristicoSerializer(ponto_turistico)
        return Response(serializer.data, status=201)

    # Comportamento alterado para apenas marcar o campo
    # aprovado como False
    # HTTP DELETE
    def destroy(self, request, *args, **kwargs):
        ponto_turistico = get_object_or_404(PontoTuristico, pk=kwargs['pk'])
        ponto_turistico.aprovado = False
        ponto_turistico.save()
        return Response(status=204)

    # HTTP GET específico
    def retrieve(self, request, pk=None):
        ponto_turistico = get_object_or_404(PontoTuristico, pk=pk)
        serializer = PontoTuristicoSerializer(ponto_turistico)
        return Response(serializer.data)


    # HTTP PUT
    def update(self, request, *args, **kwargs):
        pass

    # HTTP PATCH
    def partial_update(self, request, *args, **kwargs):
        pass

    
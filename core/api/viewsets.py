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
        # return PontoTuristico.objects.all()

    # sobrescrito de ModelViewSet
    # HTTP GET geral
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if queryset.exists():
            serializer = PontoTuristicoSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=200, data=[])

    # HTTP POST
    # Assim como está, simula o comportamento padrão do
    # método create (não da melhor forma, provavelmente)
    def create(self, request, *args, **kwargs):
        serializer = PontoTuristicoSerializer(data=request.data)
        
        if serializer.is_valid():
            ponto_turistico = PontoTuristico.objects.create(**serializer.data)
            ponto_turistico.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    # Comportamento alterado para apenas marcar o campo
    # 'aprovado' como False
    # HTTP DELETE
    def destroy(self, request, *args, **kwargs):
        ponto_turistico = get_object_or_404(PontoTuristico, pk=kwargs['pk'])
        ponto_turistico.aprovado = False
        ponto_turistico.save()
        return Response(status=204)

    # HTTP GET específico
    def retrieve(self, request, pk=None):
        ponto_turistico = self.get_queryset().filter(pk=pk)
        
        if ponto_turistico.exists():
            serializer = PontoTuristicoSerializer(ponto_turistico.last())
            return Response(serializer.data)
        else:
            return Response(status=404)

    # HTTP PUT
    def update(self, request, *args, **kwargs):
        ponto_turistico = self.get_queryset().filter(pk=kwargs['pk'])

        if ponto_turistico.exists():
            serializer = PontoTuristicoSerializer(data=request.data)

            if serializer.is_valid():
                PontoTuristico.objects.filter(pk=kwargs['pk']).update(**serializer.validated_data)
                return Response(status=200, data=serializer.validated_data)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response(status=404)

    # HTTP PATCH
    def partial_update(self, request, *args, **kwargs):
        ponto_turistico = self.get_queryset().filter(pk=kwargs['pk'])
        
        if ponto_turistico.exists():
            serializer = PontoTuristicoSerializer(data=request.data, partial=True)

            if serializer.is_valid():
                PontoTuristico.objects.filter(pk=kwargs['pk']).update(**serializer.validated_data)
                return Response(status=200, data=serializer.validated_data)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response(status=404)

    
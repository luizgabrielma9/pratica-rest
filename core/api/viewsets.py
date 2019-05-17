# Semper crescis aut decrescis

# Uma viewset é um agrupamento de views relacionadas
# a um recurso, por exemplo: listar, mostrar um objeto
# específico, apagar, substituir ou editar, etc.

from rest_framework.viewsets import ModelViewSet
from core.models import PontoTuristico
from .serializers import PontoTuristicoSerializer

class PontoTuristicoViewSet(ModelViewSet):
    """
        Uma viewset para gerenciar o banco de dados de
        pontos turísticos. 
    """
    queryset = PontoTuristico.objects.all()
    serializer_class = PontoTuristicoSerializer
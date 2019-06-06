"""pontos_turisticos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import views
from core.api.viewsets import PontoTuristicoViewSet
from atracoes.api.viewsets import AtracoesViewSet
from enderecos.api.viewsets import EnderecoViewSet
from comentarios.api.viewsets import ComentarioViewSet
from avaliacoes.api.viewsets import AvaliacaoViewSet
from django.conf import settings

# REST
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
router = routers.DefaultRouter()
# router.register(r'pontoturistico', PontoTuristicoViewSet, basename='PontoTuristico')
router.register(r'atracoes', AtracoesViewSet)
router.register(r'enderecos', EnderecoViewSet)
router.register(r'comentarios', ComentarioViewSet)
router.register(r'avaliacoes', AvaliacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token),
    path('pontoturistico/', PontoTuristicoViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('pontoturistico/<int:pk>/', PontoTuristicoViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update',
        'patch': 'partial_update',
    })),
    path('pontoturistico/<int:pk>/atracoes/', PontoTuristicoViewSet.as_view({
        'get': 'atracoes_ponto_turistico',
    })),
    path('pontoturistico/<int:pk>/atracoes/<int:pk_atracao>/',
        PontoTuristicoViewSet.as_view({
            'get': 'retrieve_atracao_ponto_turistico',
            'delete': 'apagar_atracao_ponto_turistico'
        })
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # 1. Rota de Autenticação do Django (login, logout, etc.)
    path('auth/', include('django.contrib.auth.urls')), 
    
    # 2. Rota para o Painel de Administração
    path('admin/', admin.site.urls),
    
    # 3. Inclui todas as URLs do seu aplicativo 'tarefas' (incluindo página inicial)
    path('', include('tarefas.urls')),
]

# Configuração para servir arquivos de mídia (uploads) em ambiente de desenvolvimento
if settings.DEBUG:
    # OBS: O padrão mais seguro é usar settings.MEDIA_ROOT
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

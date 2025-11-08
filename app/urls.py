from django.urls import path
from bot import views

app_name = 'bot'

urlpatterns = [
    # Status da API
    path('status/', views.status_api, name='status_api'),
    
    # Bot endpoints
    path('bot/chat/', views.BotChatView.as_view(), name='bot_chat'),
    
    # Cardápio endpoints
    path('cardapio/', views.CardapioListView.as_view(), name='cardapio_list'),
    path('cardapio/<int:id>/', views.PratoDetailView.as_view(), name='prato_detail'),
    path('buscar-prato/', views.BuscarPratoView.as_view(), name='buscar_prato'),
    path('categorias/', views.categorias_pratos, name='categorias_pratos'),
    
    # Pedidos endpoints
    path('calcular-pedido/', views.CalcularPedidoView.as_view(), name='calcular_pedido'),
    path('pedidos/', views.CriarPedidoView.as_view(), name='criar_pedido'),
    path('pedidos/listar/', views.PedidoListView.as_view(), name='listar_pedidos'),
    path('pedidos/<int:id>/', views.PedidoDetailView.as_view(), name='pedido_detail'),
    
    # Conversas endpoints
    path('conversas/', views.ConversaListView.as_view(), name='conversas_list'),
]

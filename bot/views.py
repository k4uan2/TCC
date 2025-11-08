from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import uuid
import sys
import os

# Adiciona o diretório do bot ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot_langchain.bot_restaurante_simples import BotRestauranteParaenseSimples
from .models import Prato, Conversa, Pedido, ItemPedido
from .serializers import (
    PratoSerializer, ConversaSerializer, PedidoSerializer,
    BotMensagemSerializer, BotRespostaSerializer, CalcularPedidoSerializer
)

class BotChatView(APIView):
    """View para interação com o bot"""
    
    def post(self, request):
        """Processa mensagem do usuário e retorna resposta do bot"""
        serializer = BotMensagemSerializer(data=request.data)
        
        if serializer.is_valid():
            mensagem = serializer.validated_data['mensagem']
            sessao_id = serializer.validated_data.get('sessao_id', str(uuid.uuid4()))
            
            # Inicializa o bot
            bot = BotRestauranteParaenseSimples()
            
            # Processa a mensagem
            resultado = bot.processar_mensagem(mensagem)
            
            # Salva a conversa no banco
            conversa = Conversa.objects.create(
                sessao_id=sessao_id,
                mensagem_usuario=mensagem,
                resposta_bot=resultado['resposta'],
                intencao=resultado['intencao']
            )
            conversa.set_sugestoes(resultado.get('sugestoes', []))
            conversa.save()
            
            # Prepara resposta
            resposta_data = {
                'resposta': resultado['resposta'],
                'intencao': resultado['intencao'],
                'sugestoes': resultado.get('sugestoes', []),
                'status': resultado['status'],
                'sessao_id': sessao_id
            }
            
            return Response(resposta_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CardapioListView(generics.ListAPIView):
    """View para listar cardápio"""
    queryset = Prato.objects.filter(disponivel=True)
    serializer_class = PratoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        categoria = self.request.query_params.get('categoria', None)
        
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        return queryset

class PratoDetailView(generics.RetrieveAPIView):
    """View para detalhes de um prato específico"""
    queryset = Prato.objects.all()
    serializer_class = PratoSerializer
    lookup_field = 'id'

class BuscarPratoView(APIView):
    """View para buscar prato por nome"""
    
    def get(self, request):
        nome = request.query_params.get('nome', '')
        
        if not nome:
            return Response(
                {'erro': 'Parâmetro nome é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Inicializa o bot para usar sua função de busca
        bot = BotRestauranteParaenseSimples()
        resultado = bot.buscar_prato(nome)
        
        if resultado['encontrado']:
            # Busca o prato no banco de dados
            try:
                prato = Prato.objects.get(nome__icontains=nome)
                serializer = PratoSerializer(prato)
                return Response({
                    'encontrado': True,
                    'prato': serializer.data
                })
            except Prato.DoesNotExist:
                # Se não estiver no banco, retorna dados do bot
                return Response(resultado)
        else:
            return Response(resultado)

class CalcularPedidoView(APIView):
    """View para calcular total de um pedido"""
    
    def post(self, request):
        serializer = CalcularPedidoSerializer(data=request.data)
        
        if serializer.is_valid():
            itens = serializer.validated_data['itens']
            
            # Inicializa o bot para calcular
            bot = BotRestauranteParaenseSimples()
            resultado = bot.calcular_pedido(itens)
            
            return Response(resultado, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CriarPedidoView(APIView):
    """View para criar um novo pedido"""
    
    def post(self, request):
        sessao_id = request.data.get('sessao_id', str(uuid.uuid4()))
        itens = request.data.get('itens', [])
        observacoes = request.data.get('observacoes', '')
        
        if not itens:
            return Response(
                {'erro': 'Lista de itens não pode estar vazia'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calcula o pedido usando o bot
        bot = BotRestauranteParaenseSimples()
        calculo = bot.calcular_pedido(itens)
        
        if calculo['status'] != 'sucesso':
            return Response(calculo, status=status.HTTP_400_BAD_REQUEST)
        
        # Cria o pedido
        pedido = Pedido.objects.create(
            sessao_id=sessao_id,
            total=calculo['total'],
            observacoes=observacoes
        )
        pedido.set_itens(calculo['itens'])
        pedido.save()
        
        # Cria os itens do pedido
        for item_data in calculo['itens']:
            try:
                prato = Prato.objects.get(nome=item_data['nome'])
                ItemPedido.objects.create(
                    pedido=pedido,
                    prato=prato,
                    quantidade=item_data['quantidade'],
                    preco_unitario=item_data['preco_unitario']
                )
            except Prato.DoesNotExist:
                # Se o prato não existir no banco, continua sem criar o ItemPedido
                pass
        
        serializer = PedidoSerializer(pedido)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PedidoListView(generics.ListAPIView):
    """View para listar pedidos"""
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sessao_id = self.request.query_params.get('sessao_id', None)
        
        if sessao_id:
            queryset = queryset.filter(sessao_id=sessao_id)
        
        return queryset

class PedidoDetailView(generics.RetrieveUpdateAPIView):
    """View para detalhes e atualização de pedido"""
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    lookup_field = 'id'

class ConversaListView(generics.ListAPIView):
    """View para listar conversas"""
    queryset = Conversa.objects.all()
    serializer_class = ConversaSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sessao_id = self.request.query_params.get('sessao_id', None)
        
        if sessao_id:
            queryset = queryset.filter(sessao_id=sessao_id)
        
        return queryset.order_by('-timestamp')[:50]  # Últimas 50 conversas

@api_view(['GET'])
def status_api(request):
    """Endpoint para verificar status da API"""
    return Response({
        'status': 'online',
        'versao': '1.0.0',
        'descricao': 'API do Bot Restaurante Paraense',
        'endpoints': {
            'bot_chat': '/api/bot/chat/',
            'cardapio': '/api/cardapio/',
            'buscar_prato': '/api/buscar-prato/',
            'calcular_pedido': '/api/calcular-pedido/',
            'criar_pedido': '/api/pedidos/',
            'listar_pedidos': '/api/pedidos/',
            'conversas': '/api/conversas/',
        }
    })

@api_view(['GET'])
def categorias_pratos(request):
    """Endpoint para listar categorias de pratos"""
    categorias = Prato.CATEGORIAS
    return Response({
        'categorias': [{'valor': cat[0], 'nome': cat[1]} for cat in categorias]
    })

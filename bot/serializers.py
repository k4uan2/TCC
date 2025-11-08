from rest_framework import serializers
from bot.models import Prato, Conversa, Pedido, ItemPedido

class PratoSerializer(serializers.ModelSerializer):
    """Serializer para o model Prato"""
    ingredientes_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Prato
        fields = [
            'id', 'nome', 'categoria', 'ingredientes', 'ingredientes_list',
            'descricao', 'preco', 'tempo_preparo', 'disponivel',
            'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
    
    def get_ingredientes_list(self, obj):
        """Retorna ingredientes como lista"""
        return obj.get_ingredientes_list()

class ConversaSerializer(serializers.ModelSerializer):
    """Serializer para o model Conversa"""
    sugestoes_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversa
        fields = [
            'id', 'sessao_id', 'mensagem_usuario', 'resposta_bot',
            'intencao', 'sugestoes', 'sugestoes_list', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']
    
    def get_sugestoes_list(self, obj):
        """Retorna sugestões como lista"""
        return obj.get_sugestoes()

class ItemPedidoSerializer(serializers.ModelSerializer):
    """Serializer para o model ItemPedido"""
    prato_nome = serializers.CharField(source='prato.nome', read_only=True)
    
    class Meta:
        model = ItemPedido
        fields = [
            'id', 'prato', 'prato_nome', 'quantidade',
            'preco_unitario', 'subtotal', 'observacoes'
        ]
        read_only_fields = ['id', 'subtotal']

class PedidoSerializer(serializers.ModelSerializer):
    """Serializer para o model Pedido"""
    itens_list = serializers.SerializerMethodField()
    itens_pedido = ItemPedidoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Pedido
        fields = [
            'id', 'sessao_id', 'itens', 'itens_list', 'itens_pedido',
            'total', 'status', 'observacoes', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
    
    def get_itens_list(self, obj):
        """Retorna itens como lista"""
        return obj.get_itens()

class BotMensagemSerializer(serializers.Serializer):
    """Serializer para mensagens enviadas ao bot"""
    mensagem = serializers.CharField(max_length=1000)
    sessao_id = serializers.CharField(max_length=100, required=False)

class BotRespostaSerializer(serializers.Serializer):
    """Serializer para respostas do bot"""
    resposta = serializers.CharField()
    intencao = serializers.CharField()
    sugestoes = serializers.ListField(child=serializers.DictField(), required=False)
    status = serializers.CharField()
    sessao_id = serializers.CharField()

class CalcularPedidoSerializer(serializers.Serializer):
    """Serializer para calcular pedidos"""
    itens = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )
    
    def validate_itens(self, value):
        """Valida estrutura dos itens"""
        for item in value:
            if 'nome' not in item:
                raise serializers.ValidationError("Cada item deve ter um 'nome'")
            if 'quantidade' not in item:
                item['quantidade'] = 1
            else:
                try:
                    item['quantidade'] = int(item['quantidade'])
                    if item['quantidade'] <= 0:
                        raise ValueError()
                except (ValueError, TypeError):
                    raise serializers.ValidationError("Quantidade deve ser um número inteiro positivo")
        return value


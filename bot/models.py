from django.db import models
from django.contrib.auth.models import User
import json

class Prato(models.Model):
    """Model para representar os pratos do restaurante"""
    CATEGORIAS = [
        ('prato_principal', 'Prato Principal'),
        ('sobremesa', 'Sobremesa'),
        ('aperitivo', 'Aperitivo'),
        ('acompanhamento', 'Acompanhamento'),
    ]
    
    nome = models.CharField(max_length=100, unique=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    ingredientes = models.TextField(help_text="Lista de ingredientes separados por vírgula")
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    tempo_preparo = models.CharField(max_length=50)
    disponivel = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Prato"
        verbose_name_plural = "Pratos"
        ordering = ['categoria', 'nome']
    
    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"
    
    def get_ingredientes_list(self):
        """Retorna lista de ingredientes"""
        return [ing.strip() for ing in self.ingredientes.split(',')]
    
    def set_ingredientes_list(self, ingredientes_list):
        """Define ingredientes a partir de uma lista"""
        self.ingredientes = ', '.join(ingredientes_list)

class Conversa(models.Model):
    """Model para armazenar conversas com o bot"""
    sessao_id = models.CharField(max_length=100, db_index=True)
    mensagem_usuario = models.TextField()
    resposta_bot = models.TextField()
    intencao = models.CharField(max_length=50)
    sugestoes = models.TextField(blank=True, help_text="JSON com sugestões")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Conversa"
        verbose_name_plural = "Conversas"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Conversa {self.sessao_id} - {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
    
    def get_sugestoes(self):
        """Retorna sugestões como lista"""
        if self.sugestoes:
            try:
                return json.loads(self.sugestoes)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_sugestoes(self, sugestoes_list):
        """Define sugestões a partir de uma lista"""
        self.sugestoes = json.dumps(sugestoes_list, ensure_ascii=False)

class Pedido(models.Model):
    """Model para representar pedidos"""
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('preparando', 'Preparando'),
        ('pronto', 'Pronto'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    
    sessao_id = models.CharField(max_length=100, db_index=True)
    itens = models.TextField(help_text="JSON com itens do pedido")
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Pedido {self.id} - R$ {self.total} ({self.status})"
    
    def get_itens(self):
        """Retorna itens como lista"""
        if self.itens:
            try:
                return json.loads(self.itens)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_itens(self, itens_list):
        """Define itens a partir de uma lista"""
        self.itens = json.dumps(itens_list, ensure_ascii=False)

class ItemPedido(models.Model):
    """Model para representar itens individuais de um pedido"""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens_pedido')
    prato = models.ForeignKey(Prato, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    observacoes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
    
    def __str__(self):
        return f"{self.quantidade}x {self.prato.nome}"
    
    def save(self, *args, **kwargs):
        """Calcula subtotal automaticamente"""
        self.subtotal = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)

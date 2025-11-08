#!/usr/bin/env python3
"""
Teste da versão simplificada do bot 
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot_langchain.bot_restaurante_simples import BotRestauranteParaenseSimples

def testar_bot_simples():
    """Testa as funcionalidades básicas do bot simplificado"""
    print("=== Teste do Bot Restaurante Paraense (Versão Simplificada) ===\n")
    
    # Inicializa o bot
    bot = BotRestauranteParaenseSimples()
    
    # Teste 1: Saudação
    print("1. Teste de saudação:")
    resposta = bot.processar_mensagem("Olá! Boa tarde!")
    print(f"Resposta: {resposta['resposta']}")
    print(f"Intenção detectada: {resposta['intencao']}")
    print()
    
    # Teste 2: Cardápio
    print("2. Teste de solicitação do cardápio:")
    resposta = bot.processar_mensagem("Qual é o cardápio?")
    print(f"Resposta: {resposta['resposta']}")
    print(f"Intenção detectada: {resposta['intencao']}")
    print()
    
    # Teste 3: Sugestão
    print("3. Teste de pedido de sugestão:")
    resposta = bot.processar_mensagem("O que você recomenda?")
    print(f"Resposta: {resposta['resposta']}")
    print(f"Intenção detectada: {resposta['intencao']}")
    print()
    
    # Teste 4: Busca por prato específico
    print("4. Teste de busca por prato específico:")
    resposta = bot.processar_mensagem("Me fale sobre o tacacá")
    print(f"Resposta: {resposta['resposta']}")
    print(f"Intenção detectada: {resposta['intencao']}")
    print()
    
    # Teste 5: Preços
    print("5. Teste de consulta de preços:")
    resposta = bot.processar_mensagem("Quanto custam os pratos?")
    print(f"Resposta: {resposta['resposta']}")
    print(f"Intenção detectada: {resposta['intencao']}")
    print()
    
    # Teste 6: Pedido
    print("6. Teste de fazer pedido:")
    resposta = bot.processar_mensagem("Quero fazer um pedido")
    print(f"Resposta: {resposta['resposta']}")
    print(f"Intenção detectada: {resposta['intencao']}")
    print()
    
    # Teste 7: Cálculo de pedido
    print("7. Teste de cálculo de pedido:")
    pedido = [
        {"nome": "tacacá", "quantidade": 2},
        {"nome": "açaí", "quantidade": 1}
    ]
    resultado = bot.calcular_pedido(pedido)
    if resultado['status'] == 'sucesso':
        print(f"Total do pedido: R$ {resultado['total']:.2f}")
        for item in resultado['itens']:
            print(f"- {item['nome']}: {item['quantidade']}x R$ {item['preco_unitario']:.2f} = R$ {item['subtotal']:.2f}")
    print()

if __name__ == "__main__":
    testar_bot_simples()


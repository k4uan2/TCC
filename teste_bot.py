#!/usr/bin/env python3
"""
Teste básico do bot restaurante paraense
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot_langchain.bot_restaurante import BotRestauranteParaense

def testar_bot():
    """Testa as funcionalidades básicas do bot"""
    print("=== Teste do Bot Restaurante Paraense ===\n")
    
    # Inicializa o bot
    bot = BotRestauranteParaense()
    
    # Teste 1: Saudação
    print("1. Teste de saudação:")
    resposta = bot.processar_mensagem("Olá! Boa tarde!")
    print(f"Resposta: {resposta['resposta']}")
    print(f"Intenção detectada: {resposta['intencao']}")
    print()
    
    # Teste 2: Busca por prato específico
    print("2. Teste de busca por prato:")
    resultado = bot.buscar_prato("tacacá")
    if resultado['encontrado']:
        prato = resultado['prato']
        print(f"Prato encontrado: {prato['nome']}")
        print(f"Ingredientes: {', '.join(prato['ingredientes'])}")
        print(f"Preço: R$ {prato['preco']:.2f}")
    print()
    
    # Teste 3: Listagem do cardápio
    print("3. Teste de listagem do cardápio:")
    cardapio = bot.listar_cardapio()
    print(f"Total de pratos: {cardapio['total']}")
    for prato in cardapio['pratos'][:3]:  # Mostra apenas os 3 primeiros
        print(f"- {prato['nome']} ({prato['categoria']}) - R$ {prato['preco']:.2f}")
    print()
    
    # Teste 4: Cálculo de pedido
    print("4. Teste de cálculo de pedido:")
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
    
    # Teste 5: Pergunta sobre ingredientes
    print("5. Teste de pergunta sobre ingredientes:")
    resposta = bot.processar_mensagem("Quais são os ingredientes do tacacá?")
    print(f"Resposta: {resposta['resposta']}")
    print()

if __name__ == "__main__":
    testar_bot()


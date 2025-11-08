import os
import json
import re
from typing import Dict, List, Any
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pratos_paraenses import PRATOS_PARAENSES, get_pratos_por_categoria, get_prato_por_nome, get_pratos_por_ingrediente, get_pratos_por_preco

class BotRestauranteParaenseSimples:
    def __init__(self):
        """Inicializa o bot com respostas baseadas em regras"""
        self.saudacoes = [
            "Olá! Bem-vindo ao nosso restaurante paraense! 🌿",
            "Oi! Que bom ter você aqui! Como posso ajudar?",
            "Salve! Pronto para conhecer os sabores do Pará?"
        ]
        
        self.despedidas = [
            "Até logo! Volte sempre para saborear nossa culinária paraense!",
            "Tchau! Esperamos você em breve!",
            "Até mais! Que tal experimentar nossos pratos na próxima?"
        ]
        
    def processar_mensagem(self, mensagem_usuario: str) -> Dict[str, Any]:
        """Processa a mensagem do usuário e retorna resposta estruturada"""
        try:
            mensagem_lower = mensagem_usuario.lower()
            
            # Analisa a intenção do usuário
            intencao = self._analisar_intencao(mensagem_usuario)
            
            # Gera resposta baseada na intenção
            resposta = self._gerar_resposta(mensagem_usuario, intencao)
            
            # Gera sugestões
            sugestoes = self._gerar_sugestoes(mensagem_usuario, intencao)
            
            return {
                "resposta": resposta,
                "intencao": intencao,
                "sugestoes": sugestoes,
                "status": "sucesso"
            }
            
        except Exception as e:
            return {
                "resposta": "Desculpe, tive um problema para processar sua mensagem. Pode tentar novamente?",
                "intencao": "erro",
                "sugestoes": [],
                "status": "erro",
                "erro": str(e)
            }
    
    def _analisar_intencao(self, mensagem: str) -> str:
        """Analisa a intenção do usuário baseada na mensagem"""
        mensagem_lower = mensagem.lower()
        
        # Saudações
        if any(palavra in mensagem_lower for palavra in ['oi', 'olá', 'ola', 'bom dia', 'boa tarde', 'boa noite', 'salve']):
            return 'saudacao'
        
        # Despedidas
        elif any(palavra in mensagem_lower for palavra in ['tchau', 'até', 'obrigado', 'valeu', 'bye']):
            return 'despedida'
        
        # Sugestões
        elif any(palavra in mensagem_lower for palavra in ['sugerir', 'recomendar', 'indicar', 'o que', 'qual']):
            return 'sugestao'
        
        # Informações sobre pratos
        elif any(palavra in mensagem_lower for palavra in ['ingrediente', 'feito', 'como', 'receita', 'preparo']):
            return 'informacao'
        
        # Preços
        elif any(palavra in mensagem_lower for palavra in ['preço', 'custa', 'valor', 'quanto']):
            return 'preco'
        
        # Pedidos
        elif any(palavra in mensagem_lower for palavra in ['pedir', 'quero', 'comprar', 'pedido']):
            return 'pedido'
        
        # Cardápio
        elif any(palavra in mensagem_lower for palavra in ['cardápio', 'cardapio', 'menu', 'pratos', 'opções', 'opcoes']):
            return 'cardapio'
        
        # Busca por prato específico
        elif self._encontrar_prato_na_mensagem(mensagem):
            return 'busca_prato'
        
        else:
            return 'conversa'
    
    def _encontrar_prato_na_mensagem(self, mensagem: str) -> str:
        """Encontra nome de prato na mensagem"""
        mensagem_lower = mensagem.lower()
        for key, prato in PRATOS_PARAENSES.items():
            if prato['nome'].lower() in mensagem_lower or key in mensagem_lower:
                return key
        return None
    
    def _gerar_resposta(self, mensagem: str, intencao: str) -> str:
        """Gera resposta baseada na intenção"""
        
        if intencao == 'saudacao':
            return "Olá! Bem-vindo ao nosso restaurante paraense! 🌿 Aqui você encontra os melhores sabores da Amazônia. Como posso ajudar você hoje?"
        
        elif intencao == 'despedida':
            return "Muito obrigado pela visita! Volte sempre para saborear nossa deliciosa culinária paraense. Até logo! 😊"
        
        elif intencao == 'cardapio':
            pratos_principais = get_pratos_por_categoria('prato principal')
            sobremesas = get_pratos_por_categoria('sobremesa')
            
            resposta = "🍽️ **Nosso Cardápio Paraense:**\n\n"
            resposta += "**Pratos Principais:**\n"
            for key, prato in list(pratos_principais.items())[:4]:
                resposta += f"• {prato['nome']} - R$ {prato['preco']:.2f}\n"
            
            resposta += "\n**Sobremesas:**\n"
            for key, prato in list(sobremesas.items())[:2]:
                resposta += f"• {prato['nome']} - R$ {prato['preco']:.2f}\n"
            
            resposta += "\nQuer saber mais sobre algum prato específico?"
            return resposta
        
        elif intencao == 'sugestao':
            return """🌟 **Minhas recomendações especiais:**

1. **Tacacá** (R$ 12,00) - O prato mais tradicional do Pará! Servido quentinho na cuia com jambu que "dá choque" na boca.

2. **Pato no Tucumã** (R$ 35,00) - Uma iguaria amazônica! Pato cozido no tucumã, simplesmente irresistível.

3. **Açaí** (R$ 15,00) - O verdadeiro açaí paraense, cremoso e saboroso, do jeito que tem que ser!

Qual desses desperta seu interesse? Posso contar mais detalhes sobre qualquer um! 😋"""
        
        elif intencao == 'preco':
            resposta = "💰 **Nossos preços:**\n\n"
            resposta += "**Opções econômicas (até R$ 15):**\n"
            pratos_economicos = get_pratos_por_preco(15.00)
            for key, prato in list(pratos_economicos.items())[:3]:
                resposta += f"• {prato['nome']} - R$ {prato['preco']:.2f}\n"
            
            resposta += "\n**Pratos especiais:**\n"
            pratos_especiais = {k: v for k, v in PRATOS_PARAENSES.items() if v['preco'] > 15}
            for key, prato in list(pratos_especiais.items())[:3]:
                resposta += f"• {prato['nome']} - R$ {prato['preco']:.2f}\n"
            
            return resposta
        
        elif intencao == 'busca_prato':
            prato_key = self._encontrar_prato_na_mensagem(mensagem)
            if prato_key:
                prato = PRATOS_PARAENSES[prato_key]
                resposta = f"🍽️ **{prato['nome']}**\n\n"
                resposta += f"📝 {prato['descricao']}\n\n"
                resposta += f"🥘 **Ingredientes:** {', '.join(prato['ingredientes'])}\n"
                resposta += f"💰 **Preço:** R$ {prato['preco']:.2f}\n"
                resposta += f"⏱️ **Tempo de preparo:** {prato['tempo_preparo']}\n\n"
                resposta += "Que tal fazer seu pedido? É uma delícia! 😋"
                return resposta
        
        elif intencao == 'informacao':
            return """ℹ️ **Sobre nossa culinária paraense:**

Nossa cozinha é uma celebração dos sabores amazônicos! Usamos ingredientes frescos e típicos da região como:

🌿 **Jambu** - A erva que "dá choque" e é essencial no tacacá
🥥 **Tucumã** - Fruto amazônico rico e saboroso
🍤 **Camarão seco** - Tradicional da região
🌾 **Farinha de mandioca** - Acompanha quase tudo!

Cada prato conta uma história da nossa rica cultura amazônica. Qual prato você gostaria de conhecer melhor?"""
        
        elif intencao == 'pedido':
            return """🛒 **Vamos fazer seu pedido!**

Para pedir, me diga:
• Qual prato você escolheu?
• Quantas porções?
• Alguma observação especial?

Exemplo: "Quero 2 tacacás e 1 açaí"

Estou aqui para ajudar com seu pedido! 😊"""
        
        else:
            return """Olá! Sou seu assistente virtual especializado em culinária paraense! 🌿

Posso ajudar você com:
• 📋 Ver nosso cardápio completo
• 🌟 Sugestões de pratos
• ℹ️ Informações sobre ingredientes
• 💰 Consultar preços
• 🛒 Fazer pedidos

O que você gostaria de saber sobre nossa deliciosa comida paraense?"""
    
    def _gerar_sugestoes(self, mensagem: str, intencao: str) -> List[Dict[str, Any]]:
        """Gera sugestões baseadas na mensagem e intenção"""
        sugestoes = []
        
        if intencao == 'sugestao' or intencao == 'cardapio':
            # Sugere pratos populares
            pratos_populares = ['tacacá', 'açaí', 'pato_no_tucumã']
            for prato_key in pratos_populares:
                if prato_key in PRATOS_PARAENSES:
                    prato = PRATOS_PARAENSES[prato_key]
                    sugestoes.append({
                        'nome': prato['nome'],
                        'preco': prato['preco'],
                        'categoria': prato['categoria']
                    })
        
        elif intencao == 'preco':
            # Sugere pratos por faixa de preço
            pratos_economicos = get_pratos_por_preco(15.00)
            for key, prato in list(pratos_economicos.items())[:3]:
                sugestoes.append({
                    'nome': prato['nome'],
                    'preco': prato['preco'],
                    'categoria': prato['categoria']
                })
        
        return sugestoes
    
    def buscar_prato(self, nome_prato: str) -> Dict[str, Any]:
        """Busca informações específicas de um prato"""
        prato = get_prato_por_nome(nome_prato)
        if prato:
            return {
                "encontrado": True,
                "prato": prato,
                "status": "sucesso"
            }
        else:
            return {
                "encontrado": False,
                "mensagem": f"Não encontrei o prato '{nome_prato}' em nosso cardápio.",
                "status": "nao_encontrado"
            }
    
    def listar_cardapio(self, categoria: str = None) -> Dict[str, Any]:
        """Lista o cardápio completo ou por categoria"""
        try:
            if categoria:
                pratos = get_pratos_por_categoria(categoria)
                if not pratos:
                    return {
                        "pratos": [],
                        "mensagem": f"Não temos pratos na categoria '{categoria}'.",
                        "status": "categoria_vazia"
                    }
            else:
                pratos = PRATOS_PARAENSES
            
            cardapio = []
            for key, prato in pratos.items():
                cardapio.append({
                    "nome": prato["nome"],
                    "categoria": prato["categoria"],
                    "preco": prato["preco"],
                    "descricao": prato["descricao"],
                    "disponivel": prato["disponivel"]
                })
            
            return {
                "pratos": cardapio,
                "total": len(cardapio),
                "categoria": categoria,
                "status": "sucesso"
            }
            
        except Exception as e:
            return {
                "pratos": [],
                "mensagem": "Erro ao buscar cardápio.",
                "status": "erro",
                "erro": str(e)
            }
    
    def calcular_pedido(self, itens_pedido: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcula o total de um pedido"""
        try:
            total = 0
            itens_calculados = []
            
            for item in itens_pedido:
                nome_prato = item.get('nome', '')
                quantidade = item.get('quantidade', 1)
                
                prato = get_prato_por_nome(nome_prato)
                if prato:
                    subtotal = prato['preco'] * quantidade
                    total += subtotal
                    
                    itens_calculados.append({
                        "nome": prato["nome"],
                        "preco_unitario": prato["preco"],
                        "quantidade": quantidade,
                        "subtotal": subtotal
                    })
                else:
                    return {
                        "total": 0,
                        "itens": [],
                        "mensagem": f"Prato '{nome_prato}' não encontrado.",
                        "status": "prato_nao_encontrado"
                    }
            
            return {
                "total": total,
                "itens": itens_calculados,
                "quantidade_itens": len(itens_calculados),
                "status": "sucesso"
            }
            
        except Exception as e:
            return {
                "total": 0,
                "itens": [],
                "mensagem": "Erro ao calcular pedido.",
                "status": "erro",
                "erro": str(e)
            }


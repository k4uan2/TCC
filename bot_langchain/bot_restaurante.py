import os
import json
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pratos_paraenses import PRATOS_PARAENSES, get_pratos_por_categoria, get_prato_por_nome, get_pratos_por_ingrediente, get_pratos_por_preco

class BotRestauranteParaense:
    def __init__(self):
        """Inicializa o bot com configurações do LangChain"""
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=500
        )
        
        self.system_prompt = """
        Você é um assistente virtual especializado em culinária paraense, trabalhando para uma rede de restaurantes que serve comidas típicas do Pará, Brasil.

        Suas responsabilidades incluem:
        1. Sugerir pratos típicos paraenses baseados nas preferências do cliente
        2. Explicar ingredientes, modo de preparo e características dos pratos
        3. Atuar como vendedor, incentivando pedidos e oferecendo combos
        4. Responder dúvidas sobre a culinária amazônica
        5. Ser cordial, prestativo e conhecedor da cultura paraense

        Características importantes:
        - Use linguagem calorosa e acolhedora, típica da hospitalidade paraense
        - Sempre mencione os benefícios e sabores únicos dos pratos
        - Sugira acompanhamentos e bebidas quando apropriado
        - Seja proativo em oferecer alternativas se um prato não estiver disponível
        - Use expressões regionais quando apropriado (mas sem exagerar)

        Base de dados disponível: {pratos_info}
        """
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{user_input}")
        ])
        
        self.chain = self.prompt_template | self.llm
        
    def _format_pratos_info(self) -> str:
        """Formata informações dos pratos para o prompt"""
        pratos_info = []
        for key, prato in PRATOS_PARAENSES.items():
            info = f"""
            {prato['nome']} ({prato['categoria']}):
            - Ingredientes: {', '.join(prato['ingredientes'])}
            - Descrição: {prato['descricao']}
            - Preço: R$ {prato['preco']:.2f}
            - Tempo de preparo: {prato['tempo_preparo']}
            - Disponível: {'Sim' if prato['disponivel'] else 'Não'}
            """
            pratos_info.append(info)
        return '\n'.join(pratos_info)
    
    def processar_mensagem(self, mensagem_usuario: str) -> Dict[str, Any]:
        """Processa a mensagem do usuário e retorna resposta estruturada"""
        try:
            # Prepara o prompt com informações dos pratos
            pratos_info = self._format_pratos_info()
            
            # Invoca a chain do LangChain
            response = self.chain.invoke({
                "pratos_info": pratos_info,
                "user_input": mensagem_usuario
            })
            
            # Analisa a intenção do usuário para fornecer informações extras
            intencao = self._analisar_intencao(mensagem_usuario)
            sugestoes = self._gerar_sugestoes(mensagem_usuario, intencao)
            
            return {
                "resposta": response.content,
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
        
        if any(palavra in mensagem_lower for palavra in ['sugerir', 'recomendar', 'indicar', 'o que', 'qual']):
            return 'sugestao'
        elif any(palavra in mensagem_lower for palavra in ['ingrediente', 'feito', 'como', 'receita']):
            return 'informacao'
        elif any(palavra in mensagem_lower for palavra in ['preço', 'custa', 'valor', 'quanto']):
            return 'preco'
        elif any(palavra in mensagem_lower for palavra in ['pedir', 'quero', 'comprar', 'pedido']):
            return 'pedido'
        elif any(palavra in mensagem_lower for palavra in ['cardápio', 'menu', 'pratos', 'opções']):
            return 'cardapio'
        else:
            return 'conversa'
    
    def _gerar_sugestoes(self, mensagem: str, intencao: str) -> List[Dict[str, Any]]:
        """Gera sugestões baseadas na mensagem e intenção"""
        sugestoes = []
        
        if intencao == 'sugestao':
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
        
        elif intencao == 'cardapio':
            # Mostra categorias disponíveis
            categorias = set(prato['categoria'] for prato in PRATOS_PARAENSES.values())
            for categoria in categorias:
                pratos_categoria = get_pratos_por_categoria(categoria)
                sugestoes.append({
                    'categoria': categoria,
                    'quantidade': len(pratos_categoria)
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


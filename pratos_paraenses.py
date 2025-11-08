# Base de conhecimento dos pratos típicos do Pará

PRATOS_PARAENSES = {
    "açaí": {
        "nome": "Açaí",
        "categoria": "sobremesa",
        "ingredientes": ["açaí", "guaraná", "leite condensado", "granola", "banana", "morango"],
        "descricao": "Fruto típico da região amazônica, servido como vitamina ou na tigela com acompanhamentos",
        "preco": 15.00,
        "tempo_preparo": "10 minutos",
        "disponivel": True
    },
    "tacacá": {
        "nome": "Tacacá",
        "categoria": "prato principal",
        "ingredientes": ["tucumã", "camarão seco", "jambu", "broto de feijão", "farinha de mandioca", "pimenta de cheiro"],
        "descricao": "Prato típico servido em cuia, com caldo quente e sabor marcante do jambu",
        "preco": 12.00,
        "tempo_preparo": "20 minutos",
        "disponivel": True
    },
    "pato_no_tucumã": {
        "nome": "Pato no Tucumã",
        "categoria": "prato principal",
        "ingredientes": ["pato", "tucumã", "farinha de mandioca", "pimenta do reino", "alho", "cebola"],
        "descricao": "Prato tradicional com pato cozido no tucumã, acompanhado de farinha de mandioca",
        "preco": 35.00,
        "tempo_preparo": "45 minutos",
        "disponivel": True
    },
    "maniçoba": {
        "nome": "Maniçoba",
        "categoria": "prato principal",
        "ingredientes": ["folha de mandioca", "carne seca", "linguiça", "costela de porco", "toucinho", "feijão"],
        "descricao": "Prato que leva 7 dias para ficar pronto, feito com folhas de mandioca brava",
        "preco": 28.00,
        "tempo_preparo": "7 dias",
        "disponivel": True
    },
    "caruru": {
        "nome": "Caruru",
        "categoria": "prato principal",
        "ingredientes": ["quiabo", "camarão seco", "dendê", "amendoim", "castanha do pará", "pimenta malagueta"],
        "descricao": "Prato de origem africana adaptado na região amazônica",
        "preco": 22.00,
        "tempo_preparo": "30 minutos",
        "disponivel": True
    },
    "pirarucu_de_casaca": {
        "nome": "Pirarucu de Casaca",
        "categoria": "prato principal",
        "ingredientes": ["pirarucu", "banana da terra", "farinha de mandioca", "ovos", "azeitona", "pimentão"],
        "descricao": "Prato sofisticado com o famoso peixe amazônico em camadas",
        "preco": 45.00,
        "tempo_preparo": "40 minutos",
        "disponivel": True
    },
    "cupuaçu": {
        "nome": "Doce de Cupuaçu",
        "categoria": "sobremesa",
        "ingredientes": ["cupuaçu", "açúcar", "leite condensado"],
        "descricao": "Sobremesa cremosa feita com a fruta típica da Amazônia",
        "preco": 8.00,
        "tempo_preparo": "15 minutos",
        "disponivel": True
    },
    "tucumã": {
        "nome": "Tucumã",
        "categoria": "aperitivo",
        "ingredientes": ["tucumã", "farinha de mandioca", "sal"],
        "descricao": "Fruto amazônico servido com farinha de mandioca e sal",
        "preco": 10.00,
        "tempo_preparo": "5 minutos",
        "disponivel": True
    },
    "vatapá_paraense": {
        "nome": "Vatapá Paraense",
        "categoria": "prato principal",
        "ingredientes": ["camarão", "peixe", "leite de coco", "dendê", "farinha de trigo", "amendoim", "castanha do pará"],
        "descricao": "Versão paraense do vatapá, mais encorpado e com castanha do pará",
        "preco": 25.00,
        "tempo_preparo": "35 minutos",
        "disponivel": True
    },
    "farofa_de_banana": {
        "nome": "Farofa de Banana",
        "categoria": "acompanhamento",
        "ingredientes": ["farinha de mandioca", "banana da terra", "bacon", "cebola", "alho"],
        "descricao": "Acompanhamento tradicional feito com banana da terra e farinha de mandioca",
        "preco": 12.00,
        "tempo_preparo": "20 minutos",
        "disponivel": True
    }
}

CATEGORIAS = ["prato principal", "sobremesa", "aperitivo", "acompanhamento"]

def get_pratos_por_categoria(categoria):
    """Retorna pratos de uma categoria específica"""
    return {k: v for k, v in PRATOS_PARAENSES.items() if v["categoria"] == categoria}

def get_prato_por_nome(nome):
    """Busca um prato pelo nome"""
    nome_lower = nome.lower()
    for key, prato in PRATOS_PARAENSES.items():
        if nome_lower in prato["nome"].lower() or nome_lower in key:
            return prato
    return None

def get_pratos_por_ingrediente(ingrediente):
    """Busca pratos que contenham um ingrediente específico"""
    pratos_encontrados = {}
    ingrediente_lower = ingrediente.lower()
    
    for key, prato in PRATOS_PARAENSES.items():
        for ing in prato["ingredientes"]:
            if ingrediente_lower in ing.lower():
                pratos_encontrados[key] = prato
                break
    
    return pratos_encontrados

def get_pratos_por_preco(preco_max):
    """Retorna pratos até um preço máximo"""
    return {k: v for k, v in PRATOS_PARAENSES.items() if v["preco"] <= preco_max}


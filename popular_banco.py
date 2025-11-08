
"""
Script para popular o banco de dados com os pratos paraenses
"""

import os
import sys
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from bot.models import Prato
from pratos_paraenses import PRATOS_PARAENSES

def popular_pratos():
    """Popula o banco de dados com os pratos paraenses"""
    print("Populando banco de dados com pratos paraenses...")
    
    pratos_criados = 0
    pratos_atualizados = 0
    
    for key, dados_prato in PRATOS_PARAENSES.items():
        # Mapeia categoria do dicionário para o model
        categoria_map = {
            'prato principal': 'prato_principal',
            'sobremesa': 'sobremesa',
            'aperitivo': 'aperitivo',
            'acompanhamento': 'acompanhamento'
        }
        
        categoria = categoria_map.get(dados_prato['categoria'], 'prato_principal')
        
        # Verifica se o prato já existe
        prato, criado = Prato.objects.get_or_create(
            nome=dados_prato['nome'],
            defaults={
                'categoria': categoria,
                'ingredientes': ', '.join(dados_prato['ingredientes']),
                'descricao': dados_prato['descricao'],
                'preco': dados_prato['preco'],
                'tempo_preparo': dados_prato['tempo_preparo'],
                'disponivel': dados_prato['disponivel']
            }
        )
        
        if criado:
            pratos_criados += 1
            print(f"✓ Criado: {prato.nome}")
        else:
            # Atualiza dados se necessário
            prato.categoria = categoria
            prato.ingredientes = ', '.join(dados_prato['ingredientes'])
            prato.descricao = dados_prato['descricao']
            prato.preco = dados_prato['preco']
            prato.tempo_preparo = dados_prato['tempo_preparo']
            prato.disponivel = dados_prato['disponivel']
            prato.save()
            pratos_atualizados += 1
            print(f"↻ Atualizado: {prato.nome}")
    
    print(f"\n✅ Processo concluído!")
    print(f"📊 Pratos criados: {pratos_criados}")
    print(f"📊 Pratos atualizados: {pratos_atualizados}")
    print(f"📊 Total de pratos: {Prato.objects.count()}")

if __name__ == "__main__":
    popular_pratos()


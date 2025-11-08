Bot assistente para comidas típicas do Pará.

O bot funciona como um assistente virtual para um restaurante de comidas típicas do Pará. Ele pode sugerir pratos, explicar os ingredientes, informar preços e dar informações de contato, agindo como um vendedor digital.

## Tecnologias Utilizadas
- Python
- Django
- Langchain

## Como executar o projeto

```bash
# Clone o repositório
git clone https://github.com/k4uan2/TCC.git

# Entre na pasta do projeto

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Realize as migrações do banco de dados
python manage.py migrate

# Execute o servidor
python manage.py runserver

# Acesse no navegador
http://127.0.0.1:8000/

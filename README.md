## Desafio 
Sistema de autenticação e gerenciamento de dívidas

## Tecnologias Utilizadas
- Python
- Flask
- SQLAlchemy
- SQLite

## Como Executar

1. Clonar repositório:
    git clone https://github.com/ThaysDonatti/desafiopython

2. Navegar até o diretorio:
    cd nome-do-repositorio

3. Criação do ambiente virtual e ativação:
    python3 -m venv venv
    source venv/Scripts/activate

4. Dependências:
    pip install -r requirements.txt

5. Executar:
    python app.py

## Endpoints
- POST /cadastro - Cadastro de usuário
- POST /entrar - Login
- POST /sair - Logout
- GET /dividas - Listar dívidas
- POST /dividas - Adicionar dívida (para adms)
- GET /score - Buscar score cliente


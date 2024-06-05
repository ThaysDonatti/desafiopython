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
    cd desafiopython

3. Criação do ambiente virtual e ativação:
    python3 -m venv venv /
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

## ----------------------------------------------------------------
## Usuários Comuns
POST http://127.0.0.1:5000/cadastro
{
    "cpf": "11111111111",
    "nome": "Julia Souza",
    "nascimento": "1995-08-05",
    "email": "julia.souza@desafio.com",
    "senha": "senha123"
}

{
    "cpf": "22222222222",
    "nome": "Pedro Silva",
    "nascimento": "1989-10-20",
    "email": "pedro.silva@desafio.com",
    "senha": "senha456"
}

{
    "cpf": "33333333333",
    "nome": "Ana Figueredo",
    "nascimento": "1999-03-09",
    "email": "ana.fig@desafio.com",
    "senha": "senha678"
}


## Administrador
POST http://127.0.0.1:5000/cadastro
{
  "cpf": "99999999999",
  "nome": "Thays Silva",
  "nascimento": "1998-03-09",
  "email": "thays.silva@br.dominiox.com",
  "senha": "senha"
}

## Dívidas
POST http://127.0.0.1:5000/dividas -> User Admin
GET http://127.0.0.1:5000/dividas  -> User Comum
{ "valor": 195.0, "data_vencimento": "2024-02-01", "cpf_usuario": "11111111111"}
{ "valor": 345.0, "data_vencimento": "2024-05-11", "cpf_usuario": "11111111111"}
{ "valor": 11.25, "data_vencimento": "2024-05-11", "cpf_usuario": "33333333333" }
{ "valor": 89.89, "data_vencimento": "2022-05-11", "cpf_usuario": "33333333333" }
{ "valor": 123.01, "data_vencimento": "2024-09-11", "cpf_usuario": "33333333333" }

## Login Ex.:
POST http://127.0.0.1:5000/entrar
{
  "cpf": "11111111111",
  "senha": "senha123"
}

## Deslogar Ex.:
POST http://127.0.0.1:5000/sair
{
  "cpf": "11111111111",
  "senha": "senha123"
}

## Score Ex.:
GET http://127.0.0.1:5000/score
{
  "cpf": "11111111111",
  "senha": "senha123"
}

## Lista Dividas Ex.:
GET http://127.0.0.1:5000/dividas
{
  "cpf": "11111111111",
  "senha": "senha123"
}
## ----------------------------------------------------------------

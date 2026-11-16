# Pokémon Deck Builder & Card Evaluator

Projeto Final da disciplina **Laboratório de Programação 1 (SPOLBP1)** — Técnico em Desenvolvimento de Sistemas (Prof. Igor de Moraes).

## Descrição do Sistema
Aplicação web no padrão **MPA (Multi-Page Application)** desenvolvida com **Python, Flask, Jinja2 e SQLite3**, seguindo estritamente a arquitetura **Model-View-Controller (MVC)** com **Blueprints**.

O sistema permite que treinadores gerenciem:
1. **Autenticação de Usuários:** Cadastro, login e logout com senhas protegidas por hash criptográfico (`werkzeug.security`).
2. **Meus Baralhos (Decks):** CRUD completo (criar, listar com filtro de busca, editar e excluir) de baralhos Pokémon, com parser automático da lista de cartas.
3. **Avaliação de Preços de Cartas:** CRUD completo para registrar cotações de cartas (nome, coleção, raridade e preço estimado), com filtro de busca e soma automática do valor da coleção.

## Credenciais de Teste (Usuário Inicial)
* **Usuário:** `ash`
* **Senha:** `pikachu123`

## Como Executar o Projeto
1. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicialize o banco de dados SQLite (`banco_dados.db`) e o usuário de teste:
   ```bash
   python iniciar_bd.py
   ```
4. Execute a aplicação:
   ```bash
   python run.py
   ```
5. Acesse no navegador: `http://127.0.0.1:5000`

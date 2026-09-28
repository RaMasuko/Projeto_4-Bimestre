from app import create_app
from app.database import init_db
from app.models.user import UserModel

app = create_app()

if __name__ == '__main__':
    # Cria a tabela no SQL Server se ela não existir
    init_db()

    # Cria o usuário padrão 'ash' em SQL nativo caso não esteja cadastrado
    if not UserModel.get_by_username("ash"):
        UserModel.create("ash", "pikachu123")
        print("-> Usuário 'ash' cadastrado via SQL nativo!")

    app.run(debug=True)
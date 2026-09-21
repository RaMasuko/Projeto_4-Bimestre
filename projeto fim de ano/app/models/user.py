from werkzeug.security import generate_password_hash, check_password_hash

# Lista de usuários mockados. As senhas são geradas via Hash por segurança.
USERS_DB = {
    "ash": generate_password_hash("pikachu123"),
    "red": generate_password_hash("charizard456")
}

class UserModel:
    @staticmethod
    def verify_credentials(username, password):
        hashed_password = USERS_DB.get(username)
        # Compara a senha informada no form com o hash gravado
        if hashed_password and check_password_hash(hashed_password, password):
            return True
        return False
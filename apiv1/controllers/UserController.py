from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserController:
    
    @staticmethod
    def register_user(username, email, password):
        if not username or not email or not password:
            return False, 'Todos os campos são obrigatórios', None
        
        if len(password) < 6:
            return False, 'A senha deve ter no mínimo 6 caracteres', None
        
        if User.objects.filter(username=username).exists():
            return False, 'Nome de usuário já existe', None

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            return True, f'Usuário {username} cadastrado!', user
        except Exception as e:
            return False, f'Erro: {str(e)}', None
    
    @staticmethod
    def authenticate_user(usuario, password):
        if not usuario or not password:
            return False, 'Usuário e senha obrigatórios', None
        
        user = authenticate(username=usuario, password=password)
        # Utilizando o autenticate do proprio django contrib

        if user is not None:
            return True, user
        else:
            return False, None
    
    @staticmethod
    def get_all_users():
        return User.objects.all()
    
    @staticmethod
    def get_user_data(user):
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None
        }

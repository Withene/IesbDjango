from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
import json

from apiv1.controllers.UserController import UserController


def jwt_required(view_func):
    """
    Decorator para verificar autenticação JWT
    """
    def wrapper(request, *args, **kwargs):
        jwt_authenticator = JWTAuthentication()
        try:
            # Tenta autenticar usando JWT
            response = jwt_authenticator.authenticate(request)
            if response is not None:
                user, token = response
                request.user = user
                return view_func(request, *args, **kwargs)
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Token de autenticação não fornecido'
                }, status=401)
        except AuthenticationFailed as e:
            return JsonResponse({
                'success': False,
                'message': f'Autenticação falhou: {str(e)}'
            }, status=401)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro na autenticação: {str(e)}'
            }, status=500)
    return wrapper


@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    try:
        data = json.loads(request.body)
        success, message, user = UserController.register_user(data.get('username'), data.get('email'), data.get('password'))

        if success:
            refresh = RefreshToken.for_user(user)

            return JsonResponse({
                'success': True,
                'message': message,
                'user': UserController.get_user_data(user),
                'token': str(refresh.access_token),
            }, status=200)
        else:
            return JsonResponse({
                'success': False,
                'message': message
            }, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        success, user = UserController.authenticate_user(data.get('username'), data.get('password'))

        if success:
            # Gera tokens JWT
            refresh = RefreshToken.for_user(user)

            return JsonResponse({
                'success': True,
                'message': "Ok",
                'user': UserController.get_user_data(user),
                'token': str(refresh.access_token),
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Usuário ou senha incorretos'
            }, status=401)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@jwt_required
@require_http_methods(["GET"])
def users_list_view(request):
    users = UserController.get_all_users()
    users_data = [UserController.get_user_data(user) for user in users]

    return JsonResponse({
        'success': True,
        'total': len(users_data),
        'users': users_data
    })


@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({
        'success': True,
        'response': 'Pong'
    })


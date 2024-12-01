from myapp.models import User  # Replace with your user model

def custom_user_context(request):
    if hasattr(request, 'user') and isinstance(request.user, User):
        return {'user': request.user}   
    return {'user': None}


class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example: Attach your custom user object to request.user
        user_id = request.session.get('user_name')  # Replace with your logic
        if user_id:
            try:
                request.user = User.objects.get(user_name = user_id)
            except User.DoesNotExist:
                request.user = None
        else:
            request.user = None
        return self.get_response(request)

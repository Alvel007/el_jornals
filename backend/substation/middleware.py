from django.shortcuts import redirect
from django.shortcuts import reverse

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path == reverse('login') and not request.path.startswith('/admin/'):
            return redirect(reverse('login'))
        return self.get_response(request)

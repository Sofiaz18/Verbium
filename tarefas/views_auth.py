from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

def logout_view(request):
    """View personalizada para logout"""
    logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('/')
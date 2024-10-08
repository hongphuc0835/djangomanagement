# tasks/decorators.py
from django.shortcuts import redirect

def login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('username'):
            return redirect('login')  # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập
        return view_func(request, *args, **kwargs)
    return _wrapped_view

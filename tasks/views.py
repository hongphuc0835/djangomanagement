from django.shortcuts import render, redirect
from .models import User
from .firebase_config import db
from firebase_admin import firestore
from datetime import datetime
from .decorators import login_required  # Import decorator
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Đường dẫn đến Firestore
db = firestore.client()

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        db.collection('users').add({'username': username, 'password': password})
        return redirect('login')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        users = db.collection('users').where('username', '==', username).where('password', '==', password).get()
        if users:
            request.session['username'] = username  # Lưu vào session
            return redirect('task_list')
        else:
            # Thêm thông báo lỗi nếu thông tin đăng nhập không đúng
            return render(request, 'login.html', {'error': 'Tên đăng nhập hoặc mật khẩu không đúng.'})
    return render(request, 'login.html')


def logout(request):
    request.session.flush()  # Xóa toàn bộ session
    return redirect('login')


# Kiểm tra session trong task_list view
@login_required
@never_cache  # Ngăn chặn bộ nhớ đệm
def task_list(request):
    # Logic của bạn cho danh sách task
    username = request.session['username']
    user_ref = db.collection("users").where("username", "==", username).get()
    if user_ref:
        user_id = user_ref[0].id
    else:
        return redirect('login')

    tasks_ref = db.collection('tasks').where('user_id', '==', user_id).get()
    task_list = {task.id: task.to_dict() for task in tasks_ref}

    return render(request, 'task_list.html', {'tasks': task_list, 'username': username})

@login_required  # Bảo vệ trang này
def add_task(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        deadline = request.POST['deadline']
        priority = request.POST['priority']
        username = request.session['username']
        
        user_ref = db.collection("users").where("username", "==", username).get()
        if user_ref:
            user_id = user_ref[0].id
        else:
            return redirect('login')

        task = {
            "title": title,
            "description": description,
            "deadline": deadline,
            "priority": priority,
            "completed": False,
            "user_id": user_id,
            "created_at": datetime.utcnow()
        }
        db.collection("tasks").add(task)
        return redirect('task_list')
    return render(request, 'add_task.html')


@login_required
def edit_task(request, task_id):
    doc_ref = db.collection("tasks").document(task_id)
    task = doc_ref.get().to_dict()

    if request.method == "POST":
        # Lấy các giá trị từ POST, chỉ cập nhật "completed" nếu có thay đổi
        completed = request.POST.get('completed') == 'on'
        doc_ref.update({
            "completed": completed,
            "title": request.POST.get('title', task['title']),  # Chỉ cập nhật nếu có thay đổi
            "description": request.POST.get('description', task['description']),
            "deadline": request.POST.get('deadline', task['deadline']),
            "priority": request.POST.get('priority', task['priority']),
        })
        return redirect('task_list')

    # Đảm bảo "completed" là False nếu không có thay đổi
    task['completed'] = task.get('completed', False)

    return render(request, 'edit_task.html', {'task': task})





@login_required  # Bảo vệ trang này
def delete_task(request, task_id):
    db.collection('tasks').document(task_id).delete()
    return redirect('task_list')

from django.contrib.auth import get_user_model
User = get_user_model()

editor = User.objects.get(username='33366')  # или имя пользователя редактора
print(f"is_staff: {editor.is_staff}")
print(f"Groups: {list(editor.groups.all())}")
print(f"Permissions: {list(editor.user_permissions.all())}")
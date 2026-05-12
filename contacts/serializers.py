from rest_framework import serializers
from django.core.validators import RegexValidator, MinLengthValidator
from .models import ContactMessage

# 1. Валидатор для телефона (только цифры, формат РФ)
phone_regex = RegexValidator(
    regex=r'^\+?7\d{10}$',
    message="Введите номер телефона в формате +79991234567"
)

class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания обращений с строгой валидацией (ТЗ 5.5)
    """
    
    # Переопределяем поля для явного указания правил
    name = serializers.CharField(
        max_length=100,
        min_length=2,
        error_messages={
            'required': 'Поле "Имя" обязательно для заполнения.',
            'min_length': 'Имя должно содержать минимум 2 символа.',
            'max_length': 'Имя не должно превышать 100 символов.'
        }
    )
    
    email = serializers.EmailField(
        error_messages={
            'required': 'Поле "Email" обязательно.',
            'invalid': 'Введите корректный адрес электронной почты.'
        }
    )
    
    phone = serializers.CharField(
        validators=[phone_regex],
        max_length=15,
        required=False,  # Телефон можно не указывать, но если указан - он должен быть валидным
        error_messages={
            'invalid': 'Неверный формат телефона. Используйте +7XXXXXXXXXX'
        }
    )
    
    message = serializers.CharField(
        min_length=10,
        max_length=5000,
        error_messages={
            'required': 'Текст обращения обязателен.',
            'min_length': 'Сообщение слишком короткое (минимум 10 символов).'
        }
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message', 'created_at']
        read_only_fields = ['created_at']

    # Дополнительная проверка имени (защита от цифр/спецсимволов)
    def validate_name(self, value):
        if not value.replace(' ', '').isalpha():
            raise serializers.ValidationError("Имя должно содержать только буквы.")
        return value

    # Дополнительная проверка текста (защита от спама)
    def validate_message(self, value):
        if "http" in value or "www" in value:
            raise serializers.ValidationError("Сообщение не должно содержать ссылки.")
        return value
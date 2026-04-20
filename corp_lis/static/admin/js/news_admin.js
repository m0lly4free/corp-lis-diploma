// Улучшенный редактор контента для новостей
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация редакторов
    document.querySelectorAll('.vLargeTextField').forEach(editor => {
        if (!editor.closest('.admin-textarea-container')) {
            // Создаем контейнер для редактора
            const container = document.createElement('div');
            container.className = 'admin-textarea-container';
            
            // Перемещаем textarea в новый контейнер
            const textarea = editor;
            textarea.className = 'vLargeTextField news-editor-textarea';
            textarea.removeAttribute('style');
            
            // Создаем панель инструментов
            const toolbar = document.createElement('div');
            toolbar.className = 'editor-toolbar';
            
            // Добавляем кнопки
            const buttons = [
                {type: 'bold', icon: 'B', title: 'Жирный текст (Ctrl+B)', className: 'bold-btn'},
                {type: 'italic', icon: 'I', title: 'Курсив (Ctrl+I)', className: 'italic-btn'},
                {type: 'underline', icon: 'U', title: 'Подчеркнутый (Ctrl+U)', className: 'underline-btn'},
                {type: 'h2', icon: 'H2', title: 'Заголовок 2', className: 'h2-btn'},
                {type: 'h3', icon: 'H3', title: 'Заголовок 3', className: 'h3-btn'},
                {type: 'ul', icon: '•', title: 'Ненумерованный список', className: 'list-unordered-btn'},
                {type: 'ol', icon: '1.', title: 'Нумерованный список', className: 'list-ordered-btn'},
                {type: 'image', icon: '🖼️', title: 'Вставить изображение', className: 'image-btn'},
                {type: 'link', icon: '🔗', title: 'Вставить ссылку', className: 'link-btn'}
            ];
            
            buttons.forEach(button => {
                const btn = document.createElement('button');
                btn.type = 'button';
                btn.title = button.title;
                btn.className = `editor-btn ${button.className}`;
                btn.innerHTML = button.icon;
                btn.dataset.type = button.type;
                toolbar.appendChild(btn);
            });
            
            // Добавляем элементы в контейнер
            container.appendChild(toolbar);
            container.appendChild(textarea);
            
            // Заменяем оригинальный textarea
            editor.parentElement.insertBefore(container, editor);
            editor.style.display = 'none';
            
            // Инициализируем редактор
            initEditor(textarea, toolbar);
        }
    });
    
    function initEditor(textarea, toolbar) {
        // Обработчики для кнопок
        toolbar.querySelectorAll('.editor-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                const command = this.dataset.type;
                applyCommand(textarea, command);
            });
        });
        
        // Обработчик для клавиатурных комбинаций
        textarea.addEventListener('keydown', function(e) {
            if (e.ctrlKey) {
                switch(e.key.toLowerCase()) {
                    case 'b':
                        e.preventDefault();
                        applyCommand(textarea, 'bold');
                        break;
                    case 'i':
                        e.preventDefault();
                        applyCommand(textarea, 'italic');
                        break;
                    case 'u':
                        e.preventDefault();
                        applyCommand(textarea, 'underline');
                        break;
                }
            }
        });
    }
    
    function applyCommand(textarea, command) {
        textarea.focus();
        
        switch(command) {
            case 'bold':
                document.execCommand('bold', false, null);
                break;
            case 'italic':
                document.execCommand('italic', false, null);
                break;
            case 'underline':
                document.execCommand('underline', false, null);
                break;
            case 'h2':
                document.execCommand('formatBlock', false, 'h2');
                break;
            case 'h3':
                document.execCommand('formatBlock', false, 'h3');
                break;
            case 'ul':
                document.execCommand('insertUnorderedList', false, null);
                break;
            case 'ol':
                document.execCommand('insertOrderedList', false, null);
                break;
            case 'image':
                const url = prompt('Введите URL изображения:');
                if (url) {
                    document.execCommand('insertImage', false, url);
                }
                break;
            case 'link':
                const link = prompt('Введите URL ссылки:');
                if (link) {
                    document.execCommand('createLink', false, link);
                }
                break;
        }
        
        // Устанавливаем фокус обратно в textarea
        textarea.focus();
    }
    
    // Автоматическая подстановка тегов для заголовков
    document.querySelectorAll('.vLargeTextField').forEach(textarea => {
        textarea.addEventListener('input', function() {
            // Автоматически добавляем теги для заголовков
            if (this.value.startsWith('## ')) {
                this.value = '<h2>' + this.value.substring(3) + '</h2>';
            } else if (this.value.startsWith('### ')) {
                this.value = '<h3>' + this.value.substring(4) + '</h3>';
            }
        });
    });
});
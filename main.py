# API — Application Programming Interface — интерфейс взаимодействия между программами.
# REST — архитектурный стиль проектирования API, который определяет правила работы с ресурсами.

# /api/coffee/       — получение списка кофе
# /api/coffee/5/     — получение конкретного объекта

# JSON — JavaScript Object Notation — текстовый формат обмена структурированными данными.

# HTTP STATUS CODES:
# 1xx — Информационные ответы
# 2xx — Успешные ответы
# 3xx — Перенаправление
# 4xx — Ошибки на стороне клиента
# 5xx — Ошибки на стороне сервера

# CBV — Class-Based Views — представления, реализованные в виде Python-классов.
# В DRF используются для обработки HTTP-запросов через методы класса.

# FBV — Function-Based Views — представления, реализованные в виде Python-функций.
# Вся логика обработки запроса находится внутри функции.

# Главное отличие:
# FBV — обработка запросов через функции.
# CBV — обработка запросов через методы класса.

# APIView — базовый класс DRF для создания представлений на основе классов.

# GenericAPIView — расширенный класс DRF для работы с моделями, QuerySet и сериализаторами.

# Generic Views — готовые представления на основе GenericAPIView и Mixins.

# Основные Generic Views:
# ListAPIView                    — получение списка объектов
# RetrieveAPIView                — получение одного объекта
# CreateAPIView                  — создание объекта
# UpdateAPIView                  — обновление объекта
# DestroyAPIView                 — удаление объекта
# ListCreateAPIView              — получение списка и создание объекта
# RetrieveUpdateAPIView          — получение и обновление объекта
# RetrieveDestroyAPIView         — получение и удаление объекта
# RetrieveUpdateDestroyAPIView   — получение, обновление и удаление объекта

# Основные виды Mixins:
# ListModelMixin      — получение списка объектов
# RetrieveModelMixin  — получение одного объекта
# CreateModelMixin    — создание объекта
# UpdateModelMixin    — обновление объекта
# DestroyModelMixin   — удаление объекта

# Вложенные маршруты — Nested Routes.
# Способ организации URL, при котором один ресурс находится внутри другого.

# /api/projects/             — список проектов
# /api/projects/1/           — конкретный проект
# /api/projects/1/tasks/     — список задач проекта
# /api/projects/1/tasks/1/   — конкретная задача проекта

# Пагинация — Pagination.
# Разделение большого списка объектов на отдельные страницы.

# Основные виды:
# 1. PageNumberPagination  — пагинация по номеру страницы.
# 2. LimitOffsetPagination — пагинация с использованием лимита и смещения.
# 3. CursorPagination      — пагинация с использованием курсора.

# Фильтрация и поиск:
# 1. DjangoFilterBackend — фильтрация по определённым полям.
# 2. SearchFilter        — поиск по текстовым полям.
# 3. OrderingFilter      — сортировка объектов.

# Router — автоматическое создание URL-маршрутов для ViewSet.

# Основные виды:
# 1. SimpleRouter — создаёт стандартные маршруты для ViewSet.
# 2. DefaultRouter — аналог SimpleRouter, но дополнительно создаёт API Root.

# @action — декоратор для создания дополнительных действий внутри ViewSet.

# detail=False — действие над списком объектов.
# detail=True  — действие над конкретным объектом.
# Примеры:
# @action(detail=False) — /api/projects/active/
# @action(detail=True)  — /api/projects/1/archive/

# CRUD — основные операции над данными:
# Create — создание (POST)
# Read   — получение (GET)
# Update — обновление (PUT, PATCH)
# Delete — удаление (DELETE)
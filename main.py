# API — Application Programming Interface
# REST — Набор правил для проектирования такого официанта.
# /api/coffee
# /api/coffee/5
# JSON — JavaScript Object Notation — это текстовый формат обмена структурированными данными.
# 100 — Информационные ответы
# 200 — Успешные ответы
# 300 — Коды перенаправления
# 400 — Ошибка клиента
# 500 — Ошибки сервера
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView

# CBV — Class-Based-Views — это представления, реализованные в виде Python классов. В DRF они исспользуются для обработки HTTP запросов
# FBV — Function-Based-Views — это представление, где логика обработки запроса находится внутри функции.
# Отличия CBV от FBV, в том что CBV она разделяет логику на отдельные методы класса.
# APIView — базовы класс DRF для создания представлений на основе классов
# GenericAPIView — это расширенный базовый класс DRF, предназначенный для работы с моделями, QuerySet и serializers.
# Generic Views — это готовые классы пресдтавлений, созданные на основе GenericAPIView и Mixins.
#               Основные виды Generic Views:
# ListAPIView                     — Получение списка объектов
# RetrieveAPIView                 — Получение одного объекта
# CreateAPIView                   — Создание объекта
# UpdateAPIView                   — Обновление объекта
# DestroyAPIView                  — Удаление объекта
# ListCreateAPIView               — Получение списка и создание
# RetrieveUpdateAPIView           — Получение и обновление
# RetrieveDestroyAPIView          — Получение и удаление
# RetrieveUpdateDestroyAPiView    — Получение, обновление и удаление

# Основные виды Mixins:
# ListModelMixin      — Получение списка объектов
# RetrieveModelMixin  — Получение одного объекта
# CreateModelMixin    — Создание
# UpdateModelMixin    — Обновление
# DestroyModelMixin   — Удаление

# Вложенные маршруты — Nested Routes
# Это способ организации URL—адресов, при котором один ресурс располагается внутри друого ресурса.
#
# /api/projects — список игр
# /api/projects/1/ — конкретный проект
# /api/projects/1/tasks/ — задачи определенного игры.
# /api/projects/1/tasks/1/ — конкретная задача внутри игры
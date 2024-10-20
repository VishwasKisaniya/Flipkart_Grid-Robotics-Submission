from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Home page
    path('detect/object', views.detect_object, name='detect_object'),  # Object detection route
    path('detect/fruit', views.detect_fruit, name='detect_fruit'),  # Fruit/vegetable detection route
    path('capture/camera/', views.capture_from_camera, name='capture_from_camera'),

]

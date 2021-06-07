from django.urls import path
from .views import (
    VeiklaListView,
    VeiklaCreateView,
    VeiklaUpdateView,
    VeiklaDeleteView,
    UzdarbisListView,
    UzdarbisDetailView,
    UzdarbisCreateView,
    UzdarbisUpdateView,
    UzdarbisDeleteView,
    veikla_calendar,
)
from . import views

urlpatterns = [
    path('', VeiklaListView.as_view(), name='taxes-home'),
    path('veikla/<int:pk>/', UzdarbisListView.as_view(), name='veikla-detail'),
    path('veikla/new/', VeiklaCreateView.as_view(), name='veikla-create'),
    path('veikla/<int:pk>/update/', VeiklaUpdateView.as_view(), name='veikla-update'),
    path('veikla/<int:pk>/delete/', VeiklaDeleteView.as_view(), name='veikla-delete'),
    path('uzdarbis/<int:pk>/', UzdarbisDetailView.as_view(), name='uzdarbis-detail'),
    path('veikla/<int:pk>/veikla_detaliau/', views.veikla_detaliau, name='veikla-detaliau'),
    path('uzdarbis/new/', UzdarbisCreateView.as_view(), name='uzdarbis-create'),
    path('uzdarbis/<int:pk>/update/', UzdarbisUpdateView.as_view(), name='uzdarbis-update'),
    path('uzdarbis/<int:pk>/delete/', UzdarbisDeleteView.as_view(), name='uzdarbis-delete'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='taxes-about'),
    path('calendar/', views.veikla_calendar, name='calendar'),
    path('calendar/<int:year>/<str:month>/', views.veikla_calendar, name='calendar'),
    path('visual/', views.visual, name='visu-al'),
]

from django.urls import path
from . import views

app_name = 'threads'

urlpatterns = [
    path('lists', views.ThreadListView.as_view(), name='lists'),
    path('<int:pk>/show', views.ThreadDetailView.as_view(), name='show'),
    path('create', views.ThreadCreateView.as_view(), name='create'),
    path('<int:pk>/edit', views.ThreadUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete', views.ThreadDeleteView.as_view(), name='delete'),

    path('<int:pk>/delete-sub', views.SubThreadDeleteView.as_view(), name='delete-sub'),

    path('get-lists/<str:thread_id>', views.get_sub_threads, name='sub-thread-lists'), 
    
    path('links', views.ThreadLinkListView.as_view(), name='links'),
    path('links/<int:pk>/delete', views.ThreadLinkDeleteView.as_view(), name='delete-link'),

    
]
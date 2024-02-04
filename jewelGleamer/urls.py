from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'jewelGleamer'
urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.logged_user_home, name='logged_user_home'),
    path('blog/', views.blog, name='blog'),
    path('other_blogs/', views.other_blogs, name='other_blogs'),
    path('items/', views.jewelry_items_list, name='items_list'),
    path('items/<int:item_id>', views.jewelry_item_detail, name='item_detail'),
    path('items/<int:item_id>/delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('items/search', views.search, name='search'),
    path('items/add/', views.add_item, name='add_item'),
    path('items/<int:ring_id>/delete/', views.delete_ring, name='delete_ring'),
    path('items/<int:ring_id>/edit', views.edit_ring, name='edit_ring'),
    path('items/add_item/', views.add_new_item, name='add_new_item'),
    path('items/<int:item_id>/edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('generate_description/<int:item_id>/', views.generate_description, name='generate_description'),
    path('save_description/<int:item_id>/', views.save_description, name='save_description'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

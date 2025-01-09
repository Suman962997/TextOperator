from django.urls import path
from .views import ImageUploadView,ImageTextView,TableView,SearchBar
from django.conf.urls.static import static
from django.conf import settings


urlpatterns=[
    path('upload/',ImageUploadView.as_view(),name='image_store'),
    path('view/',ImageTextView.as_view(),name='img_view'),
    path('table/',TableView.as_view(),name='Table'),
    path('search/',SearchBar.as_view(),name='searchbar'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

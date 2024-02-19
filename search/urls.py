from django.urls import path
from search.views import ParagraphView


urlpatterns = [
    path("paragraphs/", ParagraphView.as_view(), name="paragraphs")
]
from django.urls import path
from .views import send_test_email, get_character_names

urlpatterns = [
    path('send-test-email/', send_test_email, name='send_test_email'),
    path('character-names', get_character_names, name='character-names'),
]

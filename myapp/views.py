from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.conf import settings

def send_test_email(request):
    subject = 'Test Email from Django'
    message = 'This is a test email sent from Django using SMTP on Liara server.'
    recipient_list = ['omidjt2015@gmail.com']
    
    email = EmailMessage(
        subject,
        message,
        settings.EMAIL_FROM_ADDRESS,
        recipient_list,
        headers={"x-liara-tag": "test-tag"},
    )

    
    email.send(fail_silently=False)
    return HttpResponse('Test email sent successfully!')


def get_character_names(request):
    return JsonResponse({"names": ["Agile", "Normal"]})



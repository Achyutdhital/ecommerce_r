from django.core.mail import EmailMessage
import os

class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(
      subject=data['subject'],
      body=data['body'],
      from_email=os.environ.get('EMAIL_FROM'),
      to=[data['to_email']]
    )
    email.send()



from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def handle_uploaded_file(avatar_file):
    # Save the uploaded file to the default storage location
    file_path = default_storage.save(avatar_file.name, ContentFile(avatar_file.read()))
    # Return the file path where the file was saved
    return file_path

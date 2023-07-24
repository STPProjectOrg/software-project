from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import datetime, date

def compress_image(image : Image) -> Image:
    if image:
        img = Image.open(image)
        bytes_io = BytesIO()
        img.save(bytes_io, format='JPEG', quality=50)
        return InMemoryUploadedFile(bytes_io, None, image.temporary_file_path(), 
                                                'image/jpeg', bytes_io.tell(), None)
    
def define_created_at(datetime: datetime):
        if datetime != None:
            created_at = datetime
            if created_at.date() == datetime.today():
                created_at = datetime
            elif (date.today() - created_at.date()).days >= 2 :
                created_at = datetime.date()
            elif (date.today() - created_at.date()).days >= 1 :
                created_at = "Gestern"
            return created_at
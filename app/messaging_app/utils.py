from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

def compress_image(image : Image) -> Image:
    if image:
        img = Image.open(image)
        bytes_io = BytesIO()
        img.save(bytes_io, format='JPEG', quality=50)
        return InMemoryUploadedFile(bytes_io, None, image.temporary_file_path(), 
                                                'image/jpeg', bytes_io.tell(), None)
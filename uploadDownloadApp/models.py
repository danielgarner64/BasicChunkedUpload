from django.db import models
from DjangoUpDown import settings
from django.contrib.auth.models import User
import os
from chunked_upload.models import AbstractChunkedUpload
from django.core.files.storage import FileSystemStorage


# Overwrite storage because the file already exists
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT_DB_STORED_FILES, name))
        return name


class File(models.Model):
    file_name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=512, blank=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # point to the already existing file
    file = models.FileField(storage=OverwriteStorage())
    #file.size/(1024*1024) == size in MB (file.size in in Bytes)
    md5_checksum = models.CharField(max_length=255) #technically it is 128 (but extra space in case of special encoding)

    def get_abspath(self):
        return os.path.join(settings.MEDIA_ROOT, self.file.name)

    def delete(self, *args, **kwargs):
        os_path = self.get_abspath()
        if os.path.exists(os_path):
            os.remove(os_path)
        super(File, self).delete(*args, **kwargs)

    class Meta:
        pass

    def __str__(self):
        return u'File: %s' % self.file_name


class ChunkedFile(AbstractChunkedUpload):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

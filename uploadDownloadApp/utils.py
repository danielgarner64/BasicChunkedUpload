from uploadDownloadApp.models import File
import os
from DjangoUpDown import settings
import shutil
from django.contrib.auth.models import User


def get_unique_file_name(file_name):
    file_name_only, extension = os.path.splitext(file_name)

    similar_file_names = list(File.objects.filter(file_name__icontains=file_name_only))
    similar_file_names = [file_obj.file_name for file_obj in similar_file_names]

    for i in range(10000):
        if i == 0:
            if file_name not in similar_file_names:
                return file_name
        else:
            temp_file_name = file_name_only + "_" + str(i) + extension
            if temp_file_name not in similar_file_names:
                return temp_file_name
    return file_name


def create_file_in_db_with_existing_file(src_path, file_name: str, description: str, user: User, file_size, file_md5):
    new_unique_file_name = get_unique_file_name(file_name)
    dest_path = os.path.join(settings.MEDIA_ROOT_DB_STORED_FILES, os.path.basename(new_unique_file_name))

    if os.path.exists(src_path):
        try:
            shutil.move(src_path, dest_path)
        except Exception as e:
            raise Exception(f"Failed to upload file this could be caused by permissions issues or files being opened by local os.\n {e}")
    else:
        raise Exception(f"Failed to upload file source path does not exist srcPath: {src_path},\nNew File Name: {new_unique_file_name}, File Size: {int(file_size)/(1024*1024)}MB")


    new_file = File.objects.create(file=dest_path,
                        file_name=new_unique_file_name,
                        description=description,
                        author=user,
                        md5_checksum=file_md5)

    new_file.save()
    return new_file

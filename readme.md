###Simple Chunked Upload Server

Note this server has an intentional bug in it in the views.py file.
The bottom function on_completion will generate an error as a file is being written to and moved simutaneously.

To install run the following commands. (Python 3.7 or greater)
```
# Create the virtual environment
python -m venv venv

# Install dependencies
pip install -r requirements.txt

# Make migrations
python manage.py migrate

# Create django super user
python manage.py createsuperuser
```

To run the server use the following command:
```
python manage.py runserver 127.0.0.1:8000
```




To fix the error in views.py remove this code
```python
    def on_completion(self, uploaded_file, request):
        uploaded_file.file.close()

        chunked_upload = get_object_or_404(ChunkedFile, upload_id=request.POST.get("upload_id"))
        chunked_upload.delete(delete_file=False)

        uploaded_file = create_file_in_db_with_existing_file(
            src_path=chunked_upload.file.path,
            file_name=chunked_upload.filename,
            description=request.POST.get("description", ""),
            user=request.user,
            file_size=chunked_upload.file.size,
            file_md5=chunked_upload.md5
        )

    # What the get_response_data should do. (this shouldn't generate any errors
    def get_response_data(self, chunked_upload, request):
        redirect_to = "uploadDownloadApp:" + request.POST.get("source_page", "home")
        messages.add_message(request, messages.SUCCESS, "Successfully uploaded file")
        return {"status": "success", "redirect_url": reverse(redirect_to)}
```

Replace it with this code which was commented out below:
```python
    def get_response_data(self, chunked_upload, request):
        chunked_upload.file.close()
        chunked_upload.delete(delete_file=False)

        uploaded_file = create_file_in_db_with_existing_file(
            src_path=chunked_upload.file.path,
            file_name=chunked_upload.filename,
            description=request.POST.get("description", ""),
            user=request.user,
            file_size=chunked_upload.file.size,
            file_md5=chunked_upload.md5
        )
        redirect_to = "uploadDownloadApp:" + request.POST.get("source_page", "home")
        messages.add_message(request, messages.SUCCESS, f"Successfully uploaded file {uploaded_file.file.name}")
        return {"status": "success", "redirect_url": reverse(redirect_to)}
```
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect, reverse, get_object_or_404
from chunked_upload.views import ChunkedUploadView, ChunkedUploadCompleteView
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from uploadDownloadApp.models import File, ChunkedFile
from uploadDownloadApp.utils import get_unique_file_name, create_file_in_db_with_existing_file
from django.contrib.auth.decorators import login_required
import datetime
from .forms import FileForm
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.timezone import make_aware
from django.contrib import messages


def redirect_to_login(request):
    return redirect("uploadDownloadApp:login")

# Valid message types are "success", "failure"
@login_required
def home(request):
    newest_document = File.objects.all().order_by('-uploaded_at')
    files = []
    if len(newest_document) > 0:
        files = [newest_document[0]]

    return render(request, 'uploadDownloadApp/showFiles.html', {"title": "Newest Caterpillar",
                                                                "files": files,
                                                                "upload_form": FileForm(),
                                                                "source_page": "home"})


@login_required
def old_caterpillar_view(request):
    one_month_old_file = File.objects.filter(uploaded_at__lte=make_aware(datetime.datetime.utcnow() - datetime.timedelta(days=30))).order_by('-uploaded_at')
    files = []
    if len(one_month_old_file) > 0:
        files = [one_month_old_file[0]]

    return render(request, 'uploadDownloadApp/showFiles.html', {"title": "Old Caterpillar",
                                                                "files": files,
                                                                "upload_form": FileForm(),
                                                                "source_page": "old_caterpillar"})

@login_required
@staff_member_required
def show_all_files(request):
    return render(request, 'uploadDownloadApp/showFiles.html', {"title": "All Uploaded Files",
                                                                'files': File.objects.all().order_by('-uploaded_at'),
                                                                "upload_form": FileForm(),
                                                                "source_page": "full_file_list"})

@login_required
def download(request):
    if not request.method == "GET":
        raise Http404
    file_id = request.GET["fileIdToDownload"]
    file_obj_from_db = get_object_or_404(File, id=file_id)

    file_path = file_obj_from_db.file.path #FULL PATH from OS.
    try:
        with open(file_path, "rb") as fr:
            response = HttpResponse(fr.read())
            response['Content-Disposition'] = 'attachment;filename=' + file_obj_from_db.file_name
            return response
    except Exception:
        raise Http404


@login_required
@staff_member_required
def delete(request, source_view="home"):
    redirect_to = "uploadDownloadApp:" + source_view
    if request.method == "POST":
        file_id = request.POST["fileIdToDelete"]
        file_obj = get_object_or_404(File, id=file_id)
        file_obj.delete()
        messages.add_message(request, messages.SUCCESS, f"Successfully deleted file {file_obj.file_name}")
        return redirect(redirect_to)

    messages.add_message(request, messages.WARNING, f"Failed to delete file, method was not POST.")
    return redirect(redirect_to)


class MyChunkedUploadView(LoginRequiredMixin, SuperuserRequiredMixin, ChunkedUploadView):
    model = ChunkedFile
    field_name = 'file' # html id of the file we are uploading

    # Bypass chunked upload permission management
    def check_permissions(self, request):
        pass


class MyChunkedUploadCompleteView(LoginRequiredMixin, SuperuserRequiredMixin, ChunkedUploadCompleteView):
    model = ChunkedFile
    # Bypass chunked upload permission management
    def check_permissions(self, request):
        pass

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

from django.urls import path, include, re_path
from . import views
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from DjangoUpDown import settings_dev
from django.contrib.auth import views as auth_views
from django.views import defaults

from django.conf.urls.static import static


app_name = 'uploadDownloadApp'
urlpatterns = [
    path(r"", views.redirect_to_login),
    path(r'login/', auth_views.LoginView.as_view(template_name="uploadDownloadApp/login.html",
                                                 redirect_authenticated_user=True), name="login"),
    path(r'home/', views.home, name='home'),
    path(r'oldCaterpillar/', views.old_caterpillar_view, name='old_caterpillar'),
    path(r'fullFileList/', views.show_all_files, name='full_file_list'),
    path(r'changePassword/', auth_views.PasswordChangeView.as_view(template_name="uploadDownloadApp/changePassword.html",
                                                                   success_url=reverse_lazy("uploadDownloadApp:changePasswordSuccess")), name='change_password'),
    path(r'changePasswordSuccess/', auth_views.PasswordChangeDoneView.as_view(template_name=r"uploadDownloadApp/changePasswordSuccess.html"), name="changePasswordSuccess"),
    path(r'logout/', auth_views.LogoutView.as_view(next_page="uploadDownloadApp:login"), name='logout'),

    path(r'download/', views.download, name='download'),
    re_path(r'^delete/(?P<source_view>\w+)/$', views.delete, name="delete"),

    path("chunkedUploadComplete/", views.MyChunkedUploadCompleteView.as_view(), name="chunkedUploadComplete"),
    path("chunkedUpload/", views.MyChunkedUploadView.as_view(), name="chunkedUpload"),
]
#+ static(settings_dev.STATIC_ROOT, document_root=settings_dev.STATIC_ROOT) # TODO DEBUG ONLY STATIC ROOT


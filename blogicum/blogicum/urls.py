from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from blog.models import User

extra_patterns = [
    path(
        'registration/',
        CreateView.as_view(
            model=User,
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration'
    ),
    path(
        '',
        include('django.contrib.auth.urls')
    ),
]

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'auth/',
        include(
            extra_patterns,
        )
    ),
    path(
        'pages/',
        include(
            'pages.urls',
            namespace='pages'
        )
    ),
    path(
        '',
        include(
            'blog.urls',
            namespace='blog'
        )
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

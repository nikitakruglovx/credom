from django.urls import path
from . import views
from .models import Users
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.index_view, name='index'),
    path('index', views.index_view, name='index'),
    path('aboutproject', views.aboutproject_view, name='aboutproject'),
    path('home', views.home_view, name='home'),
    path('login', views.login_view, name='login'),
    path('registration', views.register_view, name='reg'),
    path('loginout', views.logout_view, name='logout'),
    path('profile', views.profile_view, name='profile'),
    path('add', views.add_item, name='additem'),
    path('about', views.about_view, name='about'),
    path('cloud', views.cloud_view, name="cloud"),
    path('cloud/folder/<int:id>', views.cloudid_view),
    path('about/<int:id>', views.itembuy_view),
    path('account/about/<int:id>', views.itembuy_view),
    path('helping', views.help_view, name='help'),
    path('news', views.news_view, name='news'),
    path('category-sitesandweb', views.sitesandweb_view, name='sitesandweb'),
    path('category-scripts', views.scripts_view, name='scripts'),
    path('category-bots', views.bots_view, name='bots'),
    path('category-mobile', views.mobile_view, name='mobile'),
    path('category-software', views.software_view, name='software'),
    path('category-templates', views.templates_view, name='templates'),
    path('category-logo', views.logotype_view, name='logotype'),
    path('category-3DModels', views.treedmodels_view, name='treedmodels'),
    path('category-books', views.books_view, name='books'),
    path('category-courses', views.courses_view, name='courses'),
    path(f'account/@<str:username>', views.account_view),
    path('edit-profile', views.editprofile_view, name='edit-profile')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
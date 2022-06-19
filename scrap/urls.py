from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Web Scraper Admin"
admin.site.site_title = "Web Scraper Admin Portal"
admin.site.index_title = "Welcome to Web Scraper"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('scraper.urls')),

]
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.decorators.cache import cache_page
from newreleases.views import new_releases, rights_flags, batchmaker, \
    batch, addbatch, root, addidea, ideamaker, failures_text, single_id, buildstatus

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       
    # Root Pages
    (r'^$', root),
    
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #Rights description
    (r'^rights/(\d+)/$', rights_flags),
    
    #Batch maker and root page
    (r'^batchmaker/$', batchmaker),
    
    #Batch viewer
    (r'^batch/(\d+)/$', batch),
    #Batch text viewer
    (r'^text/(\d+)/$', failures_text),
    #Single Id viewer
    (r'^id/(\d+)/$', single_id),
    
    #Batch maker and root page
    (r'^addbatch/$', addbatch),
    
    #Batch maker and root page
    (r'^ideamaker/$', ideamaker),
    
    #Batch maker and root page
    (r'^addidea/$', addidea),
    
    #Batch maker and root page
    (r'^status/build/$', buildstatus),
)

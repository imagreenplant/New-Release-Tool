from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, HttpResponseRedirect
from djangomako.shortcuts import render_to_response, render_to_string
from django.conf import settings
from nrdb.models import Batch, Idea

from nrforms import BatchForm, IdeaForm

import new_releases_tool
import BuildStatus
from Tools import Tools

#environment specific url prefix
url_prefix = settings.SITE_PREFIX
configs = {'url_prefix':url_prefix,'media_url':settings.MEDIA_URL}
    
def root(request):
    template = 'root.html'

    context_data = {'configs':configs}
    return render_to_response(template, context_data)

def new_releases(request):
    template = 'new_releases.html'

    releasesObject = new_releases_tool.NewReleasesTool()
    releasesObject.limit = 3  #sets default returned releases
    releases_data = releasesObject.getNewReleasesInfo()

    context_data = {'releases':releases_data,'configs':configs }
    return render_to_response(template, context_data)

def batch(request, batch_id):
    template = 'albums_listed.html'
    release_id_list = []
    
    release_object = Batch.objects.get(id=batch_id)
    
    if release_object.release_set.values():
        for release_info in release_object.release_set.values():
            release_id_list.append('alb.' + str(release_info['release_id']) )
            
    if release_id_list:
        releasesObject = new_releases_tool.NewReleasesTool()
        releases_data,error_tally = releasesObject.getAlbumDataForAlbumList(release_id_list)
        
        context_data = {'releases':releases_data,'configs':configs,'error_tally':error_tally}
        return render_to_response(template, context_data)
        
def single_id(request, album_id):
    template = 'albums_listed.html'
    
    if album_id:
        release_id_list = [('alb.' + album_id)]
        releasesObject = new_releases_tool.NewReleasesTool()
        releases_data,error_tally = releasesObject.getAlbumDataForAlbumList(release_id_list)
        
        context_data = {'releases':releases_data,'configs':configs,'error_tally':error_tally}
        return render_to_response(template, context_data)

def failures_text(request,batch_id):
    template = 'text_failures.html'
    release_id_list = []
    
    release_object = Batch.objects.get(id=batch_id)
    
    if release_object.release_set.values():
        for release_info in release_object.release_set.values():
            release_id_list.append('alb.' + str(release_info['release_id']) )
            
    if release_id_list:
        releasesObject = new_releases_tool.NewReleasesTool()
        releases_data,error_tally = releasesObject.getAlbumDataForAlbumList(release_id_list)
        
        context_data = {'releases':releases_data,'configs':configs,'error_tally':error_tally}
        return render_to_response(template, context_data)

def batchmaker(request):
    template = 'batchmaker.html'
    
    batch_form = BatchForm()
    all_batches = Batch.objects.all().order_by('-id')[:25]

    context_data = {'batch_form':batch_form,'batches':all_batches,'configs':configs}
    return render_to_response(template, context_data)
    
def addbatch(request):
    if request.method == 'POST':
        batch = BatchForm(request.POST)
    
    if batch.is_valid():
        if batch.testForValidIds():
            batch.save()
    else:
        print "error"
        #redirect back to batchmaker with error statement
    
    return HttpResponseRedirect(settings.SITE_PREFIX + "batchmaker/")
    
def addidea(request):
    if request.method == 'POST':
        idea = IdeaForm(request.POST)
    
    if idea.is_valid():
        idea.save()
    else:
        print "error saving idea"
        #redirect back to batchmaker with error statement
    
    return HttpResponseRedirect(settings.SITE_PREFIX + "ideamaker/")
    
def ideamaker(request):
    template = 'ideas.html'
    
    idea_form = IdeaForm()
    all_ideas = Idea.objects.all().order_by('-id')[:25]

    context_data = {'idea_form':idea_form,'ideas':all_ideas,'configs':configs}
    return render_to_response(template, context_data)

def rights_flags(request,rights_number):
    template = 'rights.html'

    releasesObject = new_releases_tool.NewReleasesTool()
    rights_data = releasesObject.returnRightsFlags(rights_number)

    context_data = {'rights':rights_data, 'configs':configs}
    return render_to_response(template, context_data)
    
def buildstatus(request):
    template = 'buildstatus.html'
    
    buildStatusObject = BuildStatus.BuildStatus()
    cds_data = buildStatusObject.getCDSStatus()
    cps_build = buildStatusObject.getcpsBuildStatus()
    
    context_data = {'cds':cds_data, 'cps':cps_build, 'configs':configs}
    return render_to_response(template, context_data)
    
    
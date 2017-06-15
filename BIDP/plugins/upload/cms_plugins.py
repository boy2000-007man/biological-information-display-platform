from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from django.forms.util import ErrorList
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import upload
from .forms import UploadProjectForm, UploadSampleForm
from .AccessToDB import AccessToMongoDB

import json
import datetime

tmp = {"Projects":"",'Project ID':"",'# OF Total Sequence':"",'# of ORFS':"",'# of Samples':"","Read Length":"","Create Date":"","Update Data":""}

def process_operation(request):
    print "process_operation start ..."
    if request.method == 'POST' and request.user.is_authenticated():
        operation_type = request.POST.get("operation_type")
        if  operation_type == "Upload Project":
            form = UploadProjectForm(request.POST, request.FILES)
            if form.is_valid():
                project_name = form.cleaned_data["project_name"]
                project_description = form.cleaned_data["project_description"]
                upload_file = form.cleaned_data["upload_file"]
                upload_file = upload_file.read() if upload_file else None
                project_creator = request.user.username
                project_createdate = datetime.date.today().isoformat()
                db = AccessToMongoDB()
                tmp.update({"Projects":project_name})
                ret = db.GeneralInterface("create", project_name, project_creator, tmp)
                if ret == 1:
                    db.GeneralInterface("write_document", project_name+"Project", "projects", {"name":project_name,"createDate":project_createdate,"description":project_description})
                    if upload_file:
                        db.GeneralInterface("write_document", project_name+"Project", "samples", json.loads(upload_file))
                        details = "add %s project with samples" % project_name
                    else:
                        details = "add %s project without samples" % project_name
                elif ret == 2:
                    if upload_file:
                        db.GeneralInterface("write_document", project_name+"Project", "samples", json.loads(upload_file))
                        details = "replace %s project with samples" % project_name
                    else:
                        details = "replace %s project without samples" % project_name
                elif ret == 3:
                    details = "ERROR:%s project is already created by other user" % project_name
        elif operation_type == "Upload Sample":
            form = UploadSampleForm(request.POST, request.FILES)
            if form.is_valid():
                project_name = form.cleaned_data["project_name"]
                upload_file = form.cleaned_data["upload_file"].read()
                sample_creator = request.user.username
                sample_createdate = datetime.date.today().isoformat()
                db = AccessToMongoDB()
                tmp.update({"Projects":project_name})
                ret = 2#db.GeneralInterface("create", project_name, sample_creator, tmp)
                if ret == 1:
                    db.GeneralInterface("write_document", project_name+"Project", "projects", {"name":project_name,"createDate":sample_createdate})
                    db.GeneralInterface("write_document", project_name+"Project", "samples", json.loads(upload_file))
                    details = "add sample to new %s project" % project_name
                elif ret == 2:
                    db.GeneralInterface("write_document", project_name+"Project", "samples", json.loads(upload_file))
                    details = "add sample to existed %s project" % project_name
                elif ret == 3:
                    details = "ERROR:%s project is already created by other user" % project_name
        elif operation_type == "Delete Project":
            pass
        elif operation_type == "Delete Sample":
            pass
        try:
            details
        except NameError:
            details = "ERROR:wrong operation type or form is invalid"
        new_upload = upload(username = request.user.username,
                            action = operation_type+details)
        new_upload.save()
    print "process_operation end."
    return HttpResponseRedirect(
        request.META.get("HTTP_REFERER")
            if request.META.get("HTTP_REFERER") and request.META.get("HTTP_REFERER") != reverse("process_operation")
        else "/"
    )
    
class UploadHistoryPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("UploadHistory")
    render_template = "history.html"
    admin_preview = True
    cache = False
    def render(self, context, instance, placeholder):
        if context['request'].user.is_superuser:
            context['history'] = upload.objects.all()
        elif context['request'].user.is_authenticated():
            context['history'] = upload.objects.filter(username = context['request'].user.username)
        context['instance'] = instance
        return context
        
class UploadProjectPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("UploadProject")
    render_template = "form.html"
    admin_preview = True
    cache = False
    def render(self, context, instance, placeholder):
        if context['request'].user.is_authenticated():
            context['form'] = UploadProjectForm()
        context['instance'] = instance
        return context
        
class UploadSamplePlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("UploadSample")
    render_template = "form.html"
    admin_preview = True
    cache = False
    def render(self, context, instance, placeholder):
        if context['request'].user.is_authenticated():
            context['form'] = UploadSampleForm(initial = {"project_name":context["request"].GET.get("name")})
            print context["request"].GET.get("name")
        context['instance'] = instance
        return context

plugin_pool.register_plugin(UploadHistoryPlugin)
plugin_pool.register_plugin(UploadProjectPlugin)
plugin_pool.register_plugin(UploadSamplePlugin)			

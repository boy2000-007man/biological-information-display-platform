from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

#from .models import ProjectGrid
from .AccessToDB import AccessToMongoDB

class SamplesGridPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("SamplesGrid")
    render_template = "samples_grid_template.html"
    admin_preview = True
    cache = False
    def render(self, context, instance, placeholder):
        #print("Debug")
        #print(context['request'].GET)
        #print("End debug")
        
        requestGET = context['request'].GET
        context['data'] = []
        #Add some code here
        
        #db_access = AccessToMongoDB("local")
        #instance = db_access.GetProjectInfo("")
        db = AccessToMongoDB()
        projects = db.GeneralInterface('projectLists', 'projectLists','projectInfo')

        projectname = ""
        #for i in projects :
        #    if i['Project ID'] == 'MGP-D' + '0'*(3-len(requestGET['id'])) + requestGET['id'] :
        #        projectname = i['Projects']

        projectname = requestGET['name']
        context['data'] = db.GeneralInterface("samples", projectname + "Project", "samples")

        
        
        context['instance'] = instance
        return context


plugin_pool.register_plugin(SamplesGridPlugin)

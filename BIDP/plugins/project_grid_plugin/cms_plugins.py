from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import ProjectGrid
from .AccessToDB import AccessToMongoDB


class ProjectGridPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("ProjectGrid")
    render_template = "project_grid_template.html"
    admin_preview = True
    cache = False
    def render(self, context, instance, placeholder):
        #print("Debug")
        #print(context['request'].GET)
        #print(context)
        #print("End debug")
        
        requestGET = context['request'].GET
        context['data'] = []
        
        #Add some code here 
        #db_access = AccessToMongoDB("local")
        #instance = db_access.GetProjectInfo("")
        db = AccessToMongoDB()
        context['data'] = db.GeneralInterface('projectLists', 'projectLists','projectInfo')
        print(context['data'])
        
        context['instance'] = instance
        return context


plugin_pool.register_plugin(ProjectGridPlugin)

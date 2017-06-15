from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

from .models import GetRequest

class GetRequestPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Get Request")
    render_template = "project_grid_template.html"
    admin_preview = True
    cache = False
    def render(self, context, instance, placeholder):
        print("Debug")
        print(context['request'].GET)
        print("End debug")
        
        requestGET = context['request'].GET
        
        #Add some code here 

        
        context['instance'] = instance
        return context


plugin_pool.register_plugin(GetRequestPlugin)

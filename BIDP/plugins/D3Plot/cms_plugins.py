from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin
from django.utils.translation import ugettext_lazy as _

class D3PlotPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("D3Plot")
    render_template = "D3Plot.html"
    admin_preview = True
    cache = False

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(D3PlotPlugin)

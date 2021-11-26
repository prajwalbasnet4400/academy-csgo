from django.http.response import Http404
from django.views.generic.base import TemplateView
from django.views.generic import FormView,ListView
from django.urls import reverse_lazy
from django.conf import settings

from opengsq import CSGO
from .functions import send_message_discord

from .models import LvlBase, Server, Vip
from steam.models import Profile
from . import resolver
from . import forms

class Index(TemplateView):
    template_name = 'index.html'

class ServerView(TemplateView):
    template_name = 'stats/servers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servers = Server.objects.all()
        data = []
        for server in servers:
            try:
                q = CSGO(server.ip,int(server.port),timeout=1)
                q = q.get_info()
            except:
                q = {
                    'Name':server.display_name
                }
            q['ip'] = server.ip
            q['port'] = server.port
            data.append(q)
        context['servers'] = data
        return context

class ProfileView(TemplateView):
    template_name = 'stats/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        steamid64 = self.kwargs.get('steamid64')

        profile = Profile.objects.filter(steamid64=steamid64)
        if not profile.exists():
            player = resolver.get_playerinfo_s64(steamid64)
            if player:
                profile = Profile.objects.create(steamid64=player.get('steamid'),
                                        avatar=player.get('avatarfull'),nickname=player.get('personaname'))
            else:
                raise Http404
        else:
            profile = profile.first()
        warmup_stat = LvlBase.objects.filter(steam=profile.get_steamid()).using('warmup').first()
        retake_stat = LvlBase.objects.filter(steam=profile.get_steamid()).using('retake').first()
        context['profile'] = profile
        context['warmup'] = warmup_stat
        context['retake'] = retake_stat
        return context

class VipListView(ListView):
    template_name = 'stats/vip_list.html'
    queryset = Vip.objects.all().select_related('server')

class RetakeView(ListView):
    template_name = 'stats/stats.html'
    queryset = LvlBase.objects.using('retake').order_by('-value')[:100]
    extra_context = {'table_title':'RETAKE STATS'}

class WarmupView(ListView):
    template_name = 'stats/stats.html'
    queryset = LvlBase.objects.using('warmup').order_by('-value')[:100]
    extra_context = {'table_title':'WARMUP STATS'}

class ReportView(FormView):
    template_name = 'stats/reportform.html'
    form_class = forms.ReportPlayerForm
    hook_url = settings.REPORT_DISCORD_WEBHOOK_URL
    success_url  = reverse_lazy('stats:report')
    extra_context = {'reporttitle':'REPORT PLAYER'}

    
    def form_valid(self, form):
        resp = super().form_valid(form)
        data = form.cleaned_data
        msg = f"""
--------------------------------------------------
**REPORT PLAYER**

**SUSPECT PROFILE:** {data['suspect_steam_id']}
**SUSPECT NICKNAME:** {data['suspect_nickname']}
**YOUR NAME:** {data['self_name']}
**YOUR EMAIL:** {data['self_email']}
**SERVER:** {data['server'].display_name}
**STATEMENT:** {data['comment']}
--------------------------------------------------
"""
        send_message_discord(self.hook_url,msg)
        return resp

class AppealView(FormView):
    template_name = 'stats/reportform.html'
    form_class = forms.AppealBanForm
    hook_url = settings.APPEAL_DISCORD_WEBHOOK_URL
    success_url  = reverse_lazy('stats:appeal')
    extra_context = {'reporttitle':'APPEAL BAN'}


    def form_valid(self, form):
        resp = super().form_valid(form)
        data = form.cleaned_data
        msg = f"""
--------------------------------------------------
**APPEAL BAN**

**STEAMID:** {data['steam_id']}
**NAME:** {data['name']}
**EMAIL:** {data['email']}
**REASON:** {data['reason']}
**SERVER:** {data['server'].display_name}
**COMMENT:** {data['comment']}
--------------------------------------------------
"""
        send_message_discord(self.hook_url,msg)
        return resp

class ContactView(FormView):
    template_name = 'stats/reportform.html'
    form_class = forms.ContactForm
    hook_url = settings.CONTACT_DISCORD_WEBHOOK_URL
    success_url  = reverse_lazy('stats:contact')
    extra_context = {'reporttitle':'CONTACT US'}

    def form_valid(self, form):
        resp = super().form_valid(form)
        data = form.cleaned_data
        msg = f"""
--------------------------------------------------
**CONTACT REQUEST**

**NAME:** {data['name']}
**EMAIL:** {data['email']}
**PHONE:** {data['phone']}
**SUBJECT:** {data['subject']}
**MESSAGE:** {data['message']}
--------------------------------------------------
"""
        send_message_discord(self.hook_url,msg)
        return resp

from django.shortcuts import redirect, render
from django.views.generic import View
from django.http import Http404
from django.views.generic.base import TemplateView
from django.views.generic import FormView,ListView
from django.urls import reverse_lazy

from .functions import get_steamid,get_steamid64
from .models import LvlBase, Server, Vip
from steam.models import Profile
from .forms import ReportPlayerForm,AppealBanForm,ContactForm
from opengsq import CSGO
import discord_notify as dn

import os
import dotenv

dotenv.load_dotenv()


class Index(TemplateView):
    template_name = 'index.html'

class Servers(TemplateView):
    template_name = 'stats/servers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servers = Server.objects.all()
        data = []
        for server in servers:
            q = CSGO(server.ip,int(server.port),timeout=1.5)
            q = q.get_info()
            q['ip'] = server.ip
            q['port'] = server.port
            data.append(q)
        context['servers'] = data
        return context

class VipListView(ListView):
    template_name = 'stats/vip_list.html'
    queryset = Vip.objects.filter(active=True).select_related('server')

class Retake(ListView):
    template_name = 'stats/retake.html'
    queryset = LvlBase.objects.using('retake').order_by('-value')[:100]

class Deathmatch(ListView):
    template_name = 'stats/deathmatch.html'
    queryset = LvlBase.objects.using('deathmatch').order_by('-value')[:100]

class Report(FormView):
    template_name = 'stats/report.html'
    form_class = ReportPlayerForm
    hook_url = os.environ.get('HOOK_URL')
    success_url  = reverse_lazy('stats:report')
    def form_valid(self, form):
        resp = super().form_valid(form)
        notifier = dn.Notifier(self.hook_url)
        notifier.send(form.cleaned_data,print_message=False)
        return resp

class Appeal(FormView):
    template_name = 'stats/appeal.html'
    form_class = AppealBanForm
    hook_url = os.environ.get('HOOK_URL')
    success_url  = reverse_lazy('stats:appeal')

    def form_valid(self, form):
        resp = super().form_valid(form)
        notifier = dn.Notifier(self.hook_url)
        notifier.send(form.cleaned_data,print_message=False)
        return resp

class Contact(FormView):
    template_name = 'stats/contact.html'
    form_class = ContactForm
    hook_url = os.environ.get('HOOK_URL')
    success_url  = reverse_lazy('stats:contact')

    def form_valid(self, form):
        resp = super().form_valid(form)
        notifier = dn.Notifier(self.hook_url)
        notifier.send(form.cleaned_data,print_message=False)
        return resp
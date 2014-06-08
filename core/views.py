# vim: ts=4 sw=4 et fdm=indent
from django.contrib.auth import login
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView, SingleObjectMixin

from braces.views import LoginRequiredMixin as BLoginRequiredMixin

from .forms import (RegistrationForm, CampaignForm, CampaignJoinForm,
                    CampaignOwnForm)
from .models import Hero, Campaign


class LoginRequiredMixin(BLoginRequiredMixin):
    redirect_unauthenticated_users = True
    raise_exception = False


class HeroDetailView(DetailView):
    model = Hero
    template_name = 'hero_detail.html'

    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user != self.object:
            raise Http404
        return super(HeroDetailView, self).get(request, *args, **kwargs)


class HeroRegisterView(CreateView):
    model = Hero
    form_class = RegistrationForm
    template_name = 'hero_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.next_ = self.request.GET.get('next', None)

        return super(HeroRegisterView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.next_ is not None:
            return self.next_

        return self.object.get_absolute_url()

    def get_context_data(self, *args, **kwargs):
        context = super(HeroRegisterView, self).get_context_data(*args, **kwargs)
        if self.next_ is not None:
            context['next'] = self.next_
        return context

    def form_valid(self, form, *args, **kwargs):
        hero = form.save()
        
        hero.backend='django.contrib.auth.backends.ModelBackend'
        login(self.request, hero)

        self.object = hero

        return HttpResponseRedirect(self.get_success_url())


class HomeView(TemplateView):
    template_name = 'home.html'


class CampaignAddView(CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'campaign_form.html'

    def form_valid(self, form, *args, **kwargs):
        campaign = form.save(commit=False)

        if self.request.user.is_authenticated():
            campaign.owner = self.request.user

        campaign.save()

        self.object = campaign
        
        return HttpResponseRedirect(self.get_success_url())


class CampaignDetailView(DetailView):
    model = Campaign
    template_name = 'campaign_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CampaignDetailView, self).get_context_data(**kwargs)

        context['vacancies'] = self.object.threshold - self.object.heroes.count()

        return context


class CampaignJoinView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Campaign
    form_class = CampaignJoinForm
    template_name = 'campaign_join.html'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        return super(CampaignJoinView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = self.get_object()
        campaign = self.object 

        if self.request.user not in campaign.heroes.all():
            campaign_hero = form.save(commit=False)
            campaign_hero.campaign = campaign
            campaign_hero.hero = self.request.user
            campaign_hero.save()

            messages.info(self.request, 'Joined campaign!')
        else:
            messages.error(self.request, 'Already in campaign!')

        return HttpResponseRedirect(campaign.get_absolute_url())


class CampaignOwnView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Campaign
    form_class = CampaignOwnForm
    template_name = 'campaign_own.html'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        return super(CampaignOwnView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = self.get_object()
        campaign = self.object 

        if campaign.owner:
            return PermissionDenied

        campaign.owner = self.request.user
        campaign.save()

        messages.info(self.request, 'You\'re now the owner of this campaign!')

        return HttpResponseRedirect(campaign.get_absolute_url())

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.list import MultipleObjectMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Veikla, Uzdarbis
from django.db.models import Q
from .forms import VeiklaForm, UzdarbisForm
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.urls import reverse_lazy


def home(request):
    context = {
        'veiklos': Veikla.objects.all()
    }
    return render(request, 'taxes_app/home.html', context)


def veikla_calendar(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    cal = HTMLCalendar().formatmonth(
        year,
        month_number)
    
    return render(request,
        'taxes_app/calendar.html',{
        "cal": cal,
        })

class VeiklaListView(LoginRequiredMixin, ListView, UserPassesTestMixin):
    model = Veikla
    template_name = 'taxes_app/home.html'
    context_object_name = 'veiklos'
    paginate_by = 5

    def form_valid(self, form):
        form.instance.asmuo = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        veikla = self.get_object()
        if self.request.user == veikla.asmuo:
            return True
        return False

    def get_queryset(self):
        return Veikla.objects.filter(asmuo=self.request.user).order_by('-date_posted')


class VeiklaCreateView(LoginRequiredMixin, CreateView):
    model = Veikla
    fields = ['pavadinimas', 'status3', 'status2', 'status']


    def form_valid(self, form):
        form.instance.asmuo = self.request.user
        return super().form_valid(form)

    
class VeiklaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Veikla
    fields = ['pavadinimas','status3', 'status2', 'status']

    def form_valid(self, form):
        form.instance.asmuo = self.request.user
        return super().form_valid(form)

    def test_func(self):
        veikla = self.get_object()
        if self.request.user == veikla.asmuo:
            return True
        return False


class VeiklaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Veikla
    success_url = '/'

    def test_func(self):
        veikla = self.get_object()
        if self.request.user == veikla.asmuo:
            return True
        return False

class UzdarbisListView(LoginRequiredMixin, ListView):
    model = Uzdarbis
    template_name = 'taxes_app/veikla_detail.html'
    context_object_name = 'uzdarbiai'
    paginate_by = 5
    
    def get_queryset(self):
        print(self.kwargs)
        object_list = Uzdarbis.objects.filter(darbas=self.kwargs['pk']).order_by('-date_posted')
        return object_list

    def get_context_data(self, *args, **kwargs):
        context = super(UzdarbisListView, self).get_context_data(*args, **kwargs)
        context['veikla'] = Veikla.objects.get(pk=self.kwargs['pk'])
        return context


class UzdarbisDetailView(DetailView):
    model = Uzdarbis

def veikla_detaliau(request, pk):
    veikla = Veikla.objects.get(pk=pk)
    # sumos = []
    # sumos.append(veikla.suma_pajamos)
    # sumos.append(veikla.suma_islaidos_pasirinkimas)
    # sumos.append(veikla.suma_mokesciai)
    # sumos.append(veikla.suma_pelnas)
    context = {
        "veikla": veikla,
        # "sumos" :sumos
    }

    return render(request, 'taxes_app/visas_uzdarbis_detail.html',context=context)


class UzdarbisCreateView(LoginRequiredMixin, CreateView):
    model = Uzdarbis
    # fields = ['pajamos', 'islaidos']
    form_class = UzdarbisForm

    def form_valid(self, form):
        form.instance.asmuo = self.request.user
        veikla_pk = int(self.request.GET.get('next'))
        veikla = Veikla.objects.get(pk=veikla_pk)
        form.instance.darbas = veikla
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        veikla_pk = int(self.request.GET.get('next'))
        veikla = Veikla.objects.get(pk=veikla_pk)
        if veikla.status2 == 'i30':
            islaidos = False
        else:
            islaidos = True

        context['islaidos'] = islaidos
        return context
    

class UzdarbisUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Uzdarbis
    # fields = ['pajamos', 'islaidos']
    form_class = UzdarbisForm
    

    def form_valid(self, form):
        form.instance.asmuo = self.request.user
        return super().form_valid(form)

    def test_func(self):
        uzdarbis = self.get_object()
        if self.request.user == uzdarbis.darbas.asmuo:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        veikla = context['object'].darbas
        if veikla.status2 == 'i30':
            islaidos = False
        else:
            islaidos = True

        context['islaidos'] = islaidos
        return context

    def get_success_url(self):
        uzdarbis = self.get_object().darbas.id
        return reverse_lazy('veikla-detail', kwargs={'pk': uzdarbis})


class UzdarbisDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Uzdarbis

    def test_func(self):
        uzdarbis = self.get_object()
        if self.request.user == uzdarbis.darbas.asmuo:
            return True
        return False
    
    def get_success_url(self):
        uzdarbis = self.get_object().darbas.id
        return reverse_lazy('veikla-detail', kwargs={'pk': uzdarbis})

def about(request):
    return render(request, 'taxes_app/about.html', {'pavadinimas': 'About'})


def search(request):
    
    query = request.GET.get('query')
    search_results = Veikla.objects.filter(Q(pavadinimas__icontains=query), Q(asmuo= request.user))
    return render(request, 'taxes_app/search.html', {'veiklos': search_results, 'query': query})

@login_required
def visual(request):
    veikla = Veikla.objects.filter(asmuo=request.user)
   
    context = {
        "veikla": veikla,
    }

    return render(request, 'taxes_app/visual.html', context)





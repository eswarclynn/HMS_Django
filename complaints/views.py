from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Complaint
from institute.models import Student, Official
from workers.models import Worker
from django.http.response import Http404
from django.contrib import messages
from django.views.generic import DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ComplaintCreationForm
from complaints.forms import ComplaintUpdationForm

# Create your views here.
class ComplaintDetailView(LoginRequiredMixin, DetailView):
    model = Complaint
    template_name = 'complaints/show.html'
    context_object_name = 'complaint'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComplaintUpdationForm(instance=self.get_object())
        return context
    

class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    template_name = 'complaints/new.html'
    form_class = ComplaintCreationForm

    def get_success_url(self):
        return self.request.user.home_url()

    def form_valid(self, form):
        form.instance.entity_id = (self.request.user.is_student and self.request.student.regd_no) or \
                                    (self.request.user.is_official and self.request.user.official.emp_id) or \
                                    (self.request.user.is_worker and self.request.user.worker.staff_id)
        form.instance.entity_type = (self.request.user.is_student and 'Student') or \
                                    (self.request.user.is_official and 'Official') or \
                                    (self.request.user.is_worker and 'Worker')
        form.instance.complainee = form.cleaned_data.get('complainee_id') and Student.objects.get(regd_no = form.cleaned_data.get('complainee_id'))

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Register Complaint'
        return context
    
class ComplaintUpdateView(LoginRequiredMixin, UpdateView):
    model = Complaint
    template_name = 'complaints/new.html'
    form_class = ComplaintUpdationForm

    def get_success_url(self):
        # return self.request.user.home_url()
        return reverse('complaints:complaint_detail', args=[self.get_object().pk])

class ComplaintDeleteView(LoginRequiredMixin, DeleteView):
    model = Complaint

    def get_success_url(self):
        return self.request.user.home_url()
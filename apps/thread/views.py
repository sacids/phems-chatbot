from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import JsonResponse
from .forms import ThreadForm
from .models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages


class ThreadListView(generic.ListView):
    model = Thread
    context_object_name = 'threads'
    template_name = 'threads/lists.html'
    # paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadListView, self).dispatch( *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ThreadListView, self).get_context_data(**kwargs)
        context['title'] = "Threads"

        return context

    def get_queryset(self, *args, **kwargs):
        """Filter data"""
        threads = Thread.objects.order_by('step')

        return threads


class ThreadDetailView(generic.DetailView):
    """View details"""
    model = Thread
    context_object_name = 'thread'
    template_name = 'threads/show.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadDetailView, self).dispatch( *args, **kwargs) 

    def get_context_data(self, *args, **kwargs):
        context = super(ThreadDetailView, self).get_context_data(**kwargs)
        context['title'] = "Thread"

        sub_threads = SubThread.objects.filter(thread_id=self.kwargs['pk']).order_by('view_id')
        context['sub_threads'] = sub_threads
        return context

    def post(self, request, *args, **kwargs):
        thread_id   = kwargs['pk']  
        view_id     = request.POST.get('view_id')    
        sub_thread  = request.POST.get('sub_thread') 

        new_sub           = SubThread()
        new_sub.title     = sub_thread
        new_sub.view_id   = view_id 
        new_sub.thread_id = thread_id 
        new_sub.save()

        return HttpResponseRedirect(reverse_lazy('threads:show', kwargs={'pk': thread_id}))


class ThreadCreateView(generic.CreateView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadCreateView, self).dispatch( *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'form': ThreadForm()}
        return render(request, 'threads/create.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        if form.is_valid():
            dt_menu = form.save(commit=False)
            dt_menu.created_by = request.user
            dt_menu.save()

            messages.success(request, 'Thread registered!')

            return HttpResponseRedirect(reverse_lazy('threads:lists'))
        return render(request, 'threads/create.html', {'form': form})  


class ThreadUpdateView(generic.UpdateView):
    """View to update"""
    model = Thread
    context_object_name = 'thread'
    form_class = ThreadForm
    template_name = 'threads/edit.html'

    def form_valid(self, form):
        response = form.save(commit=False)
        response.updated_by = self.request.user
        response.save()

        messages.success(self.request, 'Thread information updated!')

        return HttpResponseRedirect(reverse_lazy('threads:lists')) 


class ThreadDeleteView(generic.DeleteView):
    """View to delete a """ 
    model = Thread
    template_name = "threads/confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Thread deleted successfully")
        return reverse_lazy('threads:lists') 


class SubThreadDeleteView(generic.DeleteView):
    """View to delete a sub thread""" 
    model = SubThread
    template_name = "threads/confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Sub thread deleted successfully")
        return reverse_lazy('threads:lists') 



class ThreadLinkListView(generic.ListView):
    """Thread Links Crud Operation"""
    model = ThreadLink
    context_object_name = 'thread_links'
    template_name = 'thread_links/lists.html'
    # paginate_by = 50

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ThreadLinkListView, self).dispatch( *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ThreadLinkListView, self).get_context_data(**kwargs)
        context['title'] = "Thread Links"
        context['threads'] = Thread.objects.order_by('step')

        thread_links = ThreadLink.objects.order_by("thread__step").all()
        context['thread_links'] = thread_links

        return context

    def post(self, request):
        """create/updating thread link data"""
        thread_id = request.POST.get('thread_id')
        link_id = request.POST.get('link_id')

        sub_thread_id = None
        if request.POST.get('sub_thread_id') != '':
            sub_thread_id = request.POST.get('sub_thread_id')

        """update or create menu link"""
        thread_link, created = ThreadLink.objects.update_or_create(thread_id=thread_id, sub_thread_id=sub_thread_id, link_id=link_id, defaults={})
        
        #message
        messages.success(request, 'Thread link created/update!')

        #redirect
        return HttpResponseRedirect(reverse_lazy('threads:links'))

class ThreadLinkDeleteView(generic.DeleteView):
    """Delete a thread link""" 
    model = ThreadLink
    template_name = "thread_links/confirm_delete.html"

    def get_success_url(self):
        messages.success(self.request, "Thread link deleted successfully")
        return reverse_lazy('threads:links') 


def get_threads(request, *args, **kwargs):
    if request.method == 'GET':
        threads = Thread.objects.all().order_by('step')

        return render(None, 'threads/select.html', {'threads': threads})


def get_sub_threads(request, *args, **kwargs):
    if request.method == 'GET':
        thread_id = kwargs['thread_id']
        sub_threads = SubThread.objects.filter(thread_id=thread_id).order_by('view_id')

        return render(None, 'threads/select2.html', {'sub_threads': sub_threads})













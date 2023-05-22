from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView
from .models import Choice, Question
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.views.decorators.csrf import csrf_exempt







class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    
    if 'user_choice' in request.POST:
        user_choice_text = request.POST['user_choice'].strip()
        if user_choice_text:
            # Create a new Choice object for the user-generated choice
            user_choice = question.choice_set.create(choice_text=mark_safe(user_choice_text), votes=0)
            user_choice.save()
            # Increment the vote count for the user-generated choice
            user_choice.votes += 1
            user_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
@login_required
def AccountsView(request):
    username = User.username

    return render(request, 'registration/accounts.html', {'name':username})
@login_required


#The csrf_exempt below causes the code to be vulnerable to csrf attacks. To fix this vulnerability remove or uncomment the line.
@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()
            #update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('polls:accounts'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm()
    return render(request, 'registration/change_password.html', {'form': form})

class PasswordForm (forms.Form):
    #Here is a type of insecure design, which is considered as part of OWASP top ten list
    #Password is showed in plain text when a user is changing their password, to fix this the statement should be changed to the following:
    #password = forms.CharField(label="Enter new password:",max_length=40, widget=forms.PasswordInput)
    password = forms.CharField(label="Enter new password:",max_length=40)
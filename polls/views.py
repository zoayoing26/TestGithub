from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from .models import Question, Choice
from django.template import loader

from django.http import Http404

from django.urls import reverse

from django.db.models import F

from django.utils import timezone

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')

    context = {
        'latest_question_list': latest_question_list,
    }
    # output = ','.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)

    # return HttpResponse(template.render(context, request))

    return render(request, 'polls/index.html', context)


def detail(request, question_ids):

    question = get_object_or_404(Question, pk=question_ids)

    return render(request, 'polls/detail.html', {'question': question})

    try:
        question = Question.objects.get(pk=question_ids)
    except Question.DoesNotExist:
        raise Http404("Question does not exist 404")

    # return HttpResponse("detail Your looking at question %s."  % question_ids )

    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    
    question = get_object_or_404(Question, pk=question_id)
    
    return render(request, 'polls/results.html', {'question': question})


    # respones = "results Youer looking the result of question %s."
    # return HttpResponse(respones % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message2': "You didn't select a choice.",
        })
    else:
        #selected_choice.votes += 1
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        
        selected_choice.refresh_from_db()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls1:results', args=(question.id,)))
    


from django.views import generic

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by('-pub_date')[:5]
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        ttt ="""
        Excludes any questions that aren't published yet.
        """
       # print(ttt)
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
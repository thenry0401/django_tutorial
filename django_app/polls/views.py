from django.contrib import messages
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Question, Choice


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    latest_question_list = get_list_or_404(
        Question.objects.order_by('-pub_date')[:5]
    )
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    # detail.html 파일을 약간 수정해서 results.html을 만들고
    # 질문에 대한 모든 선택사항의 선택수(votes)를 출력
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
    }
    return render(request, 'polls/results.html', context)


def vote(request, question_id):
    # request의 method가 POST방식일 떄,
    # 전달받은 데이터중 'choice'키에 해당하는 값을
    # HttpResponse에 적절히 돌려준다
    if request.method == 'POST':
        data = request.POST
        try:
            choice_id = data['choice']
            choice = Choice.objects.get(id=choice_id)
            choice.votes += 1
            choice.save()
            return redirect('polls:results', question_id)
        except (KeyError, Choice.DoesNotExist):
            messages.add_message(
                request,
                messages.ERROR,
                "you didn't select a choice"
            )
            return redirect('polls:detail', question_id)
    else:
        return HttpResponse("You are voting on question %s." % question_id)

from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import Question


def home(request):
    return redirect('questions')

def questions(request):
    questions = list(Question.objects.all())

    current_index = int(request.GET.get("q", 0))

    # reset score at start
    if current_index == 0:
        request.session["score"] = 0
        request.session["last_answered"] = -1

    # safety init (if not present)
    request.session.setdefault("score", 0)
    request.session.setdefault("last_answered", -1)

    # if quiz finished
    if current_index >= len(questions):
        return render(request, 'myapp/result.html', {
            'total': len(questions),
            'score': request.session["score"]
        })

    question = questions[current_index]
    result = None
    selected_answer = None

    if request.method == "POST":
        selected_answer = request.POST.get("answer")

        # prevent double scoring
        if request.session.get("last_answered") != current_index:

            if selected_answer == question.correct_answer:
                result = "correct"
                request.session["score"] += 1
            else:
                result = "wrong"

            request.session["last_answered"] = current_index

    return render(request, 'myapp/questions.html', {
        'question': question,
        'result': result,
        'selected_answer': selected_answer,
        'current_index': current_index,
        'total': len(questions)
    })

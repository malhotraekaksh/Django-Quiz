from django.shortcuts import render
from .models import Question

def questions(request):
    questions = list(Question.objects.all())

    current_index = int(request.GET.get("q", 0))

   if current_index == 0:
       request.session["score"] = 0

    request.session.setdefault("last_answered", -1)

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

    # prevent re-scoring same question
    if request.session.get("last_answered") != current_index:

        if selected_answer == question.correct_answer:
            result = "correct"
            request.session["score"] += 1
        else:
            result = "wrong"

        request.session["last_answered"] = current_index

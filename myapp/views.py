from django.shortcuts import render, redirect
from .models import Question
from .forms import QuestionForm


# ---------------- HOME (redirect to dashboard)
def home(request):
    return redirect('dashboard')


# ---------------- DASHBOARD
def dashboard(request):
    return render(request, "myapp/dashboard.html")


# ---------------- START QUIZ
def start_quiz(request):
    request.session["score"] = 0
    request.session["last_answered"] = -1
    return redirect("questions")


# ---------------- QUIZ LOGIC
def questions(request):

    questions = list(Question.objects.all())
    total = len(questions)

    current_index = int(request.GET.get("q", 0))

    # safety init
    if "score" not in request.session:
        request.session["score"] = 0

    if "last_answered" not in request.session:
        request.session["last_answered"] = -1

    # FINISH CONDITION
    if current_index >= total:

        score = request.session.get("score", 0)

        # clear session after finishing
        request.session.flush()

        return render(request, "myapp/result.html", {
            "total": total,
            "score": score
        })

    question = questions[current_index]

    result = None
    selected_answer = None

    if request.method == "POST":
        selected_answer = request.POST.get("answer")

        if request.session["last_answered"] != current_index:

            if selected_answer == question.correct_answer:
                result = "correct"
                request.session["score"] += 1
            else:
                result = "wrong"

            request.session["last_answered"] = current_index

    return render(request, "myapp/questions.html", {
        "question": question,
        "result": result,
        "selected_answer": selected_answer,
        "current_index": current_index,
        "total": total
    })


# ---------------- ADD QUESTION
def add_question(request):
    form = QuestionForm()

    if request.method == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("add_question")

    return render(request, "myapp/add_question.html", {
        "form": form
    })

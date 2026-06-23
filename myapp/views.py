from django.shortcuts import render, redirect
from .models import Question
from .forms import QuestionForm


# ---------------- HOME
def home(request):
    return redirect('dashboard')


# ---------------- DASHBOARD
def dashboard(request):
    return render(request, "myapp/dashboard.html")


# ---------------- VIEW QUESTIONS
def view_questions(request):
    questions = Question.objects.all()

    return render(request, "myapp/view_questions.html", {
        "questions": questions
    })


# ---------------- START QUIZ
def start_quiz(request):
    request.session["answers"] = {}
    return redirect("questions")


# ---------------- QUIZ (FIXED SCORE SYSTEM)
def questions(request):

    questions = list(Question.objects.all())
    total = len(questions)

    current_index = int(request.GET.get("q", 0))

    # init answers only
    if "answers" not in request.session:
        request.session["answers"] = {}

    answers = request.session["answers"]

    # FINISH QUIZ → CALCULATE SCORE HERE (IMPORTANT FIX)
    if current_index >= total:

        score = 0

        for i, q in enumerate(questions):
            ans = answers.get(str(i))
            if ans == q.correct_answer:
                score += 1

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

        # store only once per question
        if str(current_index) not in answers:

            answers[str(current_index)] = selected_answer
            request.session["answers"] = answers
            request.session.modified = True

            if selected_answer == question.correct_answer:
                result = "correct"
            else:
                result = "wrong"

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
    success = False

    if request.method == "POST":

        form = QuestionForm(request.POST)

        if form.is_valid():
            form.save()
            success = True
            form = QuestionForm()

    return render(request, "myapp/add_question.html", {
        "form": form,
        "success": success
    })

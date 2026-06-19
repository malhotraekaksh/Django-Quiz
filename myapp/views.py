from django.shortcuts import render, redirect
from .models import Question
from .forms import QuestionForm
import csv
from django.http import HttpResponse


def home(request):
    return redirect('questions')


def questions(request):
    questions = list(Question.objects.all())

    current_index = int(request.GET.get("q", 0))

    if current_index == 0:
        request.session["score"] = 0
        request.session["last_answered"] = -1

    request.session.setdefault("score", 0)
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


def add_question(request):
    form = QuestionForm()

    if request.method == "POST":
        form = QuestionForm(request.POST)

        print("POST DATA RECEIVED:", request.POST)  # 👀 see input

        if form.is_valid():
            question = form.save()
            print("SAVED QUESTION:", question)  # 👀 confirm save
        else:
            print("FORM ERRORS:", form.errors)  # ❌ show problem

    return render(request, "myapp/add_question.html", {
        "form": form
    })


def start_quiz(request):
    return render(request, "myapp/start.html")


def upload_questions(request):
    if request.method == "POST":
        file = request.FILES['file']

        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded_file)

        for row in reader:
            Question.objects.create(
                question_text=row[0],
                option_a=row[1],
                option_b=row[2],
                option_c=row[3],
                option_d=row[4],
                correct_answer=row[5]
            )

        return HttpResponse("Questions uploaded successfully!")

    return render(request, "myapp/upload.html")

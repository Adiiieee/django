from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from authentication import settings
from .models import Question

# Create your views here.
def home(request):
    return render(request, "polls/home.html")

def signup(request):

    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username")
            return redirect('polls:home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('polls:home')
        
        if len(username)>10:
            messags.error(request, "Username must be under 10 characters")
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")
        
        #username : alpha-numeric
        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric!")
            return redirect('polls:home')

            

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        
        myuser.save()

        messages.success(request, "Your Account has been successfully created")

        return redirect('polls:signin')

    return render(request, "polls/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "polls/index.html", {'fname': fname})
        
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('polls:home')


    return render(request, "polls/signin.html")

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
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
#   subject = "Polls App"
#   message = "Thanks for your voting!!"
#   from_email = settings.EMAIL_HOST_USER
#   to_list = [myuser.email]
#   send_mail(subject, message, from_email, to_list, fail_silently=True)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('polls:home')
    # return render(request, "polls/signout.html")
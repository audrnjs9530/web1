from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from user.forms import CustomUserCreationForm
from django.contrib.auth import login
from post.models import Post

# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')




class SignUpView(View):
    def get(self, request):
        return render(
            request, 'registration/sign_up.html',
            {'form': CustomUserCreationForm})
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
        return redirect('home')


class MyPageView(View):
    def get(self, request, ):
        my_posts = Post.objects.filter(author=request.user).order_by('-created_at')
        context = {
            'my_posts': my_posts,

        }
        return render(request, 'mypage.html', context)
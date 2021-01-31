from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .forms import PostForm
from django.shortcuts import redirect

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
    
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    LoginUser = request.user
    author = post.author
    context = {
        'post': post,
        'LoginUser': LoginUser,
        'author': author
    }
    
    if 'publish' in request.POST:
        post.published_date = timezone.now()
        post.save()
    return render(request, 'blog/post_detail.html', context)
    
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if 'publish' in request.POST:
                post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now()
            if 'publish' in request.POST:
                post.published_date = timezone.now()
            elif 'private' in request.POST:
                post.published_date = None
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
    
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    
    return redirect('post_list')
    
def mypage(request):
    if Post.objects.filter(author=request.user):
        posts = get_list_or_404(Post, author=request.user)
    else:
        posts = None
    return render(request, 'blog/mypage.html', {'posts': posts})
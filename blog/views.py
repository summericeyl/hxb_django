from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.http import HttpResponse


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   #publish__month=month,
                                   #publish__day=day
                             )
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

def post_archive(request):
    try:
        object_list = Post.published.all()
    except Post.DoesNotExist:
        raise Http404
    return render(request, 'archives.html', {'post_list': object_list,
                                             'error': False})

def about_me(request) :
    return render(request, 'aboutme.html')


def search_tag(request,tag):
    try:
        object_list = Post.published.filter(category = tag)
    except Post.DoesNotExist:
        raise Http404

    return render(request, 'tag.html', {'post_list': object_list})
from django.shortcuts import render, get_object_or_404
from .models import NewsPost
import markdown

def news_feed(request):
    posts = NewsPost.objects.order_by('-created_at')
    for post in posts:
        post.content_html = markdown.markdown(post.content or "")
    return render(request, 'news/news_feed.html', {'posts': posts})

def news_detail(request, post_id):
    post = get_object_or_404(NewsPost, id=post_id)
    post.content_html = markdown.markdown(post.content)
    return render(request, 'news/news_detail.html', {'post': post})
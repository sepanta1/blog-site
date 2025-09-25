from django import template
from blog.models import Post, Category,Comments

register = template.Library()


@register.filter(name='inshort')
def inshort(value, arg=50):
    return value[:arg] + '...'


@register.inclusion_tag('latest-posts.html', name='latest_posts')
def latest_posts():
    posts = Post.objects.filter(status=1).order_by('-published_date')[:4]
    return {'posts': posts}


@register.inclusion_tag('category_count.html', name='category_count')
def category_count():
    posts = Post.objects.filter(status=True)
    categories = Category.objects.all()
    cat_dict=dict()
    for i in categories:
        cat_dict[i]=posts.filter(category=i).count()
       

    return {'categories': cat_dict}

@register.simple_tag(name='comments_count')
def comments_count(pid):
    post=Post.objects.get(pk=pid)
    comments=Comments.objects.filter(parent_post=post.id,approved=True).count()
    context={'post':post,'comments':comments}
    return context['comments']
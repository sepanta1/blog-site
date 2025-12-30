from django import template
from blog.models import Post, Category, Comments

register = template.Library()


@register.filter(name='inshort')
def inshort(value, arg=50):
    """
    Custom template filter to truncate a string to a specified length.
    
    Adds '...' at the end if the string is longer than the given length.
    Default length is 50 characters.
    Usage: {{ some_text|inshort:100 }}
    """
    return value[:arg] + '...'


@register.inclusion_tag('latest-posts.html', name='latest_posts')
def latest_posts():
    """
    Inclusion tag to display the 4 most recent published posts.
    
    Renders the 'latest-posts.html' template with a context containing
    the latest posts ordered by publication date.
    """
    posts = Post.objects.filter(status=1).order_by('-published_date')[:4]
    return {'posts': posts}


@register.inclusion_tag('category_count.html', name='category_count')
def category_count():
    """
    Inclusion tag to show the number of published posts in each category.
    
    Builds a dictionary mapping each Category object to its post count
    and passes it to the 'category_count.html' template.
    """
    # Get all published posts
    posts = Post.objects.filter(status=True)
    
    # Get all categories
    categories = Category.objects.all()
    
    # Create dictionary: {category_object: post_count}
    cat_dict = dict()
    for i in categories:
        cat_dict[i] = posts.filter(category=i).count()
    
    return {'categories': cat_dict}


@register.simple_tag(name='comments_count')
def comments_count(pid):
    """
    Simple tag that returns the number of approved comments for a given post.
    
    Takes the post ID (pid) and returns the count of approved comments.
    Usage in template: {% comments_count post.pk %}
    """
    # Retrieve the post object
    post = Post.objects.get(pk=pid)
    
    # Count only approved comments linked to this post
    comments = Comments.objects.filter(parent_post=post.id, approved=True).count()
    
    return comments
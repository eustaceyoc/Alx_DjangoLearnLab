from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Article

# View article
@permission_required('articles.can_view', raise_exception=True)
def view_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/view_article.html', {'article': article})

# Create article
@permission_required('articles.can_create', raise_exception=True)
def create_article(request):
    # your create logic here
    pass

# Edit article
@permission_required('articles.can_edit', raise_exception=True)
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # your edit logic here
    pass

# Delete article
@permission_required('articles.can_delete', raise_exception=True)
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # your delete logic here
    pass

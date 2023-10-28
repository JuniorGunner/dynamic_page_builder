from django.shortcuts import render, redirect, get_object_or_404
from .models import HTMLElement, WebPage
from django.http import HttpResponse
from .forms import HTMLElementForm, WebPageForm


def create_webpage(request):
    if request.method == 'POST':
        form = WebPageForm(request.POST)
        if form.is_valid():
            web_page = form.save(commit=False)
            web_page.user = request.user  # Assign the currently logged-in user
            web_page.save()
            return redirect('build_page', slug=web_page.slug)
    else:
        form = WebPageForm()

    return render(request, 'create_webpage.html', {'form': form})


def build_page(request, slug=None):
    page = get_object_or_404(WebPage, slug=slug)

    if request.method == 'POST':
        form = HTMLElementForm(request.POST)
        if form.is_valid():
            element = form.save(commit=False)
            element.page = page
            element.save()
            return redirect('preview_page', slug=slug)
    else:
        form = HTMLElementForm(initial={'page': page.id})

    return render(request, 'build_page.html', {'form': form, 'slug': slug})


def preview_page(request, slug):
    page = get_object_or_404(WebPage, slug=slug)
    root_elements = HTMLElement.objects.filter(page=page, parent=None)
    
    # Render the elements into a string but without Bootstrap for the preview
    html_str = ""
    for element in root_elements:
        html_str += element.render()  # This is from our OOP approach earlier
    
    if request.method == "POST":
        # User has confirmed the creation, so redirect to the final rendered page (which will have Bootstrap)
        return redirect('render_page', slug=slug)
    
    return render(request, 'preview.html', {'preview_content': html_str})



def render_page(request, slug):
    page = get_object_or_404(WebPage, slug=slug)
    root_elements = HTMLElement.objects.filter(page=page, parent=None)
    
    # Add the Bootstrap CDN to the rendered page
    bootstrap_css = '<link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">'
    bootstrap_js = '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>'
    
    html_str = f"<!DOCTYPE html><html><head>{bootstrap_css}</head><body>"
    
    for element in root_elements:
        html_str += element.render()  # This is from our OOP approach earlier
    
    html_str += f"{bootstrap_js}</body></html>"
    
    return HttpResponse(html_str)

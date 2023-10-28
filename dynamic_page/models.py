from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class HTMLElement(models.Model):
    TAG_CHOICES = [
        ('div', 'div'),
        ('p', 'p'),
        ('a', 'a'),
        #... Add more as needed
    ]

    tag_name = models.CharField(max_length=5, choices=TAG_CHOICES)
    content = models.TextField(blank=True, null=True)
    attributes = models.JSONField(blank=True, null=True)  # Stores attributes as JSON
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True) # For nesting
    page = models.ForeignKey('WebPage', on_delete=models.CASCADE)  # Which page this element belongs to


    def render(self):
        attributes_str = ' '.join(f'{key}="{value}"' for key, value in self.attributes.items()) if self.attributes else ''
        
        # Fetch and render children
        child_elements = HTMLElement.objects.filter(parent=self)
        child_html = ''.join(child.render() for child in child_elements)
        
        return f'<{self.tag_name} {attributes_str}>{self.content}{child_html}</{self.tag_name}>'
    
    
    def __str__(self):
        return self.tag_name + (": " + self.content if self.content else '')




class WebPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Owner of the page
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # For URL routing
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(WebPage, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.name

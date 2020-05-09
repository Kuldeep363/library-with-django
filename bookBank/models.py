from django.db import models
from django.utils.text import slugify
from django.urls import reverse 
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFit

# Create your models here.
class subjects(models.Model):
    title = models.CharField(max_length=250,default='',blank=True)
    slug = models.SlugField(blank=True,default='')
    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(subjects,self).save()

class author(models.Model):
    title = models.CharField(max_length=250,default='',blank=True)
    slug = models.SlugField(blank=True,default='')

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(author,self).save()
    

class books(models.Model):
    title = models.CharField(max_length=250, blank=True)
    authors = models.ManyToManyField(author)
    price = models.IntegerField(blank=True,default = 500)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(subjects,on_delete=models.PROTECT,null=True)
    image = models.ImageField(default = ' ', blank=True, upload_to = 'images' )
    img_thumbnail = ImageSpecField(source='image',
                    processors=[ResizeToFit(300,600)],
                    format='jpeg',
                    options={'quality':70}
            )
    pdf_file = models.FileField(default = ' ', blank = True, upload_to = 'files')
    slug = models.SlugField(blank=True)
    
    def __str__(self):
        return  self.title
    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(books,self).save()
    
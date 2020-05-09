from django.shortcuts import render,get_object_or_404
from bookBank.models import books,author,subjects
from .forms import addForm, form_add
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import FileResponse
# Create your views  
def index(request):
    item = request.GET.get('search',None)
    if item is None or item == "":
        book = books.objects.all() 
    elif item is not None:
        book = books.objects.filter(title__contains=item)
    return render(request,'bookBank/index.html',{'book':book}) 

def subject(request,slug=None):
    book = books.objects.filter(subject__slug=slug)
    return render(request,'bookBank/index.html',{'book':book})

def details(request,slug=None):
    book = get_object_or_404(books,slug=slug)
    similar_books = books.objects.all() 
    return render(request,'bookBank/details.html',{'book':book,'similar_books':similar_books})

def authors(request,slug=None):
    book = books.objects.filter(authors__slug=slug)
    return render(request,'bookBank/author.html',{'book':book,'author':slug}) 

# function to check whether field data is empty or not
def is_empty(values):
    if values == '' or values == None:
        return True
    else:
        return False
# function to remove extra space arround the authors name
def trim_space(lst):
    
    track=0
    for item in lst:
        n=len(item)-1
        if item[0] == ' ' and item[n] == ' ':
                item = item[1:n]
        elif item[0] ==' ':
                item= item[1:n+1]
        elif item[n] == ' ':
                item = item[:n]
        count = 0
        # print(item)
        for i in item:
            if i == ' ' and item[count+1] == ' ':
                item = item[:count] + item[count+1:]
            count+=1
        # print(item)
        lst[track]=item
        track+=1
    return lst


front = ['frontend','front end','frontend web development','frontend webdevelopment','frontend web','front end web','front end web development','front end webdevelopment']
back = ['backend','back end','backend web development','backend webdevelopment','backend web','back end web','back end web development','back end webdevelopment']
version = ['version','version control','project version control','versioncontrol']
db = ['data base','db','database','data base design','database design']


def addBook(request):
    title_error = price_error = desc_error = author_error = sub_error = image_error = pdf_error = upload_success = ' ' #all local variables for errors
    if request.method == 'POST': # get POST request
        form = form_add(request.POST, request.FILES) # request.FILES used gettinf files form form such as img,pdf files,etc.
        flag = 1 # flag for controll errors 

        '''
            get form data and convert the data into lowercase letters using str.lower()
            form.data['name of field in form'] eg. title for 'title' field in form <input type='text' name='title'>
        '''
        title = form.data['title'].lower() 
        price = form.data['price'].lower()
        desc = form.data['description'].lower()
        subject = form.data['subject'].lower()

        '''
            authors may be more than one, so we take input seperated by comma(,) and split data using split() method and
            convert it into list of authors name 
        '''
        authors_list = list(form.data['authors'].split(',')) 

        
        '''
            checking for field, whether they are empty or not using is_empty function defined above,
            if any of the filed is empty then flag set to 0 and there error msg's sre set.
        '''
        if is_empty(title):
            flag = 0
            title_error = 'Please Enter The Tittle of Book'
        if is_empty(price):
            flag = 0
            price_error = 'Please Enter The Price of Book'
        if is_empty(desc):
            flag = 0
            desc_error = 'Please Enter The Description For Book'
        if authors_list == ['']:
            flag = 0
            author_error = 'Please Enter The Authors of Book'
        if is_empty(subject):
            flag = 0
            sub_error = 'Please Enter The Subject or Domain of Book'

        if flag == 1:  # checking for flag i.e if flag is 0 then there is error in field and if flag is 1 then check for for form and files
            if form.is_valid:
                IMAGE_TYPE = ['png','jpg','jpeg'] # valid image extensions
                FILE_TYPE = ['pdf','docx'] # valid file extension 
                image = request.FILES['image'] # get image file
                pdf_file = request.FILES['pdf_file'] # get pdf file
                image_name = image.name # get name using of image
                file_name = pdf_file.name # get name of file

                '''
                    split the names from '.' using split() method, which convert it into list and the take last
                    list item which is the extension of file using [-1] 
                '''
                img_extension = image_name.split('.')[-1].lower() 
                file_extension = file_name.split('.')[-1].lower()
                # validate file extension 
                if img_extension not in IMAGE_TYPE and file_extension not in FILE_TYPE : # if both have wrong extension
                    flag = 0
                    image_error = 'This Format is not supported for image( Only ".jpg" ".png" ".jpeg")'
                    pdf_error = 'This format is not supported for files( Only ".pdf" ".docx")'
                    return render(request,'bookBank/add.html',{'form':form,'image_error':image_error,'pdf_error':pdf_error,'flag':flag})
                elif img_extension not in IMAGE_TYPE: # if only image have wrong extension
                    image_error = 'This Format is not supported for image( Only ".jpg" ".png" ".jpeg")'
                    flag = 0
                    return render(request,'bookBank/add.html',{'form':form,'image_error':image_error,'flag':flag})
                elif file_extension not in FILE_TYPE: # if only file have wrong extension
                    flag = 0
                    pdf_error = 'This format is not supported for files( Only ".pdf" ".docx")'
                    return render(request,'bookBank/add.html',{'form':form,'image_error':image_error,'flag':flag})
                

                # store the file in server or local storage
                FileSystemStorage(settings.MEDIA_ROOT+'/images').save(image_name,image) # FileStorageSystem takes storage location as parameter default is MEDIA_ROOT from setting.py
                FileSystemStorage(settings.MEDIA_ROOT+'/files').save(file_name,pdf_file)# save takes two parameters, one is the name of file and second is file from request.FILES
                
                
                book_obj = books(title = title,price = price, description = desc,image = image, pdf_file = pdf_file) # make model object with value of some fields
                book_obj.save() # call save() method to store in DB
                db_error = 'Some Error Please Enter Proper Data'

                # validate the author data and save in author field
                authors_list = trim_space(authors_list) # trim the extra spaces from the name of author

                # check for each author
                for auth in authors_list:
                    auth = auth.lower() # convert into lowercase
                    try:
                        author_obj = author.objects.get(title = auth) # get the given author if it exist previously in Author model
                    except:
                        author_obj = None # if author is not exist in Author model the set author_obj to None
                    if author_obj is None:
                        author_obj = author(title = auth) # if author_obj is None the create new author
                        author_obj.save() # save author in Author model
                    try:
                        book_obj.authors.add(author_obj) # add author in book object that we get above from Author model or we get just now
                    except:
                        # print('---------Author----------------')
                        return render(request,'bookBank/add.html',{'form':form,'db_error':db_error}) # if there is any runtime error in adding author to the book obj then show DB error
                #  validate subject data

                '''
                    check subject data to given subjects DS and set a specific name for given subject
                '''
                if subject in front:
                    subject = 'frontend web development'
                elif subject in back:
                    subject = 'backend web development'
                elif subject in version:
                    subject = 'version control'
                elif subject in db:
                    subject = 'data base'
                try:
                    sub_obj = subjects.objects.get(title = subject) # get the given subject from subject model
                except:
                    sub_obj = None # if subject is not exist in subject model then set it to None
                if sub_obj is None:
                    sub_obj = subjects(title = subject) # create new subject in subject model
                    sub_obj.save() # save new subject in subject model
                try:
                    book_obj.subject = sub_obj # set the subject of given book
                    book_obj.save() # save the data of book
                except:
                    # print('---------Subject----------------')
                    return render(request,'bookBank/add.html',{'form':form,'db_error':db_error}) # if there is any runtime error while setting subject field of book the show DB error
                
                form = form_add() # create new form object so that after adding when we reach to the add book page again then all fileds become empty
                upload_success = "Book Added To Library Successfully"
                return render(request,'bookBank/add.html',{'form':form,'upld_succs':upload_success})

        else:
            return render(request,'bookBank/add.html',locals())
        # return HttpResponseRedirect('/')
    else:
        form = form_add()
    return render(request,'bookBank/add.html',{'form':form})
    
def editBook(request,slug=None):
    book = get_object_or_404(books,slug=slug)
    if request.method == 'POST':
        form = addForm(request.POST, instance = book)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = addForm()
    return render(request,'bookBank/edit.html',{'form':form})

def delete(request,slug=None):
    book = get_object_or_404(books,slug=slug)
    book.delete()
    book = books.objects.all()
    return HttpResponseRedirect('../../book-bank/',{'book':book})

def download_book(request,slug=None):
    files = get_object_or_404(books,slug=slug)
    fn = files.pdf_file.name
    file_name = fn[6:]
    fe = fn.split('.')[-1]
    with open(settings.MEDIA_ROOT+'/'+fn,'rb') as pdf:
        response = HttpResponse(pdf.read())
        response['content_type'] = 'attachment/%s'%(fe)
        response['Content-Disposition'] = 'inline;filename=%s'%(file_name)
        return response

     
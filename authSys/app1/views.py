from django.shortcuts import render,redirect,HttpResponse
import pandas as pd
import numpy as np

from authSys.models import newusers,formusers
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

popular_dataframe = pd.read_pickle('popular.pkl')
pt = pd.read_pickle('pt.pkl')
books = pd.read_pickle('books.pkl')
similarity_score = pd.read_pickle('similarity_score.pkl')
# Create your views here.
# @login_required(login_url='login')
def HomePage(request):
    return render(request,'home.html')

def TopFiftyBooks(request):
    book_name=list(popular_dataframe['Book-Title'].values)
    author=list(popular_dataframe['Book-Author'].values)
    image=list(popular_dataframe['Image-URL-M'].values)
    votes=list(popular_dataframe['num_ratings'].values)
    rating=list(popular_dataframe['avg_rating'].values)
    books=zip(book_name, author, image, votes, rating)
    return render(request,'topfiftybooks.html',{'books': books})

def RecommendPage(request):
    return render(request,'recommend.html')

def Recommend(request):
    data = []  # Provide a default value for data

    if request.method == 'POST':
        user_input = request.POST.get('user_input')  # Use POST instead of form.get()

        # Your existing code to calculate similar_items and populate data
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]

        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(item)

    return render(request, 'recommend.html', {'data': data})


def SignUpPage(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        passwordConfirm=request.POST['passwordConfirm']

        if password!=passwordConfirm:
            return HttpResponse('Two different passwords, try again!')
        
        else:
            newusers(name=name,email=email,password=password).save()
            return redirect('login')
    
    return render(request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        try:
            userdetails=newusers.objects.get(email=request.POST['email'],password=request.POST['password'])
            request.session['email']=userdetails.email
            return redirect('home')
        
        except ObjectDoesNotExist:
            return HttpResponse('Invalid email or password')
             
        
    return render(request,'login.html')

def LogoutPage(request):
    # logout(request)
    # return redirect('login')
    try:
        del request.session['email']
    except:
        return redirect('login')
    
    return redirect('login')

# def FormPage(request):
#     if request.method=='POST':
#         bktype=request.POST['bktype']
#         name=request.POST['name']
#         email=request.POST['email']
#         age=request.POST['age']
#         dob=request.POST['dob']
#         phone=request.POST['phone']

#         formusers(bktype=bktype,name=name,email=email,age=age,dob=dob,phone=phone).save()
#         return HttpResponse('Applied successfully')
        
#     # return render(request,'siteform.html')
#     return render(request,'siteform.html')

def AboutPage(request):
    return render(request,'about.html')
    

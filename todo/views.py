from django.shortcuts import render
from django.db import connection
from django.shortcuts import redirect


# Create your views here.

def home (request):
    'show home page'
    return render(request,'home.html')
    

def register(request):
    
    if request.method == 'POST':
        username = request.POST.get('txt_username')
        password = request.POST.get('txt_password')
        name = request.POST.get('txt_name')
        phone = request.POST.get('txt_phone')
        Gender = request.POST.get('gender')
        dob = request.POST.get('txt_dob') 

        try:
            cursor = connection.cursor()
            sql = 'insert into users values(null, %s , %s , %s , %s , %s , %s)'
            val = (username , password , name , phone ,  Gender , dob )
            cursor.execute(sql , val)
            success = ""
            fail = ""
            id = cursor.lastrowid
            if id:
                success = "registraction sucess"
            else: 
                fail = "regestraction fail"
            return render(request , 'register.html' ,{ 'success': success,'fail': fail })
        except Exception as e:
            return render(request, 'register.html' , {'fail': str(e)})
    else: 
        return render(request, 'register.html' )


def login(request):
    if request.method == 'POST':
        username = request.POST.get('txt_username')
        password = request.POST.get('txt_password')
        cursor=connection.cursor()
        sql="select * from users where username = %s and password = %s "
        val = (username , password)
        cursor.execute(sql,val)
        record = cursor.fetchall()
        if record:
            request.session['user'] = record[0][3]
            request.session['user_id'] = record[0][0]
            return redirect ('/todo/todo')
        else:
            return render (request,'login.html',{'message':'invalid username or password'})
    else:
        return render(request,'login.html')

def todo(request):
    if not request.session.get('user'):
        return redirect('/todo/login')
    user_id = request.session['user_id']
    user = request.session['user']
    sql = "select * from todos where user_id =%s"
    val = [str(user_id)]
    cursor = connection.cursor()
    cursor.execute(sql,val)
    records = cursor.fetchall()
    return render(request, 'todo.html', {'user': user, 'todos':records})

def save(request):
    title = request.POST.get('txt_title')
    content = request.POST.get('txt_description')
    user_id = request.session['user_id']
    cursor = connection.cursor()
    sql = "insert into todos values (null, %s, %s, %s)"
    val = (title , content,str(user_id ))
    cursor.execute(sql,val)
    return redirect ('/todo/todo')

def delete(request):
    id = request.GET.get('id')
    cursor = connection.cursor()
    sql = "delete from todos where todo_id = %s"
    val = (str(id))
    cursor.execute(sql,val)
    return redirect('/todo/todo')

def logout(request):
    request.session.clear()
    return redirect('/todo')




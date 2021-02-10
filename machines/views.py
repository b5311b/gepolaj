from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, Machinery
from .models import AdminList, TechLeader, DiagResp, Driver, OilSamples
from .models import *
from .forms import *
from .forms import HomeForm, PasswChangeForm, ForgPasswForm1, ForgPasswForm2, RuningForm
from .encryption_util import encrypt, decrypt
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, JsonResponse
from django.db.models import Max

import base64
from django.db import IntegrityError

from django.utils.timezone import get_current_timezone



from django.contrib.auth.models import User

from django.views.generic import View

#def a_view(request):
    #return render_to_response("driver_pult.html", { 'time' : datetime})

def home(request):
    import datetime
    companies = Company.objects.all()
    administrators = AdminList.objects.all()    
    form = HomeForm(request.POST)
    error_message = ""
     
    if request.method == 'POST':
        
        for adm in administrators:
            
            #pf = str(form['password'].value) #methode
            if form.is_valid():
                pf = form.cleaned_data.get("password")
                uf = form.cleaned_data.get("user")
                
                if adm.comp and pf and uf:

                                       
                    company = get_object_or_404(Company, pk=adm.comp)
                    cname = company.name
                    compId = company.pk
            
                    
            
                    if decrypt(adm.password) == pf and adm.user == uf and adm.comp and not adm.mach and not adm.samp and not adm.lead:                
                        response = redirect(techleader_reg)  
                        response.set_cookie(key='adm', value=adm.pk)                                         
                        return response
                    elif decrypt(adm.password) == pf and adm.user == uf and adm.comp and not adm.mach and not adm.samp and adm.lead:
                        title = "Műszaki vezető"
                        techleader = get_object_or_404(TechLeader, pk=adm.lead)
                        day = techleader.startday
                        techleaders = TechLeader.objects.all()          
                        tod = datetime.date.today()
                        for tech in techleaders:
                            if tech.startday<=tod and tech.startday>day and techleader.company_id==tech.company_id:
                                error_message = "Ez a felhasználónév már nem műszaki vezető"
                                return render(request, 'home.html',  {'companies' : companies, 'form' : form, 'error_message' : error_message})
                            if day>tod and techleader.company_id==tech.company_id:
                                error_message = "Ez a felhasználónév még nem műszaki vezető"
                                return render(request, 'home.html',  {'companies' : companies, 'form' : form, 'error_message' : error_message})


                        
                        uname = techleader.name
                        leadId = techleader.pk
                        ceg = cname
                        response = redirect(techleader_pult)
                        #response = render(request,'techleader_pult.html', {'cname' : cname, 'compId' : compId, 'leadname' : uname, 'title' : title, 'techleader' : techleader})
                        response.set_cookie(key='tipus', value='TechLeader', max_age=2*3600)
                        response.set_cookie(key='azonosito', value=leadId, max_age=2*3600)
                        response.set_cookie(key='adm', value=adm.pk, max_age=2*3600)
                        return response
                    elif decrypt(adm.password) == pf and adm.user == uf and adm.comp and adm.mach and not adm.samp and not adm.lead:
                        title = "Gépkezelő"
                        driver = get_object_or_404(Driver, pk=adm.mach)
                        day = driver.startday
                        drivers = Driver.objects.all()          
                        tod = datetime.date.today()
                        for driv in drivers:
                            if driv.startday<=tod and driv.startday>day and driver.company_id==driv.company_id and driver.machinery_id==driv.machinery_id:
                                error_message = "Ez a felhasználónév már nem gépkezelő"
                                return render(request, 'home.html',  {'companies' : companies, 'form' : form, 'error_message' : error_message})
                            if day>tod and driver.company_id==driv.company_id and driver.machinery_id==driv.machinery_id:
                                error_message = "Ez a felhasználónév még nem gépkezelő"
                                return render(request, 'home.html',  {'companies' : companies, 'form' : form, 'error_message' : error_message})


                        
                        uname = driver.name
                        drivId = driver.pk
                        
                        response = redirect(driver_pult)
                        
                        response.set_cookie(key='tipus', value='Driver', max_age=9*3600)
                        response.set_cookie(key='azonosito', value=drivId, max_age=9*3600)
                        response.set_cookie(key='adm', value=adm.pk, max_age=9*3600)
                                               
                        return response

                    elif decrypt(adm.password) == pf and adm.user == uf and  adm.comp and not adm.mach and adm.samp and not adm.lead:
                        title = "diagRespDiagnosztikáért felelős"
                        diagResp = get_object_or_404(DiagResp, pk=adm.samp)
                        day = diagResp.startday
                        diagresps = DiagResp.objects.all()          
                        tod = datetime.date.today()
                        for dresp in diagresps:
                            if dresp.startday<=tod and dresp.startday>day and diagResp.company_id==dresp.company_id:
                                error_message = "Ez a felhasználónév már nem gépkezelő"
                                return render(request, 'home.html',  {'companies' : companies, 'form' : form, 'error_message' : error_message})
                            if day>tod and diagResp.company_id==dresp.company_id:
                                error_message = "Ez a felhasználónév még nem gépkezelő"
                                return render(request, 'home.html',  {'companies' : companies, 'form' : form, 'error_message' : error_message})


                        
                        uname = diagResp.name
                        respId = diagResp.pk
                        
                        response = redirect(response_pult)
                        
                        response.set_cookie(key='tipus', value='DiagResp', max_age=4*3600)
                        response.set_cookie(key='azonosito', value=respId, max_age=4*3600)
                        response.set_cookie(key='adm', value=adm.pk, max_age=4*3600)
                                               
                        return response
                        
                    

                else:  error_message = "Nem létező felhasználónév jelszó párossal kisérelt meg belépni. Próbálja meg újra a bejelentkezést!"
                if not adm.comp and pf and uf:
                    if decrypt(adm.password) == pf and adm.user == uf and not adm.comp and not adm.mach and not adm.samp and adm.lead:
                            title = "supevisor"
                            
                            superv = get_object_or_404(Supervisor, pk=adm.lead)
                            day = superv.wday
                            supervs = Supervisor.objects.all()          
                            tod = datetime.date.today()
                            for spv in supervs:
                                if spv.wday<=tod and spv.wday>day:
                                    error_message = "Ez a felhasználónév már nem supervisor"
                                    return render(request, 'home.html',  locals())
                                if day>tod:
                                    error_message = "Ez a felhasználónév még nem supervisor"
                                    return render(request, 'home.html',  locals())
                            uname = superv.name
                            supervId = superv.pk
                            
                            response = redirect(supervisor_pult)
                            
                            response.set_cookie(key='tipus', value='Supervisor', max_age=4*3600)
                            response.set_cookie(key='azonosito', value=supervId, max_age=4*3600 )
                            response.set_cookie(key='adm', value=adm.pk, max_age=4*3600)
                                                
                            return response

                else:  error_message = "Nem létező felhasználónév jelszó párossal kisérelt meg belépni. Próbálja meg újra a bejelentkezést!"
        #p = decrypt(companies.values('password')[3]['password'])
        return render(request, 'home.html',  {'companies' : companies, 'form' : form, 'error_message' : error_message})
    response = render(request, 'home.html',  {'companies' : companies,  'form' : form})
    response.delete_cookie('tipus')
    response.delete_cookie('azonosito')
    response.delete_cookie('adm')
    response.delete_cookie('machId')
    response.delete_cookie('ident')
    
                    

    return response



def new_company(request):
    import datetime
    form = RegForm(request.POST)
    form1 = AdminListForm(request.POST)
    error_message=''
    companies = Company.objects.all()
    admins = AdminList.objects.all()
    all_fields = Company._meta.local_fields
    allName = [f.name for f in all_fields]
    title="Regisztrált üzemek"
    if request.COOKIES.get('flag', ''):
        flag = request.COOKIES.get('flag', '')
        print(flag)
        if flag=='1':
            form = TechLRegForm(request.POST)
            companies = TechLeader.objects.all()
            title="Regisztrált műszaki vezetők"
        if flag=='2':
            form = DiagRespRegForm(request.POST)
            companies = DiagResp.objects.all()
            title="Regisztrált diag. felelősök"
        if flag=='3':
            form = DriverRegForm(request.POST)
            companies = Driver.objects.all()
            title="Regisztrált gépkezelők"
        if flag=='4':
            form = RegForm(request.POST)
            companies = Jobs.objects.all()
            title="Regisstrált munkatípusok"
    
    #responses = DiagResp.objects.all()
    #drivers = Driver.objects.all()
    #machines = Machinery.objects.all()
    #samples = OilSamples.objects.all()
    #jobs = Jobs.objects.all  

    if request.method == 'POST':
        

        if form.is_valid():
            
            topic = form.save(commit=False)
            topic.password = encrypt(topic.password)
            if form1.is_valid():
                admin = form1.save(commit=False)
                admin.user=topic.user
                admin.password=topic.password



                topic.save()
                obj = Company.objects.latest('id')
                us = obj.user
                passw = obj.password
                #com = obj.id
                #al = AdminList(user=us, password=passw, comp=com)
                #al.save()
                admin.comp=obj.id
                admin.save()
                megnevezes='vállalatot'
                sendHTMLEmail(obj.name, obj.email, megnevezes, us, passw, 1)
                return render(request, 'new_company.html', locals())
            else:
                error_message = "Van már ilyen felhasználónév. Válasszon másikat!"
                return render(request, 'new_company.html', locals())
        if request.POST['name']:
            name = request.POST['name']
            print(name)
            if request.COOKIES.get('flag', ''):
                flag = request.COOKIES.get('flag', '')
                print(flag)
                if flag=='1':
                    comp=TechLeader.objects.get(user = name)
                    
                if flag=='2':
                    comp=DiagResp.objects.get(user = name)
                    
                if flag=='3':
                    comp=Driver.objects.get(user = name)
                    
                if flag=='4':
                    comp=Jobs.objects.get(job = name)
                    setattr(comp, 'job', request.POST['email'])
                    
            else:
                comp=Company.objects.get(name = name)
            
            setattr(comp, 'email', request.POST['email'])
            comp.save()
            if request.POST['password']=="torol":
                comp.delete()
        if request.POST['password']=='1':
            print("itt")
            response = render(request, 'new_company.html', locals())
            response.set_cookie(key='flag', value='1', max_age=180)                                               
            return response
        if request.POST['password']=='2':
            response = render(request, 'new_company.html', locals())
            response.set_cookie(key='flag', value=2, max_age=180)                                               
            return response
        if request.POST['password']=='3':
            response = render(request, 'new_company.html', locals())
            response.set_cookie(key='flag', value=3, max_age=180)                                               
            return response
        if request.POST['password']=='4':
            response = render(request, 'new_company.html', locals())
            response.set_cookie(key='flag', value=4, max_age=180)                                               
            return response
        if request.POST['password']=='0':
            response = render(request, 'new_company.html', locals())
            response.delete_cookie('flag')                                               
            return response
            
    return render(request, 'new_company.html', locals())



def supervisor_reg(request):
    form = SupervisorRegForm(request.POST)
    form1 = AdminListForm(request.POST)
    error_message=''  
       
    if request.method == 'POST':
        
        if form.is_valid():            
            topic = form.save(commit=False)
            topic.password = encrypt(topic.password)
            if form1.is_valid():
                admin = form1.save(commit=False)
                admin.user=topic.user
                admin.password=topic.password
                admin.comp=0
            


                topic.save()
                obj = Supervisor.objects.latest('id')
                #us = obj.user
                #passw = obj.password
                
                admin.lead=obj.id
                #al = AdminList(user=us, password=passw, comp=com)
                #al.save()
                #admin.comp=obj.id
                admin.save()
                #megnevezes='vállalatot'
                #sendHTMLEmail(obj.name, obj.email, megnevezes, us, passw, 1)           
                return render(request, 'supervisor_reg.html', { 'form': form, 'form1' : form1 })
            else:
                error_message = "Van már ilyen felhasználónév. Válasszon másikat!"
                return render(request, 'supervisor_reg.html', { 'form1' : form1, 'error_message' : error_message })
        
   

    return render(request, 'supervisor_reg.html', { 'form': form, 'form1' : form1 })



def techleader_reg(request):
    form = TechLRegForm(request.POST)
    form1 = AdminListForm(request.POST)
    error_message=''
    
    if request.COOKIES.get('adm', ''):
        admId = int(request.COOKIES.get('adm', ''))
    else:
        return redirect(home)
    admin = get_object_or_404(AdminList, pk=admId)
    compobj = get_object_or_404(Company, pk=admin.comp)
    company = compobj.name
    leaders = TechLeader.objects.filter(company_id=admin.comp).order_by('-startday')
    domain = request.scheme + "://" + request.META['HTTP_HOST'] 

    

    
   
       
    if request.method == 'POST':
        
        if form.is_valid():            
            topic = form.save(commit=False)
            topic.password = User.objects.make_random_password()
        
            topic.password = encrypt(topic.password)
            topic.company_id = int(admin.comp)
            if form1.is_valid():
                topicadmin = form1.save(commit=False)
                topicadmin.user=topic.user
                topicadmin.password=topic.password


                topic.save()
                obj = TechLeader.objects.latest('id')
                us = obj.user
                passw = obj.password
                #lead = obj.id
                #al = AdminList(user=us, password=passw, lead=lead, comp=int(admin.comp))
                #al.save()
                topicadmin.lead=obj.id
                topicadmin.comp=int(admin.comp)
                topicadmin.save()
                megnevezes='műszaki vezetőt'
                sendHTMLEmail(obj.name, obj.email, megnevezes, us, passw, 1) 
                form=HomeForm          
                ##return render(request, 'home.html', { 'form': form })
                domain = request.scheme + "://" + request.META['HTTP_HOST']     
                return redirect(domain)
            else:
                error_message = 'Nem sikerült a regisztáció, mert olyan felhasználónévvel vagy emailcímmel próbálkozott amivel már korábban regisztráltak a rendszerbe. Válasszon másik felhasználónevet és próbálja meg újra!'
                return render(request, 'techleader_reg.html', { 'form1' : form1, 'error_message' : error_message, 'company' : company, 'leaders' : leaders })
        else:
            error_message = 'Nem sikerült a regisztáció, mert olyan felhasználónévvel vagy emailcímmel próbálkozott amivel már korábban regisztráltak a rendszerbe. Válasszon másik felhasználónevet és próbálja meg újra!'
            return render(request, 'techleader_reg.html', { 'form1' : form1, 'error_message' : error_message, 'company' : company, 'leaders' : leaders })

    return render(request, 'techleader_reg.html', { 'form': form, 'form1' : form1, 'error_message' : error_message, 'company' : company, 'leaders' : leaders, 'domain' : domain})




def respons_reg(request):
    form = DiagRespRegForm(request.POST)
    form1 = AdminListForm(request.POST)
    error_message=''

    if request.COOKIES.get('adm', ''):
        admId = int(request.COOKIES.get('adm', ''))
    else:
        return redirect(home)
    admin = get_object_or_404(AdminList, pk=admId)
    compobj = get_object_or_404(Company, pk=admin.comp)
    leadobj = get_object_or_404(TechLeader, pk=admin.lead)
    company = compobj.name
    responses = DiagResp.objects.filter(company_id=admin.comp).order_by('-startday')
    
   
       
    if request.method == 'POST':
        
        if form.is_valid():            
            topic = form.save(commit=False)
            topic.password = User.objects.make_random_password()
            topic.password = encrypt(topic.password)
            topic.company_id = int(admin.comp)
            if form1.is_valid():
                topicadmin = form1.save(commit=False)
                topicadmin.user=topic.user
                topicadmin.password=topic.password
                topic.save()
            
                obj = DiagResp.objects.latest('id')
                us = obj.user
                passw = obj.password
                #samp = obj.id
                #al = AdminList(user=us, password=passw, samp=samp, comp=int(admin.comp))
                #al.save()
                topicadmin.samp=obj.id
                topicadmin.comp=int(admin.comp)
                topicadmin.save()
                megnevezes='diagnosztikai felelős'
                sendHTMLEmail(obj.name, obj.email, megnevezes, us, passw, 1) 
                return redirect(respons_reg)
            else:
                error_message = 'Nem sikerült a regisztáció, mert olyan felhasználónévvel vagy emailcímmel próbálkozott amivel már korábban regisztráltak a rendszerbe. Válasszon másik felhasználónevet és próbálja meg újra!'
                return render(request, 'respons_reg.html', { 'form1': form1, 'error_message' : error_message, 'company' : company, 'responses' : responses, 'leadobj' : leadobj })
                
        else:
            error_message = 'Nem sikerült a regisztáció, mert olyan felhasználónévvel vagy emailcímmel próbálkozott amivel már korábban regisztráltak a rendszerbe. Válasszon másik felhasználónevet és próbálja meg újra!'
            return render(request, 'respons_reg.html', { 'form1': form1, 'error_message' : error_message, 'company' : company, 'responses' : responses, 'leadobj' : leadobj })

    return render(request, 'respons_reg.html', { 'form': form,  'form1': form1, 'error_message' : error_message, 'company' : company, 'responses' : responses, 'leadobj' : leadobj })




def machine_reg(request):
    form = MachineryRegForm(request.POST)
    error_message=''
    
    if request.COOKIES.get('adm', ''):
        admId = int(request.COOKIES.get('adm', ''))
    else:
        return redirect(home)
    admin = get_object_or_404(AdminList, pk=admId)
    compobj = get_object_or_404(Company, pk=admin.comp)
    leadobj = get_object_or_404(TechLeader, pk=admin.lead)
    company = compobj.name
    machines = Machinery.objects.filter(company_id=admin.comp).order_by('-buyday')
    
   
       
    if request.method == 'POST':
        
        if form.is_valid():
            pf = form.cleaned_data.get("identnum")
                    
            topic = form.save(commit=False)
            topic.company_id = int(admin.comp)
            topic.cidentnum=str(pf)+"-"+str(admin.comp)
            
            topic.save()
            print(str(pf)+"-"+str(admin.comp))  
            return render(request, 'machine_reg.html', { 'form': form, 'error_message' : error_message, 'company' : company, 'machines' : machines, 'leadobj' : leadobj  })
            
        
        else:
            error_message = 'Nem sikerült a regisztáció, mert egy már korábban regisztrált gépet próbált újra bevinni a rendszerbe!'
            
    return render(request, 'machine_reg.html', { 'form': form, 'error_message' : error_message, 'company' : company, 'machines' : machines, 'leadobj' : leadobj  })




def driver_reg(request):
    form = DriverRegForm(request.POST)
    form1 = AdminListForm(request.POST)
    error_message=''
    
    if request.COOKIES.get('adm', ''):
        admId = int(request.COOKIES.get('adm', ''))
    else:
        return redirect(home)
    admin = get_object_or_404(AdminList, pk=admId)
    compobj = get_object_or_404(Company, pk=admin.comp)
    leadobj = get_object_or_404(TechLeader, pk=admin.lead)
    machineobj = Machinery.objects.filter(company_id=admin.comp).order_by('identnum')
    company = compobj.name
    
    drivers = Driver.objects.filter(company_id=admin.comp).order_by('machinery_id','-startday')
       
    if request.method == 'POST':
        
        if form.is_valid():            
            topic = form.save(commit=False)
            topic.password = User.objects.make_random_password()
            topic.password = encrypt(topic.password)
            topic.company_id = int(admin.comp)            
            machId  = form.cleaned_data.get("machinery")
            topic.machinery_id = machId
            if form1.is_valid():
                topicadmin = form1.save(commit=False)
                topicadmin.user=topic.user
                topicadmin.password=topic.password

                topic.save()
                obj = Driver.objects.latest('id')
                us = obj.user
                passw = obj.password
                #mach = obj.id
                #al = AdminList(user=us, password=passw, mach=mach, comp=admin.comp)
                #al.save()
                topicadmin.comp=admin.comp
                topicadmin.mach=obj.id
                topicadmin.save()
                megnevezes='gépkezelő'
                mobj = get_object_or_404(Machinery, pk=machId)
                
                sendHTMLEmail(obj.name, obj.email, megnevezes, us, passw, mobj.identnum) 
                return redirect(driver_reg)
            else:
                error_message = 'Nem sikerült a regisztáció, mert olyan felhasználónévvel vagy emailcímmel próbálkozott amivel már korábban regisztráltak a rendszerbe. Válasszon másik felhasználónevet és próbálja meg újra!'
                return render(request, 'driver_reg.html', { 'form1': form1, 'error_message' : error_message, 'company' : company, 'drivers' : drivers, 'machineobj' : machineobj, 'leadobj' :leadobj  })
            
        
        else:
            error_message = 'Nem sikerült a regisztáció, mert olyan felhasználónévvel vagy emailcímmel próbálkozott amivel már korábban regisztráltak a rendszerbe. Válasszon másik felhasználónevet és próbálja meg újra!'
            return render(request, 'driver_reg.html', { 'form1': form1, 'error_message' : error_message, 'company' : company, 'drivers' : drivers, 'machineobj' : machineobj, 'leadobj' :leadobj  })

    return render(request, 'driver_reg.html', { 'form': form, 'form1': form1, 'error_message' : error_message, 'company' : company, 'drivers' : drivers, 'machineobj' : machineobj, 'leadobj' :leadobj  })







def techleader_pult(request):
    #techleader = request.POST.get('techleader')
    #leadname=techleader.name
    if request.COOKIES.get('adm', ''):
        admId = int(request.COOKIES.get('adm', ''))
    else:
        return redirect(home)
    admin = get_object_or_404(AdminList, pk=admId)
    compobj = get_object_or_404(Company, pk=admin.comp)
    company = compobj.name
    leadobj = get_object_or_404(TechLeader, pk=admin.lead)
    leadname = leadobj.name
    machineobj = Machinery.objects.filter(company_id=admin.comp).order_by('identnum')
    jobs = Jobs.objects.all()
    form = JobsForm(request.POST)
    if request.method == 'POST':
        if request.POST.get("form_type") == "formOne":
            if form.is_valid():            
                topic = form.save(commit=False)
                topic.save()
                return render(request,'techleader_pult.html', {'form' : form, 'cname' : company, 'leadname' : leadname, 'jobs' : jobs, 'machineobj' : machineobj })
        if request.POST.get("form_type") == "formTwo":
            machId = request.POST['machinery']
            machobj = get_object_or_404(Machinery, pk=machId)
            response = redirect(techleader_pult)                        
            response.set_cookie(key='machId', value=machId, max_age=1800)
            response.set_cookie(key='ident', value=machobj.identnum, max_age=1800)
            return response
   
   
    return render(request,'techleader_pult.html', {'form' : form, 'cname' : company, 'leadname' : leadname, 'jobs' :jobs, 'machineobj' : machineobj, })
    #return render(request,'techleader_pult.html')




def response_pult(request):
    import datetime
    
    #techleader = request.POST.get('techleader')
    #leadname=techleader.name
    if request.COOKIES.get('adm', ''):
        admId = int(request.COOKIES.get('adm', ''))
    else:
        return redirect(home)
    picobjs = SampImages.objects.order_by('id')
    admin = get_object_or_404(AdminList, pk=admId)
    compobj = get_object_or_404(Company, pk=admin.comp)
    company = compobj.name
    respobj = get_object_or_404(DiagResp, pk=admin.samp)
    respname = respobj.name
    samples = OilSamples.objects.all()
    maxId = samples.aggregate(Max('id'))['id__max']
    print(maxId)
    if maxId==None:
        maxId=1
    else:
        maxId += 1
    n=['0']*(6-len(str(maxId)))
    nStr=''.join([str(elem) for elem in n])
    mintaAzonosito = 'OC-'+ nStr + str(maxId) + '-' + str(datetime.datetime.now().year-2000)
   
    machineobj = Machinery.objects.filter(company_id=admin.comp).order_by('identnum')
    
   

    sampleobj = OilSamples.objects.order_by('-minta_azonosito')
    data1={}
    data1['summData'+str(admin.comp)]=[]
    data4={}
    data4['summData'+str(admin.comp)]=[]
    for samp in sampleobj:
        data2={}
        data2['sData'+str(admin.comp)]=[]
        data3={}
        data3['sData'+str(admin.comp)]=[]
        sData=[]
        for mach in machineobj:
            
            if mach.id==samp.machinery_id:
                data2['sData'+str(admin.comp)].append(samp.minta_azonosito)
                data2['sData'+str(admin.comp)].append(mach.identnum)
               
                data2['sData'+str(admin.comp)].append(samp.mintavetel_napja)
                data2['sData'+str(admin.comp)].append(samp.beerkezes_napja)
                age = 0
                machines = Runing.objects.filter(machinery_id=samp.machinery_id)
                for mach in machines:
                    if mach.workday <= samp.mintavetel_napja:
                        age = mach.ssum_whour

                data2['sData'+str(admin.comp)].append(age)

                data2['sData'+str(admin.comp)].append(color_var(samp,'viszkozitas_valtozas')[0])

                data2['sData'+str(admin.comp)].append(color_var(samp, 'koromtartalom')[0])
                
                data2['sData'+str(admin.comp)].append(color_var(samp, 'osszulledek')[0])
                
                data2['sData'+str(admin.comp)].append(color_var(samp, 'vasm_osszulledek')[0])
                
                data2['sData'+str(admin.comp)].append(color_var(samp, 'vastartalom')[0])
                
                data2['sData'+str(admin.comp)].append(color_var(samp, 'viztartalom')[0])
                
                data2['sData'+str(admin.comp)].append(color_var(samp, 'illoanyag')[0])
                            
                data2['sData'+str(admin.comp)].append(color_var(samp, 'lobbanaspont')[0])

                for pc in picobjs:
                    img = []
                    if pc.oilsamples_id == samp.id:
                        img.append(getattr(pc,'id'))
                        
                        img.append(getattr(pc,'sample_Img'))
                        samobj = get_object_or_404(OilSamples, pk=pc.oilsamples_id)
                        img=str(getattr(samobj,'minta_azonosito'))+"@"+str(getattr(pc,'id'))+str(getattr(pc,'sample_Img'))
                        data2['sData'+str(admin.comp)].append(img)

                data3['sData'+str(admin.comp)].append(color_var(samp,'viszkozitas_valtozas')[1])

                data3['sData'+str(admin.comp)].append(color_var(samp, 'koromtartalom')[1])
                
                data3['sData'+str(admin.comp)].append(color_var(samp, 'osszulledek')[1])
                
                data3['sData'+str(admin.comp)].append(color_var(samp, 'vasm_osszulledek')[1])
                
                data3['sData'+str(admin.comp)].append(color_var(samp, 'vastartalom')[1])
                
                data3['sData'+str(admin.comp)].append(color_var(samp, 'viztartalom')[1])
                
                data3['sData'+str(admin.comp)].append(color_var(samp, 'illoanyag')[1])
                            
                data3['sData'+str(admin.comp)].append(color_var(samp, 'lobbanaspont')[1])
                
        
        data1['summData'+str(admin.comp)].append(data2['sData'+str(admin.comp)])       
        data4['summData'+str(admin.comp)].append(data3['sData'+str(admin.comp)])    
    superData=data1['summData'+str(admin.comp)]           
    
    
    superData1=data4['summData'+str(admin.comp)]



    from datetime import datetime
    form = OilSamplesForm(request.POST, request.FILES)    
    if request.method == 'POST': 
        machineryId=request.POST['machID']
        if machineryId:
            endtime=request.POST['mintavetel_napja'] 
            machines = Runing.objects.filter(machinery_id=machineryId)
            
            age = 0
            for mach in machines:
                if mach.workday <= datetime.strptime(endtime, "%Y-%m-%d").date():
                    age = mach.ssum_whour
            if form.is_valid():
                
                topic = form.save(commit=False)
                topic.machinery_id = machineryId   
                topic.save() 
                return render(request,'response_pult.html', locals())
        if request.POST['minta1']:
            ident=request.POST['minta1']
            sampobj=OilSamples.objects.get(minta_azonosito = ident)
            print(sampobj.pk)
            lista=["viszkozitas_valtozas", "koromtartalom", "osszulledek", "vasm_osszulledek", "vastartalom", "illoanyag", "lobbanaspont"]
            nums=["1", "2", "3"]
            for oj in lista:
                for num in nums:
                    az = oj+num
                    print(az)
                    #print(getattr(sampobj, az))
                    if request.POST[az]:
                        #print(request.POST[az])
                        
                        setattr(sampobj, az, request.POST[az])
            sampobj.save()
            return redirect(response_pult)
            #return render(request,'response_pult.html', locals())            
    



    

                
        

   
   
    return render(request,'response_pult.html', locals())
   


def color_var(samp, var_name): # a három megfigyelést átlagoló.
    sum=0.0
    dict = {'1': var_name+'1','2': var_name+'2','3': var_name+'3'}
    for i in ['1','2','3']:
        #print (dict[i])
        #print (getattr(samp, dict[i]))
        if getattr(samp, dict[i]):
            sum+=getattr(samp, dict[i])
    #print(sum)
    
    #var_name=[k for k, v in local().items() if v==samp.sampfield][0] # a változónév stringgé alakítása
    #sum=samp.(instance.__dict__[var_name+"1"])+samp.(instance.__dict__[var_name+"2"])+samp.(instance.__dict__[var_name+"3"])
    name=['NULL',1]
    
    
    if getattr(samp, dict['1']) and  not getattr(samp, dict['2']) and not getattr(samp, dict['3']):
        name[0]=round(sum/1, 2)
        name[1]=2
    if getattr(samp, dict['1']) and  getattr(samp, dict['2']) and not getattr(samp, dict['3']):
        name[0]=round(sum/2, 2)
        name[1]=3
    if getattr(samp, dict['1']) and  getattr(samp, dict['2']) and getattr(samp, dict['3']):
        name[0]=round(sum/3, 2)
        name[1]=4
       
    return (name)


def delete(request, id):
    #obj = SampImages.objects.get(pk=id)
    #obj.delete()
    obj = get_object_or_404(SampImages, pk=id)
    if request.method == 'POST':
        obj.delete()
        return redirect(supervisor_pult)
    
    return redirect(supervisor_pult)

def supervisor_pult(request):
    
    import datetime

    if request.COOKIES.get('adm', ''):
        admId = int(request.COOKIES.get('adm', ''))
    else:
        return redirect(home)
    
    picobjs = SampImages.objects.order_by('id')
    
    sampleobj = OilSamples.objects.order_by('-minta_azonosito')
    
    machineobj = Machinery.objects.all()

    data1={}
    data1['summData']=[]
    data4={}
    data4['summData']=[]
    for samp in sampleobj:
        data2={}
        data2['sData']=[]
        data3={}
        data3['sData']=[]
        sData=[]
        for mach in machineobj:
            
            if mach.id==samp.machinery_id:
                data2['sData'].append(samp.minta_azonosito)
                
                

                data2['sData'].append(mach.identnum)
               
                data2['sData'].append(samp.mintavetel_napja)
                data2['sData'].append(samp.beerkezes_napja)
                age = 0
                machines = Runing.objects.filter(machinery_id=samp.machinery_id)
                for machin in machines:
                    if machin.workday <= samp.mintavetel_napja:
                        age = machin.ssum_whour

                data2['sData'].append(age)

                data2['sData'].append(color_var(samp,'viszkozitas_valtozas')[0])

                data2['sData'].append(color_var(samp, 'koromtartalom')[0])
                
                data2['sData'].append(color_var(samp, 'osszulledek')[0])
                
                data2['sData'].append(color_var(samp, 'vasm_osszulledek')[0])
                
                data2['sData'].append(color_var(samp, 'vastartalom')[0])
                
                data2['sData'].append(color_var(samp, 'viztartalom')[0])
                
                data2['sData'].append(color_var(samp, 'illoanyag')[0])
                            
                data2['sData'].append(color_var(samp, 'lobbanaspont')[0])
                               


                compobj = get_object_or_404(Company, pk=mach.company_id)
                data2['sData'].append(compobj.name)
                techleaders =TechLeader.objects.filter(company_id=mach.company_id).order_by('startday')
                ttechl=""
                temail=""
                for techl in techleaders:
                    if techl.startday <= samp.beerkezes_napja:
                        ttechl = techl.name
                        temail = techl.email
                data2['sData'].append(ttechl)
                data2['sData'].append(temail)
                respons =DiagResp.objects.filter(company_id=mach.company_id).order_by('startday')
                ttechl=""
                temail=""
                for resp in respons:
                    if resp.startday <= samp.beerkezes_napja:
                        ttechl = resp.name
                        temail = resp.email
                data2['sData'].append(ttechl)
                data2['sData'].append(temail)
                for pc in picobjs:
                    img = []
                    if pc.oilsamples_id == samp.id:
                        img.append(getattr(pc,'id'))
                        
                        img.append(getattr(pc,'sample_Img'))
                        samobj = get_object_or_404(OilSamples, pk=pc.oilsamples_id)
                        img=str(getattr(samobj,'minta_azonosito'))+"@"+str(getattr(pc,'id'))+str(getattr(pc,'sample_Img'))
                        data2['sData'].append(img)

                data3['sData'].append(color_var(samp,'viszkozitas_valtozas')[1])

                data3['sData'].append(color_var(samp, 'koromtartalom')[1])
                
                data3['sData'].append(color_var(samp, 'osszulledek')[1])
                
                data3['sData'].append(color_var(samp, 'vasm_osszulledek')[1])
                
                data3['sData'].append(color_var(samp, 'vastartalom')[1])
                
                data3['sData'].append(color_var(samp, 'viztartalom')[1])
                
                data3['sData'].append(color_var(samp, 'illoanyag')[1])
                            
                data3['sData'].append(color_var(samp, 'lobbanaspont')[1])
                
        
        data1['summData'].append(data2['sData'])       
        data4['summData'].append(data3['sData'])    
    superData=data1['summData']           
    
    
    superData1=data4['summData']

    from datetime import datetime
    form1 = OilSamplesForm(request.POST)  
    form2 = SampImagesForm(request.POST, request.FILES)

    if request.method == 'POST':
        if request.POST.get("form_type") == "formTwo": 
            ident=request.POST['pic']
            #print(ident)
            sampobj = get_object_or_404(OilSamples, minta_azonosito=ident)
            if form2.is_valid():
                    
                topic = form2.save(commit=False)
                topic.oilsamples_id = sampobj.id   
                topic.save() 
                return redirect(supervisor_pult)

        elif request.POST.get("form_type") == "formOne":
            
        
            #idid=request.POST['clearId']
            ident=request.POST['minta1']
            sampobj=OilSamples.objects.get(minta_azonosito = ident)
            print(sampobj.pk)
            lista=["viszkozitas_valtozas", "koromtartalom", "osszulledek", "vasm_osszulledek", "vastartalom", "viztartalom", "illoanyag", "lobbanaspont"]
            nums=["1", "2", "3"]
            for oj in lista:
                for num in nums:
                    az = oj+num
                    #print(az)
                    #print(getattr(sampobj, az))
                    if request.POST[az]:
                        #print(request.POST[az])
                        
                        setattr(sampobj, az, request.POST[az])
             
            sampobj.save()
            return redirect(supervisor_pult)
            #return render(request,'response_pult.html', locals())            
    



    

                
        

   
   
    return render(request,'supervisor_pult.html', locals())
   










from datetime import datetime
def driver_pult(request):
    form = RuningForm(request.POST)
    form2 = FuellingForm(request.POST)
    form3 = OilChangeForm(request.POST)
    
   
    error_message=""
    if request.COOKIES.get('adm', ''):
        admId = int(request.COOKIES.get('adm', ''))
    else:
        return redirect(home)
    admin = get_object_or_404(AdminList, pk=admId)
    compobj = get_object_or_404(Company, pk=admin.comp)
    company = compobj.name
    drivobj = get_object_or_404(Driver, pk=admin.mach)
    drivename = drivobj.name
    machId = drivobj.machinery_id
    
    machobj = get_object_or_404(Machinery, pk=machId)
    ident = machobj.identnum
    unit = machobj.run_unit
    jobs = Jobs.objects.all()
    runhist = get_object_or_404(Machinery, pk=machId).run_hist 

    if request.method == 'POST':

        if request.POST.get("form_type") == "formOne":
            if form.is_valid():
                if request.COOKIES.get('starttime', ''):
                    row = Runing.objects.get(start_time=request.COOKIES.get('starttime', ''), machinery_id=machId)
                    endtime = form.cleaned_data.get("end_time")
                    endkmeter  = form.cleaned_data.get("end_kmeter")
                    row.end_time = endtime
                    row.end_kmeter = endkmeter
                    row.sum_whour = ((datetime.strptime(endtime, "%Y. %m. %d. %H:%M")- datetime.strptime(request.COOKIES.get('starttime', ''), "%Y. %m. %d. %H:%M")).total_seconds())/3600
                    queryset = Runing.objects.all()
                    total = runhist
                    for instance in queryset:
                        if instance.machinery_id == machId and instance.sum_whour != None:
                            total = total + instance.sum_whour
                    
                    print (total)

                    row.ssum_whour = total+row.sum_whour

                    
                    
                    row.save()
                    response=redirect(driver_pult)
                    response.delete_cookie('starttime')
                    response.delete_cookie('machinery_id')
                    response.delete_cookie('wtype')
                                
                    return response
                        
                else:           
                    topic = form.save(commit=False)                       
                    topic.machinery_id = machId
                    starttime = form.cleaned_data.get("start_time")
                    wtype = form.cleaned_data.get("wtype")

                    topic.save()
                    response=redirect(driver_pult)
                    #response = render(request,'driver_pult.html', instance.__dict__)
                    response.set_cookie(key='starttime', value=starttime)
                    response.set_cookie(key='machinery_id', value=machId)
                    response.set_cookie(key='wtype', value=wtype)
                                 
                    return response
            else:
                print("nem")
                
            
        elif request.POST.get("form_type") == "formTwo":
            
                
            if form2.is_valid and request.POST['liter']:
                topicFuell = form2.save(commit=False)
                topicFuell.machinery_id = machId
                
                myend = Runing.objects.filter(machinery_id=machId).aggregate(Max('end_time'))          
                topicFuell.extime = get_object_or_404(Runing, end_time=myend['end_time__max']).ssum_whour
                topicFuell.save()
                return redirect(driver_pult)
            else:
                return redirect(driver_pult)

        elif request.POST.get("form_type") == "formThree":
            
                
            if form3.is_valid and request.POST['liter']:
                topicFuell = form3.save(commit=False)
                topicFuell.machinery_id = machId

                myend = Runing.objects.filter(machinery_id=machId).aggregate(Max('end_time'))          
                topicFuell.extime = get_object_or_404(Runing, end_time=myend['end_time__max']).ssum_whour

                topicFuell.save()
                return redirect(driver_pult)
            else:
                return redirect(driver_pult)

        else:
            return redirect(driver_pult)
 
    myfuellings = Fuelling.objects.filter(machinery_id=machId).order_by('-ftime')
    myoilch = OilChange.objects.filter(machinery_id=machId).order_by('-ftime')

    startday = drivobj.startday
    myruning = Runing.objects.filter(machinery_id=machId).order_by('-start_time')
    
    #tank1 = get_object_or_404(Runing, pk=19)
    #tank2 = get_object_or_404(Runing, pk=39)
   

    
    #print( str( (datetime.strptime(tank2.start_time, "%Y. %m. %d. %H:%M")- datetime.strptime(tank1.start_time, "%Y. %m. %d. %H:%M")).total_seconds()    ))

    #return render(request,'driver_pult.html', instance.__dict__)
    return render(request,'driver_pult.html', locals())

    #return render(request,'driver_pult.html', { 'error_message' : error_message, 'form' : form, 'form2' : form2, 'company' : company, 'drivename' : drivename, 'ident' : ident, 'jobs' : jobs, 'machId' : machId, 'unit' : unit })


#class consupt_works(View):
    #template_name = 'consupt_works.html'
#
    #def get_context_data(self, **kwargs):
       # context = super().get_context_data(**kwargs)
       # context["qs"] = Runing.objects.all()
       # return context

# tankolt mennyiségek grafikus megjelenítése tankolás napja fügvényben
def consupt_works(request):
    labels = []
    data = []

    querys = Fuelling.objects.filter(machinery_id=3).order_by('ftime')
    print(querys)
    print(len(querys))
    
    for fuell in querys:
        labels.append(fuell.ftime)
        data.append(fuell.liter)

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def chart(request):
    return render(request, 'chart.html')


def consupt_works2(request):
    labels = []
    data = []
    helper =[]
    gdata=[]
    valueFuell = []
    timeFuell = []
    machHour = []
    if request.COOKIES.get('machId', ''):
        machId=request.COOKIES.get('machId', '')
    else:
        admId = int(request.COOKIES.get('adm', ''))
        admin = get_object_or_404(AdminList, pk=admId)
        compobj = get_object_or_404(Company, pk=admin.comp)
        company = compobj.name
        drivobj = get_object_or_404(Driver, pk=admin.mach)
        drivename = drivobj.name
        machId = drivobj.machinery_id
    
        

    queryset = Fuelling.objects.filter(machinery_id=machId).order_by('-ftime')
    for q in queryset:
        hhelp=q.extime
        thelp=q.ftime
        idhelp=q.id    
        for h in machHour:
            if h==q.extime:
                hhelp=0
        if hhelp!=0:
            machHour.append(hhelp)
            timeFuell.append(thelp)
            helper.append(idhelp)
            querys = Fuelling.objects.filter(extime=hhelp)
            lithelp=0
            for hq in querys:
                lithelp = lithelp+hq.liter
            valueFuell.append(lithelp)

    #for q in queryset:
        #helper.append(q.id)
        #valueFuell.append(q.liter)
        #timeFuell.append(q.ftime)
        #machHour.append(q.extime)

    query=Runing.objects.filter(machinery_id=machId).order_by('-id')
    jquery=Jobs.objects.order_by('id')
    
    
    sor=[]
    i=0
    for x in range(len(queryset)):
        if (x>=0 and x<len(machHour)-1):
            ower=get_object_or_404(Fuelling, pk=helper[x], machinery_id=machId).extime
            lower=get_object_or_404(Fuelling, pk=helper[x+1], machinery_id=machId).extime
            
            labels=[]  #a munka tipusa
            datai=[]  #a munkával töltött idő
            gdatai=[["Munkák két tankolás között", "A gépídő arányában"],] #agoogle charthoz
            for qjob in jquery:
                labels.append(qjob.job)
                datai.append(0.0)
                gdatai.append([qjob.job, 0.0])
            for run in query:
                if (run.ssum_whour<=ower and run.ssum_whour>lower):
                    for y in range(len(labels)):
                        if labels[y] == run.wtype:
                            datai[y] += run.sum_whour
                            gdatai[y+1] = [run.wtype, datai[y]]
            sum=0.0
        
            for y in range(len(datai)):
                sum+=datai[y]
            
            for y in range(len(datai)):
                 datai[y]=round(datai[y]*100/sum,0)   

            

            #labels.append(labelsi)
            gdata.append(gdatai)
            data.append(datai)
            sor.append(i)
            i+=1

        

    print(sor)    
    

    return JsonResponse(data={
        #'labels': labels,
        #'data': data[0],
        'gdata' : gdata,
        'sor' : sor,
        #'valueFuell' : valueFuell,
        #'timeFuell' : timeFuell,
        #'machHour' : machHour,
        })

    

def chart2(request):
    import datetime
    
    if request.COOKIES.get('machId', ''):
        machId=request.COOKIES.get('machId', '')
        myend = Driver.objects.filter(machinery_id=machId).aggregate(Max('startday'))          
        driverobj = get_object_or_404(Driver, startday=myend['startday__max'])
        drivename=driverobj.name
        compobj = get_object_or_404(Company, pk=driverobj.company_id)
        company = compobj.name
    else:
        admId = int(request.COOKIES.get('adm', ''))
        admin = get_object_or_404(AdminList, pk=admId)
        compobj = get_object_or_404(Company, pk=admin.comp)
        company = compobj.name
        drivobj = get_object_or_404(Driver, pk=admin.mach)
        drivename = drivobj.name
        machId = drivobj.machinery_id
    
   
    machinery = get_object_or_404(Machinery, pk=machId)
    ident=machinery.identnum
    timeFuell = []
    valueFuell = []   
    machHour = []
    machHourMom = []
    consupt = []
    consuptAlter = []
    consuptTotal = []

    dataS = []
    dataSummary = []
   
    queryset = Fuelling.objects.filter(machinery_id=machId).order_by('-ftime')
    timeLimit =  datetime.date.today()
    
    i=0
    for q in queryset:
       
        if q.ftime <= timeLimit:            
            #timeFuell.append(q.ftime)        
            #valueFuell.append(q.liter)       
            #machHour.append(q.extime)       
            #machHourMom.append(q.extime)
            hhelp=q.extime
            thelp=q.ftime
            idhelp=q.ftime   
            for h in machHour:
                if h==q.extime:
                    hhelp=0
            if hhelp!=0:
                machHour.append(hhelp)
                machHourMom.append(hhelp)
                timeFuell.append(thelp)
               
                querys = Fuelling.objects.filter(extime=hhelp)
                lithelp=0
                for hq in querys:
                    lithelp = lithelp+hq.liter
                valueFuell.append(lithelp)
                if i>0:
                    machHourMom[i-1]=machHour[i-1]-machHourMom[i]     

                i+=1
                print(i)
    j=0
    if q and j==0:
        machHourMom[i-1]=machHour[i-1]-q.extime
        j=1

    summ=0
    for q in queryset:        
        summ+=q.liter
    
    machobj = get_object_or_404(Machinery, pk=machId)
    firsttank = queryset.last().liter
    print(firsttank)
    i=0
    for q in machHourMom:
        consupt.append(0.0)
        if q!=0:
            consupt[i] = round(valueFuell[i]/q,2)
        if (machHour[i]-machobj.run_hist) !=0:        
            consuptTotal.append(round((summ-queryset.last().liter)/(machHour[i]-machobj.run_hist),2))
        summ=summ-valueFuell[i]
        i+=1
        default=consupt[i-2]
    if request.method == "POST":
        baze = request.POST['baze']
        baze = float(baze.replace(',', '.'))
        print(baze)
        
    else:
        baze = consupt[i-2]
    
   
    i=0
    for q in consupt:
        consuptAlter.append(0.0)
        if q-baze!=0:
            consuptAlter[i]=round((q-baze)*100/baze,1)
        i+=1

    queryset = Fuelling.objects.filter(machinery_id=machId).order_by('ftime')
    
    i=0
    dataSummary=[]
    for q in timeFuell:
        if i<len(timeFuell)-1:
            dataS=[]
            dataS.append(q)
            dataS.append(valueFuell[i])
            dataS.append(machHour[i])
            dataS.append(machHourMom[i])
            dataS.append(consupt[i])
            dataS.append(consuptAlter[i])
            dataS.append(consuptTotal[i])
            dataSummary.append(dataS)

            i+=1
    
    print (dataSummary)


    return render(request, 'chart2.html', locals())


def consupt_works3(request):
    labels = []
    data = []
    helper =[]
    gdata=[]
    valueFuell = []
    timeFuell = []
    machHour = []
    if request.COOKIES.get('machId', ''):
        machId=request.COOKIES.get('machId', '')
    else:
        admId = int(request.COOKIES.get('adm', ''))
        admin = get_object_or_404(AdminList, pk=admId)
        compobj = get_object_or_404(Company, pk=admin.comp)
        company = compobj.name
        drivobj = get_object_or_404(Driver, pk=admin.mach)
        drivename = drivobj.name
        machId = drivobj.machinery_id
    
        

    queryset = OilChange.objects.filter(machinery_id=machId).order_by('-ftime')
    for q in queryset:
        #helper.append(q.id)
        #valueFuell.append(q.liter)
        #timeFuell.append(q.ftime)
        #machHour.append(q.extime)
        hhelp=q.extime
        thelp=q.ftime
        idhelp=q.id    
        for h in machHour:
            if h==q.extime:
                hhelp=0
        if hhelp!=0:
            machHour.append(hhelp)
            timeFuell.append(thelp)
            helper.append(idhelp)
            querys = OilChange.objects.filter(extime=hhelp)
            lithelp=0
            for hq in querys:
                lithelp = lithelp+hq.liter
            valueFuell.append(lithelp)

    query=Runing.objects.filter(machinery_id=machId).order_by('-id')
    jquery=Jobs.objects.order_by('id')
    labels=['A munka típus:',] #a munka tipusa
    labelsHelp=[]
    for qjob in jquery:
        labels.append(qjob.job)
        labelsHelp.append(qjob.job)

    gdata.append(labels)
    
    sor=[]
    i=0
    for x in range(len(queryset)):
        if (x>=0 and x<len(machHour)-1):
            ower=get_object_or_404(OilChange, pk=helper[x], machinery_id=machId).extime
            lower=get_object_or_404(OilChange, pk=helper[x+1], machinery_id=machId).extime
            
           
            datai=[]  #a munkával töltött idő
            
            datai.append(str(get_object_or_404(OilChange, pk=helper[x], machinery_id=machId).ftime))
            for qjob in jquery:
                
                datai.append(0.0)
                
            for run in query:
                if (run.ssum_whour<=ower and run.ssum_whour>lower):
                    for y in range(len(labelsHelp)):
                        if labelsHelp[y] == run.wtype:
                            datai[y+1] += run.sum_whour
                            #gdatai[y+1] = [run.wtype, run.sum_whour]
            sum=0.0
        

            

            #labels.append(labelsi)
            gdata.append(datai) 
            data.append(datai)
            
    
    


    print(gdata)    
    

    return JsonResponse(data={
        #'labels': labels,
        #'data': data[0],
        'gdata' : gdata,
        #'data' : data,
        #'sor' : sor,
        #'valueFuell' : valueFuell,
        #'timeFuell' : timeFuell,
        #'machHour' : machHour,
        })



def chart_oil(request):
    import datetime
    if request.COOKIES.get('machId', ''):
        machId=request.COOKIES.get('machId', '')
        myend = Driver.objects.filter(machinery_id=machId).aggregate(Max('startday'))          
        driverobj = get_object_or_404(Driver, startday=myend['startday__max'])
        drivename=driverobj.name
        compobj = get_object_or_404(Company, pk=driverobj.company_id)
        company = compobj.name
    else:
        admId = int(request.COOKIES.get('adm', ''))
        admin = get_object_or_404(AdminList, pk=admId)
        compobj = get_object_or_404(Company, pk=admin.comp)
        company = compobj.name
        drivobj = get_object_or_404(Driver, pk=admin.mach)
        drivename = drivobj.name
        machId = drivobj.machinery_id
    machinery = get_object_or_404(Machinery, pk=machId)
    ident=machinery.identnum
   
    

    
   
    return render(request, 'chart_oil.html', locals())





def lead_samples(request):
    import datetime
    if request.COOKIES.get('adm', ''):
            admId = int(request.COOKIES.get('adm', ''))
    else:
        return redirect(home)
    picobjs = SampImages.objects.order_by('id')
    admin = get_object_or_404(AdminList, pk=admId)    
    if request.COOKIES.get('machId', ''):
        machId=request.COOKIES.get('machId', '')
        sampleobj = OilSamples.objects.order_by('-minta_azonosito')
        data1={}
        data1['summData'+str(admin.lead)]=[]
        data4={}
        data4['summData'+str(admin.lead)]=[]
        for samp in sampleobj:
            data2={}
            data2['sData'+str(admin.lead)]=[]
            data3={}
            data3['sData'+str(admin.lead)]=[]
            sData=[]
            
            if str(machId)==str(samp.machinery_id):
                print(samp.machinery_id)
                mach = get_object_or_404(Machinery, pk=machId)
                
                data2['sData'+str(admin.lead)].append(samp.minta_azonosito)
                data2['sData'+str(admin.lead)].append(mach.identnum)
            
                data2['sData'+str(admin.lead)].append(samp.mintavetel_napja)
                data2['sData'+str(admin.lead)].append(samp.beerkezes_napja)
                age = 0
                machines = Runing.objects.filter(machinery_id=machId)
                for mach in machines:
                    if mach.workday <= samp.mintavetel_napja:
                        age = mach.ssum_whour
                data2['sData'+str(admin.lead)].append(age)

                data2['sData'+str(admin.lead)].append(color_var(samp,'viszkozitas_valtozas')[0])

                data2['sData'+str(admin.lead)].append(color_var(samp, 'koromtartalom')[0])
                
                data2['sData'+str(admin.lead)].append(color_var(samp, 'osszulledek')[0])
                
                data2['sData'+str(admin.lead)].append(color_var(samp, 'vasm_osszulledek')[0])
                
                data2['sData'+str(admin.lead)].append(color_var(samp, 'vastartalom')[0])
                
                data2['sData'+str(admin.lead)].append(color_var(samp, 'viztartalom')[0])
                
                data2['sData'+str(admin.lead)].append(color_var(samp, 'illoanyag')[0])
                            
                data2['sData'+str(admin.lead)].append(color_var(samp, 'lobbanaspont')[0])

                for pc in picobjs:
                    img = []
                    if pc.oilsamples_id == samp.id:
                        img.append(getattr(pc,'id'))
                        
                        img.append(getattr(pc,'sample_Img'))
                        samobj = get_object_or_404(OilSamples, pk=pc.oilsamples_id)
                        img=str(getattr(samobj,'minta_azonosito'))+"@"+str(getattr(pc,'id'))+str(getattr(pc,'sample_Img'))
                        data2['sData'+str(admin.lead)].append(img)

                data3['sData'+str(admin.lead)].append(color_var(samp,'viszkozitas_valtozas')[1])

                data3['sData'+str(admin.lead)].append(color_var(samp, 'koromtartalom')[1])
                
                data3['sData'+str(admin.lead)].append(color_var(samp, 'osszulledek')[1])
                
                data3['sData'+str(admin.lead)].append(color_var(samp, 'vasm_osszulledek')[1])
                
                data3['sData'+str(admin.lead)].append(color_var(samp, 'vastartalom')[1])
                
                data3['sData'+str(admin.lead)].append(color_var(samp, 'viztartalom')[1])
                
                data3['sData'+str(admin.lead)].append(color_var(samp, 'illoanyag')[1])
                            
                data3['sData'+str(admin.lead)].append(color_var(samp, 'lobbanaspont')[1])
                
            #print(data2['sData'+str(admin.lead)])
                data1['summData'+str(admin.lead)].append(data2['sData'+str(admin.lead)])       
                data4['summData'+str(admin.lead)].append(data3['sData'+str(admin.lead)])
    else:
        return redirect(home)
    superData=data1['summData'+str(admin.lead)]           


    superData1=data4['summData'+str(admin.lead)]
    return render(request, 'lead_samples.html', locals())




#email küldés

def sendSimpleEmail(name, emailto, calling):
   text = '\n\n Üdvözöljük! \r \n\n'
   text += 'Ezt az emailt azért kapta mert regisztráltuk:  ' + str(name) + ' néven, mint ' + str(calling) + ' a Gépkontrol rendszerében \r\n'
   return send_mail("Oil Control Regisztráció", str(text), "ctrl@weblap.name", [emailto])


def sendHTMLEmail(name , emailto, calling, user, password, rendsz):
    html_content = "<strong>Üdvözöljük!</strong><br><br>"
    html_content += "Ezt az emailt azért kapta mert regisztráltuk <b>" + str(name) + "</b> néven, mint <b>" + str(calling) + "</b> a Gépkontrol rendszerében <br>"
    html_content += "Felhasználónév: <b>" + str(user) + "</b><br>"
    html_content += "Jelszó: <b>" + decrypt(str(password)) + "</b><br>"
    html_content += "Lépjen be a saját webböngészőjében a oilcontrol.com címen elérhető oldalra és jelentkezzen be a fenti adatokkal!<br>"
    if str(calling) == 'vállalatot':
        html_content += "A belépéskor megnyíló regisztrációs oldalon regisztrálhatja a vállalkozás műszaki vezetőjét, <br>"
        html_content += "akinek lehetősége lesz menedzselni a gépeket , gépkezelőket, olajvizsgálatokat. <br><br>"   
    if str(calling) == 'műszaki vezetőt':
        html_content += "A belépéskor megnyíló oldalon menedzselheti a vállat robbanómotoros munkagép parkjával és kezelő személyzetével kapcsolatos adatokat., <br>"
        html_content += "-- új gépet regisztrálhat <br>"
        html_content += "-- regisztrálhatja a gépek kezelőit <br>"
        html_content += "-- és regisztrálhatja az olajdiagnosztkáért felelős személyt <br>"
        html_content += "-- Ön láthatja a gépkezelők által rögzitett futási, munkavégzési, és tankolási adatokat <br>"
        html_content += "-- láthatja és elemzheti az olajvizsgálatok adatait <br>"
    if str(calling) == 'gépkezelő':
        html_content += "A belépés után egy - egy gomb megnyomással - tudja rögzíteni az Ön által kezelt " + rendsz + " azonosítóju gép <br>"
        html_content += "futási, tankolási és olajcerére vonatkozó adatait.  <br><br>"
        html_content += "Első bejelentkezéskor célszerű a kapott jelszót megváltoztatni (kattintson a jelszóváltoztatás linkre!). <br><br>"    

        
    html_content += "<i>OilControl</i><br><br>"


    email = EmailMessage("Oil Control Regisztráció", html_content, "ctrl@weblap.name", [emailto])
    email.content_subtype = "html"
  
    return  email.send()


def investigate(requesstart_timet, pl, plObj, pltext, comp, f):
    day = pl.startday
    techleaders = plObj.objects.all()          
    tod = datetime.date.today()
    for tech in techleaders:
        if tech.startday<=tod and tech.startday>day and pl.company_id==tech.company_id:
            error_message = "Ez a felhasználónév már nem " + str(pltext) + "."
            return render(request, 'home.html',  {'companies' : comp, 'form' : f, 'error_message' : error_message})
        if day>tod and pl.company_id==tech.company_id:
            error_message = "Ez a felhasználónév még nem " + str(pltext) + "."
            return render(request, 'home.html',  {'companies' : comp, 'form' : f, 'error_message' : error_message})


    

def password_ch(request):
    #techleader = TechLeader.objects.get(pk=id)
    message = ""
   
    if 'azonosito' in request.COOKIES:
        id = int(request.COOKIES['azonosito'])
    else:
        message = "Jelentkezzen be újból!"
    if 'tipus' in request.COOKIES:
        tipus = request.COOKIES['tipus']
    else:
        message = "Jelentkezzen be újból!"
    
    if tipus=="TechLeader":
        group = get_object_or_404(TechLeader, pk=id)
        row = AdminList.objects.get(lead=id)
    if tipus=="DiagResp":
        group = get_object_or_404(DiagResp, pk=id)
        row = AdminList.objects.get(samp=id)
    if tipus=="Driver":
        group = get_object_or_404(Driver, pk=id)
        row = AdminList.objects.get(mach=id)
    if tipus=="Supervisor":
        group = get_object_or_404(Supervisor, pk=id)
        row = AdminList.objects.get(comp=None, lead=id)
    password1=decrypt(group.password)
    user=group.user
    name=group.name
    pf=""  
    
    form = PasswChangeForm(request.POST)
    if form.is_valid():
        pf=form.cleaned_data.get("password")   
        pfnew = form.cleaned_data.get("passwordnew")
        pfforse = form.cleaned_data.get("passwordforse")  
        if pf==password1:
            if pfnew==pfforse:
                row.password=encrypt(pfnew)
                row.save()
                group.password=encrypt(pfnew)
                group.save()
                message="Az Ön belépési jelszava megváltozott. Kérjük, hogy az új jelszavával jelentkezzen be!"
                
                
                return HttpResponseRedirect(reverse('home')) 
                #return render(request, 'home.html',  {'form' : form, 'error_message' : message})
            else:
                message="Az új jelszó és a megerősítés nem egyezik meg. Próbálja újra!"
                return render(request, 'password_ch.html', {'form' : form, 'name' : name, 'message' : message})
        else:
            message="Hibás jelszó! Próbálja újra!"
            return render(request, 'password_ch.html', {'form' : form, 'name' : name, 'message' : message})



    return render(request, 'password_ch.html', {'form' : form, 'name' : name, 'message' : message})


def forgot_passw(request):
    message = ""
    password = ""
    id = ""
    tipus=""    
    if 'tipus' in request.COOKIES:
        tipus = request.COOKIES['tipus']
        t = True
    else:
        t = False
    if t:
        form = ForgPasswForm1(request.POST)
    else:
        form = ForgPasswForm2(request.POST)
        if form.is_valid():
            tipus = form.cleaned_data.get("usergroup")
    if tipus == "TechLeader":
        objts = TechLeader.objects.all()
    if tipus == "DiagResp":
        objts = DiagResp.objects.all()
    if tipus == "Driver":
        objts = Driver.objects.all()
    if tipus == "Supervisor":
        objts = Supervisor.objects.all()
    flag = False
    if form.is_valid():
        email1 = form.cleaned_data.get("email").strip()
        user1 = form.cleaned_data.get("user").strip()
        for oj in objts:
            
            if oj.email.strip() == email1 and oj.user.strip() == user1:
                flag=True
                id = oj.pk
        if flag==False:
            message="Ez a felhasználó nem ezzel az email címmel regisztrált."
            return render(request, 'forgot_password.html', {'form' : form, 'message' : message, 'flag' : flag})
    if flag:
        if tipus=="TechLeader":
            group = get_object_or_404(TechLeader, pk=id)
            row = AdminList.objects.get(lead=id)
        if tipus=="DiagResp":
            group = get_object_or_404(DiagResp, pk=id)
            row = AdminList.objects.get(samp=id)
        if tipus=="Driver":
            group = get_object_or_404(Driver, pk=id)
            row = AdminList.objects.get(mach=id)
        if tipus=="Supervisor":
            group = get_object_or_404(Supervisor, pk=id)
            row = AdminList.objects.get(comp=None, lead=id)
        password = User.objects.make_random_password()
        row.password=encrypt(password)
        row.save()
        group.password=encrypt(password)
        group.save()
        html_content = "<strong>Üdvözöljük!</strong><br><br>"
        html_content += "Ezt az emailt azért kapta mert elfelejtett jelszavát helyreállítottuk. <br>"
        html_content += "Az új jelszava: <b>" + str(password) + "</b><br>"
        html_content += "Jelentkezzen be a felhasználónevével és az új jelszavával,<br>"
        html_content += "és változtassa meg a levelünkben kapott új jelszót.<br><b>"
        html_content += "<i>OilConntrol</i><br>"
        email = EmailMessage("Oil Control Új jelszó", html_content, "ctrl@weblap.name", [email1])
        email.content_subtype = "html"  
        email.send()

        message="A helyreállított jelszót elküldtük a regisztrációs email címre. Jelentkezzen be!"

       

        
        
    return render(request, 'forgot_password.html', {'form' : form, 'message' : message, 'flag' : flag})






from django import forms
from .models import *
#from datetimepicker.widgets import DateTimePicker
from bootstrap_datepicker_plus import DatePickerInput
from django.forms.widgets import HiddenInput




class RegForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Név: ")
    email = forms.EmailField(max_length=254, label="Email cím: ")
    user = forms.CharField(max_length=10, label="Választott felhasználónév: ")
    password = forms.CharField(widget=forms.PasswordInput, label="Jelszó: " )
    

    class Meta:
        model = Company
        fields = ('name', 'email', 'user', 'password')

class SupervisorRegForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Név: ")
    email = forms.EmailField(max_length=254, label="Email cím: ")
    user = forms.CharField(max_length=10, label="Választott felhasználónév: ")
    password = forms.CharField(widget=forms.PasswordInput, label="Jelszó: " )
    

    class Meta:
        model = Supervisor
        fields = ('name', 'email', 'user', 'password')



class HomeForm(forms.Form):
    user = forms.CharField(max_length=30, label="Felhasználónév ")
    password = forms.CharField(widget=forms.PasswordInput, label="Jelszó ")





class TechLRegForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Név: ", required=True)
    startday = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'), label="A munkába állás napja")
    #startday = forms.DateField(widget=forms.DateInput(attrs={'id' : 'datetomepicker12'}), label="A munkába állás napja")
    email = forms.EmailField(max_length=254, label="Email cím: ")
    user = forms.CharField(max_length=10, label="Választott felhasználónév: ")
    password = forms.CharField(widget=forms.PasswordInput, label="Jelszó: ")
    

    class Meta:
        model = TechLeader
        fields = ('name', 'startday', 'email', 'user', 'password')


class DiagRespRegForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Név: ", required=True)
    startday = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'), label="A munkába állás napja")
    email = forms.EmailField(max_length=254, label="Email cím: ")
    user = forms.CharField(max_length=10, label="Választott felhasználónév: ")
    password = forms.CharField(widget=forms.PasswordInput, label="Jelszó: " )
    

    class Meta:
        model = DiagResp
        fields = ('name', 'startday', 'email', 'user', 'password')

class DriverRegForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Név: ", required=True)
    startday = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'), label="A munkába állás napja")
    email = forms.EmailField(max_length=254, label="Email cím: ")
    user = forms.CharField(max_length=10, label="Választott felhasználónév: ")
    password = forms.CharField(widget=forms.PasswordInput, label="Jelszó: " )
    machinery = forms.CharField(label="Melyik gép kezelője?")
    #machinery = forms.ModelChoiceField(queryset=Machinery.objects.filter(company_id=26).order_by('identnum'), label="Melyik gép kezelője?")

    class Meta:
        model = Driver
        fields = ('name', 'startday', 'email', 'user', 'password')
    
    

UNIT_CHOICES= [
    ('munkaóra', 'munkaóra'),
    ('kilometer', 'kilometer'),
]
FUEL_CHOICES= [
    ('gázolaj', 'gázolaj'),
    ('benzin', 'benzin'),
]

class MachineryRegForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label="Megnevezése, tipusa ", required=True)
    identnum = forms.CharField(max_length=10, label="Azonosítója, rendszáma ", required=True)
    
    buyday = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'), label="A gép beszerzésének napja")
    run_unit = forms.CharField(label="Futásteljesítmény mértékegysége ", widget=forms.Select(choices=UNIT_CHOICES))
    run_hist = forms.IntegerField(label="Óraállás (üzemóra) regisztráláskor")
    fuel = forms.CharField(label="Üzemanyag fajtája ", widget=forms.Select(choices=FUEL_CHOICES))
    

    class Meta:
        model = Machinery
        fields = ('name', 'identnum', 'cidentnum',  'buyday', 'run_unit', 'run_hist', 'fuel')


USER_GROUP_CHOICE=[
    ('gépkezelő', 'gépkezelő'),
    ('diagfelelos', 'diagnosztika felelős'),
    ('műszaki vezeető', 'műszaki vezető'),
    
]

class ForgPasswForm1(forms.Form):
    user = forms.CharField(max_length=10, label="Választott felhasználónév: ")
    email = forms.EmailField(max_length=254, label="Regisztrált email cím: ")

class ForgPasswForm2(forms.Form):
    usergroup = forms.CharField(label='Milyen minőségben van regisztrálva a rendszerben?', widget=forms.RadioSelect(choices=USER_GROUP_CHOICE))
    user = forms.CharField(max_length=10, label="Választott felhasználónév: ")
    email = forms.EmailField(max_length=254, label="Email cím: ")

        
class PasswChangeForm(forms.Form):
    #usergroup= forms.CharField(label='Milyne minőségben van regisztrálva a rendszerben?', widget=forms.RadioSelect(choices=USER_GROUP_CHOICE))
    user = forms.CharField(max_length=10, label="Felhasználónév: ")
    password = forms.CharField(widget=forms.PasswordInput, label="Jelenlegi jelszó: " )
    passwordnew = forms.CharField(widget=forms.PasswordInput, label="Új jelszó: " )
    passwordforse = forms.CharField(widget=forms.PasswordInput, label="Új jelszó megerősítése: " )
    


class RuningForm(forms.ModelForm):
    wtype = forms.CharField(max_length=20, label="Wtype: ", required=False)
    start_time = forms.CharField(max_length=20, label="Wtype: ", required=False)
    end_time = forms.CharField(max_length=20, label="Wtype: ", required=False)
    sum_whour=forms.FloatField(required=False)
    start_kmeter = forms.IntegerField(label="induló km", required=False)
    end_kmeter = forms.IntegerField(label="erkezo km", required=False)

    class Meta:
        model = Runing
        fields = ('wtype', 'start_time', 'end_time', 'sum_whour', 'start_kmeter', 'end_kmeter')

class JobsForm(forms.ModelForm):
    job = forms.CharField(max_length=20, label="Újabb munkatípus: ")

    class Meta:
        model = Jobs
        fields = ('job', )

class AdminListForm(forms.ModelForm):
    class Meta:
        model = AdminList
        fields = ('user', 'password', 'comp', 'mach', 'samp', 'lead')

class FuellingForm(forms.ModelForm):
    kmeter = forms.IntegerField(label="Kilométer óra állása", required=False)
    liter = forms.IntegerField(label="Tankolt mennyiség (liter)", required=True)

    class Meta:
        model = Fuelling
        fields = ('kmeter', 'liter')

class OilChangeForm(forms.ModelForm):
    kmeter = forms.IntegerField(label="Kilométer óra állása", required=False)
    liter = forms.IntegerField(label="Tankolt mennyiség (liter)", required=True)

    class Meta:
        model = OilChange
        fields = ('kmeter', 'liter')

class OilSamplesForm(forms.ModelForm):
    minta_azonosito = forms.CharField(max_length=15, label="Mintaazonosító")
    beerkezes_napja = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'), label="A minta beérkezésének napja", required=True)
    mintavetel_napja = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'), label="Mintavétel napja", required=True)
   
    viszkozitas_valtozas1 = forms.FloatField(label="", required=False, )
    viszkozitas_valtozas2 = forms.FloatField(label="", required=False)
    viszkozitas_valtozas3 = forms.FloatField(label="", required=False)
   
    koromtartalom1 = forms.FloatField(label="", required=False)
    koromtartalom2 = forms.FloatField(label="", required=False)
    koromtartalom3 = forms.FloatField(label="", required=False)
    
    osszulledek1 = forms.FloatField(label="", required=False)
    osszulledek2 = forms.FloatField(label="", required=False)
    osszulledek3 = forms.FloatField(label="", required=False)
    
    vasm_osszulledek1 = forms.FloatField(label="", required=False)
    vasm_osszulledek2 = forms.FloatField(label="", required=False)
    vasm_osszulledek3 = forms.FloatField(label="", required=False)
    
    vastartalom1 = forms.FloatField(label="", required=False)
    vastartalom2 = forms.FloatField(label="", required=False)
    vastartalom3 = forms.FloatField(label="", required=False)
    
    viztartalom1 = forms.FloatField(label="", required=False)
    viztartalom2 = forms.FloatField(label="", required=False)
    viztartalom3 = forms.FloatField(label="", required=False)
    
    illoanyag1 = forms.FloatField(label="", required=False)
    illoanyag2 = forms.FloatField(label="", required=False)
    illoanyag3 = forms.FloatField(label="", required=False)
    
    lobbanaspont1 = forms.FloatField(label="", required=False)
    lobbanaspont2 = forms.FloatField(label="", required=False)
    lobbanaspont3 = forms.FloatField(label="", required=False)
    
    

    class Meta:
        model = OilSamples
        fields = ['minta_azonosito', 'beerkezes_napja', 'mintavetel_napja', 'viszkozitas_valtozas1', 'viszkozitas_valtozas2', 
                'viszkozitas_valtozas3', 'koromtartalom1', 'koromtartalom2', 'koromtartalom1', 'koromtartalom3', 'osszulledek1', 
                'osszulledek2',  'osszulledek3', 'vasm_osszulledek1', 'vasm_osszulledek2', 'vasm_osszulledek3', 'vastartalom1', 
                'vastartalom2', 'vastartalom3', 'viztartalom1', 'viztartalom2', 'viztartalom3', 'illoanyag1', 'illoanyag2', 'illoanyag3',
                'lobbanaspont1', 'lobbanaspont2', 'lobbanaspont3', 'kep1', 'kep2', 'kep3' 
                ]       
        
class SampImagesForm(forms.ModelForm):
    sample_Img=forms.ImageField(label="", required=False)

    class Meta:
        model = SampImages
        fields = ['sample_Img',]
    

    
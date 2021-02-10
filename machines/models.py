from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    wday = models.DateField(auto_now_add=True)
    user = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128, null=False)
    objects = models.Manager()

    def __str__(self):
        return self.name

class Supervisor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    wday = models.DateField(auto_now_add=True)
    user = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128, null=False)
    objects = models.Manager()

    def __str__(self):
        return self.name

class TechLeader(models.Model):
    name = models.CharField(max_length=100)
    wday = models.DateField(auto_now_add=True)
    startday = models.DateField()
    email = models.EmailField(max_length=254, default='to1@example.com')
    user = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='techleaders')

    def __str__(self):
        return self.name

class DiagResp(models.Model):
    name = models.CharField(max_length=100)
    wday = models.DateField(auto_now_add=True)
    startday = models.DateField()
    email = models.EmailField(max_length=254, unique=True)
    user = models.CharField(max_length=30, null=False, unique=True)
    password = models.CharField(max_length=128, null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='diagresps')

    def __str__(self):
        return self.name

class Machinery(models.Model):
    name = models.CharField(max_length=100)
    identnum = models.CharField(max_length=10)
    cidentnum = models.CharField(max_length=10, unique=True, null=True, blank=True)
    wday = models.DateField(auto_now_add=True)
    buyday = models.DateField(null=False)
    run_unit = models.CharField(max_length=10)
    run_hist = models.IntegerField(null=True, blank=True)
    fuel = models.CharField(max_length=10)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='machinerys')

    def __str__(self):
        return self.name

class Driver(models.Model):
    name = models.CharField(max_length=100)
    wday = models.DateField(auto_now_add=True)
    startday = models.DateField()
    email = models.EmailField(max_length=254, unique=True)
    user = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    machinery = models.ForeignKey(Machinery, on_delete=models.CASCADE, null=True, related_name='drivers')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='drivers')
    def __str__(self):
        return self.name

class Fuelling(models.Model):
    ftime = models.DateField(auto_now_add=True)
    extime = models.FloatField(null=True)
    kmeter = models.PositiveIntegerField(null=True)
    liter =  models.PositiveSmallIntegerField()
    machinery = models.ForeignKey(Machinery, on_delete=models.CASCADE, related_name='fuelings')

    

class OilChange(models.Model):
    ftime = models.DateField(auto_now_add=True)
    extime = models.FloatField(null=True)
    kmeter = models.PositiveIntegerField(null=True)
    liter =  models.PositiveSmallIntegerField(null=False)
    machinery = models.ForeignKey(Machinery, on_delete=models.CASCADE, related_name='oilchanges')

    

class Runing(models.Model):
    workday = models.DateField(auto_now_add=True)
    wtype = models.CharField(max_length=20, null=True, blank=True)
    start_time = models.CharField(max_length=20, null=True, blank=True)
    end_time = models.CharField(max_length=20, null=True, blank=True)
    sum_whour = models.FloatField(null=True)
    ssum_whour = models.FloatField(null=True)
    start_kmeter = models.PositiveIntegerField(null=True)
    end_kmeter = models.PositiveIntegerField(null=True)
    machinery = models.ForeignKey(Machinery, on_delete=models.CASCADE, related_name='runings')

    

class OilSamples(models.Model):
    minta_azonosito = models.CharField(max_length=15, unique=True)
    beerkezes_napja = models.DateField()
    mintavetel_napja = models.DateField()
    
    viszkozitas_valtozas1 = models.SmallIntegerField(null=True, blank=True)
    viszkozitas_valtozas2 = models.SmallIntegerField(null=True, blank=True)
    viszkozitas_valtozas3 = models.SmallIntegerField(null=True, blank=True)
    
    koromtartalom1 = models.FloatField(null=True, blank=True)
    koromtartalom2 = models.FloatField(null=True, blank=True)
    koromtartalom3 = models.FloatField(null=True, blank=True)
    
    osszulledek1 = models.SmallIntegerField(null=True, blank=True)
    osszulledek2 = models.SmallIntegerField(null=True, blank=True)
    osszulledek3 = models.SmallIntegerField(null=True, blank=True)
    
    vasm_osszulledek1 = models.SmallIntegerField(null=True, blank=True)
    vasm_osszulledek2 = models.SmallIntegerField(null=True, blank=True)
    vasm_osszulledek3 = models.SmallIntegerField(null=True, blank=True)
    
    vastartalom1 = models.SmallIntegerField(null=True, blank=True)
    vastartalom2 = models.SmallIntegerField(null=True, blank=True)
    vastartalom3 = models.SmallIntegerField(null=True, blank=True)
   
    viztartalom1 = models.FloatField(null=True, blank=True)
    viztartalom2 = models.FloatField(null=True, blank=True)
    viztartalom3 = models.FloatField(null=True, blank=True)
    
    illoanyag1 = models.FloatField(null=True, blank=True)
    illoanyag2 = models.FloatField(null=True, blank=True)
    illoanyag3 = models.FloatField(null=True, blank=True)
    
    lobbanaspont1 = models.SmallIntegerField(null=True, blank=True)
    lobbanaspont2 = models.SmallIntegerField(null=True, blank=True)
    lobbanaspont3 = models.SmallIntegerField(null=True, blank=True)
    
    kep1 = models.ImageField(null=True, blank=True, upload_to='images/')    
    kep2 = models.ImageField(null=True, blank=True, upload_to='images/')
    kep3 = models.ImageField(null=True, blank=True, upload_to='images/')
    machinery = models.ForeignKey(Machinery, on_delete=models.CASCADE, related_name='oilsamples')

    def __str__(self):
        return self.minta_azonosito


class AdminList(models.Model):
    user = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    comp = models.IntegerField(null=True, blank=True)
    mach = models.IntegerField(null=True, blank=True)
    samp = models.IntegerField(null=True, blank=True)
    lead = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user

class Jobs(models.Model):
    job = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.job


class SampImages(models.Model):
    sample_Img = models.ImageField(null=True, blank=True, upload_to='images/') 
    oilsamples = models.ForeignKey(OilSamples, on_delete=models.CASCADE, related_name='sampleimages')

    def __str__(self):
        return self.sample_Img
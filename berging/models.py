'''
Created on Sep 1, 2014

@author: theo
'''
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import pandas as pd

NEERSLAG = (('d','droog'),('g','gemiddeld'),)
BODEMTYPE = (('z','zand op klei'),)
KWALITEIT=(('f', 'zoet'),('b','brak'),('s','zout'))
IRRIGATIE=(('i', 'DI systeem'),('d','druppelbevloeiing'))
REKENTYPE = (('o','oppervlakte'),('v','volume'))
           
class Scenario(models.Model):
    naam = models.CharField(max_length=100)
    neerslag = models.CharField(max_length=1,choices=NEERSLAG,default='g',verbose_name='waterbehoefte')
    bodem = models.CharField(max_length=1,choices=BODEMTYPE,default='z',verbose_name='bodemtype')
    kwaliteit = models.CharField(max_length=1,choices=KWALITEIT,default='f',verbose_name='waterkwaliteit')
    irrigatie = models.CharField(max_length=1,choices=IRRIGATIE,default='d',verbose_name='methode van watergift')
    reken = models.CharField(max_length=1,choices=REKENTYPE,default='o',verbose_name='berekeningsmethode')
    oppervlakte = models.FloatField(default=1, validators = [MinValueValidator(0.1), MaxValueValidator(1000)], verbose_name='grootte', help_text = 'oppervlakte perceel (Ha)')
    volume = models.FloatField(default=5000, validators = [MinValueValidator(0.1), MaxValueValidator(1000000)], verbose_name='grootte', help_text = 'volume bassin (m3)')

    def __unicode__(self):
        return self.naam

    def matrix_code(self):
        ''' bepaal matrix code adhv gemaakte keuzes'''
        return self.neerslag+self.bodem+self.kwaliteit+self.irrigatie
            
class Matrix(models.Model):
    code = models.CharField(max_length=10, unique=True)
    toelichting = models.TextField(blank=True)
    file = models.FileField(upload_to='matrix')
    rijnaam = models.CharField(default = 'Oppervlakte (m2)', max_length=50)
    rijmin = models.FloatField(blank=True)
    rijmax = models.FloatField(blank=True)
    kolomnaam = models.CharField(default = 'Volume (m3)', max_length=50)
    kolmin = models.FloatField(blank=True)
    kolmax = models.FloatField(blank=True)

    def get_dimensions(self, f=None):
        src = f or self.file.path
        df = pd.read_csv(src,index_col=0)
        self.code = df.index.name
        self.rijmin = float(df.index[0]) 
        self.rijmax = float(df.index[-1]) 
        self.kolmin = float(df.columns[0]) 
        self.kolmax = float(df.columns[-1])
        drow = (self.rijmax - self.rijmin) / (df.shape[0]-1)
        dcol = (self.kolmax - self.kolmin) / (df.shape[1]-1)
        return (drow,dcol)
        
    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name_plural = 'matrices'

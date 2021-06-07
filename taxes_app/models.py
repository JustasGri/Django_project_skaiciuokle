from typing import Text
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



class Veikla(models.Model):
    pavadinimas = models.CharField(
        max_length=100,
        help_text='Individualios veiklos pavadinimas',
        verbose_name='',
        )
    date_posted = models.DateTimeField(default=timezone.now)
    asmuo = models.ForeignKey(User, on_delete=models.CASCADE, related_name='veiklos')


    LENGVATA_STATUS = (
            ('y', 'Taip'),
            ('n', 'Ne'),
    )

    status3 = models.CharField(
        max_length=1,
        choices=LENGVATA_STATUS,
        blank=False,
        default='n',
        help_text='Ar norite pasinaudoti sodros mokesčių lengvata?',
        verbose_name='',
    )

    ISLAIDOS_STATUS = (
        ('i30', 'Išlaidos 30%'),
        ('isf', 'Faktinės išlaidos'),
    )

    status2 = models.CharField(
        max_length=3,
        choices=ISLAIDOS_STATUS,
        blank=False,
        default='isf',
        help_text='Pasirinkite išlaidas',
        verbose_name='',
    )

    PENSIJA_STATUS = (
        ('p24', 'Pensija 2.4%'),
        ('p3', 'Pensija 3%'),
        ('pn', 'Nekaupiama'),
    )

    status = models.CharField(
        max_length=3,
        choices=PENSIJA_STATUS,
        blank=False,
        default='pn',
        help_text='Ar kaupiate pensija?',
        verbose_name='',
    )


    @property
    def suma_pajamos(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.pajamos
        return sum
    

    @property
    def suma_islaidos_pasirinkimas(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.islaidos_pasirinkimas
        return sum

    @property
    def suma_islaidos30(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.islaidos30
        return sum

    @property
    def suma_islaidos_30_GPM(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.islaidos_30_GPM
        return sum

    @property
    def suma_islaidos_faktines(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.islaidos_faktines
        return sum
    
    @property
    def suma_islaidos_faktines_GPM(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.islaidos_faktines_GPM
        return sum

    @property
    def suma_islaidos_faktines(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.islaidos_faktines
        return sum

    @property
    def suma_sodra(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.sodra
        return sum

    @property
    def suma_vsd(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.vsd
        return sum

    @property
    def suma_psd(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.psd
        return sum
    
    @property
    def suma_mokesciai_sodra(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.mokesciai_sodra
        return sum

    @property
    def suma_mokesciai(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.mokesciai
        return sum

    @property
    def suma_pajamos_po_mokesciu(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.pajamos_po_mokesciu
        return sum

    @property
    def suma_pelnas(self):
        sum = 0
        for uzdarbis in self.uzdarbiai.all():
            sum += uzdarbis.pelnas
        return sum

    def __str__(self):
            return self.pavadinimas

        
    def get_absolute_url(self):
        return reverse('veikla-detail', kwargs={'pk': self.pk})


class Uzdarbis(models.Model):
    pajamos = models.FloatField(
        max_length=100, 
        null=True,
        verbose_name='',
        help_text='Įveskite pajamas',
        )
    islaidos = models.FloatField(
        max_length=100,
        default = 0, 
        null=True,
        verbose_name='',
        help_text='Įveskite išlaidas',
        )

    date_posted = models.DateTimeField(default=timezone.now)
    darbas = models.ForeignKey(Veikla, on_delete=models.CASCADE, related_name='uzdarbiai')
    
            
    @property
    def islaidos30(self):
        pajamos_po_30_isl = self.pajamos - (self.pajamos * 30) / 100
        return pajamos_po_30_isl
    
    @property
    def islaidos30_pr(self):
        return (self.pajamos * 30) / 100
  
    @property
    def islaidos_faktines(self):
        pajamos_po_fakt_isl = self.pajamos - self.islaidos
        return pajamos_po_fakt_isl
   
    @property
    def islaidos_pasirinkimas(self):
        if self.darbas.status2 == 'i30':
            return self.islaidos30_pr
        if self.darbas.status2 == 'isf':
            return self.islaidos

    @property
    def islaidos_30_GPM(self):
        gpm_30 = (self.islaidos30 * 5) / 100
        return gpm_30

    @property
    def islaidos_faktines_GPM(self):
        gpm_fak = (self.islaidos_faktines * 5) / 100
        if gpm_fak < 0:
            return 0
        return gpm_fak

    @property
    def sodra(self):
        if self.darbas.status3 == 'n':
            return self.pajamos - (self.pajamos * 37) / 100
        if self.darbas.status3 == 'y':
            return 0


    @property
    def vsd(self):
        if self.darbas.status == 'p3':
            return (self.sodra * 15.52) / 100
        if self.darbas.status == 'p24':
            return (self.sodra * 14.92) / 100
        if self.darbas.status == 'pn':
            return (self.sodra * 12.52) / 100

    
    @property
    def psd(self):
        sodra_psd = (self.sodra * 6.98) / 100
        return sodra_psd

    @property
    def mokesciai_sodra(self):
        sodra_m = self.vsd + self.psd
        return sodra_m
    

    @property
    def mokesciai(self):
        if self.darbas.status2 == 'i30':
            return self.mokesciai_sodra + self.islaidos_30_GPM
        if self.darbas.status2 == 'isf':
            return self.mokesciai_sodra + self.islaidos_faktines_GPM
        

    @property
    def pajamos_po_mokesciu(self):
        po_mokesciu = self.pajamos - self.mokesciai
        return po_mokesciu

    @property
    def pelnas(self):
        if self.darbas.status2 == 'i30':
            return self.pajamos_po_mokesciu - self.islaidos30_pr
        if self.darbas.status2 == 'isf':
            return self.pajamos_po_mokesciu - self.islaidos


    def __str__(self):
        return f"{self.pajamos}"

    def get_absolute_url(self):
        return reverse('uzdarbis-detail', kwargs={'pk': self.pk})

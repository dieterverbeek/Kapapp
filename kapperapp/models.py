from django.db import models
from django.contrib.auth.models import User

class Klant(models.Model):
    voornaam = models.CharField(max_length=100)
    achternaam = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    gsm = models.CharField(max_length=20, blank=True, null=True)
    volledig_adres = models.TextField(blank=True, null=True)
    allergieen = models.TextField(blank=True, null=True)

    huid = models.TextField(blank=True, null=True)
    behandeling_hiervoor = models.TextField(blank=True, null=True)

    haartype = models.CharField(max_length=100, blank=True, null=True)
    natuurlijke_haarkleur = models.CharField(max_length=100, blank=True, null=True)
 
    toonhoogte_lengtes = models.CharField(max_length=100, blank=True, null=True)
    weerschijn = models.CharField(max_length=100, blank=True, null=True)
    percentage_witte_haren_voor = models.IntegerField(blank=True, null=True)
    percentage_witte_haren_achter = models.IntegerField(blank=True, null=True)
    wens = models.TextField(blank=True, null=True)
    color_formula = models.CharField(max_length=200, blank=True, null=True)
    
    techniek = models.TextField(blank=True, null=True)
   
    producten = models.TextField(blank=True, null=True)
    inwerktijd = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    laatste_rekening = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.voornaam} {self.achternaam}"




class Note(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.text[:50]
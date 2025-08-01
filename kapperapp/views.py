# KAPPERAPP/kapperapp/views.py
from django.shortcuts import render, redirect, get_object_or_404 # Add get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Klant, Note
from django.db.models import Q
import openpyxl
from django.http import HttpResponse


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Changed from '/' to 'dashboard'

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Ongeldige gebruikersnaam of wachtwoord.")
        else:
            messages.error(request, "Ongeldige gebruikersnaam of wachtwoord.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "U bent uitgelogd.")
    return redirect('/login/')

@login_required
def dashboard_view(request):
    if request.method == 'POST':
        if 'note_text' in request.POST:
            # Add new note
            note_text = request.POST.get('note_text')
            if note_text:
                Note.objects.create(text=note_text, user=request.user)
                messages.success(request, 'Notitie toegevoegd!')
        elif 'delete_note_id' in request.POST:
            # Delete note
            note_id = request.POST.get('delete_note_id')
            try:
                note = Note.objects.get(id=note_id, user=request.user)
                note.delete()
                messages.success(request, 'Notitie verwijderd!')
            except Note.DoesNotExist:
                messages.error(request, 'Notitie niet gevonden!')
        
        return redirect('dashboard')
    
    notes = Note.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'notes': notes})



@login_required
def klanten_view(request):
    zoek = request.GET.get('zoek', '')
    
    if zoek:
        klanten = Klant.objects.filter(
            Q(voornaam__icontains=zoek) | 
            Q(achternaam__icontains=zoek)
        ).order_by('voornaam', 'achternaam')
    else:
        klanten = Klant.objects.all().order_by('voornaam', 'achternaam')
    
    return render(request, 'klanten.html', {
        'klanten': klanten,
        'zoek': zoek
    })

def klant_verwijderen_view(request, klant_id):
    if request.method == 'POST':
        klant = get_object_or_404(Klant, id=klant_id) # <--- 'get_object_or_404' is not defined
        klant.delete()
    return redirect('klanten')

@login_required 
def afrekenen_view(request):
    # Deze code wordt uitgevoerd als het formulier wordt verstuurd (opslaan)
    if request.method == 'POST':
        # 1. Haal de data uit het verstuurde formulier
        klant_id = request.POST.get('klant_id')
        rekening_data_json = request.POST.get('rekening_data')

        # 2. Validatie: controleer of een klant en diensten zijn geselecteerd
        if not klant_id or not rekening_data_json:
            messages.error(request, 'Selecteer een klant en voeg minstens één dienst toe.')
            return redirect('afrekenen') # Stuur terug naar de afrekenpagina

        # 3. Probeer de klant op te halen en de rekening op te slaan
        try:
            klant = get_object_or_404(Klant, id=klant_id)
            
            # Sla de JSON-string direct op in het 'laatste_rekening' veld
            klant.laatste_rekening = rekening_data_json
            klant.save() # De wijziging wordt opgeslagen in de database

            # Geef een succesbericht en stuur door naar het dashboard
            messages.success(request, f'Rekening succesvol opgeslagen voor {klant.voornaam} {klant.achternaam}.')
            return redirect('dashboard')

        except Klant.DoesNotExist:
            messages.error(request, 'De geselecteerde klant kon niet worden gevonden.')
            return redirect('afrekenen')


    # --- Deze code wordt uitgevoerd als de pagina normaal wordt geladen (GET) ---
    alle_klanten = Klant.objects.all().order_by('voornaam', 'achternaam') 
    context = {
        'klanten': alle_klanten
    }
    return render(request, 'afrekenen.html', context)

@login_required
def klant_toevoegen_view(request):
    if request.method == 'POST':
        # Haal de percentage waardes op en converteer ze naar int of None
        # Zorg ervoor dat lege strings None worden voor IntegerField (null=True)
        percentage_voor_str = request.POST.get('percentage_witte_haren_voor')
        percentage_voor = int(percentage_voor_str) if percentage_voor_str else None

        percentage_achter_str = request.POST.get('percentage_witte_haren_achter')
        percentage_achter = int(percentage_achter_str) if percentage_achter_str else None

        # Voor 'huid' moet je de samengevoegde string van de checkboxes gebruiken
        # Die wordt door je JavaScript in een hidden input 'huid' gezet
        huid_data = request.POST.get('huid', '')

        klant = Klant(
            voornaam=request.POST['voornaam'],
            achternaam=request.POST['achternaam'],
            email=request.POST.get('email', ''),
            gsm=request.POST.get('gsm', ''),
            allergieen=request.POST.get('allergieen', ''),
            # Gebruik het correcte veld 'huid' dat door je JS wordt gevuld
            huid=huid_data,
            behandeling_hiervoor=request.POST.get('behandeling_hiervoor', ''),
            haartype=request.POST.get('haartype', ''),
            natuurlijke_haarkleur=request.POST.get('natuurlijke_haarkleur', ''),
       
            toonhoogte_lengtes=request.POST.get('toonhoogte_lengtes', ''),
            weerschijn=request.POST.get('weerschijn', ''),
           
            percentage_witte_haren_voor=percentage_voor,
            percentage_witte_haren_achter=percentage_achter,
            wens=request.POST.get('wens', ''), 
            color_formula=request.POST.get('color_formula', ''),
            volledig_adres=request.POST.get('volledig_adres', ''),
            techniek=request.POST.get('techniek', ''),
            producten=request.POST.get('producten', ''), 
            inwerktijd=request.POST.get('inwerktijd', ''),
        )
        klant.save()
        return redirect('klanten') # Zorg dat deze URL bestaat in je urls.py

    return render(request, 'klant_toevoegen.html', {})


import json # <-- Import the json library at the top of your file
from django.http import JsonResponse # <-- Import JsonResponse
from django.views.decorators.http import require_POST # <-- Import for security

@login_required
@require_POST # Zorgt ervoor dat deze view alleen POST-requests accepteert
def klant_bewerken_view(request, klant_id):
    try:
        # Zoek het bestaande klantobject
        klant = get_object_or_404(Klant, id=klant_id)

        # Laad de JSON-data die vanuit de JavaScript fetch-request is verstuurd
        data = json.loads(request.body)

        # Werk het Klant-object bij met de nieuwe data uit het formulier
        klant.voornaam = data.get('voornaam', klant.voornaam)
        klant.achternaam = data.get('achternaam', klant.achternaam)
        klant.email = data.get('email', klant.email)
        klant.gsm = data.get('gsm', klant.gsm)
        klant.volledig_adres = data.get('volledig_adres', klant.volledig_adres)
        klant.allergieen = data.get('allergieen', klant.allergieen)
        klant.huid = data.get('huid', klant.huid)
        klant.behandeling_hiervoor = data.get('behandeling_hiervoor', klant.behandeling_hiervoor)
        klant.haartype = data.get('haartype', klant.haartype)
        klant.natuurlijke_haarkleur = data.get('natuurlijke_haarkleur', klant.natuurlijke_haarkleur)
        klant.toonhoogte_lengtes = data.get('toonhoogte_lengtes', klant.toonhoogte_lengtes)
        klant.weerschijn = data.get('weerschijn', klant.weerschijn)
        
        # Behandel integer velden zorgvuldig, converteer lege strings naar None
        percentage_voor = data.get('percentage_witte_haren_voor')
        klant.percentage_witte_haren_voor = int(percentage_voor) if percentage_voor else None

        percentage_achter = data.get('percentage_witte_haren_achter')
        klant.percentage_witte_haren_achter = int(percentage_achter) if percentage_achter else None
        
        klant.wens = data.get('wens', klant.wens)
        klant.color_formula = data.get('color_formula', klant.color_formula)
        klant.techniek = data.get('techniek', klant.techniek)
        klant.producten = data.get('producten', klant.producten)
        klant.inwerktijd = data.get('inwerktijd', klant.inwerktijd)
        
        # NIEUWE REGEL: Werk het 'laatste_rekening' veld bij
        klant.laatste_rekening = data.get('laatste_rekening', klant.laatste_rekening)

        # Sla de wijzigingen op in de database
        klant.save()

        # Stuur een succes-respons terug
        return JsonResponse({'success': True, 'message': 'Klant succesvol bijgewerkt!'})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        # Vang eventuele andere fouten op
        return JsonResponse({'success': False, 'message': str(e)}, status=500)





@login_required
def export_klanten_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="klanten_overzicht.xlsx"'

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Klanten Overzicht"

    # Defineer de headers voor je Excel-bestand
    headers = [
        "Voornaam", "Achternaam", "Email", "GSM", "Volledig Adres", "Allergieën",
        "Huid", "Behandeling Hiervoor", "Haartype", "Natuurlijke Haarkleur",
        "Toonhoogte Lengtes", "Weerschijn", "Percentage Witte Haren Voor",
        "Percentage Witte Haren Achter", "Wens", "Color Formula", "Techniek",
        "Producten", "Inwerktijd", "Laatste Rekening"
    ]
    sheet.append(headers)

    # Haal alle klanten op uit de database
    klanten = Klant.objects.all().order_by('achternaam', 'voornaam') # Sorteer eventueel

    for klant in klanten:
        row_data = [
            klant.voornaam,
            klant.achternaam,
            klant.email,
            klant.gsm,
            klant.volledig_adres,
            klant.allergieen,
            klant.huid,
            klant.behandeling_hiervoor,
            klant.haartype,
            klant.natuurlijke_haarkleur,
            klant.toonhoogte_lengtes,
            klant.weerschijn,
            klant.percentage_witte_haren_voor,
            klant.percentage_witte_haren_achter,
            klant.wens,
            klant.color_formula,
            klant.techniek,
            klant.producten,
            klant.inwerktijd,
            klant.laatste_rekening # Dit zal de JSON string zijn
        ]
        sheet.append(row_data)

    workbook.save(response)
    return response

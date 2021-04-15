#from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
import csv
import math
from .models import Operators
from pprint import pprint
from .forms import OperatorsForm
from .constants import OPERATORS, GENERATIONS, STATUT, S_OPERATORS
from django.contrib.gis.geos import fromstr, Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D


def index(request):
    telecoms = []
    form = OperatorsForm(request.POST)
    message = "Vous devez remplir au préalable le formulaire pour voir des résultats."

    if request.method == 'POST' and form.is_valid():
        telecoms = Operators.objects
        lat = request.POST.get("lat")
        longitude = request.POST.get("longitude")
        message = "Aucun résultat n'a été trouvé pour votre recherche"

        try:
            lat = float(lat)
            longitude = float(longitude)
        except:
            raise Exception("Veuillez saisir une adresse valide")   
        
        if request.POST.get("operators") != OPERATORS[0] and request.POST.get("operators") in OPERATORS:
            telecoms = telecoms.filter(adm_lb_nom=request.POST.get("operators"))

        if request.POST.get("generation") != GENERATIONS[0] and request.POST.get("generation") in GENERATIONS:
            telecoms = telecoms.filter(generation=request.POST.get("generation"))
        
        if request.POST.get("statut") != STATUT[0] and request.POST.get("statut") in STATUT:
            telecoms = telecoms.filter(statut=request.POST.get("statut"))
        
        if request.POST.get("sous_operator") != S_OPERATORS[0] and request.POST.get("sous_operator") in S_OPERATORS:
            telecoms = telecoms.filter(sous_operator=request.POST.get("sous_operator"))
        
        if request.POST.get("forfait"):
            try:
                telecoms = telecoms.filter(forfait__lte=float(request.POST.get("forfait")))
            except:
                raise Exception('Veuillez entrer un prix valide')   

        point = fromstr(f'POINT({longitude} {lat})', srid=4326)
        telecoms = telecoms.filter(location__dwithin=(point, distance_to_decimal_degrees(D(km=500), lat))).annotate(distance=Distance('location', point))
        
    return render(request, "index.html", {
        'telecoms': telecoms.order_by('distance')[:3],
        'form': form,
        'message': message
    })

def importation(request):
    with open("out.csv", encoding="utf8", errors='ignore') as f:
        reader = csv.reader(f)
        next(reader, None)
        
        for row in reader:
            ##id_zone=int(row[2]),
            try:
                obj, created = Operators.objects.get_or_create(
                    adm_lb_nom=row[2],
                    generation=row[3],
                    statut=row[4],
                    location=fromstr(f'POINT({row[5]} {row[6]})', srid=4326),
                    sous_operator=row[7],
                    image=row[8],
                    forfait=float(row[10]),
                    link=row[11],
                )
                obj.save()
            except:
                raise Exception("L'objet du model n'a pas pu être sauvegardé")

    return HttpResponse("Fin de l'importation")


def distance_to_decimal_degrees(distance, latitude):
    lat_radians = latitude * (math.pi / 180)
    return distance.m / (111_319.5 * math.cos(lat_radians))
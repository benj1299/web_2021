from comparator.models import Operators
from django.contrib.gis.geos import fromstr
import csv

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
                if created:
                    obj.save()
            except Exception as e:
                raise Exception("L'objet du model n'a pas pu être sauvegardé pour la raison : "+ str(e))
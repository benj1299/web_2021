from django.test import TestCase
from comparator.models import Operators
from django.contrib.gis.geos import fromstr
from django.test import Client
from django.contrib.gis.geos.point import Point
from comparator.forms import OperatorsForm

class OperatorsTestCase(TestCase):
    def setUp(self):
        Operators.objects.create(
            adm_lb_nom	= "SFR",
            generation	= "4G",
            statut	    = "En service",
            location = fromstr(f'POINT({48.346666666667} {2.323333333333})', srid=4326),
            sous_operator = "Prixtel",
            image = "https://cdn.shortpixel.ai/client/q_glossy,ret_img/https://lemon.fr/wp-content/uploads/2016/02/Red-by-sfr.png",
            forfait = 12.5,
            link = "https://lemon.fr/offres/red-60go/"
        )

    def test_operator_make_point(self):
        sfr = Operators.objects.get(adm_lb_nom="SFR")
        self.assertTrue(type(sfr.location) is Point)


    def test_form_validity(self):
        form = OperatorsForm(data={"operators": "SFR", "generation": "4G", 'sous_operator': 'Prixtel', "statut": "En Service", "forfait": 10})
        self.assertTrue(form.is_valid())
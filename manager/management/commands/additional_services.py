from django.core.management import BaseCommand

from manager.models import AdditionalService, AdditionalServiceCategory, AdditionalServiceSubcategory, Catalog


class Command(BaseCommand):

    def _create_furniture(self, catalog: 'Catalog') -> None:
        furniture = AdditionalServiceCategory.objects.create(name="Furniture")

        chairs = AdditionalServiceSubcategory.objects.create(category=furniture, name="Chairs")
        tables = AdditionalServiceSubcategory.objects.create(category=furniture, name="Tables")

        # Chairs
        AdditionalService.objects.create(
            catalog=catalog, subcategory=chairs, name="Metallic chair", price=5.0, taxes=0.1, status=True
        )
        AdditionalService.objects.create(
            catalog=catalog, subcategory=chairs, name="Wooden chair", price=5.0, taxes=0.1, status=True
        )
        AdditionalService.objects.create(
            catalog=catalog, subcategory=chairs, name="Office chair", price=10.0, taxes=0.1, status=True
        )

        # Tables
        AdditionalService.objects.create(
            catalog=catalog, subcategory=tables, name="Metallic table", price=10.0, taxes=0.1, status=True
        )
        AdditionalService.objects.create(
            catalog=catalog, subcategory=tables, name="Wooden table", price=15.0, taxes=0.1, status=True
        )
        AdditionalService.objects.create(
            catalog=catalog, subcategory=tables, name="Glass table", price=25.0, taxes=0.1, status=True
        )

    def _create_utilities(self, catalog: 'Catalog') -> None:
        utilities = AdditionalServiceCategory.objects.create(name="Utilities")

        water = AdditionalServiceSubcategory.objects.create(category=utilities, name="Water")
        internet = AdditionalServiceSubcategory.objects.create(category=utilities, name="Internet")
        electricity = AdditionalServiceSubcategory.objects.create(category=utilities, name="Electricity")

        # Water
        AdditionalService.objects.create(
            catalog=catalog, subcategory=water, name="500 Ml bottles", price=0.5, taxes=0.1, status=True
        )
        AdditionalService.objects.create(
            catalog=catalog, subcategory=water, name="1L bottles", price=1.0, taxes=0.1, status=True
        )
        AdditionalService.objects.create(
            catalog=catalog, subcategory=water, name="Dispenser w/ 10L", price=25.0, taxes=0.1, status=True
        )

        # Internet
        AdditionalService.objects.create(
            catalog=catalog, subcategory=internet, name="Wireless connection", price=10.0, taxes=0.21, status=True
        )
        AdditionalService.objects.create(
            catalog=catalog, subcategory=internet, name="Wired connection 50 Mbps", price=20.0, taxes=0.21, status=True
        )
        AdditionalService.objects.create(
            catalog=catalog, subcategory=internet, name="Wired connection 1 Gbps", price=50.0, taxes=0.21, status=True
        )
        AdditionalService.objects.create(
            catalog=catalog, subcategory=internet, name="Static IP", price=30.0, taxes=0.21, status=True
        )

        # Electricity
        AdditionalService.objects.create(
            catalog=catalog, subcategory=electricity, name="2 kW", price=10.0, taxes=0.1, status=True
        )
        AdditionalService.objects.create(
            catalog=catalog, subcategory=electricity, name="4 kW", price=18.0, taxes=0.1, status=True
        )
        AdditionalService.objects.create(
            catalog=catalog, subcategory=electricity, name="8 kW", price=35.0, taxes=0.1, status=True
        )

    def handle(self, *args, **options):
        catalog = Catalog.objects.create(name="Catalog")
        self._create_furniture(catalog)
        self._create_utilities(catalog)

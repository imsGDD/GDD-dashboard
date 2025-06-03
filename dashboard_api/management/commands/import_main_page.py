import json
from django.core.management.base import BaseCommand
from dashboard_api.models import Hero, HeroDetail, Progress, SecondaryProgress, LastUpdated, CardMain, CardDetail, CardDetailSecondary
from datetime import datetime


class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='JSON file containing data')

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']

        with open(filename, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        # Save last_updated
        last_updated_data = data['last_updated']
        last_updated_date = datetime.strptime(last_updated_data['date'], '%d/%m/%Y')
        last_updated_time = datetime.strptime(last_updated_data['time'], '%H:%M')
        last_updated_obj = LastUpdated.objects.create(date=last_updated_date, time=last_updated_time)

        # Save hero data
        for hero_data in data['hero']:
            hero_obj = Hero.objects.create(
                icon=hero_data['Icon'],
                number=hero_data['number'],
                text=hero_data['text'],
                textsm=hero_data['textsm']
            )

            # Save hero details
            for detail_data in hero_data.get('details', []):
                HeroDetail.objects.create(
                    hero=hero_obj,
                    icon=detail_data['Icon'],
                    number=detail_data['number'],
                    text=detail_data['text']
                )

        # Save progress data
        main_progress_data = data['progress']['main']
        Progress.objects.create(
            percentage=main_progress_data['percentage'],
            total=main_progress_data['total']
        )

        secondary_progress_data = data['progress']['secondary']
        for key, value in secondary_progress_data.items():
            SecondaryProgress.objects.create(
                progress=Progress.objects.first(),
                percentage=value['percentage'],
                total=value['total']
            )

        # Save cards data
        for card_data in data['cards']:
            card_main_obj = CardMain.objects.create(
                id=card_data['id'],
                title=card_data['title'],
                route=card_data['route']
            )

            # Save card details
            for detail_data in card_data['details']:
                card_detail_obj = CardDetail.objects.create(
                    card=card_main_obj,
                    main_icon=detail_data['main']['icon'],
                    main_text=detail_data['main']['text'],
                    main_subtext=detail_data['main']['subtext'],
                    main_number=detail_data['main']['number']
                )

                # Save card detail secondary
                for secondary_data in detail_data.get('secondary', []):
                    CardDetailSecondary.objects.create(
                        card_detail=card_detail_obj,  # Ensure card_detail_obj is saved before creating CardDetailSecondary
                        img=secondary_data['img'],
                        title=secondary_data['title'],
                        number=secondary_data['number'],
                        numberText=secondary_data['numberText']
                    )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))

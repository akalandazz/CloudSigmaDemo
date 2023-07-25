from wh.app import create_app
from wh.models import BeerModel
from datetime import datetime


if __name__ == '__main__':
    application = create_app()
    application.app_context().push()

    # Create some test data
    test_data = [
        # username, timestamp, text
        ('amiran', datetime(1962, 5, 11, 9, 53, 41),
         "Busch Light"),
        ('amiran', datetime(1962, 5, 11, 9, 58, 23),
         "Keystone"),
        ('stephen', datetime(1962, 5, 11, 19, 53, 41),
         "Miller64"),
        ('stephen', datetime(1962, 5, 11, 19, 58, 23),
         "Michelob Ultra"),
    ]
    for username, timestamp, text in test_data:
        beer = BeerModel(username=username, text=text, timestamp=timestamp)
        application.db.session.add(beer)

    application.db.session.commit()

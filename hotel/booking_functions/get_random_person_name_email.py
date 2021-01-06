import random
from django.conf import settings


def get_random_person_name_email():
    tlds = ['.com', '.net', '.co.uk', '.edu', '.tech', '.dev']
    with open(settings.BASE_DIR + "/hotel/booking_functions/text_lists/names.txt", "r") as f:
        data = f.read().lower().split(',')
        names = list(map(str.strip, data))
        name = random.choice(names)
        mail_domain = random.choice(names)
        tld = random.choice(tlds)
        separator = '@'
        email = name + separator + mail_domain + tld

        return(name, email)

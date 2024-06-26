import json
import random
from datetime import date, timedelta
import faker

fake = faker.Faker()

def generate_users(usernames_no=1000):
    usernames = set()

    while len(usernames) < usernames_no:
        usernames.add(fake.user_name())

    users = get_users(usernames)
    rough_data = get_data(users)

    data = []
    for datum in rough_data:
        for campaign in datum['campaigns']:
            campaign.update({
                'user': datum['user']
            })
            data.append(campaign)

    with open('data.json', 'w') as stream:
        stream.write(json.dumps(data))

def get_users(usernames):
    users = []
    for username in usernames:
        name, gender = get_random_name_and_gender()
        user = {
            'username': username,
            'name': name,
            'gender': gender,
            'email': fake.email(),
            'age': fake.random_int(min=18, max=90),
            'address': fake.address(),
        }
        users.append(user)
    return users

def get_random_name_and_gender():
    skew = .6
    male = random.random() > skew
    if male:
        return fake.name_male(), 'M'
    else:
        return fake.name_female(), 'F'

def get_data(users):
    data = []
    for user in users:
        campaigns = [get_campaign_data()
                     for _ in range(random.randint(2, 8))
                     ]
        data.append({
            'user': user,
            'campaigns': campaigns
        })
    return data

def get_campaign_data():
    name = get_campaign_name()
    budget = random.randint(10 ** 3, 10 ** 6)
    spent = random.randint(10 ** 2, budget)
    clicks = int(random.triangular(10 ** 2, 10 ** 5, 0.2 * 10 ** 5))
    impressions = int(random.gauss(0.5 * 10 ** 6, 2))
    return {
        'cmp_name': name,
        'cmp_bgt': budget,
        'cmp_spent': spent,
        'cmp_clicks': clicks,
        'cmp_impr': impressions
    }

def get_campaign_name():
    separator = '_'
    type_ = get_type()
    start, end = get_start_end_dates()
    age = get_age()
    gender = get_gender()
    currency = get_currency()
    return separator.join(
        (type_, start, end, age, gender, currency)
    )

def get_type():
    types = ['AKX', 'BYU', 'GRZ', 'KTR']
    return random.choice(types)

def get_start_end_dates():
    duration = random.randint(1, 2 * 365)
    offset = random.randint(-365, 365)
    start = date.today() - timedelta(days=offset)
    end = start + timedelta(days=duration)

    def _format_date(date_):
        return date_.strftime("%Y%m%d")

    return _format_date(start), _format_date(end)

def get_age():
    age = random.randint(20, 45)
    age -= age % 5
    diff = random.randint(5, 25)
    diff -= diff % 5
    return '{}-{}'.format(age, age + diff)

def get_gender():
    return random.choice(('M', 'F', 'B'))

def get_currency():
    return random.choice(('GBP', 'EUR', 'USD'))

if __name__ == "__main__":
    generate_users()

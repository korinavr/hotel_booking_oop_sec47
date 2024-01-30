import pandas as pd

df = pd.read_csv('hotels.csv', dtype={'id': str})
df_cards = pd.read_csv('cards.csv', dtype=str).to_dict(orient='records')
df_cards_secure = pd.read_csv('card_security.csv', dtype=str)


class Hotel:
    def __init__(self, hotel_ID):
        self.hotel_ID = hotel_ID
        self.name = df.loc[df['id'] == self.hotel_ID, 'name'].squeeze()

    def book(self):
        """Book a hotel by changing its availability into no"""
        df.loc[df['id'] == self.hotel_ID, 'available'] = 'no'
        df.to_csv('hotels.csv', index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df['id'] == self.hotel_ID, 'available'].squeeze()
        if availability == 'yes':
            return True
        else:
            return False


class ReservationTicket:

    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, cvc, holder):
        card_data = {'number': self.number, 'expiration': expiration,
                     'cvc': cvc, 'holder': holder}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_secure.loc[df_cards_secure['number']==self.number, 'password'].squeeze()
        if password == given_password:
            return True
        else:
            return False


print(df)
hotel_id = input('Enter the id of the hotel: ')
hotel = Hotel(hotel_id)

if hotel.available():
    credit_card = SecureCreditCard(number='1234567890123456')
    if credit_card.validate(expiration='12/26', cvc='123', holder='JOHN SMITH'):
        if credit_card.authenticate(given_password='mypass'):
            hotel.book()
            name = input('Enter your name: ')
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
        else:
            print('Authentication failed.')
    else:
        print('There was a problem with the payment')
else:
    print('Hotel is not available.')


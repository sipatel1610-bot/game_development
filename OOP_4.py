class Movie_Ticket:
    def __init__(self, movie_name, ticket_price, number_of_tickets):
        self.movie_name = movie_name
        self.ticket_price = ticket_price
        self.number_of_tickets = number_of_tickets
    def calculate_total(self):
        print(self.ticket_price * self.number_of_tickets)
    def display_booking(self):
        print("Movie_name:", self.movie_name)
        print("Ticket_price:", self.ticket_price)
        print("Number_of_tickets:", self.number_of_tickets)
Movie_Ticket_1 = Movie_Ticket("Project Hail Mary", 15, 2)
Movie_Ticket_2 = Movie_Ticket("Avengers", 20, 5)
Movie_Ticket_1.display_booking()
Movie_Ticket_1.calculate_total()
Movie_Ticket_2.display_booking()
Movie_Ticket_2.calculate_total()

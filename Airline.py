import os
import datetime


FLIGHTS_FILE = "flights.txt"
BOOKINGS_FILE = "bookings.txt"
REPORT_FILE = "report.txt"
CANCELLATION_FILE ="cancellations.txt"



class AirlineSystem:
    def __init__(self):
        self.flights = {}
        self.cancellations = []
        self.bookings = []


    def load_flights(self):
        """Load flight from flight.txt"""
        try:
            with open(FLIGHTS_FILE, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        flight_no, origin, destination, seats = parts
                        self.flights[flight_no] = {
                            "origin": origin,
                            "destination": destination,
                            "seats": int(seats)
                        }
            print("Flights loaded successfully!\n")
        except FileNotFoundError:
            print("No flights file found. Starting with empty data.\n")


    def display_flights(self):
        """Display all available flights"""
        if not self.flights:
            print("No flights available")
            return
        print("\nAvailable Flights:")
        print("Flight No.\tOrigin\t\tDestination\tAvailable Seats")
        print("-" * 60)
        for flight_no, details in self.flights.items():
            print(f"{flight_no}\t\t{details['origin']}\t\t{details['destination']}\t\t{details['seats']}")


    def book_ticket(self):
        """Book a ticket for a flight"""
        flight_no = input("Enter flight number: ").strip()
        if flight_no not in self.flights:
            print("Error: Invalid flight number")
            return
        if self.flights[flight_no]['seats'] <= 0:
            print("Error: No seats available on this flight")
            return
        

        
        
        self.flights[flight_no]['seats'] -= 1
        


        
        booking = {
            'flight_no': flight_no,
            'origin': self.flights[flight_no]['origin'],
            'destination': self.flights[flight_no]['destination'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.bookings.append(booking)



        
        self._save_booking(booking)
        print("Booking successful!")



    def cancel_ticket(self):
        """Cancel an existing booking"""
        if not self.bookings:
            print("No bookings to cancel")
            return
        
        print("\nYour Bookings:")
        for i, booking in enumerate(self.bookings, 1):
            print(f"{i}. Flight {booking['flight_no']}: {booking['origin']} to {booking['destination']} ({booking['timestamp']})")
            choice = int(input("Select booking to cancel (0 to cancel): "))
            if choice == 0:
                return
            if choice < 1 or choice > len(self.bookings):
                print("Invalid selection")
                return
            

            
            booking = self.bookings.pop(choice - 1)


            
            self.flights[booking['flight_no']]['seats'] += 1



            cancellation = {
                'flight_no': booking['flight_no'],
                'origin': booking['origin'],
                'destination': booking['destination'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.cancellations.append(cancellation)

        with open(CANCELLATIONS_FILE, "a") as file:
            file.write(f"{cancellation['flight_no']},{cancellation['origin']},{cancellation['destination']},{cancellation['time']}\n")

        print("Cancellation successful!\n")

    def generate_report(self):
        """Save report to file"""
        with open(REPORT_FILE, "w") as file:
            file.write("AIRLINE DAILY REPORT\n")
            file.write("======================\n")
            file.write(f"Generated: {datetime.now()}\n\n")

            file.write("FLIGHTS STATUS:\n")
            for fno, details in self.flights.items():
                file.write(f"{fno}: {details['origin']} -> {details['destination']} | Seats: {details['seats']}\n")

            file.write("\nBookings:\n")
            for b in self.bookings:
                file.write(f"{b['flight_no']} | {b['origin']} -> {b['destination']} | {b['time']}\n")

            file.write("\nCancellations:\n")
            for c in self.cancellations:
                file.write(f"{c['flight_no']} | {c['origin']} -> {c['destination']} | {c['time']}\n")

        print("Report generated!\n")



if __name__ == "__main__":
    system = AirlineSystem()
    system.load_flights()

    while True:
        print("\n--- Airline Reservation System ---")
        print("1. Show Flights")
        print("2. Book Ticket")
        print("3. Cancel Ticket")
        print("4. Generate Report")
        print("5. Exit")

        choice = input("Enter choice: ")
        if choice == "1":
            system.display_flights()
        elif choice == "2":
            system.book_ticket()
        elif choice == "3":
            system.cancel_ticket()
        elif choice == "4":
            system.generate_report()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
             print("Invalid choice. Try again.\n")


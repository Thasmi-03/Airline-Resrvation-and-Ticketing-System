import os
import datetime

# file definitions
FLIGHTS_FILE = "flights.txt"
BOOKINGS_FILE = "bookings.txt"
REPORT_FILE = "report.txt"
CANCELLATION_FILE ="cancellations.txt"


# data structures
class AirlineSystem:
    def __init__(self):
        self.flights = {}
        self.cancellations = []
        self.bookings = []


#file handling
    def load_flights(self, filename="flights.txt"):
        """Load flight data from file with error handling"""
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"{filename} not found")
            with open(filename, 'r') as file:
                content = file.read().strip()
                if not content:
                    raise ValueError("File is empty")
                lines = content.split('\n')
                for line in lines:
                    if line.strip():
                        try:
                            flight_no, origin, destination, seats = line.strip().split(',')
                            self.flights[flight_no] = {
                                'origin': origin,
                                'destination': destination,
                                'seats': int(seats)
                            }
                        except ValueError:
                            print(f"Warning: Invalid format in line: {line}")
                            continue
            print("Flight data loaded successfully!")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print("Starting with empty flight data")
        except Exception as e:
            print(f"Error loading flights: {e}")
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
        

        
        # Reduce available seats
        self.flights[flight_no]['seats'] -= 1
        


        # Create booking record
        booking = {
            'flight_no': flight_no,
            'origin': self.flights[flight_no]['origin'],
            'destination': self.flights[flight_no]['destination'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.bookings.append(booking)


        # Save to file
        self._save_booking(booking)
        print("Booking successful!")
    def cancel_ticket(self):
        """Cancel a booked ticket"""
        if not self.bookings:
            print("No bookings to cancel")
            return
        print("\nYour Bookings:")
        for i, booking in enumerate(self.bookings, 1):
            print(f"{i}. Flight {booking['flight_no']}: {booking['origin']} to {booking['destination']} ({booking['timestamp']})")
        try:
            choice = int(input("Select booking to cancel (0 to cancel): "))
            if choice == 0:
                return
            if choice < 1 or choice > len(self.bookings):
                print("Invalid selection")
                return
            

            # Get the booking to cancel
            booking = self.bookings.pop(choice - 1)


            # Increase available seats
            self.flights[booking['flight_no']]['seats'] += 1


            # Add to cancellations
            cancellation = {
                'flight_no': booking['flight_no'],
                'origin': booking['origin'],
                'destination': booking['destination'],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.cancellations.append(cancellation)


            # Save to file
            self._save_cancellation(cancellation)
            print("Cancellation successful!")
        except ValueError:
            print("Please enter a valid number")
    def _save_booking(self, booking):
        """Save booking to file"""
        try:
            with open("bookings.txt", "a") as file:
                file.write(f"{booking['flight_no']},{booking['origin']},{booking['destination']},{booking['timestamp']}\n")
        except Exception as e:
            print(f"Error saving booking: {e}")
    def _save_cancellation(self, cancellation):
        """Save cancellation to file"""
        try:
            with open("cancellations.txt", "a") as file:
                file.write(f"{cancellation['flight_no']},{cancellation['origin']},{cancellation['destination']},{cancellation['timestamp']}\n")
        except Exception as e:
            print(f"Error saving cancellation: {e}")
    def generate_report(self):
        """Generate daily report"""
        try:
            with open("report.txt", "w") as file:
                file.write("AIRLINE RESERVATION SYSTEM - DAILY REPORT\n")
                file.write("=" * 50 + "\n")
                file.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                file.write("FLIGHT STATUS:\n")
                file.write("-" * 30 + "\n")
                for flight_no, details in self.flights.items():
                    file.write(f"{flight_no}: {details['origin']} to {details['destination']} - {details['seats']} seats available\n")
                file.write("\nBOOKINGS TODAY:\n")
                file.write("-" * 30 + "\n")
                for booking in self.bookings:
                    file.write(f"Flight {booking['flight_no']}: {booking['origin']} to {booking['destination']} at {booking['timestamp']}\n")
                file.write("\nCANCELLATIONS TODAY:\n")
                file.write("-" * 30 + "\n")
                for cancellation in self.cancellations:
                    file.write(f"Flight {cancellation['flight_no']}: {cancellation['origin']} to {cancellation['destination']} at {cancellation['timestamp']}\n")
                file.write(f"\nSUMMARY:\n")
                file.write("-" * 30 + "\n")
                file.write(f"Total bookings: {len(self.bookings)}\n")
                file.write(f"Total cancellations: {len(self.cancellations)}\n")
                file.write(f"Net tickets booked: {len(self.bookings) - len(self.cancellations)}\n")
            print('Report generates successfully')

        except:  print("An exception occurred")

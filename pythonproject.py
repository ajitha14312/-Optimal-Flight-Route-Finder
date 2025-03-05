import heapq

# A simple class to represent a flight connection between two cities
class Flight:
    def __init__(self, departure, destination, duration, cost, layovers):
        self.departure = departure
        self.destination = destination
        self.duration = duration
        self.cost = cost
        self.layovers = layovers

    def __repr__(self):
        return f"{self.departure} -> {self.destination} | Duration: {self.duration}h, Cost: ${self.cost}, Layovers: {self.layovers}"

# Flight Network represented as a graph (City -> [Flight Connections])
flight_network = {
    "New York": [Flight("New York", "Los Angeles", 6, 300, 1), Flight("New York", "Chicago", 3, 150, 0)],
    "Los Angeles": [Flight("Los Angeles", "New York", 6, 300, 1), Flight("Los Angeles", "San Francisco", 1, 100, 0)],
    "Chicago": [Flight("Chicago", "New York", 3, 150, 0), Flight("Chicago", "San Francisco", 4, 200, 1)],
    "San Francisco": [Flight("San Francisco", "Los Angeles", 1, 100, 0), Flight("San Francisco", "Chicago", 4, 200, 1)],
}

# Dijkstra's Algorithm to find the shortest path (minimizing duration)
def dijkstra(start, end, flight_network, preference="duration"):
    # Priority queue for cities to explore: (cost, city, layovers)
    priority_queue = [(0, start, 0)]  # (cost, city, layovers)
    visited = {}  # To store the shortest path to each city
    visited[start] = (0, 0)  # (cost, layovers)

    while priority_queue:
        current_cost, current_city, current_layovers = heapq.heappop(priority_queue)

        if current_city == end:
            return current_cost, current_layovers

        for flight in flight_network.get(current_city, []):
            # Select the appropriate metric based on user preference
            if preference == "duration":
                new_cost = current_cost + flight.duration
                new_layovers = current_layovers + flight.layovers
            elif preference == "cost":
                new_cost = current_cost + flight.cost
                new_layovers = current_layovers + flight.layovers
            else:  # Default: optimize for layovers
                new_cost = current_cost + flight.duration
                new_layovers = current_layovers + flight.layovers

            if (flight.destination not in visited or 
                visited[flight.destination][0] > new_cost or
                visited[flight.destination][1] > new_layovers):
                visited[flight.destination] = (new_cost, new_layovers)
                heapq.heappush(priority_queue, (new_cost, flight.destination, new_layovers))

    return None  # If no path exists

# Function to handle user input and find optimal flight route
def find_optimal_route():
    print("Welcome to the Optimal Flight Route Finder!")
    
    start_city = input("Enter departure city: ")
    end_city = input("Enter destination city: ")
    preference = input("Enter preference (duration/cost/layovers): ").lower()
    
    if preference not in ["duration", "cost", "layovers"]:
        print("Invalid preference! Defaulting to 'duration'.")
        preference = "duration"

    result = dijkstra(start_city, end_city, flight_network, preference)
    
    if result:
        total_cost, total_layovers = result
        print(f"Optimal route found: Total Travel Time: {total_cost} hours, Layovers: {total_layovers}")
    else:
        print(f"No available route found from {start_city} to {end_city}.")

# Run the program
find_optimal_route()

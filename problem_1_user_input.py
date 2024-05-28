# This was a late submission to provide a solution that allows for user input, rather than hard coding the values as seen in problem_1.py. 

def prompt_for_number(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Please enter a valid number.")


class Package:
    def __init__(self, id, weight_in_kg, distance_in_km, discount_code):
        self.id = id
        self.weight_in_kg = weight_in_kg
        self.distance_in_km = distance_in_km
        self.discount_code = discount_code

    def validate_discount_code(self):
        discount_code_valid = False
        discount_percentage = 0

        if self.discount_code == "OFR001" and self.distance_in_km < 200 and 70 <= self.weight_in_kg <= 200:
            discount_code_valid = True
            discount_percentage = 0.1
        if self.discount_code == "OFR002" and 50 <= self.distance_in_km <= 150 and 100 <= self.weight_in_kg <= 250:
            discount_code_valid = True
            discount_percentage = 0.07
        if self.discount_code == "OFR003" and 50 <= self.distance_in_km <= 250 and 10 <= self.weight_in_kg <= 150:
            discount_code_valid = True
            discount_percentage = 0.05

        return discount_code_valid, discount_percentage

def create_packages(no_of_packages):
    packages = []
    for i in range(no_of_packages):
        id = input(f"Enter ID for package {i+1}: ")
        weight_in_kg = prompt_for_number(f"Enter weight in kg for package {id}: ")
        distance_in_km = prompt_for_number(f"Enter delivery distance in km for package {id}: ")
        discount_code = input(f"Enter discount code to be applied to package {id}: ")
        print(f"Package id: {id} created with weight of {weight_in_kg}kg and a distance of {distance_in_km}. Entered discount code: {discount_code}")
        packages.append(Package(id, weight_in_kg, distance_in_km, discount_code))
    return packages

def calculate_delivery_cost(base_delivery_cost, packages):
    for package in packages:
        delivery_cost = base_delivery_cost + (package.weight_in_kg * 10) + (package.distance_in_km * 5)
        discount_code_valid, discount_percentage = package.validate_discount_code()
        discount_applied = discount_percentage * delivery_cost if discount_code_valid else 0
        total_cost = delivery_cost - discount_applied
        print(f"{package.id} {discount_applied:.2f} {total_cost:.2f}")


base_delivery_cost = prompt_for_number("Enter base delivery cost: ")
no_of_packages = prompt_for_number("Enter number of packages: ")
packages = create_packages(no_of_packages)
calculate_delivery_cost(base_delivery_cost, packages)
from itertools import combinations
import math

no_of_vehicles = 2
max_speed = 70
max_carriable_weight = 200
no_of_packages = 5
base_delivery_cost = 100

class Package:
  def __init__(self, id, weight_in_kg, distance_in_km, discount_code):
    self.id = id
    self.weight_in_kg = weight_in_kg
    self.distance_in_km = distance_in_km
    self.discount_code = discount_code

  def __repr__(self):
        return f"Package(id={self.id}, weight={self.weight_in_kg}, distance={self.distance_in_km}, offer_code={self.discount_code})"

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

class Vehicle:
    def __init__(self, id, weight_limit):
        self.id = id
        self.weight_limit = weight_limit
        self.available_after = 0 


def calculate_delivery_return_time(distance, speed):
    return distance / speed * 2


def calculate_delivery_cost(package): 
    delivery_cost = base_delivery_cost + (package.weight_in_kg * 10) + (package.distance_in_km * 5)

    discount_code_valid, discount_percentage = package.validate_discount_code()
    if discount_code_valid == True:
      discount_applied = discount_percentage*delivery_cost
    else: 
      discount_applied = 0

    total_cost = delivery_cost - discount_applied

    return discount_applied, total_cost


def find_best_packages_combination(packages, max_carriable_weight):
  best_packages_combination = []
  best_amount_of_packages = len(best_packages_combination)
  best_weight = 0
  best_distance = 0

  for i in range(1, len(packages) + 1):
    for combination in combinations(packages, i):
      total_weight = sum(pkg.weight_in_kg for pkg in combination)
      delivery_distance = max(pkg.distance_in_km for pkg in combination)
      # if the total weight of the combination is under the weight limit, 
      # if the length of the combination array is the  highest, set it the packages to be the best combination
      # or if the length of the array is the same as other combinations, then check the total weight against other weights with same array length
      # if size and weight is the same, take preference on shortest delivery distance
      if total_weight <= max_carriable_weight:
        if len(combination) > best_amount_of_packages or \
          (len(combination) == len(best_packages_combination) and total_weight > best_weight) or \
          (len(combination) == best_amount_of_packages and total_weight == best_weight and delivery_distance < best_distance):
          best_packages_combination = combination
          best_amount_of_packages = len(combination)
          best_weight = total_weight
          delivery_distance = best_distance
          

  return best_packages_combination

def run_delivery(packages, vehicles, max_speed):
    package_deliveries = []

    while packages:
        # choose the vehicle with lowest available after, first batch of runs will start at 0
        available_vehicle = min(vehicles, key=lambda vehicle: vehicle.available_after)
        # call previous function
        best_combination = find_best_packages_combination(packages, available_vehicle.weight_limit)
        if not best_combination:
            break

        # calculate delivery time for each selected package
        for pkg in best_combination:
            # rounding to 2 decimal places
            package_delivery_time = math.floor((pkg.distance_in_km / max_speed)*100) / 100
            # to get output as intended, including cost/discount
            discount_applied, total_cost = calculate_delivery_cost(pkg)
            # record the packages being delivered and delivery time *taking into account the vehicle available after time for delivery*
            package_deliveries.append((pkg.id, discount_applied, total_cost, available_vehicle.available_after + package_delivery_time))

        # calculate van return route time, using longest distance from selected packages
        max_distance_delivered = max(pkg.distance_in_km for pkg in best_combination)
        travel_time = calculate_delivery_return_time(max_distance_delivered, max_speed)

        # update the available after time for the vehicles
        available_vehicle.available_after += travel_time

        # remaining packages are the packages that aren't in included in this iteration of the loop
        packages = [pkg for pkg in packages if pkg not in best_combination]

    return package_deliveries


vehicles = [Vehicle(1, 200), Vehicle(2, 200)]

packages_array = [
Package("PKG1", 50, 30, "OFR001"),
Package("PKG2", 75, 125, "OFR002"),
Package("PKG3", 175, 100, "OFR003"),
Package("PKG4", 110, 60, "OFR002"),
Package("PKG5", 155, 95, None),
  ]

delivered_packages = run_delivery(packages_array, vehicles, max_speed)

for delivery in delivered_packages:
    pkg_id, discount_applied, total_cost, actual_delivery_time = delivery

    print(f"Package {pkg_id} - Discount: {discount_applied}, Total cost: {total_cost}, Estimated delivery time: {actual_delivery_time:.2f} hours")



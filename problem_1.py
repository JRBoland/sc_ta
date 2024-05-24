base_delivery_cost = 100
no_of_packages = 3

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

packages_array = [
Package("PKG1", 5, 5, "OFR001"),
Package("PKG2", 15, 5, "OFR002"),
Package("PKG3", 10, 100, "OFR003"),
  ]

def calculate_delivery_cost(): 
  for package in packages_array:
    delivery_cost = base_delivery_cost + (package.weight_in_kg * 10) + (package.distance_in_km * 5)

    discount_code_valid, discount_percentage = package.validate_discount_code()
    if discount_code_valid == True:
      discount_applied = discount_percentage*delivery_cost
    else: 
      discount_applied = 0

    total_cost = delivery_cost - discount_applied

    print(package.id, discount_applied, total_cost)
 

calculate_delivery_cost()


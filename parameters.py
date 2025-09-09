from constants import *

# REACTOR
outer_ring_is_hydrogen_side = 0
# Sizes
# Lengthes
length = 5 # m
innerdiameter = 0.5 # m
outerdiameter = 2 # m
innerperimeter = pi*innerdiameter # m
outerperimeter = pi*outerdiameter # m
# Areas
innerarea = pi/4*innerdiameter**2 # m2
outerarea = pi/4*outerdiameter**2 - innerarea # m2
# Volumes
inV = innerarea * length # m3
outV = outerarea * length # m3
# Surfaces
inS = innerperimeter * length # m2
outS = outerperimeter * length + 2*(innerarea + outerarea)
# MASS CALCULATION
steeldensity = 7700     # kg/m3
steelheatcapacity = 460 # J/kg K
wallt = 0.01 # m
bigcylinderV = pi/4 * (outerdiameter+wallt)**2 * (length+2*wallt) # m3
smallcylinderV = pi/4 * outerdiameter**2 * length # m3
reactor_wall_volume = bigcylinderV - smallcylinderV # m3
steelmass = reactor_wall_volume * steeldensity # kg

catalystdensity = 350     # kg/m3
catalystheatcapacity = 460 # J/kg K
catalystmass = catalystdensity * outV;
if outer_ring_is_hydrogen_side:
  catalystmass = catalystdensity * inV
# ^- kg
totalheatcapacity = 2*(steelheatcapacity * steelmass
                +catalystheatcapacity * catalystmass) # J/K
def coolingpower(tempreature):
  return 5.67e-8 * (temperature-273.15-ambienttemperature)**4 * outS # J/s
# First reactor
V1 = outV
if outer_ring_is_hydrogen_side:
  V1 = inV
f1rate = 1.75
f2rate = 0.5
f3rate = 0.1
# H2 side
V1h = inV
if outer_ring_is_hydrogen_side:
  V1h = outV
#Membrane properties
#thickness1 = 0.0001
#area1 = inS
#ndiff1 = 0.5

# Second reactor
V2 = outV
if outer_ring_is_hydrogen_side:
  V2 = inV
s1rate = 0.5
s2rate = 1.75
s3rate = 0.1
# H2 side
V2h = inV
if outer_ring_is_hydrogen_side:
  V2h = outV
#Membrane properties
thickness = 0.0001
area = inS
ndiff = 1.0

# Gas transport coefficients
incellconductivity = 0.2
cell_zero_to_cell_one_conductivity = 0.9
cell_one_to_burncell_conductivity = 0.2
outcells_to_outlet_conductivity = 0.99
# Feed pressure
ch4inletpressure = 1000000
h2oinletpressure = 2000000
initialpressure = 1
# Temp coefficients
burnpercent = 0.75
overcoolingfactor = 1
burncellvolume = bigcylinderV * 10
# Simulation parameters
time_max = 1000
initial_step = 0.01
to_adapt = True
adapt_key = 'h2'
step_divisor = 4
print_threshold = 0
write_counter = 0
write_trigger = 10

traditionaltemperature = 800

# Empirical
k0 = {
  'k0': None,
  '1':    3.71e17,
  '2':    5.43056,
  '3':    0.28339,
  'eq1':  7.846e22,
  'eq2':  0.01412,
  'eq3':  1.11e21,
  'co':   8.23e-10,
  'h2':   6.12e-14,
  'ch4':  6.64e-9,
  'h2o':  177000,
  'diff': 2.9e-9,
 }
Ea = {
  'Ea': None,
  '1':    240100,
  '2':    67130,
  '3':    243900,
  'eq1':  220200,
  'eq2': -37720,
  'eq3':  182400,
  'co':  -70650,
  'h2':  -82900,
  'ch4': -38280,
  'h2o':  88680,
  'diff': 22175,
 }

# Temperature-dependent
##k = {}
##for key in k0:
##  k[key] = k0[key]*e**(-Ea[key]/RT())
def k(key, temperature):
  return k0[key]*e**(-Ea[key]/RT(temperature))

def give_parameters_dicts():
  consts = [
    "pi",
    "R",
    "e",
    "zero",
    "ambienttemperature",
    "ch4heat",
    "h2heat",
    "coheat",
    ]
  items = [
      "length",
      "innerdiameter",
      "outerdiameter",
      "innerperimeter",
      "outerperimeter",
      "innerarea",
      "outerarea",
      "inV",
      "outV",
      "inS",
      "outS",
      "steeldensity",
      "steelheatcapacity" ,
      "wallt",
      "bigcylinderV",
      "smallcylinderV",
      "reactor_wall_volume",
      "steelmass",
      "catalystdensity",
      "catalystheatcapacity",
      "catalystmass",
      "totalheatcapacity",
      "V1",
      "f1rate",
      "f2rate",
      "f3rate",
      "V1h",
      "V2",
      "s1rate",
      "s2rate",
      "s3rate",
      "V2h",
      "thickness",
      "area",
      "ndiff",
      "incellconductivity",
      "cell_zero_to_cell_one_conductivity",
      "cell_one_to_burncell_conductivity",
      "outcells_to_outlet_conductivity",
      "burnpercent",
      "burncellvolume",
      "overcoolingfactor",
      "ch4inletpressure",
      "h2oinletpressure",
      ]
  vals = {"Values": None}
  for item in items:
    vals[item] = eval(item)
  consts_d = {"Constants": None}
  for item in consts:
    consts_d[item] = eval(item)
  return vals, k0, Ea, consts_d, k2_H, k1_H, k0_H

def control_sum():
  temp = [97, 97]
  is_zeros = True
  items = give_parameters_dicts()[0]
  for key in items:
    if items[key] is None:
      continue
    value = int(items[key])
    if value == 0:
      value = int(items[key] * 10)
    temp[int(is_zeros)] = (temp[int(is_zeros)] + value) % 26 + 97
    is_zeros = not is_zeros
  return chr(temp[0]) + chr(temp[1])

if __name__ == '__main__':
  #print(give_parameters_dicts())
  print(control_sum())

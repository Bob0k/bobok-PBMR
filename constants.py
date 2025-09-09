### Constants ###

# Fundamental
pi = 3.14159265358979323846
R = 8.31446261815324
e = 2.71828182845904523536
zero = 1e-20

# Heat parameters
ambienttemperature = 24 # °C
ch4heat = 891510 # J/mol
h2heat  = 286130 # J/mol
coheat  = 285000 # J/mol
# Reaction enthalpies
k2_H = { 'k2_dH' : None,
  '1': -0.0260529194807972,
  '2': -0.0187287127364453,
  '3': 0.002791773,
  }
k1_H = { 'k1_dH' : None,
  '1': 58.97462847,
  '2': 68.75174809,
  '3': 87.43089161,
  }
k0_H = { 'k0_dH' : None,
  '1': 190840.476260997,
  '2': -60291.76631,
  '3': 138169.0258,
  }

# Initial conditions
time = 0

def RT(temperature):
  return R*temperature
def dH(key, temperature): # J/mol
  return (k2_H[key]*temperature**2
          +k1_H[key]*temperature
          +k0_H[key])

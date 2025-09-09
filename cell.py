from constants import *
from parameters import *

def rdiff(p1, p2, temperature): 
  return k('diff', temperature)*area*(p1**ndiff-p2**ndiff)/thickness

class Cell():
  def __init__(self,
               name = "",
               ch4in = zero,
               h2oin = zero,
               coin  = zero,
               co2in = zero,
               h2in  = zero,
               volume = 1,
               k1 = 1,
               k2 = 1,
               k3 = 1
               ):
    self.name = name
    self.volume = volume
    self.nu = {
      'ch4': ch4in,
      'h2o': h2oin,
      'co':  coin,
      'co2': co2in,
      'h2':  h2in,
     }
    self.k1 = k1
    self.k2 = k2
    self.k3 = k3
    self.neighbours = []
    self.neighbours_conductivity = []

  def add_neighbour(self, neighbour, conductivity = -1):
    self.neighbours.append(neighbour)
    self.neighbours_conductivity.append(conductivity)

  def give(self, step, temperature):
    for i, neighbour in enumerate(self.neighbours):
      if self.neighbours_conductivity[i] == -1:
        rdr = rdiff(self.p('h2', temperature),
                    neighbour.p('h2', temperature),
                    temperature
                    ) * step
        if (self.nu['h2'] - rdr > 0
            and neighbour.nu['h2'] + rdr > 0):
          self.nu['h2'] -= rdr
          neighbour.nu['h2'] += rdr
        else:
          neighbour.nu['h2'] += self.nu['h2'] - zero
          self.nu['h2'] = zero
      else:
        for key in neighbour.nu:
          rgr = (self.p(key, temperature)
                 - neighbour.p(key, temperature)
                 ) / 2.0 * (
                   self.neighbours_conductivity[i]
                   * (self.volume + neighbour.volume) / RT(temperature)
                   * step)
          if (self.nu[key] - rgr > 0
              and neighbour.nu[key] + rgr > 0):
            self.nu[key] -= rgr
            neighbour.nu[key] += rgr
          else:
            neighbour.nu[key] += self.nu[key] - zero
            self.nu[key] = zero

  def burn(self, percent = 1):
    dt = percent * (
      self.nu['ch4'] * ch4heat
      + self.nu['h2'] * h2heat
      + self.nu['co'] * coheat
      ) / totalheatcapacity
    self.nu['ch4'] *= (1 - percent)
    self.nu['h2']  *= (1 - percent)
    self.nu['co']  *= (1 - percent)
    return dt

  def c(self, key):
    if self.volume == -1:
      return 0
    return self.nu[key]/self.volume
  def p(self, key, temperature):
    return self.c(key)*RT(temperature)

  def DEN(self, temperature):
    return (1
            +k('ch4', temperature)*self.p('ch4', temperature)
            +k('co', temperature)*self.p('co', temperature)
            +k('h2', temperature)*self.p('h2', temperature)
            +k('h2o', temperature)*self.p('h2o', temperature)/self.p('h2', temperature)
            )

  def r1rate(self, temperature):
##    if self.p('h2') == 0:
##      return 0
    return (
      k('1', temperature)/(self.p('h2', temperature)**2.5)
      *(
        self.p('ch4', temperature)*self.p('h2o', temperature)
        -(self.p('h2', temperature)**3)*self.p('co', temperature)/k('eq1', temperature)
        )
      /(self.DEN(temperature)**2)
      )
  def r2rate(self, temperature):
##    if self.p('h2') == 0:
##      return 0
    return (
      k('2', temperature)/self.p('h2', temperature)
      *(
        self.p('co', temperature)*self.p('h2o', temperature)
        -self.p('h2', temperature)*self.p('co2', temperature)/k('eq2', temperature)
        )
      /self.DEN(temperature)**2
      )
  def r3rate(self, temperature):
##    if self.p('h2') == 0:
##      return 0
    return (
      k('3', temperature)/(self.p('h2', temperature)**3.5)
      *(
        self.p('ch4', temperature)*self.p('h2o', temperature)**2
        -(self.p('h2', temperature)**4)*self.p('co2', temperature)/k('eq3', temperature)
        )
      /(self.DEN(temperature)**2)
      )
  
  def react_rates(self, temperature):
    r1r = self.r1rate(temperature) * self.k1
    r2r = self.r2rate(temperature) * self.k2
    r3r = self.r3rate(temperature) * self.k3
    return r1r, r2r, r3r
  
  def react(self, step, temperature):
    r1r, r2r, r3r = self.react_rates(temperature)
    self.nu['ch4'] = max(zero, self.nu['ch4'] + step * (-r1r - r3r))
    self.nu['h2o'] = max(zero, self.nu['h2o'] + step * (-r1r - r2r - 2*r3r))
    self.nu['co']  = max(zero, self.nu['co']  + step * (r1r - r2r))
    self.nu['h2']  = max(zero, self.nu['h2']  + step * (3*r1r + r2r + 4*r3r))
    self.nu['co2'] = max(zero, self.nu['co2'] + step * (r2r + r3r))
    return r1r, r2r, r3r

  def react_nu_change(self, temperature):
    r1r, r2r, r3r = self.react_rates(temperature)
    return {
      'ch4': (-r1r - r3r),
      'h2o': (-r1r - r2r - 2*r3r),
      'co':  (r1r - r2r),
      'h2':  (3*r1r + r2r + 4*r3r),
      'co2': (r2r + r3r)
      }

  def get_step(self, temperature, key = 'ch4', divisor = 2):
    return abs(self.nu[key] / self.react_nu_change(temperature)[key]) / divisor

##def poly4(k0,k1,k2,k3,k4,x):
##  return (k0
##          +k1*x
##          +k2*x**2
##          +k3*x**3
##          +k4*x**4
##          )
##
##def poly3(k0,k1,k2,k3,x):
##  return poly4(k0,
##               k1,
##               k2,
##               k3,
##               0,
##               x)
##def mtanh(k1,k2,k3,k4,dx,y0,x):
##  return (e**(k1*(x-dx))-e**(k2*(x-dx)))/(e**(k3*(x-dx))+e**(k4*(x-dx)))

#!/usr/bin/env python
## \file   channels_analytic.py
## \author Seth R. Johnson
## \brief  Calculate analytic coefficients for Larsen--Trahan VHTR channel prob

from math import exp, cos, sin, pi
from numpy import arange, append
import scipy.integrate

################################################################################
class CoarseIntegrator(object):
    def __init__(self, n):
        self.n = n #number of integrating points

    def __call__(self, f, lower, upper):
        """Simulate a transport solution with product quadrature set
        by using a midpoint-rule integration."""
        delta = (upper - lower)
        x = arange(lower, upper, delta / self.n) + delta/(2*self.n)
        return sum( map(f, x) ) * delta / len(x)

def FineIntegrator(*args):
    "Call scipy's accurate numerical integration routine"
    return scipy.integrate.quad(*args)[0]

################################################################################

def f_product_factory( f, x, trig ):
    "Return a lambda function for the final integrand; trig=cos for Dxx"
    return (lambda theta: f(x, cos(theta)) * trig(theta)**2)

################################################################################
class ChannelDiffusionCalculator(object):
    """Class to calculate anisotropic diffusion cross sections for the channel
    problem"""

    def __init__(self):
        self.sigt0 = 0.01 # channel cross section
        self.sigt1 = 1.0  # rest of the medium's cross section

        self.w = 0.5 # channel half-width

        self.integrator = FineIntegrator

        self.precalculate()

    def precalculate(self):
        self.invdiff = (1 / self.sigt0 - 1 / self.sigt1)
        self.sigt1inv = 1/self.sigt1

    def f1_channel(self, x, mu):
        "f(x,\\theta) inside the channel for 0 \\le \\theta < \\pi/2"
        return self.sigt1inv + self.invdiff * (
                1 - exp( - self.sigt0 * (self.w + x) / mu ) )

    def f2_channel(self, x, mu):
        "f(x,\\theta) inside the channel for \\pi2 < \\theta \\le \\pi"
        return self.sigt1inv + self.invdiff * (
                1 - exp( self.sigt0 * (self.w - x) / mu ) )

    def f1_medium(self, x, mu):
        "f(x,\\theta) inside the medium for 0 \\le \\theta < \\pi/2"
        return self.sigt1inv + self.invdiff * (
                exp( self.sigt1 * (self.w - x) / mu ) ) * (
                1 - exp(-self.sigt0 * 2 * self.w / mu ) )

    def f2_medium(self, x, mu):
        "f(x,\\theta) inside the medium for 0 \\le \\theta < \\pi/2"
        return self.sigt1inv

    def _calc_D(self, f1, f2, x, trig):
        result = self.integrator( f_product_factory(f1, x, trig),
            0, pi/2)
        result2 = self.integrator( f_product_factory(f2, x, trig),
            pi/2, pi)
        return (result + result2) / pi

    def calc_Dxx(self, x):
        assert x >= 0
        if x < self.w:
            d = self._calc_D(self.f1_channel, self.f2_channel, x, cos)
        else:
            d = self._calc_D(self.f1_medium,  self.f2_medium,  x, cos)
        return d

    def calc_Dyy(self, x):
        assert x >= 0
        if x < self.w:
            d = self._calc_D(self.f1_channel, self.f2_channel, x, sin)
        else:
            d = self._calc_D(self.f1_medium,  self.f2_medium,  x, sin)
        return d

################################################################################
def plot_coefficients():
    "Plot the anisotropic diffusion coefficients as a function of x"
    c = ChannelDiffusionCalculator()
    cell_width = 0.125
    half_period = c.w + 5.0
    x = arange( 0.0, half_period, cell_width ) + cell_width/2
    dxx = map( c.calc_Dxx, x )
    dyy = map( c.calc_Dyy, x )
    print "D^{yy}(%f) = %f" % (x[0], dyy[0])

    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(x, dxx, 'k-', label="D^{xx}")
    plt.plot(x, dyy, 'r--', label="D^{yy}")
    plt.ylim(0.5, 2.5)
    plt.legend()
    plt.xlabel('Distance from channel centerline')
    plt.ylabel('Diffusion coefficient')

def calc_integrator_convergence():
    """Figure out how the analytic solutions for D_yy converge as our quadrature
    set gets better."""
    x = 0.125
    c = ChannelDiffusionCalculator()

    exact = c.calc_Dyy( x )
    logn = range(2,12)
    angles = [2 ** i for i in logn]
    values = []
    for n in angles:
        c.integrator = CoarseIntegrator( n )
        values.append( c.calc_Dyy( x ) )

    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(logn, values, 'k-')
    plt.plot((logn[0], logn[-1]), (exact, exact), 'b--')
    plt.ylim(1.2,2.4)
    plt.xlabel('log_2(number of angles per quadrant)')
    plt.ylabel('D_{yy} at x=%.f' % x)

def plot_theta_function():
    "Plot the integrand in the Dxx and Dyy calculation"
    x = 0.0
    c = ChannelDiffusionCalculator()

    theta1 = arange(0, pi/2, pi/1024) + pi/2048
    theta2 = arange(pi/2, pi, pi/1024) + pi/2048

    f1x = map( f_product_factory(c.f1_channel, x, cos), theta1)
    #f2x = map( f_product_factory(c.f2_channel, x, cos), theta2)

    f1y = map( f_product_factory(c.f1_channel, x, sin), theta1)
    #f2y = map( f_product_factory(c.f2_channel, x, sin), theta2)

    #theta = list(theta1) + list(theta2)
    import matplotlib.pyplot as plt
    plt.figure()
    plt.polar( theta1, f1x , 'k-' )#+ f2x
    plt.polar( theta1, f1y , 'r--')#+ f2y
    plt.yscale('log')
    plt.xlim(0, pi)

#******************************************************************************#
if __name__ == '__main__':
    plot_coefficients()
    calc_integrator_convergence()
    #plot_theta_function()

    raw_input("[ENTER] TO EXIT")

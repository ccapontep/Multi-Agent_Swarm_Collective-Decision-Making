#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: cdimidov
"""
import math
import numpy as np
import numpy.random as R


#define the uniform distribution
def uniform_distribution(a, b):
  return a + (b-a) * R.rand()

#define the expponential distribution
def exponential_distribution(l):
# https://github.com/ampl/gsl/blob/master/randist/exponential.c
  u=uniform_distribution(0.0,1.0)
  x=(-l)*np.log(1-u)
  return x

#define the wrapped cauchy distribution
def wrapped_cauchy_ppf (c):
  q = 0.5
  u = uniform_distribution(0.0,1.0)
  val = (1.0-c)/(1.0+c)
  theta = 2*atan(val*tan(np.pi*(u-q)))
  return theta

############################################################################
#The stable Levy probability distributions have the form
  # p(x) dx = (1/(2 np.pi)) \int dt exp(- it x - |c t|^alpha)
#   with 0 < alpha <= 2.
#   For alpha = 1, we get the Cauchy distribution
#   For alpha = 2, we get the Gaussian distribution with sigma = sqrt(2)c.
#############################################################################
#define levy distribution
def levy ( c, alpha):

  u = np.pi * (uniform_distribution(0.0,1.0) - 0.5) #see uniform distribution

# cauchy case
  if (alpha == 1):
      t = np.tan(u)
      return c * t
  while True:
      v = exponential_distribution (1.0) #see exponential distribution
      if not (v == 0):
         break

# gaussian case
  if (alpha == 2):
      # https://github.com/gpeyre/matlab-toolboxes/blob/master/toolbox_curve/gen_levy_flight.m
      # https://github.com/BrianGladman/gsl/blob/master/randist/levy.c
      t = 2 * np.sin(u) * np.sqrt(v)
      return  c * t

# general case
  t = np.sin(alpha * u) / pow(np.cos(u), 1 / alpha)
  s = pow(np.cos((1 - alpha) * u) / v, (1 - alpha) / alpha)
  return  c * t * s

##########################################################################################
#The stable Levy probability distributions have the form
#   2*np.pi* p(x) dx
#    = \int dt exp(mu*i*t-|sigma*t|^alpha*(1-i*beta*sign(t)*tan(np.pi*alpha/2))) for alpha!=1
#    = \int dt exp(mu*i*t-|sigma*t|^alpha*(1+i*beta*sign(t)*2/np.pi*log(|t|)))   for alpha==1
#   with 0<alpha<=2, -1<=beta<=1, sigma>0.
#   For beta=0, sigma=c, mu=0, we get gsl_ran_levy above
#   For alpha = 1, beta=0, we get the Lorentz distribution
#   For alpha = 2, beta=0, we get the Gaussian distribution
###########################################################################################
#define levy_skew distribution
def levy_skew ( c, alpha, beta):

  # symmetric case
  if (beta == 0):
     return levy (c, alpha)

  V = np.pi * (uniform_distribution(0.0,1.0) - 0.5)

  while True:
      W = exponential_distribution(1.0)
      if not (W == 0):
         break

  if (alpha == 1):
      X = ((np.pi/2) + beta * V) * np.tan(V) - beta * np.log((np.pi/2) * W * cos (V)/((np.pi/2) + beta * V))/(np.pi/2)
      return c * (X + beta * np.log(c)/(np.pi/2))

  else :

       t = beta * np.tan((np.pi/2) * alpha)
       B = atan(t) / alpha
       S = pow(1 + t * t, 1/(2 * alpha))

       X = S * np.sin(alpha * (V + B))/pow(np.cos(V), 1 / alpha) * pow(cos(V - alpha * (V + B))/W, (1 - alpha)/alpha)
       return c * X

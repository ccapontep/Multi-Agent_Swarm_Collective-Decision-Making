# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 16:41:29 2014

@author: vtrianni
"""

import os, math, random, sys, getopt, importlib, copy
import xml.etree.ElementTree as ET
import numpy as np

####################################################################
# Pysage 2D vector (http://www.pygame.org/wiki/2DVectorClass )
########################################################################
import operator

class Vec2d(object):
    """2d vector class, supports vector and scalar operators,
    and also provides a bunch of high level functions
    """
    __slots__ = ['x', 'y']
 
    def __init__(self, x_or_pair, y = None):
        if y == None:
            self.x = x_or_pair[0]
            self.y = x_or_pair[1]
        else:
            self.x = x_or_pair
            self.y = y
 
    def __len__(self):
        return 2
 
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
 
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec2d")
                
        
    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec2d(%s, %s)' % (self.x, self.y)
 
    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        else:
            return False
 
    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 2:
            return self.x != other[0] or self.y != other[1]
        else:
            return True
 
    def __nonzero__(self):
        return bool(self.x or self.y)
 
    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vec2d"
        if isinstance(other, Vec2d):
            return Vec2d(f(self.x, other.x),
                         f(self.y, other.y))
        elif (hasattr(other, "__getitem__")):
            return Vec2d(f(self.x, other[0]),
                         f(self.y, other[1]))
        else:
            return Vec2d(f(self.x, other),
                         f(self.y, other))
 
    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vec2d"
        if (hasattr(other, "__getitem__")):
            return Vec2d(f(other[0], self.x),
                         f(other[1], self.y))
        else:
            return Vec2d(f(other, self.x),
                         f(other, self.y))
 
    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
        return self
 
    # Addition
    def __add__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x + other.x, self.y + other.y)
        elif hasattr(other, "__getitem__"):
            return Vec2d(self.x + other[0], self.y + other[1])
        else:
            return Vec2d(self.x + other, self.y + other)
    __radd__ = __add__
 
    def __iadd__(self, other):
        if isinstance(other, Vec2d):
            self.x += other.x
            self.y += other.y
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
        else:
            self.x += other
            self.y += other
        return self
 
    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x - other.x, self.y - other.y)
        elif (hasattr(other, "__getitem__")):
            return Vec2d(self.x - other[0], self.y - other[1])
        else:
            return Vec2d(self.x - other, self.y - other)
    def __rsub__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(other.x - self.x, other.y - self.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(other[0] - self.x, other[1] - self.y)
        else:
            return Vec2d(other - self.x, other - self.y)
    def __isub__(self, other):
        if isinstance(other, Vec2d):
            self.x -= other.x
            self.y -= other.y
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
        else:
            self.x -= other
            self.y -= other
        return self
 
    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vec2d):
            return Vec2d(self.x*other.x, self.y*other.y)
        if (hasattr(other, "__getitem__")):
            return Vec2d(self.x*other[0], self.y*other[1])
        else:
            return Vec2d(self.x*other, self.y*other)
    __rmul__ = __mul__
 
    def __imul__(self, other):
        if isinstance(other, Vec2d):
            self.x *= other.x
            self.y *= other.y
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
        else:
            self.x *= other
            self.y *= other
        return self
 
    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        return self._io(other, operator.div)
 
    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)
 
    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)
 
    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)
 
    def __divmod__(self, other):
        return self._o2(other, operator.divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)
 
    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)
 
    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)
 
    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
 
    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__
 
    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__
 
    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__
 
    # Unary operations
    def __neg__(self):
        return Vec2d(operator.neg(self.x), operator.neg(self.y))
 
    def __pos__(self):
        return Vec2d(operator.pos(self.x), operator.pos(self.y))
 
    def __abs__(self):
        return Vec2d(abs(self.x), abs(self.y))
 
    def __invert__(self):
        return Vec2d(-self.x, -self.y)
 
    # vectory functions
    def get_length_sqrd(self):
        return self.x**2 + self.y**2
 
    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)
    def __setlength(self, value):
        length = self.get_length()
        self.x *= value/length
        self.y *= value/length
    length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")
 
    def rotate(self, angle_radians ):
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y
 
    def rotated(self, angle_radians):
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vec2d(x, y)
 
    def get_angle(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.atan2(self.y, self.x)
    def __setangle(self, angle_radians):
        self.x = self.length
        self.y = 0
        self.rotate(angle_radians)
    angle = property(get_angle, __setangle, None, "gets or sets the angle of a vector")
 
    def get_angle_between(self, other):
        cross = self.x*other[1] - self.y*other[0]
        dot = self.x*other[0] + self.y*other[1]
        return math.atan2(cross, dot)
 
    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return Vec2d(self)
 
    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
        return length
 
    def perpendicular(self):
        return Vec2d(-self.y, self.x)
 
    def perpendicular_normal(self):
        length = self.length
        if length != 0:
            return Vec2d(-self.y/length, self.x/length)
        return Vec2d(self)
 
    def dot(self, other):
        return float(self.x*other[0] + self.y*other[1])
 
    def get_distance(self, other):
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)
 
    def get_dist_sqrd(self, other):
        return (self.x - other[0])**2 + (self.y - other[1])**2
 
    def projection(self, other):
        other_length_sqrd = other[0]*other[0] + other[1]*other[1]
        projected_length_times_other_length = self.dot(other)
        return other*(projected_length_times_other_length/other_length_sqrd)

    def return_within_circle(self,other):
        O=Vec2d(other)
        A=self.__sub__(O)
        return O.__add__(other[0]*A.normalized())
 
    def cross(self, other):
        return self.x*other[1] - self.y*other[0]
 
    def interpolate_to(self, other, range):
        return Vec2d(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range)
 
    def convert_to_basis(self, x_vector, y_vector):
        return Vec2d(self.dot(x_vector)/x_vector.get_length_sqrd(), self.dot(y_vector)/y_vector.get_length_sqrd())
 
    def __getstate__(self):
        return [self.x, self.y]
 
    def __setstate__(self, dict):
        self.x, self.y = dict
 

####################################################################
# Pysage 3D vector (http://www.pygame.org/wiki/3DVectorClass)
########################################################################
 
class Vec3d(object):
    """3d vector class, supports vector and scalar operators,
        and also provides a bunch of high level functions.
        reproduced from the vec2d class on the pygame wiki site.
        """
    __slots__ = ['x', 'y', 'z']
 
    def __init__(self, x_or_triple, y = None, z = None):
        if y == None:
            self.x = x_or_triple[0]
            self.y = x_or_triple[1]
            self.z = x_or_triple[2]
        else:
            self.x = x_or_triple
            self.y = y
            self.z = z
 
    def __len__(self):
        return 3
 
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec3d")
 
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise IndexError("Invalid subscript "+str(key)+" to Vec3d")
 
    # String representaion (for debugging)
    def __repr__(self):
        return 'Vec3d(%s, %s, %s)' % (self.x, self.y, self.z)
    
    # Comparison
    def __eq__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 3:
            return self.x == other[0] and self.y == other[1] and self.z == other[2]
        else:
            return False
    
    def __ne__(self, other):
        if hasattr(other, "__getitem__") and len(other) == 3:
            return self.x != other[0] or self.y != other[1] or self.z != other[2]
        else:
            return True
 
    def __nonzero__(self):
        return self.x or self.y or self.z
 
    # Generic operator handlers
    def _o2(self, other, f):
        "Any two-operator operation where the left operand is a Vec3d"
        if isinstance(other, Vec3d):
            return Vec3d(f(self.x, other.x),
                         f(self.y, other.y),
                         f(self.z, other.z))
        elif (hasattr(other, "__getitem__")):
            return Vec3d(f(self.x, other[0]),
                         f(self.y, other[1]),
                         f(self.z, other[2]))
        else:
            return Vec3d(f(self.x, other),
                         f(self.y, other),
                         f(self.z, other))
 
    def _r_o2(self, other, f):
        "Any two-operator operation where the right operand is a Vec3d"
        if (hasattr(other, "__getitem__")):
            return Vec3d(f(other[0], self.x),
                         f(other[1], self.y),
                         f(other[2], self.z))
        else:
            return Vec3d(f(other, self.x),
                         f(other, self.y),
                         f(other, self.z))
 
    def _io(self, other, f):
        "inplace operator"
        if (hasattr(other, "__getitem__")):
            self.x = f(self.x, other[0])
            self.y = f(self.y, other[1])
            self.z = f(self.z, other[2])
        else:
            self.x = f(self.x, other)
            self.y = f(self.y, other)
            self.z = f(self.z, other)
        return self
 
    # Addition
    def __add__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x + other.x, self.y + other.y, self.z + other.z)
        elif hasattr(other, "__getitem__"):
            return Vec3d(self.x + other[0], self.y + other[1], self.z + other[2])
        else:
            return Vec3d(self.x + other, self.y + other, self.z + other)
    __radd__ = __add__
    
    def __iadd__(self, other):
        if isinstance(other, Vec3d):
            self.x += other.x
            self.y += other.y
            self.z += other.z
        elif hasattr(other, "__getitem__"):
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]
        else:
            self.x += other
            self.y += other
            self.z += other
        return self
 
    # Subtraction
    def __sub__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x - other.x, self.y - other.y, self.z - other.z)
        elif (hasattr(other, "__getitem__")):
            return Vec3d(self.x - other[0], self.y - other[1], self.z - other[2])
        else:
            return Vec3d(self.x - other, self.y - other, self.z - other)
    def __rsub__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(other.x - self.x, other.y - self.y, other.z - self.z)
        if (hasattr(other, "__getitem__")):
            return Vec3d(other[0] - self.x, other[1] - self.y, other[2] - self.z)
        else:
            return Vec3d(other - self.x, other - self.y, other - self.z)
    def __isub__(self, other):
        if isinstance(other, Vec3d):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        elif (hasattr(other, "__getitem__")):
            self.x -= other[0]
            self.y -= other[1]
            self.z -= other[2]
        else:
            self.x -= other
            self.y -= other
            self.z -= other
        return self
 
    # Multiplication
    def __mul__(self, other):
        if isinstance(other, Vec3d):
            return Vec3d(self.x*other.x, self.y*other.y, self.z*other.z)
        if (hasattr(other, "__getitem__")):
            return Vec3d(self.x*other[0], self.y*other[1], self.z*other[2])
        else:
            return Vec3d(self.x*other, self.y*other, self.z*other)
    __rmul__ = __mul__
    
    def __imul__(self, other):
        if isinstance(other, Vec3d):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.z
        elif (hasattr(other, "__getitem__")):
            self.x *= other[0]
            self.y *= other[1]
            self.z *= other[2]
        else:
            self.x *= other
            self.y *= other
            self.z *= other
        return self
 
    # Division
    def __div__(self, other):
        return self._o2(other, operator.div)
    def __rdiv__(self, other):
        return self._r_o2(other, operator.div)
    def __idiv__(self, other):
        return self._io(other, operator.div)
 
    def __floordiv__(self, other):
        return self._o2(other, operator.floordiv)
    def __rfloordiv__(self, other):
        return self._r_o2(other, operator.floordiv)
    def __ifloordiv__(self, other):
        return self._io(other, operator.floordiv)
 
    def __truediv__(self, other):
        return self._o2(other, operator.truediv)
    def __rtruediv__(self, other):
        return self._r_o2(other, operator.truediv)
    def __itruediv__(self, other):
        return self._io(other, operator.floordiv)
 
    # Modulo
    def __mod__(self, other):
        return self._o2(other, operator.mod)
    def __rmod__(self, other):
        return self._r_o2(other, operator.mod)
 
    def __divmod__(self, other):
        return self._o2(other, operator.divmod)
    def __rdivmod__(self, other):
        return self._r_o2(other, operator.divmod)
 
    # Exponentation
    def __pow__(self, other):
        return self._o2(other, operator.pow)
    def __rpow__(self, other):
        return self._r_o2(other, operator.pow)
 
    # Bitwise operators
    def __lshift__(self, other):
        return self._o2(other, operator.lshift)
    def __rlshift__(self, other):
        return self._r_o2(other, operator.lshift)
 
    def __rshift__(self, other):
        return self._o2(other, operator.rshift)
    def __rrshift__(self, other):
        return self._r_o2(other, operator.rshift)
 
    def __and__(self, other):
        return self._o2(other, operator.and_)
    __rand__ = __and__
 
    def __or__(self, other):
        return self._o2(other, operator.or_)
    __ror__ = __or__
 
    def __xor__(self, other):
        return self._o2(other, operator.xor)
    __rxor__ = __xor__
 
    # Unary operations
    def __neg__(self):
        return Vec3d(operator.neg(self.x), operator.neg(self.y), operator.neg(self.z))
 
    def __pos__(self):
        return Vec3d(operator.pos(self.x), operator.pos(self.y), operator.pos(self.z))
 
    def __abs__(self):
        return Vec3d(abs(self.x), abs(self.y), abs(self.z))
 
    def __invert__(self):
        return Vec3d(-self.x, -self.y, -self.z)
 
    # vectory functions
    def get_length_sqrd(self): 
        return self.x**2 + self.y**2 + self.z**2
 
    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)      
    def __setlength(self, value):
        length = self.get_length()
        self.x *= value/length
        self.y *= value/length
        self.z *= value/length
    length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")
        
    def rotate_around_z(self, angle_radians):
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        self.x = x
        self.y = y
 
    def rotate_around_x(self, angle_radians):
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        y = self.y*cos - self.z*sin
        z = self.y*sin + self.z*cos
        self.y = y
        self.z = z
 
    def rotate_around_y(self, angle_radians):
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        z = self.z*cos - self.x*sin
        x = self.z*sin + self.x*cos
        self.z = z
        self.x = x
 
    def rotated_around_z(self, angle_radians):
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        x = self.x*cos - self.y*sin
        y = self.x*sin + self.y*cos
        return Vec3d(x, y, self.z)
    
    def rotated_around_x(self, angle_radians):
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        y = self.y*cos - self.z*sin
        z = self.y*sin + self.z*cos
        return Vec3d(self.x, y, z)
    
    def rotated_around_y(self, angle_radians):
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        z = self.z*cos - self.x*sin
        x = self.z*sin + self.x*cos
        return Vec3d(x, self.y, z)
    
    def get_angle_around_z(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.atan2(self.y, self.x)
    def __setangle_around_z(self, angle_radians):
        self.x = math.sqrt(self.x**2 + self.y**2)
        self.y = 0
        self.rotate_around_z(angle_radians)
    angle_around_z = property(get_angle_around_z, __setangle_around_z, None, "gets or sets the angle of a vector in the XY plane")
 
    def get_angle_around_x(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.atan2(self.z, self.y)
    def __setangle_around_x(self, angle_radians):
        self.y = math.sqrt(self.y**2 + self.z**2)
        self.z = 0
        self.rotate_around_x(angle_radians)
    angle_around_x = property(get_angle_around_x, __setangle_around_x, None, "gets or sets the angle of a vector in the YZ plane")
 
    def get_angle_around_y(self):
        if (self.get_length_sqrd() == 0):
            return 0
        return math.atan2(self.x, self.z)
    def __setangle_around_y(self, angle_radians):
        self.z = math.sqrt(self.z**2 + self.x**2)
        self.x = 0
        self.rotate_around_y(angle_radians)
    angle_around_y = property(get_angle_around_y, __setangle_around_y, None, "gets or sets the angle of a vector in the ZX plane")
 
    def get_angle_between(self, other):
        v1 = self.normalized()
        v2 = Vec3d(other)
        v2.normalize_return_length()
        return math.acos(v1.dot(v2))
            
    def normalized(self):
        length = self.length
        if length != 0:
            return self/length
        return Vec3d(self)
 
    def normalize_return_length(self):
        length = self.length
        if length != 0:
            self.x /= length
            self.y /= length
            self.z /= length
        return length
 
    def dot(self, other):
        return float(self.x*other[0] + self.y*other[1] + self.z*other[2])
        
    def get_distance(self, other):
        return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2 + (self.z - other[2])**2)
        
    def get_dist_sqrd(self, other):
        return (self.x - other[0])**2 + (self.y - other[1])**2 + (self.z - other[2])**2
        
    def projection(self, other):
        other_length_sqrd = other[0]*other[0] + other[1]*other[1] + other[2]*other[2]
        projected_length_times_other_length = self.dot(other)
        return other*(projected_length_times_other_length/other_length_sqrd)
    
    def cross(self, other):
        return Vec3d(self.y*other[2] - self.z*other[1], self.z*other[0] - self.x*other[2], self.x*other[1] - self.y*other[0])
    
    def interpolate_to(self, other, range):
        return Vec3d(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range, self.z + (other[2] - self.z)*range)
    
    def convert_to_basis(self, x_vector, y_vector, z_vector):
        return Vec3d(self.dot(x_vector)/x_vector.get_length_sqrd(),
            self.dot(y_vector)/y_vector.get_length_sqrd(),
            self.dot(z_vector)/z_vector.get_length_sqrd())
 
    def __getstate__(self):
        return [self.x, self.y, self.z]
        
    def __setstate__(self, dict):
        self.x, self.y, self.z = dict



########################################################################################
## Pysage Agent
########################################################################################

##########################################################################
# factory to dynamically create agents
class AgentFactory:
    factories = {}
    def add_factory(id, agent_factory):
        AgentFactory.factories[id] = agent_factory
    add_factory = staticmethod(add_factory)

    def create_agent(config_element, arena):
        agent_pkg = config_element.attrib.get("pkg")
        if agent_pkg is None:
            return Agent.Factory().create(config_element, arena)
        id = agent_pkg + ".agent"
        agent_type = config_element.attrib.get("type")
        if agent_type is not None:
            id = agent_pkg + "." + agent_type + ".agent"
        return AgentFactory.factories[id].create(config_element, arena)
    create_agent = staticmethod(create_agent)


##########################################################################
# the main agent class
class Agent:
    'Definition of an agent in 2D space'
    num_agents = 0
    size       = 0.01
    mass       = 0.01
    arena      = None

    class Factory:
        def create(self, config_element, arena): return Agent(config_element, arena)


    ##########################################################################
    # Initialisation of the Agent class    
    def __init__(self, config_element, arena):
        
        # identification
        self.id = Agent.num_agents
        
        # reference to the arena
        Agent.arena = arena

        # position in meters
        self.prev_pos = Vec2d(0,0)
        self.position = Vec2d(0,0)
        
        # velocity in m/s - initialise with a null value 
        self.prev_vel = Vec2d(0,0)
        self.velocity = Vec2d(0,0)

        # desired movements after control loop
        self.apply_force = 0.0
        self.apply_velocity = 0.0
        self.apply_movement = Vec2d(0,0)
        self.apply_sa = {"step" : 0, "angle" : 0}
        
        # store initial positions and velocity for reset
        self.init_pos = copy.deepcopy(self.position)
        self.init_vel = copy.deepcopy(self.velocity)
        
        # parse custon parameters from configuration file
        Agent.mass = 0.01 if config_element.attrib.get("mass") is None else float(config_element.attrib["mass"])
        Agent.size = 0.02 if config_element.attrib.get("size") is None else float(config_element.attrib["size"])
        Agent.num_agents += 1

        # flag to check if an agent is selected from the GUI
        self.selected = False


    ##########################################################################
    # String representaion (for debugging)
    def __repr__(self):
        return 'Agent %d(%s, %s)' % ( self.id, self.position.x, self.position.y)

    ##########################################################################
    # compute the desired motion and the next state of the agent
    def control(self):
        neighbours = Agent.arena.get_neighbour_agents(self, 0.1)
        random_motion = Vec2d(0.1,0)
        random_motion.rotate(self.velocity.get_angle() + random.gauss(0,0.1))
        self.apply_velocity = self.velocity + random_motion
        for a in neighbours:
            self.apply_velocity += 0.1*a.velocity
        self.apply_velocity = self.apply_velocity.normalized()*0.1

    ##########################################################################
    # generic init function brings back to initial positions
    def init_experiment( self ):
        self.position = copy.deepcopy(self.init_pos)
        self.velocity = copy.deepcopy(self.init_vel)

    ##########################################################################
    # generic update function to be overloaded by subclasses 
    def update( self ):
        self.prev_pos = copy.deepcopy(self.position)
        self.prev_vel = copy.deepcopy(self.velocity)
        self.update_velocity()
        
    ##########################################################################
    # Update the position and velocity of an agent according to an applied force
    def update_force( self ):
        self.velocity += self.apply_force*Agent.arena.timestep_length/Agent.mass;
        self.position += self.velocity*Agent.arena.timestep_length

    ##########################################################################
    # Update the position and velocity according to a desired velocity
    def update_velocity( self):
        self.velocity = self.apply_velocity
        self.position += self.velocity*Agent.arena.timestep_length

    ##########################################################################
    # Update the position and velocity according to a position variation
    def update_position( self ):
        self.velocity  = self.apply_movement/Agent.arena.timestep_length
        self.position += self.apply_movement

    ##########################################################################
     # Update the position and velocity according to a linear step and subseqent rotation
    def update_step_angle( self ):
        pos_step = Vec2d(self.apply_sa["step"], 0)
        pos_step.rotate(self.apply_sa["angle"]+self.velocity.angle)
        self.velocity = pos_step/Agent.arena.timestep_length
        self.position += pos_step

    ##########################################################################
    # set the selected flag to 'status'
    def set_selected_flag( self, status ):
        self.selected = status



########################################################################################
## Pysage arena
########################################################################################

##########################################################################
# factory to dynamically create the arena
class ArenaFactory:
    factories = {}
    def add_factory(id, arena_factory):
        ArenaFactory.factories[id] = arena_factory
    add_factory = staticmethod(add_factory)

    def create_arena(config_element):
        arena_pkg = config_element.attrib.get("pkg")
        if arena_pkg is None:
            return Arena.Factory().create(config_element)#, arena)
        id = arena_pkg + ".arena"
        arena_type = config_element.attrib.get("type")
        if arena_type is not None:
            id = arena_pkg + "." + arena_type + ".arena"
        return ArenaFactory.factories[id].create(config_element)
    create_arena = staticmethod(create_arena)


##########################################################################
# main arena class
class Arena:    
    'this class manages the enviroment of the multi-agent simualtion'
    
    class Factory:
        def create(self, config_element): return Arena(config_element)

    ##########################################################################
    # standart class init
    def __init__( self, config_element ):

        # random seed
        self.random_seed = None if config_element.attrib.get("random_seed") is None else int(config_element.attrib["random_seed"])
        
        # arena size
        ssize = config_element.attrib.get("size");
        if ssize is None:
            print ("[ERROR] missing attribute 'size' in tag <arena>")
            sys.exit(2)
        self.dimensions = Vec2d( map(float, ssize.split(',')) )
            
        # number of agents to initialize
        if config_element.attrib.get("num_agents") is None:
            print ("[ERROR] missing attribute 'num_agents' in tag <arena>")
            sys.exit(2)
        self.num_agents = int(config_element.attrib["num_agents"])

        # number of runs to execute 
        self.num_runs = 1 if config_element.attrib.get("num_runs") is None else int(config_element.attrib["num_runs"])
        self.run_id = 0
        
        # current simulation step and max number of simulation steps - 0 means no limits
        self.num_steps = 0
        self.max_steps = 0 if config_element.attrib.get("max_steps") is None else int(config_element.attrib["max_steps"])

        # length of a simulation step (in seconds)
        self.timestep_length = 0.1 if config_element.attrib.get("timestep_length") is None else float(config_element.attrib["timestep_length"])

        self.agents = []
        self.create_agents(config_element)

    ##########################################################################
    # create the agents
    def create_agents( self, config_element ):
        # Get the node correspnding to agent parameters
        agent_config= config_element.find('agent')
        if agent_config is None:
            print ("[ERROR] required tag <agent> in configuration file is missing")
            sys.exit(2)

        # dynamically load the desired module
        lib_pkg    = agent_config.attrib.get("pkg")
        if lib_pkg is not None:
            importlib.import_module(lib_pkg + ".agent", lib_pkg)

        for i in range(0,self.num_agents):
            self.agents.append(AgentFactory.create_agent(agent_config, self))

            
    ##########################################################################
    # set the random seed
    def set_random_seed( self, seed = None ):
        if seed is not None:
            random.seed(seed)
        elif self.random_seed is not 0:
            random.seed(self.random_seed)
        else:
            random.seed()

            
    ##########################################################################
    # initialisation/reset of the experiment variables
    def init_experiment( self ):
        self.num_steps = 0
        for agent in self.agents:
            agent.init_experiment()
            agent.position = Vec2d(random.uniform(0,self.dimensions.x),random.uniform(0,self.dimensions.y))
            agent.velocity = Vec2d(0.1,0)
            agent.velocity.rotate(random.uniform(-math.pi,math.pi))
            
    ##########################################################################
    # run experiment unitl finished
    def run_experiment( self ):
        while not self.experiment_finished():
            self.update()


    ##########################################################################
    # updates the simulation state
    def update( self ):
        # first, call the control() function for each agent, 
        # which computes the desired motion and the next agent state
        for a in self.agents:
            a.control()
            
        # then, apply the desired motion and update the agent state
        for a in self.agents:
            a.update()
            a.position = a.position % self.dimensions # Implement the periodic boundary conditions
            #### CODE FOR A BOUNDED ARENA
            ## if a.position.x < 0:
            ##     a.position.x = 0
            ## elif a.position.x > self.dimensions.x:
            ##     a.position.x = self.dimensions.x 

            ## if a.position.y < 0:
            ##     a.position.y = 0
            ## elif a.position.y > self.dimensions.y:
            ##     a.position.y = self.dimensions.y

        self.num_steps += 1

        
    ##########################################################################
    # determines if an exeperiment is finished
    def experiment_finished( self ):
        return (self.max_steps > 0) and (self.max_steps <= self.num_steps)


    ##########################################################################
    # save results to file, if any
    def save_results( self ):
        return None

    
    ##########################################################################
    # return a list of neighbours
    def get_neighbour_agents( self, agent, distance_range ):
        neighbour_list = []
        for a in self.agents:
            if (a is not agent) and (self.distance_on_torus(a.position,agent.position) < distance_range):
                neighbour_list.append(a)
        return neighbour_list
        
        
    ##########################################################################
    # returns the minimum distance calucalted on the torus given by periodic boundary conditions
    def distance_on_torus( self, pos_1, pos_2 ):
        return math.sqrt(min(abs(pos_1.x - pos_2.x), self.dimensions.x - abs(pos_1.x - pos_2.x))**2 + 
                    min(abs(pos_1.y - pos_2.y), self.dimensions.y - abs(pos_1.y - pos_2.y))**2)

    ##########################################################################
    # returns the minimum length vector from pos_2 to pos_1 calucalted on the torus given by periodic boundary conditions
    def direction_on_torus(self, pos_1, pos_2):
        dir = pos_1 - pos_2
        if abs(pos_1.x - pos_2.x) > self.dimensions.x - abs(pos_1.x - pos_2.x):
            dir.x += self.dimensions.x if pos_1.x < pos_2.x else -self.dimensions.x
        if abs(pos_1.y - pos_2.y) > self.dimensions.y - abs(pos_1.y - pos_2.y):
            dir.y += self.dimensions.y if pos_1.y < pos_2.y else -self.dimensions.y
        return dir



########################################################################################
## Pysage GUI
########################################################################################

##########################################################################
# factory to dynamically create the gui
class GUIFactory:
    factories = {}
    def add_factory(id, gui_factory):
        GUIFactory.factories[id] = gui_factory
    add_factory = staticmethod(add_factory)

    def create_gui(master, arena, config_element):
        gui_pkg = config_element.attrib.get("pkg")
        if gui_pkg is None:
            return PysageGUI.Factory().create(master, arena, config_element)
        id = gui_pkg + ".gui"
        gui_type = config_element.attrib.get("type")
        if gui_type is not None:
            id = gui_pkg + "." + gui_type + ".gui"
        return GUIFactory.factories[id].create(master, arena, config_element)
    create_gui = staticmethod(create_gui)


##########################################################################
# GUI main class
class PysageGUI(object):
    
    class Factory:
        def create(self, master, arena, config_element): return PysageGUI(master, arena, config_element)

    ##########################################################################
    # standart class init
    def __init__(self, master, arena, config_element):
        self.master = master

        self.delay  = 1.0 if config_element.attrib.get("delay")  is None else float(config_element.attrib["delay"])
        self.pixels_per_meter = 250 if config_element.attrib.get("pixels_per_meter")  is None else int(config_element.attrib["pixels_per_meter"])

        # Initialize the arena and the agents
        self.arena = arena
        self.agents_id = [0]*self.arena.num_agents;
        self.arena.set_random_seed()
        self.arena.init_experiment()

        # start the GUI
        self.timestep = 0
        self.timestring = tk.StringVar()
        self.timestring.set(str(self.timestep))
        self.initialize()

        # Draw the arena
        self.draw_arena(True)
        
        # initialise running state
        self.isRunning = False


    ##########################################################################
    # GUI step function: advance the simulation by one time step
    def step(self):
        if not self.arena.experiment_finished():
            self.arena.update()
            self.draw_arena()
            self.timestring.set( str(self.arena.num_steps) )
            self.master.update_idletasks()
        else:
            self.draw_arena()
            self.stop()


    ##########################################################################
    # GUI run helper function
    def run_( self ):
        if self.isRunning:
            self.step()
            ms = int(10.0 * max(self.delay, 1.0))

            self.master.after(ms, self.run_)

    ##########################################################################
    # GUI run function: advance the simulation
    def run(self):
        if not self.isRunning:
            self.step_button.config(state="disabled")
            self.run_button.config(state="disabled")
            self.reset_button.config(state="disabled")
            self.isRunning = True
            self.run_()

    ##########################################################################
    # GUI stop function: stops the simulation
    def stop(self):
        self.isRunning = False
        self.timestring.set( str(self.timestep) )
        self.step_button.config(state="normal")
        self.run_button.config(state="normal")
        self.reset_button.config(state="normal")
        self.timestring.set( str(self.arena.num_steps) )
        self.master.update_idletasks()

    ##########################################################################
    # GUI reset function: reset the simulation
    def reset(self):
        self.arena.init_experiment()
        self.draw_arena(True)
        self.timestring.set( str(self.arena.num_steps) )
        self.master.update_idletasks()

    ##########################################################################
    # GUI intialize function: stup the tk environemt
    def initialize(self):
        self.toolbar = tk.Frame(self.master, relief='raised', bd=2)
        self.toolbar.pack(side='top', fill='x')

        self.step_button = tk.Button(self.toolbar, text="Step", command=self.step)
        self.run_button = tk.Button(self.toolbar, text="Run", command=self.run)
        self.stop_button = tk.Button(self.toolbar, text="Stop", command=self.stop)
        self.reset_button = tk.Button(self.toolbar, text="Reset", command=self.reset)
        self.step_button.pack(side='left')
        self.stop_button.pack(side='left')
        self.run_button.pack(side='left')
        self.reset_button.pack(side='left')
        self.scale = tk.Scale(self.toolbar, orient='h', from_=1, to=10, resolution=0.5, command=lambda d: setattr(self, 'delay', float(d)))
        self.scale.set(self.delay)
        self.scale.pack(side='left')

        self.label = tk.Label(self.toolbar, textvariable = self.timestring)
        self.label.pack(side='right')

        print ("Canvas size", self.pixels_per_meter*self.arena.dimensions)
        self.w = tk.Canvas(self.master, width=int(self.pixels_per_meter*self.arena.dimensions.x), height=int(self.pixels_per_meter*self.arena.dimensions.y), background="#EEE")
        self.w.pack()

        for a in self.arena.agents:
            xpos = int(a.position.x*self.pixels_per_meter)
            ypos = int(a.position.y*self.pixels_per_meter)
            agent_halfsize = int(Agent.size*self.pixels_per_meter/2)
            agent_tag = "agent_%d" % a.id
            self.agents_id[a.id] = self.w.create_oval((xpos-agent_halfsize,ypos-agent_halfsize,xpos+agent_halfsize,ypos+agent_halfsize), fill="blue", tags=(agent_tag))
            self.w.tag_bind(agent_tag, "<ButtonPress-1>", lambda event, agent_tag = agent_tag: self.agent_selected(event, agent_tag))


    ##########################################################################
    # GUI draw function: standard draw of the arena and of the agent
    def draw_arena(self, init=False):
        self.w.bind("<Button-1>", self.unselect_agent)
        for a in self.arena.agents:
            xpos = int(a.position.x*self.pixels_per_meter)
            ypos = int(a.position.y*self.pixels_per_meter)
            agent_halfsize = int(Agent.size*self.pixels_per_meter/2)
            self.w.coords(self.agents_id[a.id], (xpos-agent_halfsize,ypos-agent_halfsize,xpos+agent_halfsize,ypos+agent_halfsize))
        
    ##########################################################################
    # de-select an agent that was previously selected by a click
    def unselect_agent( self, event ):
        if not event.widget.find_withtag(tk.CURRENT):
            self.w.itemconfigure('selected',fill="blue")
            self.w.dtag('all','selected')
            for agent in self.arena.agents:
                agent.set_selected_flag(False)
        self.master.update_idletasks()
            
    ##########################################################################
    # select an agent through a mouse click
    def agent_selected( self, event, agent_tag ):
        self.w.itemconfigure('selected',fill="blue")
        self.w.dtag('all','selected')
        self.w.addtag('selected','withtag',agent_tag)
        self.w.itemconfigure('selected',fill="red")
        self.master.update_idletasks()
        a_str, a_id = agent_tag.split("_")
        self.arena.agents[int(a_id)].set_selected_flag(True)





########################################################################################
## Pysage main functions
########################################################################################


def print_usage(errcode = None):
    print 'Usage: run_pysage -c <config_file> [-g]'
    sys.exit(errcode)

def start(argv):
    configfile = ''
    try:
        opts, args = getopt.getopt(argv,"hgc:",["config="])
    except getopt.GetoptError:
        print '[FATAL] Error in parsing command line arguments'
        print_usage(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
        elif opt in ("-c", "--config"):
            configfile = arg

    if len(configfile)==0:
        print '[FATAL] missing configuration file'
        print_usage(2)
        
    print 'Reading configuration file "%s"' % configfile

    sys.path.insert(0, os.getcwd())
    
    # parse configuration file    run
    tree = ET.parse(configfile)   
    
    # get the node for the arena configuration
    arena_config = tree.getroot().find('arena')
    if arena_config is None:
        print "[ERROR] required tag <arena> in configuration file is missing"
        sys.exit(2)
        
    # dynamically load the library
    lib_pkg = arena_config.attrib.get("pkg")
    if lib_pkg is not None:
        importlib.import_module(".arena",lib_pkg)
        
    arena = ArenaFactory.create_arena(arena_config)

    gui_config = tree.getroot().find('gui')
    if gui_config is not None:
        global tk
        import Tkinter as tk
        print 'Graphical user interface is on'
        root = tk.Tk()
        root.lift()
        root.call('wm', 'attributes', '.', '-topmost', True)
        root.after_idle(root.call, 'wm', 'attributes', '.', '-topmost', False)

        # dynamically load the library
        lib_pkg    = gui_config.attrib.get("pkg")
        if lib_pkg is not None:
            importlib.import_module(lib_pkg + ".gui", lib_pkg)
        
        GUIFactory.create_gui(root, arena, gui_config )
        root.mainloop()
    else:
        num_runs = 0
        while num_runs < arena.num_runs:
            num_runs += 1
            arena.run_id = num_runs
            if arena.random_seed is None:
                arena.set_random_seed()
            else:
                arena.run_id += arena.random_seed
                arena.set_random_seed(arena.run_id)
            arena.init_experiment()
            arena.run_experiment()
        arena.save_results()
        #where this resoult are saved??? 





if __name__ == "__main__":
    start(sys.argv[1:])
    
#sys.argv is the list of commandline arguments passed to the Python program
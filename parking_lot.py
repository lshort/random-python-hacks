"""A parking lot, ported from C++"""
import math
from enum import Enum

""""
  This code is organized in bottom up fashion: first the math
  utilities, then the distance class ('dist'), then the classes 'car'
  and 'parking_space' , then finally the 'parking_lot' class
"""


#  First, some functions to compare IEEE double precision numbers
#

#MAX_DBL_SIG_FIG = numeric_limits<double>::digits - 1;
max_sig_fig = 6

def FloatEqual(a, b, sig_figs = max_sig_fig):
    """Compares two IEEE floating values for equality, to some # of s.f."""
    exponent = -min( max_sig_fig, sig_figs )
    allowable_delta = a * math.pow(10.0, exponent)
    return abs(a-b) < allowable_delta

def FloatGreater(a, b, sig_figs = max_sig_fig):
    """Compares two IEEE floating values out to some # of sig figs"""
    return (a>b) and not FloatEqual(a,b)

class Distance:
    """Denotes a distance, tagged with units of measurement"""
    Units = Enum('DistanceUnits','CM INCH FOOT METER YARD')
    units = None;
    distance = None;
    def __init__(self, d_units, d_value):
        self.units = d_units
        self.distance = d_value
    def get_dist(self, unit_requested):
        return self.distance*conversion(units_requested,self.units)
    def set_dist(self,new_units,new_distance):
        self.units = new_units
        self.distance = new_distance
    def conversion(fr, to):
        return conversions[fr]/conversions[to];
    def is_greater(a, b):
        return FloatGreater( a.get_dist(Units.CM), b.get_dist(Units.CM))
    foot = 2.54*12.0
    yard = foot*3.0
    conversions = {Units.CM:1.0, Units.INCH:2.54, Units.FOOT:foot, \
                   Units.METER:100.0, Units.YARD:yard}

class Car:
    """Represents a car, within the context of a parking lot"""
    width = None
    length = None
    height = None
    license_plate = None
    def __init__(self, w, l, h, lic):
        self.width = w
        self.length = l
        self.height = h
        self.license_plate = lic


class ParkingSpace:
    """Represents a single uncovered parking space"""
    width = None
    length = None
    row = None
    number = None
    occupant = None
    def __init__(self, w, l, r, no):
        self.width = w
        self.length = l
        self.row = r
        self.number = no
        self.occupant = None


class ParkingLot:
    """Represents a single level parking lot (no height restrictions)"""
    spaces_by_row = {}
    license_plate_dict = {}
    available_spaces = []
    def add_to_row( self, width, length, row, first, count ):
        row_spaces = self.spaces_by_row[row]
        for x in range (first, first+count):
            row_spaces[x] = ParkingSpace(width, length, row, x)
            self.available_spaces.append(row_spaces[x])
    def add_space( self, width, length, row, number ):
        self.add_to_row(width, length, row, number, 1)
    def park_car( car ):
        for index in range(len(self.available_spaces)):
            space = self.available_spaces[index]
            if is_greater(space.width, car.width) and \
               is_greater(space.length, car.length):
                space.occupant = car
                self.license_plate_map[car.license_plate] = space
                del self.available_spaces[index]
                return (str(space.row) + "-" + str(space.number))
    def remove_car( license ):
        if license in self.license_plate_map.keys():
            space = self.license_plate_map[license]
            space.occupant = None
            del self.license_plate_map[license]
            self.available_spaces.append(space)
    def find_car( license ) :
        if license in self.license_plate_map.keys():
            return self.license_plate_map[license]
        else:
            return None
    def find_occupant( row, number ) :
        return self.spaces_by_row[row][number]
    def printable_string():
        retval = "Parking Lot Report\n"
        for row in self.spaces_by_row.keys():
            retval += "*Row " + row + "\n"
            for space in self.spaces_by_row[row]:
                retval += "   " + str(space) + " : " + str(space.occupant) + "\n"



if __name__ == "__main__":
    p = ParkingLot()
    w1 = Distance(Distance.Units.METER, 2.45)
    w2 = Distance(Distance.Units.METER, 2.6)
    w3 = Distance(Distance.Units.METER, 2.7)
    l1 = Distance(Distance.Units.FOOT, 17.0)
    l2 = Distance(Distance.Units.FOOT, 19.0)
    l3 = Distance(Distance.Units.FOOT, 21.0)
    c1 =  Car(w1, l2, w1, "PINOTNV" );
    c2 =  Car(w3, l2, w1, "133ABD" );
    c3 =  Car(w1, l1, w1, "166ABC" );
    c4 =  Car(w1, l2, w1, "CU LTR" );

    p.add_space( w1, l1, 'A', 1 );
    p.add_space( w1, l1, 'A', 2 );
    p.add_to_row( w2, l2, 'B', 1, 4 );
    p.add_to_row( w3, l3, 'C', 11, 4 );

    print( p.park_car(c1) )
    print( p.park_car(c2) )
    print( p.park_car(c3) )
    print( p.park_car(c4) )

    print( p.printable_string())
    p.remove_car( "PINOTNV" );
    print( p.printable_string())

    p.find_car("CU LTR");
    p.find_occupant('C',12);

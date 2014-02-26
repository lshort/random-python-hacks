"""Some graph algorithms, ported from C++"""
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
    def __init__(self, units, value):
        self.units = units
        self.distance = value
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
      Units.METER:100.0, Units.YARD:yd}
    units;
    distance;

class Car:
    """Represents a car, within the context of a parking lot"""
    def __init__(self, w, l, h, lic):
        self.width = w
        self.length = l
        self.height = h
        self.license_plate = lic
    width
    length
    height
    license_plate


class ParkingSpace:
    """Represents a single uncovered parking space"""
    def __init__(self, w, l, r, no):
        self.width = w
        self.length = l
        self.row = r
        self.number = no
        self.occupant = None
    width
    length
    row
    number
    occupant


class ParkingLot:
    """Represents a single level parking lot (no height restrictions)"""
    def add_to_row( width, length, row, first, count ):
        row_spaces = spaces_by_row[row]
        for x in range (first, first+count):
            row_spaces[x] = ParkingSpace(width, length, row, x)
            available_spaces.append(row_spaces[x])
    def add_space( width, length, row, number ):
        add_to_row(width, length, row, number, 1)
    def park_car( car ):
        for index in range(len(available_spaces)):
            space = available_spaces[index]
            if is_greater(space.width, car.width) and \
               is_greater(space.length, car.length):
                space.occupant = car
                license_plate_map[car.license_plate] = space
                del available_spaces[index]
                print "Parking in " + space.row + " " + str(space.number) + "\n"
    def remove_car( license ):
        if license in license_plate_map.keys():
            space = license_plate_map[license]
            space.occupant = None
            del license_plate_map[license]
            available_spaces.append(space)
    def find_car( license ) :
        if license in license_plate_map.keys():
            return license_plate_map[license]
        else
            return None
    def find_occupant( row, number ) :
        return spaces_by_row[row][number]
    def printable_string():
        retval = "Parking Lot Report\n"
        for row in spaces_by_row.keys():
            retval += "*Row " + row + "\n"
            for space in spaces_by_row[row]:
                retval += "   " + str(space) + " : " + str(space.occupant) + "\n"
    spaces_by_row = {{}}
    license_plate_dict = {}
    available_spaces = []



if __name__ == "__main__":
    p = ParkingLot()
    w1 = Distance(Distance.Units.METER, 2.45)
    w2 = Distance(Distance.Units.METER, 2.6)
    w3 = Distance(Distance.Units.METER, 2.7)
    l1 = Distance(Distance.Units.FOOT, 17.0)
    l2 = Distance(Distance.Units.FOOT, 19.0)
    l3 = Distance(Distance.Units.FOOT, 21.0)
    c1 =  Car(w1, l2, w1, string("PINOTNV") );
    c2 =  Car(w3, l2, w1, string("133ABD") );
    c3 =  Car(w1, l1, w1, string("166ABC") );
    c4 =  Car(w1, l2, w1, string("CU LTR") );

    p.add_space( w1, l1, 'A', 1 );
    p.add_space( w1, l1, 'A', 2 );
    p.add_to_row( w2, l2, 'B', 1, 4 );
    p.add_to_row( w3, l3, 'C', 11, 4 );


    p.park_car(c1)
    p.park_car(c2)
    p.park_car(c3)
    p.park_car(c4)

    print printable_string(p)
    p.remove_car( "PINOTNV" );
    print printable_string(p)

    p.find_car("CU LTR");
    p.find_occupant('C',12);
}

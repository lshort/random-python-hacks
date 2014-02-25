"""Some graph algorithms, ported from C++"""
import math
from enum import Enum


//  This code is organized in bottom up fashion: first the math
//  utilities, then the distance class ('dist'), then the classes 'car'
//  and 'parking_space' , then finally the 'parking_lot' class



//  First, some functions to compare IEEE double precision numbers
//

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
    Units = Enum('DistanceUnits','CM INCH FOOT METER YARD)
    def __init__(self, units, value):
        self.units = units
        self.distance = value
    def get_dist(self, unit_requested):
        return self.distance*conversion(units_requested,self.units)
    def set_dist(self,new_units,new_distance):
        self.units = new_units
        self.distance = new_distance
    def conversion(from, to):
        return conversions[from]/conversions[to];
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
    width
    length
    height
    license_plate
    def __init__(self, w, l, h, lic):
        self.width = w
        self.length = l
        self.height = h
        self.license_plac = lic


class ParkingSpace:
    """Represents a single uncovered parking space"""
#    width
#    length
#    row
#    number
#    occupant
    def __init__(self, w, l, r, no):
        self.width = w
        self.length = l
        self.row = r
        self.number = no
        self.occupant = None


///  instances represent a single-level parking lot
///
class ParkingLot:


class parking_lot {
public:
  parking_lot() {};
  parking_lot(const parking_lot &orig);   // make a deep copy
  parking_lot(const parking_lot &&orig) ;
  friend void swap( parking_lot& first, parking_lot& second );
  parking_lot &operator = (parking_lot orig);
  void add_space( const dist &w, const dist &l,
                  const char row, const unsigned int no );
  void add_to_row( const dist &w, const dist &l, const char row,   // add multiple
                   const unsigned int first, const unsigned int count ); // spaces
  bool park_car( const car &veh );
  bool remove_car( const string &license );
  optional<parking_space> find_car( const string &license ) const;
  optional<car> find_occupant( char row, unsigned int no ) const;
  void print_report(ostream &out) const;
private:
  // stores all the parking spaces in a single row
  typedef map<char, vector<parking_space>> row_data;
  row_data spaces_by_row;
  // parking_space_ref allows us to efficiently point to entries in
  // the vector of row_data.  we can't use a direct pointer to the
  // individual parking_spaces, the vector could be reallocated and
  // moved  and then the individual pointers would be invalid
  typedef pair<vector<parking_space>*,int> parking_space_ref;
  unordered_map<string, parking_space_ref>  license_plate_map;
  deque<parking_space_ref> available_spaces;
  static parking_space &get_space( const parking_space_ref &r )
    { return  (*get<0>(r))[get<1>(r)]; };
  parking_space_ref copy_ref( const parking_space_ref &r );
};

/**  Print out the argument to the specified ostream
     @param[in] p The parking_space to print */
ostream & operator << (ostream & out, const parking_lot &p ) {
  p.print_report(out);
  return out;
}


/** A function to swap two parking_lot objects
    @param[in,out] first The first parking_lot to swap
    @param[in,out] second The second parking lot to swap */
void swap( parking_lot& first, parking_lot& second ) {
  std::swap( first.spaces_by_row, second.spaces_by_row );
  std::swap( first.license_plate_map, second.license_plate_map );
  std::swap( first.available_spaces, second.available_spaces );
}

/** The move constructor
    @param[in] orig The parking_lot which is assigned from */
parking_lot::parking_lot(const parking_lot &&orig) {
  spaces_by_row     = move(orig.spaces_by_row);
  license_plate_map = move(orig.license_plate_map);
  available_spaces  = move(orig.available_spaces);
}

/** The parameter 'r' points to a parking_space_ref in a different
    parking_lot.  We build and return a parking_space_ref in our own
    parking_lot that points to the parking_space that has the same
    row and number as 'r' points to.  Needed for the copy constructor.
    @param[in] r The reference that we are copying
    @return The reference that we have built  */
parking_lot::parking_space_ref parking_lot::copy_ref( const parking_space_ref &r ) {
  vector<parking_space> *oldvec = get<0>(r);
  int index = get<1>(r);
  parking_space &space = (*oldvec)[index];
  vector<parking_space> *newvec = &spaces_by_row[space.row];
  return make_pair( newvec, index );
}

/** The copy constructor, makes a deep copy
    @param[in] orig The parking_lot which is assigned from */
parking_lot::parking_lot(const parking_lot &orig) {
  // get our own copy of the map and vectors of data it contains
  spaces_by_row = orig.spaces_by_row;
  for ( auto &entry : orig.license_plate_map )  {
    parking_space_ref spaceref = get<1>(entry);
    license_plate_map[get<0>(entry)] = copy_ref( spaceref );
  }
  for ( auto &spaceref : orig.available_spaces ) {
    available_spaces.push_back(copy_ref(spaceref));
  }
}

/** The assignment operator
    @param[in] orig The parking_lot which is assigned from
    @return Returns the value to be assigned */
parking_lot &parking_lot::operator = (parking_lot orig) {
  swap(*this, orig);
  return *this;
}

/** Adds a single space to the row
    @param[in] w The width of the parking space
    @param[in] l The length of the parking space
    @param[in] row The row's identifying letter
    @param[in] no The number of the parking space */
void parking_lot::add_space(const dist &w, const dist &l, char row, unsigned int no )
{
  add_to_row( w, l, row, no, 1 );
}

/** Adds several parking spaces to the row, numbering them sequentially
    @param[in] w The width of the parking spaces
    @param[in] l The length of the parking spaces
    @param[in] row The row's identifying letter
    @param[in] first The number of the first parking space
    @param[in] count The number of parking spaces to add   */
void parking_lot::add_to_row(const dist &w, const dist &l, char row,
                             unsigned int first, unsigned int count )
{
  auto mypair = spaces_by_row.find(row);
  if ( spaces_by_row.end() == mypair )  {
    spaces_by_row[row] = vector<parking_space>();
    mypair = spaces_by_row.find(row);
  }
  vector<parking_space> &vec = get<1>(*mypair);
  for (unsigned int i=first; i<first+count; ++i)  {
    vec.push_back( parking_space{ w, l, row, i, no_car } );
    available_spaces.push_back( make_pair(&vec,vec.size()-1) );
  }
}

/** Parks the car in an appropriately sized parking space
    @param[in] veh The car
    @return Returns false if no space was available, true otherwise */
bool parking_lot::park_car( const car &veh )
{
  dist  l = veh.length;
  dist  w = veh.width;
  auto spaceref = find_if( available_spaces.begin(), available_spaces.end(),
             [&l,&w, this] (parking_space_ref ref)  {
             parking_space &p = get_space(ref);
             return (   is_greater(p.length,l)
                     && is_greater(p.width,w)  ); });
  if ( available_spaces.end() != spaceref ) {
    auto &space = get_space( *spaceref );
    space.occupant = optional<car>(veh);
    license_plate_map[veh.license_plate] = *spaceref;
    available_spaces.erase(spaceref);
    return true;
  } else {
    return false;
  }
}

/** Removes the car with the specified license plate
    @param[in] license The license plate to search for
    @return Returns true if it found a matching car, false otherwise */
bool parking_lot::remove_car( const string &license )
{
  auto entry = license_plate_map.find(license);
  if ( entry == license_plate_map.end() )  {
    return false;
  }
  parking_space &space = get_space(get<1>(*entry));
  space.occupant = no_car;
  license_plate_map.erase(license);
  available_spaces.push_back(get<1>(*entry));
  return true;
}

/** Prints a report
    @param[in] out The stream to print the report to */
void parking_lot::print_report(ostream &out) const
{
  out << endl << endl << "Parking Lot Report" << endl;
  for ( auto &mypair : spaces_by_row ) {
    out << "  Row " << get<0>(mypair) << endl;
    for ( auto &space : get<1>(mypair) )  {
      out << "    Space " << space.number << " : ";
      if ( !space.occupant )  {
        out << "empty" << endl;
      }  else  {
        out << space.occupant.get().license_plate << endl;
      }
    }
  }
  out << endl;
}

/**  Find the car the occupies a specific parking space
     @param[in] row  The row of the parking space
     @param[in] no   The number of the parking space
     @return If not found -- the empty object
     @return If found -- the car data */
optional<car> parking_lot::find_occupant( char row, unsigned int no ) const
{
  auto mypair = spaces_by_row.find(row);
  if ( spaces_by_row.end() != mypair )  {
    const vector<parking_space> &vec = get<1>(*mypair);
    for (auto &space : vec)
      if ( space.number == no )
        return space.occupant;
  }
  return no_car;
}

/**  Find a car with the specified license plate
     @param [in] license The license plate to find
     @return If not found -- the empty object
     @return If found -- the parking space data */
optional<parking_space> parking_lot::find_car( const string &license ) const {
  try {
    const parking_space_ref &ref = license_plate_map.at(license);
    vector<parking_space> *vec = get<0>(ref);
    int index = get<1>(ref);
    return optional<parking_space>((*vec)[index]);
  } catch (const std::out_of_range & out) {
    return optional<parking_space>();
  }
}



int main() {
  parking_lot p;
  dist w1(dist::METER, 2.45);
  dist l1(dist::FOOT, 17.0);
  dist w2(dist::METER, 2.6);
  dist l2(dist::FOOT, 19.0);
  dist w3(dist::METER, 2.7);
  dist l3(dist::FOOT, 21.0);
  car c1{ w1, l2, w1, string("PINOTNV") };
  car c2{ w3, l2, w2, string("133ABD") };
  car c3{ w1, l1, w1, string("166ABC") };
  car c4{ w1, l2, w1, string("CU LTR") };

  p.add_space( w1, l1, 'A', 1 );
  p.add_space( w1, l1, 'A', 2 );
  p.add_to_row( w2, l2, 'B', 1, 4 );
  p.add_to_row( w3, l3, 'C', 11, 4 );

  cout << "Park 1 " <<  p.park_car(c1) << endl;
  cout << "Park 2 " <<  p.park_car(c2) << endl;
  cout << "Park 3 " <<  p.park_car(c3) << endl;
  p.park_car(c4);

  cout << p;
  p.remove_car( "PINOTNV" );
  cout << p;
  p.find_car("CU LTR");
  p.find_occupant('C',12);
}

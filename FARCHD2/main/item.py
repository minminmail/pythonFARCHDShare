"""
	This file is part of KEEL-software, the Data Mining tool for regression,
	classification, clustering, pattern mining and so on.

	Copyright (C) 2004-2010

	F. Herrera (herrera@decsai.ugr.es)
    L. Sánchez (luciano@uniovi.es)
    J. Alcalá-Fdez (jalcala@decsai.ugr.es)
    S. García (sglopez@ujaen.es)
    A. Fernández (alberto.fernandez@ujaen.es)
    J. Luengo (julianlm@decsai.ugr.es)

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see http://www.gnu.org/licenses/

"""

"""

/**
 * <p>Title: Item</p>
 *
 * <p>Description: This class contains the representation of a item</p>
 *
 * <p>Copyright: Copyright KEEL (c) 2007</p>
 *
 * <p>Company: KEEL </p>
 *
 * @author Jesus Alcalá (University of Granada) 09/02/2011
 * @version 1.0
 * @since JDK1.6
 */

"""
import copy
class item :
    variable=None
    value = None

    def __init__(self,variable_pass,value_pass):
        self.variable = variable_pass
        self.value = value_pass

    # It sets the pair of values to the item
    """
    * @param variable Value which represents an input attribute of a rule
    * @param value Value attached to the variable
    """
    def set_values(self,variable_pass,value_pass):
        self.variable = variable_pass
        self.value =  value_pass

    def get_variable(self):
        return self.variable

    #It returns the value of the item

    def get_value(self):
        return self.value
    """
        public Item clone(){
        Item d = new Item();
        d.variable = this.variable;
        d.value = this.value;

	    return d;
        }
    
    """
    def clone(self):
        new_item = item(self.variable,self.value)
        return new_item

    def is_equal(self,item_pass):
        if(self.variable== item_pass.variable) and (self.value==item_pass.value):
            return True
        else:
            return False

    def compare_to(self, item_object):
        if item_object.variable> self.variable:

            return -1
        elif item_object.variable < self.variable:
            return 1
        elif item_object.value > self.value:
            return -1
        elif item_object.value < self.value:
            return 1

        return 0







"""
/***********************************************************************

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

**********************************************************************/
"""

"""
/**
 * <p>Title: ExampleWeight</p>
 * <p>Description: The objects of this class contain the weights of a patterns</p>
 * <p>Copyright: Copyright KEEL (c) 2007</p>
 * <p>Company: KEEL </p>
 * @author Written by Jesus Alcala (University of Granada) 09/02/2011
 * @version 1.0
 * @since JDK1.6
 */

"""
class example_weight:
    weight = None
    count = None
    K = None

    """
    * Builder
    * @param K Covered patterns in the second stage are completely eliminated when they have been covered more than K times.
    """

    def __init__(self,k_pass):
        self.K = k_pass
        self.count = 0
        self.weight = 1.0
    """
     * Increments in 1 the number of times that it has been covered.
     * If this number exceed the value K after been incremented, it is completely eliminated, reducing the weight to 0.
     * Otherwise the weight is updated inversely proportional to the times covered.
    
    """
    def increase_count(self):
        self.count = self.count + 1
        if self.count >= int(self.K):
            self.weight = 0.0
        else:
            self.weight = 1.0/(self.count + 1.0)
    """
     * Returns the number of times counted.
     * @return Number of times counted.
    """
    def get_count(self):
        return self.count

    """
     * Checks if the pattern is active. 
     * This means checking if the number of times counted are smaller than the fixed K.
     * @return True if the number of times counted are smaller than the fixed K. False otherwise. 
    """
    def is_active(self):
        return self.count < int(self.K)

    """
     * Returns the weight given to the pattern.
     * @return the weight given to the pattern
    """
    def get_weight_value(self):
        return self.weight


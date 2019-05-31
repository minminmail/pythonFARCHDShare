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
* <p>Title: Itemset</p>
 * <p>Description: This class contains the representation of a itemset</p>
 * <p>Copyright: Copyright KEEL (c) 2007</p>
 * <p>Company: KEEL </p>
 * @author Jesus Alcalá (University of Granada) 09/02/2011

"""

import copy
from item import item

class item_set:
    item_set_list=  []
    # int
    class_type= None
    #double
    support = None
    support_rule = None

    def __init__(self,class_type_pass):
        self.item_set_list =[]
        self.class_type = class_type_pass
        self.support = 0
        self.support_rule = 0

    # return Return a copy of the itemset


    def clone_item_set(self):

        new_item_set = item_set(self.class_type)

        #print("len(self.item_set_list) is " + str(len(self.item_set_list)))

        for i in range(0,len(self.item_set_list)):
            new_item_set.add(self.item_set_list[i].clone())
        new_item_set.support = self.support
        new_item_set.support_rule = self.support_rule

        return new_item_set

    #Function to add an item to our itemset list

    def add(self,item_pass):
        #print("begin add in item_set function, item_pass type is : " + str(item_pass))
        self.item_set_list.append((item_pass))
        #print("after add in item_set function, self.item_set_list type is : " + str(self.item_set_list))

    """
     * It returns the item located in the given position of the itemset
     * @param pos Position of the requested item into the itemset
     * @return The requested item of the itemset 
    """
    def get_item(self,position):
        #print("position is :" + str(position))
        return self.item_set_list[position]

    """
    
   * Function to remove the item located in the given position
   * @param pos Position of the requested item into the itemset
   * @return The removed item of the itemset
    """
    def remove(self,position):
        #print("In item_set remove index is :" + str(position))
        self.item_set_list.pop(position)
        return self.item_set_list
    """
    * It returns the size of the itemset (the number of items it has)
    * @return Number of items the itemset stores
    """
    def size(self):
        return len(self.item_set_list)

    """
    * It returns the support of the antecedent of the itemset
    * @return Support of the antecedent of the itemset
    """
    def get_support(self):
        return self.support

    """
    * It returns the support of the itemset for its related output class
    * </p>
    * @return Support of the itemset for its related output class
    """
    def get_support_class(self):
        return self.support_rule

    """
     It returns the support of the itemset for its related output class
     return Support of the itemset for its related output class
    """
    def get_support_rule(self):
        return self.support_rule

    """
     * It returns the output class of the itemset
     * @return output class of the itemset
    """
    def get_class_type(self):
        return self.class_type
    """
     * Set the class type with the value given as argument.
     * @param class type class given.
     """
    def set_class(self,class_type_pass):
        self.class_type = class_type_pass

    """
    * Function to check if an itemset is equal to another given

    * @param a Itemset to compare with ours
    * @return boolean true = they are equal, false = they aren't.
    """
    def is_equal(self,item_set_list_pass):
        if not (len(self.item_set_list) ==len(item_set_list_pass)):
            return False
        if not (self.class_type ==item_set_list_pass.get_class_type(self)):
            return False

        for i in range(0,len(item_set_list_pass)):
            item = self.item_set_list.get(i)
            if not(item.is_equal(item_set_list_pass.get(i))):
                return False
        return True

    """
    * It computes the support, rule support, hits, misses and PER of our itemset for a given dataset
    * @param dataBase Given training dataset useful information to calculate supports.
    * @param train Given training dataset to be able to calculate supports.
     """

    def calculate_supports(self,data_base_pass,my_train_data_set_pass):
        degree_num = None
        self.support = 0.0
        self.support_rule = 0.0
        for i in range(0,my_train_data_set_pass.size()):
            degree_num = self.degree(data_base_pass,my_train_data_set_pass.getExample(i))
            #print("degree in calculate_supports is: "+str(degree_num))
            self.support = self.support + degree_num
            if my_train_data_set_pass.getOutputAsIntegerWithPos(i)==self.class_type:
                self.support_rule =self.support_rule + degree_num
        self.support = self.support / my_train_data_set_pass.getnData()
        self.support_rule = self.support_rule/my_train_data_set_pass.getnData()

    """
    /**
     * Calculate the degree of the given example inside the given data-set.
     * @param dataBase Given training dataset useful information to calculate the degree.
     * @param ejemplo Given example to calculate its degree.
     * @return
     */
     """
    def degree(self,data_base_pass,example_list_pass):
        return self.__degree_product(data_base_pass,example_list_pass)

    def __degree_product(self,data_base_pass,example_list_pass):
        degree_num = 1.0

        #print("The length of item list has :" + str(len(self.item_set_list)))
        #print("The item list has :" + str(self.item_set_list))
        for i in range(0,len(self.item_set_list)):
            if degree_num > 0.0:

                item_here = self.item_set_list[i]

                degree_num = degree_num * data_base_pass.matching(item_here.get_variable(),item_here.get_value(),example_list_pass[item_here.get_variable()])
        return degree_num




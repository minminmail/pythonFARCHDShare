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
from RuleBase import RuleBase
from item_set import item_set
from item import item
import gc

class apriori:

    L2=[] #ArrayList<Itemset>
    # double
    minsup = None
    maxconf= None

    min_supps=[] #double[]
    # int
    nClasses = None
    nVariables = None
    depth = None

    #long
    rule_stage1 = None
    # RuleBase instances:
    ruleBase =  None
    ruleBaseClass = None

    train_MyDataSet = None
    dataBase = None

    def __init__(self):
        print("init of apriori... ")

    """
    * @param ruleBase Rule base
    * @param dataBase Data Base
    * @param train Training dataset
    * @param minsup Minimum support.
    * @param minconf Maximum Confidence.
    * @param depth Depth of the trees (Depthmax)
    */
    """
    def init_with_more_parameters(self,ruleBase_pass,dataBase_pass,train_data_set_pass,minsup_pass,maxconf_pass,depth_pass):
        self.train_MyDataSet = train_data_set_pass
        self.dataBase = dataBase_pass
        self.ruleBase = ruleBase_pass
        self.maxconf = maxconf_pass
        self.depth = depth_pass
        self.nClasses = self.train_MyDataSet.getnClasses()
        self.nVariables = self.train_MyDataSet.getnInputs()
        self.L2 = []
        #print("self.nClasses : " + str(self.nClasses))
        self.min_supps= [ None for x in range (self.nClasses)]
        for i in range(0,self.nClasses):
            #print(" minsup_pass is : " + str(minsup_pass))
            self.min_supps[i] = float(self.train_MyDataSet.frecuent_class(i)) * float(minsup_pass)


    def generate_RB(self):
        #int
        uncover= None
        self.rule_stage1 = 0
        #Generate the rule set (Stage 1 and 2)
        self.ruleBaseClass = RuleBase(self.dataBase,self.train_MyDataSet,self.ruleBase.get_K(),self.ruleBase.get_type_inference())
        print(" generate_RB begin,self.nClasses is  : " + str(self.nClasses))

        for i in range (0, self.nClasses):
            self.minsup = self.min_supps[i]
            #print(" __generate_L2 begin : ")
            self.__generate_L2(i)
            #print(" generate_large begin : ")
            self.generate_large(self.L2, i)
            print(" generate_RB reduce_rules ,parameter i is : " + str(i) )
            self.ruleBaseClass.reduce_rules(i)

            self.ruleBase.add_ruleBase(self.ruleBaseClass)
            self.ruleBaseClass.clear_in_rule_base()
            # force the Garbage Collector to release unreferenced memory
            gc.collect()

    def __generate_L2(self,class_int):
        uncover = None

        self.L2.clear()
        item_set_here = item_set(class_int)
        clone_item_set = item_set_here
        #print("begin __generate_L2 ,class_int :" + str(class_int))
        for i in range(0,self.nVariables):
            if int(self.dataBase.numLabels(i))>1:
                for j in range (0,int(self.dataBase.numLabels(i))):
                    item_here = item(i,j)
                    #print(" before pass to add item , the item_here i is :" + str(i) + " , j is :"+str(j))
                    #print(" before pass to add item , the item_here type is :" + str(item_here))
                    item_set_here.add(item_here)
                    item_set_here.calculate_supports(self.dataBase,self.train_MyDataSet)
                    if item_set_here.get_support_class()>=self.minsup:
                        #print(" item_set_here.size () is : " + str(item_set_here.size()))
                        clone_item_set = item_set_here.clone_item_set()
                        #print(" clone_item_set.size () is : " + str(clone_item_set.size()))
                        self.L2.append(clone_item_set)
                    #print("item_set_here is :" + str(item_set_here))
                    item_set_here.remove(0)
                    #print(" after remove 0 ,clone_item_set.size () is : " + str(clone_item_set.size()))

        #print("self.L2 length is :" + str(len(self.L2)))


        #for i in range(0, len(self.L2)):
            #print("L2[" + str(i) + "] size is :" + str(self.L2[i].size()))

        self.generate_rules(self.L2,class_int)
    """  
     * Indentifies how many times a class has been uncovered.
     * @param clas Class given to compute the number of times.
     * @return number of times that class has been uncovered.     
    """

    def has_uncover_class(self,class_int):

        uncover = 0
        degree = None
        item_set=None
        stop = None

        for i in range(0,len(self.train_MyDataSet)):
            if self.train_MyDataSet.getOutputAsIntegerWithPos(i)==class_int:
                stop = False
                for j in range(0,len(self.L2)):
                    if not stop:
                        item_set= self.L2[j]
                        degree = item_set.degree(self.dataBase,self.train_MyDataSet.getExample(i))
                        if degree > 0.0 :
                            stop = True
                if not stop:
                     uncover = uncover + 1
        return uncover

    #ArrayList<Itemset> Lk, int clas
    def generate_large(self,item_set_list_pass,class_int_pass):
        """
        int i, j, size;
	    ArrayList<Itemset> Lnew;
	    Itemset newItemset, itemseti, itemsetj;

	    size = Lk.size();

        """
        new_item_set_list = []
        new_item_set = None
        item_set_i = None
        item_set_j = None

        size = len(item_set_list_pass)
        #print("From beginning the size is : " + str(size))
        for i  in range(0, len(item_set_list_pass)):
            item_set_object_change = item_set_list_pass[i]
            #print("item_set_object.size() is : " + str(item_set_object_change.size()))

        #print(" In generate_large, the len(item_set_list_pass) is: " +str(len(item_set_list_pass)))
        if size >1:
            length_item_0 = item_set_list_pass[0].size()

            #print(" the size of length_item_0 is :" + str(length_item_0))
            #  if (((Lk.get(0)).size() < this.nVariables) && ((Lk.get(0)).size() < this.depth)) {
            if length_item_0 < int(self.nVariables) and length_item_0 < int(self.depth):
                # Lnew = new ArrayList<Itemset> ();
                new_item_set_list = []
                for i in range(0,size-1):
                    item_set_i = item_set_list_pass[i]
                    #print(" size of item_set_i is : " + str(item_set_i.size()))
                    for j in range(i+1,size):

                        item_set_j = item_set_list_pass[j]
                        #print(" size of item_set_j is : " + str(item_set_j.size()))
                        if self.is_combinable(item_set_i,item_set_j) :
                            new_item_set = item_set_i.clone_item_set()
                            #print("new_item_set.add((item_set_j[len(item_set_j)-1]).clone())")
                            new_item_set.add((item_set_j.get_item(item_set_j.size()-1)).clone())
                            new_item_set.calculate_supports(self.dataBase,self.train_MyDataSet)
                            #print("new_item_set.get_support_class()" +str(new_item_set.get_support_class()))
                            #print("self.minsup" + str(self.minsup))
                            if new_item_set.get_support_class()>= self.minsup:
                                #print("new_item_set_list.append(new_item_set)")
                                #print("the size of new_item_set just added is:  " + str(new_item_set.size()))
                                new_item_set_list.append(new_item_set)
                    self.generate_rules(new_item_set_list,class_int_pass)
                    self.generate_large(new_item_set_list,class_int_pass)
                    new_item_set_list.clear()
                    # force the Garbage Collector to release unreferenced memory
                    gc.collect()

    def is_combinable(self,item_set_i_pass,item_set_j_pass):

        i_value = item_set_i_pass.size()-1
        j_value = item_set_j_pass.size()-1
        #print(" i_value:  " + str(i_value) + "j_value : " + str(j_value))
        item_i = (item_set_i_pass.get_item(i_value))
        item_j = (item_set_j_pass.get_item(j_value))
        #print("item_i:" + str(item_i))
        if item_i.get_variable()>=item_j.get_variable():
            return False
        return True


    """
     * Returns the rules generated on the Stage 1. 
     * @return the rules of the Stage 1
    """

    def get_rules_stage1(self):
        return self.rule_stage1

    def generate_rules(self,item_set_list_pass,class_int):
        uncover = None
        item_set_here = None
        confidence = None
        #print(" len(item_set_list_pass)-1 is "  + str(len(item_set_list_pass)-1))

        for i in range (len(item_set_list_pass)-1,-1,-1):

            item_set_here = item_set_list_pass[i]
            #print("item_set_here is " + str(item_set_here))
            #print("item_set_here size is " + str(item_set_here.size()))
            #print("item_set_here.get_support() " + str(item_set_here.get_support()))
            if item_set_here.get_support()>0.0:
                confidence = item_set_here.get_support_class() /item_set_here.get_support()
                #print("confidence in generate_rules is: " + str(confidence))
            else:
                confidence = 0.0
            if confidence > 0.4:
                print("confidence is bigger than 0.4 ")
                self.ruleBaseClass.add_item_set(item_set_here)
                self.rule_stage1 = self.rule_stage1 + 1
            if confidence > float(self.maxconf):
                #print("confidence > float(self.maxconf ")
                #print("delete " + str(i) + " , in the L2 list")
                item_set_list_pass.pop(i)

        if self.ruleBaseClass.size()>500000 :
            print(" self.ruleBaseClass.size()>500000, pass the parameter class_int is  : " + str(class_int))
            self.ruleBaseClass.reduce_rules(class_int)
            gc.collect()





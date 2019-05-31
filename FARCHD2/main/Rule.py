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

from Fuzzy import Fuzzy
from DataBase import DataBase
from example_weight import example_weight


"""
 * <p>Title: Rule</p>
 * <p>Description: This class codes a Fuzzy Rule</p>
 * <p>Copyright: KEEL Copyright (c) 2008</p>
 * <p>Company: KEEL </p>
 * @author Written by Jesus Alcala (University of Granada) 09/02/2011
 * @version 1.0
 * @since JDK1.6

"""
import numpy as np

class Rule:

  antecedent=[]
  clas=None
  nAnts = None
  conf = None
  supp = None
  wracc = None
  dataBase = None

  """
  * Create a rule with another one
  * @param r This a rule
  """

  """
  * Create a new rule
  * @param dataBase The database
  """

  def __init__(self, choose,rule_or_data_base_pass):

   #print("__init__ of Rule")
   if choose==1:
      print(" init the rule with choose==1 ")
      self.antecedent = [None for x in range (len(rule_or_data_base_pass.antecedent))]
      for k in range(0,len(self.antecedent)):
        self.antecedent[k] = rule_or_data_base_pass.antecedent[k]
      self.clas = rule_or_data_base_pass.clas
      self.dataBase = rule_or_data_base_pass.dataBase
      self.conf = rule_or_data_base_pass.conf
      self.supp = rule_or_data_base_pass.supp
      self.nAnts = rule_or_data_base_pass.nAnts
      self.wracc = rule_or_data_base_pass.wracc

   elif choose==2:

      data_base_pass_transfer = rule_or_data_base_pass
      print(" init the rule with choose==2 ")
      self.antecedent = [None for x in range(data_base_pass_transfer.numVariables())]
      for i in range(0, len(self.antecedent)):
        self.antecedent[i] = -1
        self.dataBase = rule_or_data_base_pass
        self.conf = 0.0
        self.supp = 0.0
        self.nAnts = 0
        self.wracc = 0.0


  
  """
  * Clone
  * @return A copy of the rule
  """

  def clone(self):
    rule = Rule(2,self.dataBase)
    print("clone in rule pass the parameter 2 for init rule instance......")
    rule.antecedent = [None for x in range(0,len(self.antecedent))]
    for i in range(0,len(self.antecedent)):
      rule.antecedent[i] = self.antecedent[i]
      rule.clas = self.clas
      rule.dataBase = self.dataBase
      rule.conf = self.conf
      rule.supp = self.supp
      rule.nAnts = self.nAnts
      rule.wracc = self.wracc

    return rule


  """
     * It sets the antecedent of the rule
     * @param antecedent Antecedent of the rule
  """

  def asignaAntecedente(self,antecedent_pass):
    self.nAnts = 0

    for i in range(0,len(self.antecedent)):
      self.antecedent[i] = antecedent_pass[i]
      if self.antecedent[i]>-1:
        self.nAnts

  """
   * It sets the consequent of the rule
   * @param clas Class of the rule
  """
  def setConsequent(self,clas_pass):
    self.clas = clas_pass

  """
   * Function to check if a given example matchs with the rule (the rule correctly classifies it)
     * @param example  Example to be classified
   * @return 0.0 = doesn't match, >0.0 = does.
   """
  def matching(self,example_pass):
     #print("In began of matching, the is example_pass :" + str(example_pass))
     return self.degreeProduct(example_pass)


  def degreeProduct(self,example_pass):
    degree = 1.0
    #print("In began of degreeProduct, the is example_pass :"+str(example_pass))

    for i in range(0,len(self.antecedent)):
      if degree>0.0:

        degree = degree* self.dataBase.matching(i,self.antecedent[i],example_pass[i])
    #print("self.conf is :"+str(self.conf))
    return degree * self.conf


  """
   * It sets the confidence of the rule
   * @param conf Confidence to be set
  """
  def setConfidence(self,conf_pass):
    #print("setConfidence is :"+str(conf_pass))
    self.conf = conf_pass

  """
   * It sets the support of the rule
     * @param supp  Support to be set
   """
  def setSupport(self,supp_pass):

    self.supp = supp_pass
  """
  * It sets the Wracc of the rule
  * @param wracc Wracc to be set
  """

  def setWracc(self,wracc):
    self.wracc = wracc

 
  """
   * It returns the Confidence of the rule
   * @return Confidence of the rule
  """
  def getConfidence(self):
    return self.conf

  """
  * It returns the support of the rule
  * @return Support of the rule
  
  """
  def getSupport(self):
    return self.supp


  """
   * It returns the Wracc of the rule
   * @return Wracc of the rule
   """
  def get_Wracc(self):
    return self.wracc
  """
  * It returns the output class of the rule
  * @return Output class of the rule
  
  """

  def get_class(self):
    return self.clas

  """

   * Function to check if a given rule is a subrule of this rule
   * @param a Rule to be examinated
   * @return false = it isn't, true = it is.
  """
  def isSubset(self,rule_pass):

    if self.clas !=rule_pass.clas or self.nAnts > rule_pass.nAnts:
      return False
    else:
      for k in range(0,len(self.antecedent)):
        if self.antecedent[k]>-1:
          if self.antecedent[k]!=rule_pass.antecedent[k]:
            return False
    return True

  """
  * Calculate Wracc for this rule.
  * The value of the measure Wracc for this rule will be stored on the attribute "wracc".
  * @param train Training dataset
  * @param exampleWeight Weights of the patterns

  """
  """
   public void calculateWracc (myDataset train, ArrayList<ExampleWeight> exampleWeight) {
	  int i;
	  double n_A, n_AC, n_C, degree;
	  ExampleWeight ex;

	  n_A = n_AC = 0.0;
	  n_C = 0.0;
	  
	  for (i=0; i < train.size(); i++) {
		  ex = exampleWeight.get(i);

		  if (ex.isActive()) {
			  degree = this.matching(train.getExample(i));
			  if (degree > 0.0) {
				  degree *= ex.getWeight();
				  n_A += degree;
				  
				  if (train.getOutputAsInteger(i) == this.clas) {
					  n_AC += degree;
					  n_C += ex.getWeight();
				  }
			  }
			  else if (train.getOutputAsInteger(i) == this.clas)  n_C += ex.getWeight();
		  }
	  }

	  if ((n_A < 0.0000000001) || (n_AC < 0.0000000001) || (n_C < 0.0000000001))  this.wracc = -1.0;
	  else  this.wracc = (n_AC / n_C) * ((n_AC / n_A) - train.frecuentClass(this.clas));
  }
  
  """
  def calculate_Wracc(self,train_ds_pass,example_weight_array_pass):
    #double, double n_A, n_AC, n_C, degree;
    degree = None
    #ExampleWeight ex , instance

    example_weight_here = None

    #n_A = n_AC = 0.0;n_C = 0.0;

    n_A = 0.0
    n_AC = 0.0
    n_C = 0.0

    for i in range(0,train_ds_pass.size()):
      example_weight_here = example_weight_array_pass[i]
      if example_weight_here.is_active():
        degree = self.matching(train_ds_pass.getExample(i))
        if degree > 0.0:
          degree = degree * example_weight_here.get_weight_value()
          n_A = n_A + degree
          if train_ds_pass.getOutputAsIntegerWithPos(i)==self.clas:
            n_AC = n_AC + degree
            n_C = n_C + example_weight_here.get_weight_value()
        # degree not > 0.0
        else:
          if train_ds_pass.getOutputAsIntegerWithPos(i) == self.clas:
            n_C = n_C + example_weight_here.get_weight_value()

    if n_A < 0.0000000001 or n_AC < 0.0000000001  or n_C < 0.0000000001:
      self.wracc = -1.0
    else:
      self.wracc = (n_AC/n_C)*((n_AC / n_A) - train_ds_pass.frecuent_class(self.clas))


  """
  /**
     * Reduces the weight of the examples that match with the rule (the rule correctly classifies them)
     * @param train training examples given to match them to the rule.
     * @param exampleWeight Each example weight to be updated.
     * @return Number of examples that have become not active after the weight reduction.
     */
  """

  def reduce_weight(self,train_ds_pass,example_weight_pass):
    count = 0
    example_weight_here = None
    for i in range(0,train_ds_pass.size()):
      example_weight_here = example_weight_pass[i]
      if example_weight_here.is_active():
        if self.matching(train_ds_pass.getExample(i))>0.0:
          example_weight_here.increase_count()
          if not example_weight_here.is_active() and train_ds_pass.getOutputAsIntegerWithPos(i)==self.clas:
            count = count + 1

    return count




  """
  /**
   * It sets the label for a given position in the antecedent (for a given attribute)
   * @param pos Location of the attribute which we want to set the label
   * @param label New label value to set
   */
  """

  def setLabel(self,pos_pass,lable_pass):

    if self.antecedent[pos_pass]<0 and lable_pass > -1:
      self.nAnts = self.nAnts + 1
    if self.antecedent[pos_pass] > -1 and lable_pass < 0:
      self.nAnts = self.nAnts - 1
    self.antecedent[pos_pass] = lable_pass

  """
     * Function to compare objects of the Rule class.
   * Necessary to be able to use "sort" function
   * It sorts in an decreasing order of wracc
   * @param a Rule object to compare with.
   * @return 1 if a is bigger, -1 if smaller and 0 otherwise.
  
  """
  def compareTo(self, object_a):

    if object_a.wracc < self.wracc:
      return  -1
    if object_a.wracc > self.wracc:
      return 1
    return  0


  """



  def setTwoParameters( self,n_variables,  compatibilityType):
    print("In rule calss , setTwoParameters method, the n_variables = "+str(n_variables))
    self.antecedent = [Fuzzy() for x in range(n_variables)]
    self.compatibilityType = compatibilityType

     # * It assigns the class of the rule
     # * @param clas int

  def setClass(self, clas):
    self.clas = clas

   # * It assigns the rule weight to the rule
   # * @param train myDataset the training set
   # * @param ruleWeight int the type of rule weight

  def assingConsequent(self,train, ruleWeight) :
    if ruleWeight == Fuzzy_Chi.Fuzzy_Chi.CF:
      self.consequent_CF(train)

    elif ruleWeight == Fuzzy_Chi.Fuzzy_Chi.PCF_II:
      self.consequent_PCF2(train)

    elif ruleWeight == Fuzzy_Chi.Fuzzy_Chi.PCF_IV:
      self.consequent_PCF4(train)

    elif ruleWeight == Fuzzy_Chi.Fuzzy_Chi.NO_RW:
      self.weight = 1.0

   # * It computes the compatibility of the rule with an input example
   # * @param example double[] The input example
   # * @return double the degree of compatibility

  def compatibility(self,example):
    if (self.compatibilityType == Fuzzy_Chi.Fuzzy_Chi.MINIMUM):
      #print("self.compatibilityType == Fuzzy_Chi.Fuzzy_Chi.MINIMUM")
      return self.minimumCompatibility(example)

    else :
      #print("self.compatibilityType != Fuzzy_Chi.Fuzzy_Chi.MINIMUM"+", self.compatibilityType = "+ str(self.compatibilityType))
      return self.productCompatibility(example)


   # * Operator T-min
   # * @param example double[] The input example
   # * @return double the computation the the minimum T-norm

  def minimumCompatibility(self,example):
    minimum=None
    membershipDegree=None
    minimum = 1.0
    for i in range(0, len(self.antecedent)):
      print("example["+str(i)+"] = "+example[i])
      membershipDegree = self.antecedent[i].setX(example[i])
      print("membershipDegree in minimumCompatibility = " + str(membershipDegree))
      minimum = min(membershipDegree, minimum)

    return minimum

   # * Operator T-product
   # * @param example double[] The input example
   # * @return double the computation the the product T-norm

  def productCompatibility(self, example):

    product = 1.0
    antecedent_number=len(self.antecedent)
    print("antecedent_number = " + str(antecedent_number))
    for i in range( 0, antecedent_number):
      print("example[i="+ str(i)+"]"+":"+ str(example[i]))
      membershipDegree = self.antecedent[i].setX(example[i])
      print("membershipDegree in productCompatibility  = " +str(membershipDegree))
      product = product * membershipDegree
      print("product: "+ str(product))
    return product


   # * Classic Certainty Factor weight
   # * @param train myDataset training dataset

  def consequent_CF( self,train):
    train_Class_Number = train.getnClasses()
    classes_sum = [0.0 for x in range(train_Class_Number)]
    for i in range( 0,train.getnClasses()):
       classes_sum[i] = 0.0

    total = 0.0
    comp = None
    #Computation of the sum by classes */
    for i in range( 0,train.size()):
      comp = self.compatibility(train.getExample(i))
      classes_sum[train.getOutputAsIntegerWithPos(i)] = classes_sum[train.getOutputAsIntegerWithPos(i)]+ comp
      total =total+ comp

    print("classes_sum[self.clas]  = " + str(classes_sum[self.clas] ) +"total" +str(total))
    self.weight = classes_sum[self.clas] / total

   # * Penalized Certainty Factor weight II (by Ishibuchi)
   # * @param train myDataset training dataset

  def consequent_PCF2(self,train) :
    classes_sum = float[train.getnClasses()]
    for i in range (0, train.getnClasses()):
       classes_sum[i] = 0.0

    total = 0.0
    comp = None
  # Computation of the sum by classes */
    for i in range (0,  train.size()):
      comp = self.compatibility(train.getExample(i))
      classes_sum[train.getOutputAsIntegerWithPos(i)] = classes_sum[train.getOutputAsIntegerWithPos(i)]+comp
      total = total+comp

    sum = (total - classes_sum[self.clas]) / (train.getnClasses() - 1.0)
    self.weight = (classes_sum[self.clas] - sum) / total

   # * Penalized Certainty Factor weight IV (by Ishibuchi)
   # * @param train myDataset training dataset

  def consequent_PCF4( self,train) :
    classes_sum =  [0.0 for x in range(train.getnClasses())]
    for  i in range( 0, train.getnClasses()):
      classes_sum[i] = 0.0

    total = 0.0
    comp= None

    train_size=train.size()
    print("train_size: " + str(train_size))
    # Computation of the sum by classes */
    for i in range( 0, train_size):
      comp = self.compatibility(train.getExample(i))
      print("comp = " + str(comp))
      classes_sum[train.getOutputAsIntegerWithPos(i)] = classes_sum[train.getOutputAsIntegerWithPos(i)]+ comp
      total = total+ comp

    print("self.clas ="+ str(self.clas)+"classes_sum[self.clas] :" + str(classes_sum[self.clas]))
    sum = total - classes_sum[self.clas]
    self.weight = (classes_sum[self.clas] - sum) / total

   # * This function detects if one rule is already included in the Rule Set
   # * @param r Rule Rule to compare
   # * @return boolean true if the rule already exists, else false

  def comparison(self,rule) :
    contador = 0
    for j in range (0, len(self.antecedent)):
      if (self.antecedent[j].label == rule.antecedent[j].label) :
        contador= contador + 1

    if (contador == len(rule.antecedent)):
      if (self.clas != rule.clas) : #Comparison of the rule weights
        if (self.weight < rule.weight) :
          #Rule Update
          self.clas = rule.clas
          self.weight = rule.weight

      return True
    else:
      return False
  """








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
from Rule import Rule
import gc

 # * This class contains the representation of a Rule Set
 # *
 # * @author Written by Alberto Fern谩ndez (University of Granada) 29/10/2007
 # * @version 1.0
 # * @since JDK1.5


class RuleBase :
    # rule array
    rule_base_array=[]
    # database
    dataBase= None
    # myDataSet
    my_train_dataset = None
    # int
    n_variables= None
    K = None
    nUncover = None
    type_inference = None
    default_rule = None

    # int array
    nUncover_class = []
    # double
    fitness = None # double

    """
    * Maximization
    * @param a first number
    * @param b second number
    * @return boolean true if a is greater than b
    */
    """
    def better(self,a_int_pass, b_int_pass):
        if a_int_pass > b_int_pass:
            return True
        return False


    def __init__(self, data_base_pass=None,  my_data_set_pass=None,  K_pass=None, type_inference_pass=None):
            print("RuleBase init begin...")
            if data_base_pass is not None and my_data_set_pass is not None and K_pass is not None and type_inference_pass is not None:
                self.rule_base_array = [] #new ArrayList<Rule> ();
                self.dataBase = data_base_pass
                self.my_train_dataset = my_data_set_pass

                self.n_variables = data_base_pass.numVariables()
                self.fitness = 0.0
                print("K_pass in rule base  is :" + str(K_pass))
                self.K = K_pass
                self.type_inference = type_inference_pass
                self.default_rule = -1
                self.nUncover = 0
                # int array
                self.nUncover_class = [None for x in range(self.my_train_dataset.getnClasses())]
            else :
                print(" Initial RuleBase with empty parameters......")

    def clone(self):
        print("Clone begin in ruleBase ......")
        rule_base = RuleBase(self)
        rule_base.rule_base_array = []
        for i in range(0,len(self.rule_base_array)):
            rule_base.rule_base_array.append(self.rule_base_array[i].clone())
        rule_base.dataBase = self.dataBase
        rule_base.my_train_dataset = self.my_train_dataset
        rule_base.n_variables = self.n_variables
        rule_base.fitness = self.fitness
        rule_base.K = self.K
        rule_base.type_inference = self.type_inference
        rule_base.default_rule = self.default_rule
        rule_base.nUncover = self.nUncover
        class_num = self.my_train_dataset.getnClasses()
        rule_base.nUncover_class = [None for x in range (class_num)]

        for i in range(0,class_num):
            rule_base.nUncover_class[i] = self.nUncover_class[i]
        return rule_base


    def add_rule(self,rule):
        self.rule_base_array.append(rule)

    """
    * It adds the rules of the rule_base_array given.
    * @param ruleBase Rules to be added

    """
    def add_ruleBase(self,rule_base_pass):
        print("rule_base_pass.size() :" + str(rule_base_pass.size()))

        for i in range(0,rule_base_pass.size()):
            rule_here = rule_base_pass.get_from_pos(i)
            print("conf of rule_here in add_ruleBase is : " + str(rule_here.conf))
            self.rule_base_array.append(rule_here.clone())

         # * It checks if a specific rule is already in the rule base
         # * @param r Rget_nLabels_realget_nLabels_realgetgetule the rule for comparison
         # * @return boolean true if the rule is already in the rule base, false in other case
    """
    It adds a rule to the rule base
    @param itemset itemset to be added
    
    """

    def add_item_set(self,item_set):
        item = None
        antecedent = [None for x in range(self.n_variables)] # int array
        for i in range(0,self.n_variables):
            antecedent[i] = -1 # do not care
        for i in range(0,item_set.size()):
            item = item_set.get_item(i)
            antecedent[item.get_variable()] = item.get_value()
        print("Init rule with parameter 2 begin ......")
        rule_here = Rule(2,self.dataBase)
        rule_here.asignaAntecedente(antecedent)
        rule_here.setConsequent(item_set.get_class_type())
        rule_here.setConfidence(item_set.get_support_class()/item_set.get_support())
        rule_here.setSupport(item_set.get_support_class())
        print(" add a new rule,rule_here, in add_item_set, the conf of the rule is :"+ str(rule_here.conf))
        self.rule_base_array.append(rule_here)

    """
    * Function to get a rule from the rule base
    * @param pos Position in the rule base where the desired rule is stored
    * @return The desired rule
    """

    def get_from_pos(self,pos_int):
        return self.rule_base_array[pos_int]
    """
    * It returns the number of rules in the rule base
    * @return Rule base's size 
    """
    def size(self):
        return len(self.rule_base_array)

    """
        Function to sort the rule base
    """
    def sort(self):
        # sort according to rule wracc

        for i in range(0,len(self.rule_base_array)):
            print(" before soret the conf of rule is :" + str(self.rule_base_array[i].conf))

        self.rule_base_array.sort(key=lambda x: x.wracc,reverse=True)
        #sorted(self.rule_base_array)
        for i in range(0,len(self.rule_base_array)):
            print(" after soret the conf of rule is  :" + str(self.rule_base_array[i].conf))

    """
    * It removes the rule stored in the given position
    * @param pos Position where the rule we want to remove is
    * @return Removed rule
    """
    def clear_in_rule_base(self):
        print("clear in rule_base_array ")
        self.rule_base_array.clear()
        self.fitness = 0.0

    def remove(self,pos):
        print("remove rule from rule_base_array, remove pos is : " + str(pos))
        return self.rule_base_array.pop(pos)


    """
    /**
    * Returns the type of inference used to build the rules.
    * @return  the type of inference used.
    */  
    """
    def get_type_inference(self):
        return self.type_inference
    """
    * Function to return the fitness of the rule base
    * @return Fitness of the rule base    
    """
    def get_accuracy(self):
        return self.fitness

    """
     * Sets the default rule.
     * The default rule classifies all the examples to the majority class.
    """

    def set_default_rule(self):
        best_rule = 0
        for i in range(1,self.my_train_dataset.getnClasses()):
            if self.my_train_dataset.numberInstances(best_rule) <self.my_train_dataset.numberInstances(i):
                best_rule = i
        self.default_rule = best_rule

    """
     * Checks if there are examples uncovered by the rules.
     * @return True if there are some examples, False otherwise.

    """
    def has_uncover(self):
        return self.nUncover >0
   
    """
    /**
     * Returns the number of examples uncovered by the rules
     * @return Number of examples uncovered
     */

    """
    def get_uncover(self):
        return self.nUncover

    """
     * Returns the value of the parameter K.
     * (The maximum times covered letting an example active.
     * @return the value of the parameter K.
    """
    def get_K(self):
        return  self.K

    """
    * Function to evaluate the whole rule base by using the training dataset.
    """
    def evaluate_all(self):
        nHits = 0
        prediction = None
        self.nUncover = 0

        for i in range(0,self.my_train_dataset.getnClasses()):
            self.nUncover_class[i] = 0

        for i in range(0,len(self.my_train_dataset)):
            prediction = self.FRM_one(self.my_train_dataset.getExample(i))
            if self.my_train_dataset.getOutputAsIntegerWithPos(i)==prediction:
                nHits = nHits + 1
            if prediction < 0:
                self.nUncover = self.nUncover + 1
                self.nUncover_class[self.my_train_dataset.getOutputAsInteger(i)] = self.nUncover_class[self.my_train_dataset.getOutputAsInteger(i)] + 1

        self.fitness = (100.0 * nHits) / (1.0 * len(self.my_train_dataset))

    """
     /**
     * Function to evaluate the selected rules by using the training dataset and the fuzzy functions stored in the gene given.
     * @param gene Representation where the fuzzy functions needed to evaluate are stored
     * @param selected Selection of rules to be evaluated
     */
    """
    def evaluate_selected_rules(self,gene_array_double,selected_array_int):
        nHits = 0
        prediction= None
        self.dataBase.decode(gene_array_double)
        self.nUncover = 0

        for i in range(0,self.my_train_dataset.getnClasses()):
            self.nUncover_class[i] = 0

        for j in range(0,self.my_train_dataset.size()):
            prediction = self.FRM_two(self.my_train_dataset.getExample(j),selected_array_int)
            if self.my_train_dataset.getOutputAsIntegerWithPos(j)==prediction:
                nHits = nHits + 1
            if prediction < 0:
                self.nUncover = self.nUncover + 1
                self.nUncover_class[self.my_train_dataset.getOutputAsIntegerWithPos(j)] =self.nUncover_class[self.my_train_dataset.getOutputAsIntegerWithPos(j)] + 1


        self.fitness = (100.0 * nHits) / (1.0 * self.my_train_dataset.size())


    """
     * Predicts the class value for a given example, using the rules and type of inference stored on the rule_base_array. 
     * @param example Example to be predicted.
     * @return Class predicted.
    """

    def FRM_one(self,example_array):
        print("In FRM_one the example_array is :" +str(example_array))
        if self.type_inference==0:
            #print("begin  FRM_WR ......." )
            return self.FRM_WR_one(self,example_array)
        else:
            #print("begin FRM_AC ......." )
            return self.FRM_AC_one(example_array)


    """
     * Predicts the class value for a given example, using the selected rules and type of inference stored on the rule_base_array. 
     * @param example Example to be predicted.
     * @param selected Selection of rules to be considered for the class prediction.
     * @return Class predicted.
	
    """
    def FRM_two(self,example,selected):
        #print("In FRM_two the example is :" + str(example))
        if self.type_inference ==0:
            return self.FRM_WR_two(example,selected)
        else:
            return self.FRM_AC_two(example,selected)

    def FRM_WR_two(self,example,selected):
        print("In FRM_WR the example is :" + str(example))
        max = 0.0
        degree = None
        class_num = self.default_rule

        for i in range(0,len(self.rule_base_array)):
            if selected[i] > 0:
                rule = self.rule_base_array[i]
                print("rule conf is : " +str(rule.conf))
                degree = rule.matching(example)

                if degree>max:
                    max = degree
                    class_num = rule.get_class()

        return class_num

    def FRM_WR_one(self,example):
        print("In FRM_WR the example is :" + str(example))
        class_num = None
        max = 0.0
        degree = None
        class_num = self.default_rule
        for i in range(0,len(self.rule_base_array)):
            rule = self.rule_base_array[i]
            degree = rule.matching(example)

            if degree > max:
                max = degree
                class_num = rule.get_class
        return class_num

    def FRM_AC_one(self,example):
        # int
        class_num = None
        #double
        degree = None
        max_degree = None

        class_num = self.default_rule
        # double array
        degree_class = [0.0 for x in range(self.my_train_dataset.getnClasses())]

        for i in range(0, self.my_train_dataset.getnClasses()):
            degree_class[i] = 0.0

        print("how many rules in rule base is : " +str(len(self.rule_base_array)))
        for i in range(0, len(self.rule_base_array)):
            rule = self.rule_base_array[i]
            print("In FRM_AC_one : " + str(rule.conf))
            degree = rule.matching(example)
            degree_class[rule.get_class()] = degree_class[rule.get_class()] + degree

        max_degree = 0.0
        n_classes = self.my_train_dataset.getnClasses()
        for i in range(0, n_classes):
            if degree_class[i] > max_degree:
                max_degree = degree_class[i]
                class_num = i

        return class_num

    def FRM_AC_two(self,example,selected):
        class_num = None
        degree = None
        max_degree = None
        class_num = self.default_rule
        degree_class = [0.0 for x in range(self.my_train_dataset.getnClasses())]

        for i in range(0, self.my_train_dataset.getnClasses()):
            degree_class[i] = 0.0


        for i in range(0, len(self.rule_base_array)):
            if selected[i] > 0:
                #print(" geneR, selected[" +str(i)+"] : " + str(selected[i]))
                rule = self.rule_base_array[i]
                #print("selected is not None ,rule conf in FRM_AC is : " + str(rule.conf))
                #print(" in FRM_AC the example : " + str(example))
                degree = rule.matching(example)
                degree_class[rule.get_class()] = degree_class[rule.get_class()] + degree

        max_degree = 0.0
        n_classes = self.my_train_dataset.getnClasses()
        for i in range(0, n_classes):
            if degree_class[i] > max_degree:
                max_degree = degree_class[i]
                class_num = i

        return class_num


    """
      /**
     * Indentifies how many classes are uncovered with a selection of rules.
     * @param selected rules selected to be tested
     * @return number of classes uncovered.
     */
    
    """
    def has_class_uncovered(self,selected):
        count = 0
        cover = [0 for x in range(self.my_train_dataset.getnClasses())]
        for i in range(0,len(cover)):
            if self.my_train_dataset.numberInstances(i) >0:
                cover[i] = 0
            else:
                cover[i] = 1

        for i in range(0,len(self.rule_base_array)):
            if selected[i]>0:
                cover[self.rule_base_array[i].get_class()] = cover[self.rule_base_array[i].get_class()] + 1
        count = 0

        for i in range(0,len(cover)):
            if cover[i]==0:
                count = count + 1
        return count


    """
   * Function to eliminate the rules that are not needed (Redundant, not enough accurate,...) for a given class.
   * @param clas class whose rules are being tested
    
    """
    def reduce_rules(self,class_num):
        print("begin the reduce_rules ......")
        # example weight object array
        example_weight_list=[]
        # int
        pos_best_Wracc = None
        nExamples = None
        nRule_select = None
        # double
        best_Wracc = None
        # int array
        selected = []
        # rule object
        rule = None

        for i in range(0,self.my_train_dataset.size()):
            example_weight_list.append(example_weight(self.K))

        selected = [None for x in range(len(self.rule_base_array))]

        for i in range(0,len(self.rule_base_array)):
            selected[i] = 0
        print("class_num pass in reduce rule in rule base is :" + str(class_num))
        nExamples = self.my_train_dataset.numberInstances(class_num)
        nRule_select = 0

        loop_time = 0
        while True:
            loop_time = loop_time +1
            print("begin the loop in the reduce rule")
            best_Wracc = -1.0
            pos_best_Wracc = -1

            for i in range(0,len(self.rule_base_array)):
                if selected[i]==0:
                    rule = self.rule_base_array[i]
                    rule.calculate_Wracc(self.my_train_dataset,example_weight_list)
                    rule_wracc_value =  rule.get_Wracc()
                    print("rule_wracc_value is :"+str(rule_wracc_value))
                    if rule_wracc_value >best_Wracc:
                        best_Wracc = rule.get_Wracc()
                        pos_best_Wracc = i
                        print("pos_best_Wracc is :" + str(pos_best_Wracc))

            if pos_best_Wracc > -1:
                selected[pos_best_Wracc] = 1
                print(" selected[ i ] is :" + str(pos_best_Wracc))
                nRule_select = nRule_select + 1
                rule = self.rule_base_array[pos_best_Wracc]
                nExamples = nExamples - rule.reduce_weight(self.my_train_dataset,example_weight_list)
            #  while ((nExamples > 0) && (nRuleSelect < this.rule_base_array.size()) && (posBestWracc > -1));
            if nExamples >0 and nRule_select< len(self.rule_base_array) and pos_best_Wracc> -1:
                print(" Condition is : (nExamples >0 and nRule_select< len(self.rule_base_array) and pos_best_Wracc> -1)")
                print(" nExamples:"+str(nExamples)+" is not >0")
                print("nRule_select is" +str(nRule_select))
                print("len(self.rule_base_array) is :"+str(len(self.rule_base_array)))
                print(" pos_best_Wracc is :"+str(pos_best_Wracc))
                print("continue the loop in reduce rule......")

            else:
                print(" Condition is : not(nExamples >0 and nRule_select< len(self.rule_base_array) and pos_best_Wracc> -1)")
                print(" nExamples:" + str(nExamples) + " is not >0")
                print("nRule_select is" + str(nRule_select))
                print("len(self.rule_base_array) is :" + str(len(self.rule_base_array)))
                print(" pos_best_Wracc is :" + str(pos_best_Wracc))
                print("break from the loop in reduce rule......")
                break
        print("loop times is : " + str(loop_time))
        for i in range(len(self.rule_base_array)-1,-1,-1):
            print("Decrementing loop : " +str(i))
            if selected[i] == 0:
                print("the rule" + str(i)+ " : will be removed , because the rule.getWracc() not bigger than -1 " + str(self.rule_base_array[i].get_Wracc()))
                self.rule_base_array.pop(i) # remove by index, remove(i) means remove by value
        example_weight_list.clear()
        gc.collect()


    """
    * It prints the whole rule_base_array
    * @return The whole rule_base_array
    """


    def print_string(self):
        ant = 0 # int
        names = self.my_train_dataset.getNames()
        class_array = self.my_train_dataset.getClasses()
        string_out = ""

        for i in range(0,len(self.rule_base_array)):
            rule = self.rule_base_array[i]
            string_out = string_out + str( i + 1 )+ ":"
            for j in range(0,self.n_variables):
                if rule.antecedent[j]>=0:
                    break
            if j<self.n_variables and rule.antecedent[j]>=0:
                string_out = string_out + names[j] + " IS " + rule.dataBase.print_attribute(j,rule.antecedent[j])
                ant = ant + 1
            j=j+1
            for j in range(j,self.n_variables-1):
                if rule.antecedent[j]>=0:
                    string_out = string_out + " AND " + names[j] + " IS " + rule.dataBase.print_attribute(j, rule.antecedent[j])
                    ant = ant + 1
            j=j+1
            if j < self.n_variables and rule.antecedent[j]>=0:
                string_out = string_out +" AND " + names[j] + " IS " + rule.dataBase.print_attribute(j, rule.antecedent[j]) + ": " + class_array[rule.clas]
                ant = ant + 1
            else:
                string_out = string_out + ": " + str(class_array[rule.clas])

            string_out = string_out+ " CF: " + str(rule.getConfidence()) + "\n"



        string_out = string_out + "\n\n"
        string_out = string_out + "@supp and CF:\n\n"
        for i in range(0,len(self.rule_base_array)):
            rule = self.rule_base_array[i]
            string_out = string_out + str(i + 1) + ": "
            string_out = string_out + "supp: " + str(rule.getSupport()) + " AND CF: " + str(rule.getConfidence())+"\n"

        string_out =  "@Number of rules: " + str(len(self.rule_base_array)) + " Number of Antecedents by rule: " + str(ant * 1.0 / len(self.rule_base_array)) + "\n\n" + string_out


        return string_out


    """
    * It stores the rule base in a given file
    * @param filename Name for the rule_base_array file
    """
    def save_file(self,file_name_pass):
        string_out = self.print_string()
        file = open(file_name_pass, "w+")
        file.write(string_out)
        file.close()



    """



         # * Rule Learning Mechanism for the Chi et al.'s method
         # * @param train myDataset the training data-set

    def Generation( self,train) :
            print("In Generation, the size of train is :" +str(train.size()))
            for i in range( 0, train.size()) :
                rule = self.searchForBestAntecedent(train.getExample(i),train.getOutputAsIntegerWithPos(i))
                rule.assingConsequent(train, self.ruleWeight)
                if (not (self.duplicated(rule)) and(rule.weight > 0)):
                    self.ruleBase.append(rule)
         # * This function obtains the best fuzzy label for each variable of the example and assigns
         # * it to the rule
         # * @param example double[] the input example
         # * @param clas int the class of the input example
         # * @return Rule the fuzzy rule with the highest membership degree with the example

    def searchForBestAntecedent(self,example,clas):
            ruleInstance=Rule( )
            ruleInstance.setTwoParameters(self.n_variables, self.compatibilityType)
            print("In searchForBestAntecedent ,self.n_variables is :" + str(self.n_variables))
            ruleInstance.setClass(clas)
            print("In searchForBestAntecedent ,self.n_labels is :" + str(self.n_labels))
            for i in range( 0,self.n_variables):
                max = 0.0
                etq = -1
                per= None
                for j in range( 0, self.n_labels) :
                    print("Inside the second loop of searchForBestAntecedent......")
                    per = self.dataBase.membershipFunction(i, j, example[i])
                    if (per > max) :
                        max = per
                        etq = j
                if (max == 0.0) :
                    print("There was an Error while searching for the antecedent of the rule")
                    print("Example: ")
                    for j in range(0,self.n_variables):
                        print(example[j] + "\t")

                    print("Variable " + str(i))
                    exit(1)

                ruleInstance.antecedent[i] = self.dataBase.clone(i, etq)
            return ruleInstance
         # * It prints the rule base into an string
         # * @return String an string containing the rule base

    def printString(self) :
            i=None
            j= None
            cadena = ""
            cadena += "@Number of rules: " + str(len(self.ruleBase)) + "\n\n"
            for i in range( 0, len(self.ruleBase)):
                rule = self.ruleBase[i]
                cadena += str(i + 1) + ": "
                for j in range(0,  self.n_variables - 1) :
                    cadena += self.names[j] + " IS " + rule.antecedent[j].name + " AND "
                j=j+1
                cadena += self.names[j] + " IS " + rule.antecedent[j].name + ": " + str(self.classes[rule.clas]) + " with Rule Weight: " + str(rule.weight) + "\n"
            print("RuleBase cadena is:" + cadena)
            return cadena

         # * It writes the rule base into an ouput file
         # * @param filename String the name of the output file

    def writeFile(self,filename) :
            outputString = ""
            outputString = self.printString()
            file = open(filename, "w")
            file.write(outputString)
            file.close()
         # * Fuzzy Reasoning Method
         # * @param example double[] the input example
         # * @return int the predicted class label (id)

    def FRM(self,example):
          if (self.inferenceType == Fuzzy_Chi.Fuzzy_Chi.WINNING_RULE):
                return self.FRM_WR(example)
          else :
                return self.FRM_AC(example)

         # * Winning Rule FRM
         # * @param example double[] the input example
         # * @return int the class label for the rule with highest membership degree to the example
    def FRM_WR(self,example):
            clas = -1
            max = 0.0
            for i in range( 0, len(self.ruleBase)):
                rule= self.ruleBase[i]
                produc = rule.compatibility(example)
                produc *= rule.weight
                print("produc: "+ str(produc)+", rule.weight :"+str(rule.weight))
                if (produc > max) :
                    max = produc
                    clas = rule.clas
                    print("max: " + str(max) + ", clas = rule.clas :" + str(clas))
            return clas

     # * Additive Combination FRM
     # * @param example double[] the input example
     # * @return int the class label for the set of rules with the highest sum of membership degree per class

    def FRM_AC(self,example):
         clas = -1
         class_degrees = []
         for i in range( 0, len(self.ruleBase)) :
            rule = self.ruleBase[i]
            produc = rule.compatibility(example)
            produc *= rule.weight
            if (rule.clas > len(class_degrees) - 1) :
                aux = [ 0.0 for x in range (len(class_degrees))]
                for j in range( 0, len(aux)):
                    aux[j] = class_degrees[j]

                class_degrees = [ 0.0 for x in range (rule.clas+1)]
                for j in range( 0,len(aux)):
                    class_degrees[j] = aux[j]

            class_degrees[rule.clas] += produc

         max = 0.0
         for l in range( 0,len(class_degrees)):
            if (class_degrees[l] > max) :
                max = class_degrees[l]
                clas = l

         return clas
    """








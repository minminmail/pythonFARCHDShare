"""

***********************************************************************

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
 * <p>Title: Population</p>
 * <p>Description: Class for the CHC algorithm</p>
 * <p>Copyright: KEEL Copyright (c) 2010</p>
 * <p>Company: KEEL </p>
 * @author Written by Jesus Alcalá (University of Granada) 09/02/2011
 * @version 1.2
 * @since JDK1.6
 */

"""
from individual import individual
import random
class population :
    idivi_list = [] # Individual objects,	Population = new ArrayList<Individual>();

    # double type
    alpha = None
    w1 = None
    L = None
    lini = None
    best_fitness = None
    best_accuracy = None

    # int type
    n_variables = None
    pop_size = None
    maxTrials = None
    nTrials = None
    BITS_GEN = None
    selected = []

    my_train_data_set = None # myDataset
    data_base= None # DataBase
    rule_base =  None # RuleBase

    """
      /**
     * Maximization
     * @param a int first number
     * @param b int second number
     * @return boolean true if a is greater than b
     */
    
    """
    def better (self,a,b):
        if a > b:
            return  True
        return False

    """
     * @param train Training dataset
    * @param dataBase Data Base
    * @param ruleBase Rule set
    * @param size Population size
    * @param BITS_GEN Bits per gen
    * @param maxTrials Maximum number of evaluacions
    * @param alpha Parameter alpha

    """
    def __init__(self,my_train_data_set_pass,data_base_pass,rule_base_pass,size_pass,BITS_GEN_Pass,maxTrials_pass,alpha_pass):

        self.my_train_data_set = my_train_data_set_pass
        self.data_base = data_base_pass
        self.rule_base = rule_base_pass
        print("self.rule_base in init of population has type or not : " + str(self.rule_base))
        self.pop_size = int(size_pass)
        self.BITS_GEN = BITS_GEN_Pass
        self.maxTrials = maxTrials_pass
        self.alpha = alpha_pass

        self.n_variables = data_base_pass.numVariables()
        # ((dataBase.getnLabelsReal() * BITS_GEN) + ruleBase.size()) / 4.0;
        self.lini = (data_base_pass.get_nLabels_real() * float(BITS_GEN_Pass) + rule_base_pass.size())/4.0
        self.L = self.lini
        print(" rule_base_pass.size() is :"+str(rule_base_pass.size()))
        self.w1 = float(self.alpha) * rule_base_pass.size()
        print(" self.w1  is :" + str(self.w1 ))
        self.idivi_list = []
        #selected = new int[this.pop_size];
        self.selected = [None for x in range (int(self.pop_size))]

    # Run the CHC algorithm (Stage 3)

    def generation(self):
        self.init_here()
        self.evaluate(0)

        while True:
            self.selection()
            self.__crossover()
            #print(" the self.pop_size is : " + str(self.pop_size))
            self.evaluate(self.pop_size)
            self.__elitist()

            if not self.__hasNew():
                self.L = self.L - 1
                if self.L < 0.0:
                    self.restart()
            #while (this.nTrials < this.maxTrials);
            if not self.nTrials < int(self.maxTrials):
                break
    def init_here(self):
        #print("init_here,  initial a new indIn clone of individual, copy the self.geneR6 isividual ......")
        ind = individual()
        ind.init_three(self.rule_base, self.data_base, self.w1)
        ind.reset()
        self.idivi_list.append(ind)
        #print("self.pop_size in init_here for add how many individual into idivi_list is :"+ str(self.pop_size))
        for i in range(1,int(self.pop_size)):
            #print("in loop initial a new individual ......")
            ind = individual()
            ind.init_three(self.rule_base, self.data_base, self.w1)
            ind.random_values()
            #print("going to add a new individual ......")
            self.idivi_list.append(ind)
        #print(" how many idividuals were added in self.idivi_list : "+ str(len(self.idivi_list)))
        self.best_fitness = 0.0
        self.nTrials = 0

    def evaluate(self,pos):
        # print("len(self.idivi_list) in evaluate is :" + str(len(self.idivi_list)))
        for i in range(int(pos),len(self.idivi_list)):
            #print(" in evaluate the pos i is :" + str(i))
            #print(" self.idivi_list[i] is : " + str(self.idivi_list[i]))
            self.idivi_list[i].evaluate()
        self.nTrials = self.nTrials +len(self.idivi_list)- int(pos)

    def selection(self):
        aux = None
        random_get = None
        size_here = int(self.pop_size)
        #print(" size_here is : " + str(size_here))
        for i in range(0,size_here):
            self.selected[i] = i

        for i in range (0,size_here):
            random_get = random.randint(0, size_here-1) # should not include size_here, otherwise it will be index out of list
            #print(" random_get is : " + str(random_get))
            aux = self.selected[random_get]
            self.selected[random_get] = self.selected[i]
            self.selected[i] = aux



    def xPC_BLX(self,double_value, son1_individual, son2_individual) :
        son1_individual.xPC_BLX(son2_individual, double_value)

    def Hux(self,son1_individual,son2_individual):
        son1_individual.hux(son2_individual)


    def __crossover(self):

        dist= None #double
        # #Individual
        dad =  None
        mom =  None
        son1 =  None
        son2 =  None

        for i in range( 0, int(self.pop_size),2) :
            dad = self.idivi_list[self.selected[i]]
            mom = self.idivi_list[self.selected[i + 1]]
            dist = float(dad.distHamming(mom, self.BITS_GEN))

            dist = float(dist / 2.0)

            if dist > self.L:
                son1 = dad.clone()
                son2 = mom.clone()

                self.xPC_BLX(1.0, son1, son2)
                self.Hux(son1, son2)
                son1.on_new()
                son2.on_new()

                self.idivi_list.append(son1)
                self.idivi_list.append(son2)

    """
    # To sort the list in place...
    ut.sort(key=lambda x: x.count, reverse=True)

    # To return a new list, use the sorted() built-in function...
    newlist = sorted(ut, key=lambda x: x.count, reverse=True)    
    """
    def __elitist(self):

        self.idivi_list.sort(key = lambda x:x.fitness,reverse= True)
        while len(self.idivi_list) > int(self.pop_size):
            self.idivi_list.pop(int(self.pop_size))

        self.best_fitness = self.idivi_list[0].get_fitness()

    def __hasNew(self):

        # boolean

        state = None
        ind = None # individual
        state = False

        for i in range(0,int(self.pop_size)):

            ind = self.idivi_list[i]
            if ind.is_new():
                ind.off_new()
                state = True
        return state

    def restart(self):
        dist = None
        # Individual
        indivi= None


        self.w1 = 0.0
        #self.idivi_list.sort(key = lambda x:x.fitness)
        #sorted(self.idivi_list)
        self.idivi_list.sort(key=lambda x: x.fitness,reverse= True)
        indivi = self.idivi_list[0].clone()
        """
        for i in range(0,len(indivi.geneR)):
            print("After self.idivi_list[0].clone() the indivi.geneR["+str(i)+"] is "+str(indivi.geneR[i]))
        """
        indivi.set_w1(self.w1)

        self.idivi_list.clear()
        self.idivi_list.append(indivi)

        for i in range(1,self.pop_size):
            indivi = individual()
            indivi.init_three(self.rule_base,self.data_base,self.w1)
            indivi.random_values()
            self.idivi_list.append(indivi)

        self.evaluate(0)
        self.L = self.lini


    """
    * Return the best individual in the population
    * @return Return the rule set of the best individual in the population

    """

    def rulebase_get_bestRB(self):
        rule_base_here= None

        #sorted(self.idivi_list)
        self.idivi_list.sort(key=lambda x: x.fitness,reverse=1)

        num_idivi_list=len(self.idivi_list)
        print("How many idiv in the list is :"+str(num_idivi_list))

        num = len(self.idivi_list[0].geneR)
        for i in range(0,num):
            print("The geneR" + str(i) +"is "+ str(self.idivi_list[0].geneR[i]))

        rule_base_here = self.idivi_list[0].generate_RB()

        return rule_base_here



	





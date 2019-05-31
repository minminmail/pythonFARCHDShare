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

/**
 * <p>Title: Individual</p>
 *
 * <p>Description: This class contains the representation of the individuals of the population (CHC Algorithm)</p>
 *
 * <p>Copyright: Copyright KEEL (c) 2007</p>
 *
 * <p>Company: KEEL </p>
 *
 * @author Written by Jesus Alcalá (University of Granada) 09/02/2011
 * @version 1.0
 * @since JDK1.6
 */
"""
import numpy as np
import random
import math
from RuleBase import RuleBase

class individual:

    gene = [] # double
    # int
    geneR = []
    #double
    fitness = None
    accuracy = None
    w1 = None
    # int
    nGenes = None
    n_e = None
    #RuleBase ruleBase;
    rule_base = None

    """
    * @param ruleBase Rule set
    * @param dataBase Database
    * @param w1 Weight for the fitness function
    */
    """
    def __init__(self):
        self.rule_base = None
        # print(" init with empty parameters in individual")

    def init_three(self,rule_base_pass,data_base_pass,w1_double_pass):
        #print(" init_three in individual")
        self.rule_base = rule_base_pass
        #print("w1_double_pass is :" + str(w1_double_pass) )
        self.w1 = w1_double_pass
        # Negative Infinity
        self.fitness = float('-Inf')
        self.accuracy = 0.0
        self.n_e = 0
        self.nGenes = data_base_pass.get_nLabels_real()
        #print("self.nGenes is :" + str(self.nGenes))

        #this.gene = new double[this.nGenes];
        if self.nGenes > 0:
            self.gene = [None for x in range(self.nGenes)] # float
        # this.geneR = new int[this.ruleBase.size()];
        #print("self.rule_base.size() is :" +str(self.rule_base.size()))
        self.geneR = [None for x in range(self.rule_base.size())] # int

    """
       * Clone Function
       * @return Copy of the Individual object.
    """

    def clone(self):
        # print("in clone inital a new individual.....")
        indivi = individual()
        indivi.rule_base = self.rule_base
        indivi.w1 = self.w1
        indivi.fitness = self.fitness
        indivi.accuracy = self.accuracy
        indivi.n_e = self.n_e
        indivi.nGenes = self.nGenes
        if self.nGenes > 0:
            indivi.gene = [None for x in range(self.nGenes)]
            for j in range(0,self.nGenes):
                indivi.gene[j] = self.gene[j]
        """
          	ind.geneR = new int[this.geneR.length];
            for (int j = 0; j < this.geneR.length; j++)  ind.geneR[j] = this.geneR[j];   
        """
        indivi.geneR = [None for x in range(len(self.geneR))]
        for i in range(0,len(self.geneR)):
            #print("In clone of individual, copy the self.geneR" +str(i)+" is :"+str(self.geneR[i]))
            indivi.geneR[i] = self.geneR[i]

        return indivi

    # Resets the gene with the same value
    def reset(self):
        if self.nGenes > 0:
            for i in range(0,self.nGenes):
                self.gene[i]=0.5
            for i in range(0,len(self.geneR)):
                self.geneR[i]= 1

    #Initialization of the individual with random values
    def random_values(self):
        #print("In random_values ,self.nGenes is "+str(self.nGenes))
        if self.nGenes > 0:

            for i in range(0,self.nGenes):
                self.gene[i] = random.random()
                #print("first set with random.random, gene["+str(i)+"] is: " + str(self.gene[i]))
                #print("self.gene["+str(i)+"] is " + str(self.gene[i]))
        for i in range(0,len(self.geneR)):
            if random.random() < 0.5:
                #print("second time set, with random < 0.5, set with random.random, geneR[" + str(i) + "] is: " + str(self.gene[i]))
                self.geneR[i] =0
            else:
                #print("second time set, with random >= 0.5,, geneR[" + str(i) + "] is: " + str(self.gene[i]))
                self.geneR[i] = 1

    """
       * It returns the number of rules in the rule base
       * @return int Rule base's size
    
    """
    def size(self):
        return len(self.geneR)

    """
    
        /**
         * Returns the number of genes selected.
         * @return the number of genes selected.
         */
    """
    def get_nSelected(self):
        count = 0
        # print("self.geneR is: " +str(self.geneR))
        for i in range(0,len(self.geneR)):
            if self.geneR[i]>0:
                count = count +1
        return count

    """"
    
       * Function to return if this individual is new in the population
       * @return boolean true = it is-, false = it isn't
    
    """
    def is_new(self):
        return self.n_e == 1
    # Modifies the new flag to true.

    def on_new(self):
        self.n_e = 1

    """
         * Modifies the new flag to false. 
    """
    def off_new(self):
        self.n_e = 0

    """
        /**
         * Sets the value of w1 with the given argument. 
         * @param value value given to set w1.
    
    """
    def set_w1(self,value_double_pass):
        #print("In set_w1 , the value_double_pass is : " + str(value_double_pass))
        self.w1 = value_double_pass

    """
       * Function to return the accuracy of the individual
       * @return double The accuracy of the individual
    
    """
    def get_accuracy(self):
        return self.accuracy


    """
       * Function to return the fitness of the individual
       * </p>
       * @return double The fitness of the individual
    """
    def get_fitness(self):
        return self.fitness

    def StringRep(self,indiv, BITS_GEN):

        pos = None
        length = None
        count = None

        n = None # long
        last_char = None
        INCREMENTO = None # float


        length = int(self.nGenes) * int(BITS_GEN)
        stringIndiv1 = ['' for x in range(length) ]
        stringIndiv2 = ['' for x in range(length) ]
        stringAux = ['' for x in range(length) ]

        INCREMENTO = float(1.0 / (math.pow(2.0, float(BITS_GEN)) - 1.0))
        pos = 0
        for i in range(0,self.nGenes):
            n = int(self.gene[i]/ INCREMENTO+0.5)
            for j in range(int(BITS_GEN)-1,-1,-1):
                stringAux[j] = str(0 + (n & 1))
                n >>=1
        last = '0'

        for j in range(0,int(BITS_GEN)):
            if stringAux[j]!=last:
                stringIndiv1[pos] = str(0 + 1)
            else:
                stringIndiv1[pos] = str(0 + 0)
                last = stringAux[j]
            pos = pos + 1
        pos = 0
        for i in range(0,self.nGenes):
            n = int(indiv.gene[i]/INCREMENTO + 0.5)

            for j in range(int(BITS_GEN) - 1,-1,-1):
                stringAux[j] = str(0+(n & 1)) # str(n & 1)
                n >>=1
        last = '0'
        for i in range(0,int(BITS_GEN)):
            if stringAux[i]!= last:
                stringIndiv2[pos] =str(0 + 1) # '0' + str(1)
            else:
                stringIndiv2[pos] =str(0 + 0) #'0' + str(0)
            last = stringAux[i]
            pos = pos + 1
        count = 0
        for i in range(0,length):
            if stringIndiv1[i]!=stringIndiv2[i]:
                count = count + 1
        return count

    """
       /**
         * Computes the Hamming distance with the Individual given as a argument.
         * In case a transformation from float representation to string is needed, the argument BITS_GEN will guide the process.
         * @param ind Individual given to compute the distance.
         * @param BITS_GEN Number of bits to guide the transformation of representation.
         * @return Hamming distance with the Individual given.
         */
         
         
    """
    def distHamming(self,indivi, BITS_GEN):
        count = 0
        for i in range(0,len(self.geneR)):
            if self.geneR[i] !=indivi.geneR[i]:
                count = count + 1

        if self.nGenes >0:
            count = count + self.StringRep( indivi, BITS_GEN)
        return count

    """
          /**
     * Crosses the individuals using the HUX operator.
     * Exactly half of the different bits are flipped.
     * The results are stored in each Individual object, the method caller and the argument.
     * @param indiv Individual to cross with.
     */
     """
    """
		 

    
    """
    # Individual indiv
    def hux(self,indiv):

        # int ,	 int i, dist, random, aux, nPos;
        i = None
        dist = None
        random_here = None
        aux = None
        n_pos = None

        # int array,	 int [] position
        # position = new int[this.geneR.length];
        position = [None for i in range(len(self.geneR))]
        dist = 0


        for i in range(0,len(self.geneR)):
            if self.geneR[i]!=indiv.geneR[i]:
                position[dist] = i
                #print("position[" + str(i) + "]:" + str(position[dist]))
                dist = dist + 1



        #print("dist is :"+str(dist))
        n_pos = int(dist/2)
        #print("n_pos is :" + str(n_pos))

        for i in range(0,n_pos):
            random_here = random.randint(0,dist-1)
            #print("random_here is :" + str(random_here))
            #print("position[random_here] is :"+str(position[random_here]))
            aux = self.geneR[position[random_here]]
            #print(" self.geneR[position[random_here]] is :" + str(aux))
            #print("position[random_here] is " + str(position[random_here]))
            self.geneR[position[random_here]] =  indiv.geneR[position[random_here]]
            #print("self.geneR[position[random_here]]  is " + str(self.geneR[position[random_here]]))
            indiv.geneR[position[random_here]] = aux
            dist = dist - 1

            aux = position[dist]
            #print("aux =position[dist],:" + str(position[dist]))
            position[dist]=position[random_here]
            position[random_here] =  aux

        """
         * Crosses the individuals using the BLX operator.
         * The results are stored in each Individual object, the method caller and the argument.
         * @param indiv Individual to cross with.
         * @param d proportion of the diference of each gene that BLX will allow to exceed.
        """
    def xPC_BLX(self, indiv, double_value_pass):
            i_double = None
            a1_double = None
            c1_double = None

            for i in range(0,self.nGenes):
                i_double = double_value_pass * math.fabs(self.gene[i]-indiv.gene[i])
                a1_double = self.gene[i]-i_double

                if a1_double < 0.0 :
                    a1_double = 0.0

                c1_double = self.gene[i] + i_double

                if c1_double > 1.0 :
                    c1_double = 1.0
                self.gene[i] = a1_double + random.random()*(c1_double - a1_double)

                a1_double = indiv.gene[i]-i_double
                if a1_double <0.0:
                    a1_double = 0.0
                c1_double = indiv.gene[i]+i_double
                if c1_double > 1.0 :
                    c1_double = 1.0
                indiv.gene[i] = a1_double + random.random()* (c1_double-a1_double)

    """
         * Generates the Rule Base with adjusted to the optimization done.
         * @return RuleBase The whole FARCHD rule set
    
    """

    def generate_RB(self):
        #int

        rule_base = self.rule_base.clone()
        rule_base.evaluate_selected_rules(self.gene,self.geneR)
        rule_base.set_default_rule()

        # for (i=geneR.length - 1; i >= 0; i--) {
        for i in range( len(self.geneR)-1,-1,-1):
            print("self.geneR["+str(i)+"] in generate_RB is : " +str(self.geneR[i]))
            if self.geneR[i] < 1:
                rule_base.remove(i)

        return rule_base

    """
     Evaluate this individual (fitness function)
    """
    def evaluate(self):

        self.rule_base.evaluate_selected_rules(self.gene,self.geneR)
        self.accuracy = self.rule_base.get_accuracy()
        #  this.fitness = this.accuracy - (this.w1 / (this.ruleBase.size() - this.getnSelected() + 1.0)) - (5.0 * this.ruleBase.getUncover()) - (5.0 * this.ruleBase.hasClassUncovered(this.geneR));
        # print("self.w1 is :" + str(self.w1))
        temp1= float(self.w1)/(self.rule_base.size()- int(self.get_nSelected()) + 1.0)
        temp2=5.0*self.rule_base.get_uncover()
        temp3=5.0 * self.rule_base.has_class_uncovered(self.geneR)
        self.fitness = self.accuracy - temp1-temp2-temp3

    """
      /**
       * It interchanges the values between the position pointCross1 and pointCross2
       * @param indiv Inidividual an individual
       * @param pointCross1 int left posotion
       * @param pointCross2 int right posotion
       */
    """
    def interchange_values(self,indiv_object,point_cross1_int, point_cross2_int):
        aux = None
        for i in range(point_cross1_int,point_cross2_int):
            aux = self.chromosome[i]
            self.chromosome[i] =  indiv_object.chromosome[i]
            indiv_object.chromosome[i] = aux
        self.n_e = 1
        indiv_object.n_e = 1

    """
      /**
       * <p>
       * It returns the number of rules in the rule base
       * </p>
       * @return int Rule base's size
       */
    
    """
    def size(self):
        return len(self.chromosome)
    """
       * It applies the mutation operator
       * @param prob Probability that a chromosome has to mutate.
    """
    def mutation(self,prob_double):
        for i in range(0,len(self.chromosome)):
            if random.random() < prob_double:
                if self.chromosome[i]==0:
                    self.chromosome[i] = 1
                else:
                    self.chromosome[i] = 0
                self.n_e = 1


    """
      /**
       * Function to return if this individual is new in the population
       * @return boolean true = it is-, false = it isn't
       */
    
    """
    def is_new(self):
        if self.n_e == 1:
            return True
        else:
            return False
    """
       * Function to return the accuracy of the individual
       * @return double The accuracy of the individual
    """
    def get_accuracy(self):
        return self.accuracy

    """
       * Function to return the fitness of the individual
       * @return double The fitness of the individual
    """
    def get_fitness(self):
        return self.fitness
    """
     /**
       * Function to return the minimum support of the individual
       * @return double The minimum support of the individual  
    """
    def get_MinFS(self):
        minFS = 0.0
        i = 0

        for j in range(self.lengthSC-1,-1,-1):
            if self.chromosome[i]>0:
                minFS = minFS + math.pow(2.0,j)
            i =  i + 1

        minFS = minFS /math.pow(2.0, self.lengthSC)

    """
      /**
       * Function to return the minimum confidence of the individual
       * @return double The minimum confidence of the individual
       */
    """
    def get_minFC(self) :

        minFC = 0.0
        i = self.lengthSC

        for j in range(self.lengthSC-1,-1,-1):
            if self.chromosome[i] > 0:
                minFC = minFC + math.pow(2.0,j)
            i = i + 1

        minFC = minFC / math.pow(2.0,self.lengthSC)

        return minFC

        """
       * Function to compare objects of the Individual class
       * Necessary to be able to use "sort" function
       * It sorts in an increasing order of fitness
       * @param a Individual to be compared.
        
        """
    def compare_to(self, object_a):
            if object_a.fitness < self.fitness:
                return -1
            elif object_a.fitness > self.fitness:
                return 1
            else:
                return 0

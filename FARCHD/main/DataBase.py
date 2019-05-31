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
 * <p>Title: DataBase</p>
 * <p>Description: Fuzzy Data Base</p>
 * <p>Copyright: Copyright KEEL (c) 2008</p>
 * <p>Company: KEEL </p>
 * @author Written by Jesus Alcalá (University of Granada) 09/02/2011
 * @version 1.0
 * @since JDK1.6
 */

"""

import numpy as np
from Fuzzy import Fuzzy
import math

class DataBase :

    n_variables = None # int
    partitions = None #int
    nLabels = [] #int array
    varReal = [] #boolean array
    dataBase = [] # fuzzy array
    dataBaseIni = [] # fuzzy array
    names = [] # str array

    """
    /**
    * This method builds the database, creating the initial linguistic partitions
    * @param nLabels Number of Linguistic Values
    * @param train Training dataset
    */
    """

    def __init__(self, nlabelsPass, train_myDataSet):
        print("nlabelsPass is :"+str(nlabelsPass))
        #double variables
        mark = None
        value = None
        rank = None
        labels = None

        ranks = train_myDataSet.returnRanks() # double array
        self.n_variables = train_myDataSet.getnInputs()
        self.names = train_myDataSet.getNames()
        #print("DataBase init self.names =" + self.names)
        self.nLabels = [None for x in range(self.n_variables)] # int array
        self.varReal = [None for x in range(self.n_variables)] # boolean array
        for i in range (0, self.n_variables):
            self.dataBase.append([]) # fuzzy array
            self.dataBaseIni.append([]) # fuzzy array
        """
        column=len(train_myDataSet.returnRanks()[0])
        row = len(train_myDataSet.returnRanks())
        print("column is:" +str(column)+"row is : "+str(row))


        for i in range (0,row):
            for j in range(0,column):
                #ranks[i][j]=train_myDataSet.returnRanks()[i][j]
                value = ranks[i][j]
                print("rank [" + str(i)+"]" + "[" + str(j) + "]" + str(value))

         """

        """
        this.dataBase = new Fuzzy[this.n_variables][];
        this.dataBaseIni = new Fuzzy[this.n_variables][];    
        """

        print("loop n_variables is " + str(self.n_variables))

        for i in range (0, self.n_variables):
            rank = float(math.fabs(ranks[i][1]- ranks[i][0]))
            if i==4:
                print("when i equal to 4, the rank is :"+ str(rank))
            if i==3:
                print("when i equal to 3, the rank is :"+ str(rank))
            self.varReal[i] = False

            if train_myDataSet.isNominal(i):
                self.nLabels[i] = int(rank) + 1
            elif train_myDataSet.isInteger(i) and ((int(rank)+1)<=nlabelsPass):
                self.nLabels[i] = int(rank) + 1
            else:
                self.nLabels[i] = nlabelsPass
                self.varReal[i] = True

            print("self.nLabels[i]"+str(self.nLabels[i]))

            self.dataBase[i] = [Fuzzy() for x in range (int(self.nLabels[i]))]
            self.dataBaseIni[i] = [Fuzzy() for x in range(int(self.nLabels[i]))]

            mark = float(rank /(float(self.nLabels[i])-1.0))
            print("rank is :"+str(rank))
            print("mark is :"+str(mark))


            for j in range(0,int(self.nLabels[i])):
                self.dataBase[i][j] = Fuzzy()
                self.dataBaseIni[i][j] = Fuzzy()
                value = ranks[i][0] + mark * (j-1)
                print("value is :"+str(value))
                #print("float issue i is :" + str(i) + "j is :" +str(j))
                self.dataBase[i][j].x0 = self.setValue(value,ranks[i][0],ranks[i][1])
                self.dataBaseIni[i][j].x0 = self.dataBase[i][j].x0
                print("self.dataBase[i][j].x0 :" + str(i) + "j is :" + str(j)+ "x0 is : "+str(self.dataBase[i][j].x0))

                value = ranks[i][0] + mark * j
                print("value is :" + str(value))
                self.dataBase[i][j].x1 = self.setValue(value, ranks[i][0], ranks[i][1])
                self.dataBaseIni[i][j].x1 = self.dataBase[i][j].x1
                #print("self.dataBase[i][j].x1 :" + str(i) + "j is :" + str(j) + "x1 is : " +str(self.dataBase[i][j].x1))

                value = ranks[i][0] + mark * (j+1)
                print("value is :" + str(value))
                self.dataBase[i][j].x3 = self.setValue(value, ranks[i][0], ranks[i][1])
                self.dataBaseIni[i][j].x3 = self.dataBase[i][j].x3
                #print("self.dataBase[i][j].x3 :" + str(i) + "j is :" + str(j)  + "x3 is : " +str(self.dataBase[i][j].x3))

                self.dataBase[i][j].y = 1.0
                self.dataBaseIni[i][j].y = self.dataBase[i][j].y

                self.dataBase[i][j].name = "L_" + str(j)+" ("+ str(self.nLabels[i])+ ") "
                #print("self.dataBase[i][j].name is :"+str(self.dataBase[i][j].name))
                self.dataBaseIni[i][j].name = self.dataBase[i][j].name

    def setValue(self, val_pass, min_pass,tope_pass):

            #print("setValue begin...")
            if val_pass> (min_pass- (10**-4)) and val_pass < (min_pass + (10**-4)):
                return min_pass
            if val_pass > (tope_pass -(10**-4)) and val_pass < (tope_pass +(10**-4) ):
                return tope_pass
            return val_pass

    """
           for compare with Chi-W


            self.n_variables = int(n_variables)
            self.n_labels = int(n_labels)
            print("self.n_variables: "+ str(self.n_variables)+" self.n_labels : "+str(self.n_labels))
            #First columns , Second rows
            self.dataBase = [[Fuzzy() for y in range(self.n_labels)] for x in range (self.n_variables)]
            self.dataBase = np(self.dataBase )
            self.names = names

            rangos=np(rangos)
            marca=0.0

            for  i in range(0,self.n_variables):
                print("i= " + str(i))
                marca = (float(rangos[i][1]) - float(rangos[i][0])) / ( float(n_labels) - 1)
                if marca == 0: #there are no ranges (an unique valor)
                    print("Marca =0 in DataBase init method...")

                    for etq in range(0,self.n_labels):
                        print("etq= " + str(etq))
                        self.dataBase[i][etq] =  Fuzzy()
                        self.dataBase[i][etq].x0 = rangos[i][1] - 0.00000000000001
                        self.dataBase[i][etq].x1 = rangos[i][1]
                        self.dataBase[i][etq].x3 = rangos[i][1] + 0.00000000000001
                        self.dataBase[i][etq].y = 1
                        self.dataBase[i][etq].name = "L_" + str(etq)
                        self.dataBase[i][etq].label = etq

                else:
                    print("Marca !=0 in DataBase init method...")
                    print("n_labels = "+n_labels)
                    for etq in range(0, int(n_labels)):
                        print(" i = " + str(i) + ",etq = " + str(etq))
                        self.dataBase[i][etq].x0 = rangos[i][0] + marca * (etq - 1)
                        self.dataBase[i][etq].x1 = rangos[i][0] + marca * etq
                        self.dataBase[i][etq].x3 = rangos[i][0] + marca * (etq + 1)
                        self.dataBase[i][etq].y = 1
                        self.dataBase[i][etq].name = ("L_" + str(etq))
                        self.dataBase[i][etq].label = etq
    """

    """
    /**
     * Decode the gene representation for the GA into the DataBase one based on the Triangular Membership Functions 
     * @param gene Gene representation of the individual being decoded.
     */
    """
    def decode(self,gene_arry):
        #print("begin decode...")
        pos = 0
        displacement = None # double

        for i in range(0,self.n_variables):
            if self.varReal[i]:
                for j in range(0,int(self.nLabels[i])):

                    if j==0:
                        displacement = (gene_arry[pos]-0.5)*(self.dataBaseIni[i][j+1].x1-self.dataBaseIni[i][j].x1)
                    elif j== int(self.nLabels[i])-1 :
                        displacement = (gene_arry[pos] - 0.5) * (self.dataBaseIni[i][j].x1 - self.dataBaseIni[i][j - 1].x1)
                    else:
                        if (gene_arry[pos] - 0.5) < 0.0:
                            displacement = (gene_arry[pos] - 0.5) * (self.dataBaseIni[i][j].x1 - self.dataBaseIni[i][j - 1].x1)
                        else:
                            displacement = (gene_arry[pos] - 0.5) * (self.dataBaseIni[i][j+1].x1 - self.dataBaseIni[i][j].x1)

                    self.dataBase[i][j].x0 = self.dataBaseIni[i][j].x0 + displacement
                    #print("decode, self.dataBase[i][j].x0" +str(self.dataBase[i][j].x0))
                    self.dataBase[i][j].x1 = self.dataBaseIni[i][j].x1 + displacement
                    #print("self.dataBase[i][j].x1" + str(self.dataBase[i][j].x1))
                    self.dataBase[i][j].x3 = self.dataBaseIni[i][j].x3 + displacement
                    #print("self.dataBase[i][j].x3" + str(self.dataBase[i][j].x3))
                    pos = pos + 1

    # '''
    #      * @return int the number of input variables
    # '''
    def numVariables(self):
        return self.n_variables

    """
     * Returns the number of total real labels held by the input attributes.
     * @return The number of real labels
    """
    def get_nLabels_real(self):
        count = 0
        for i in range(0,self.n_variables):
             if self.varReal[i]:
                 count = count + int(self.nLabels[i])

        return count


     # '''
     #     * @return int the number of fuzzy labels
     # '''
    def numLabels(self, variable_pass):
        return self.nLabels[variable_pass]


    """
    * It return the whole array of number of labels for every attribute
    * @return the whole array of number of labels for every attribute 
    """
    def get_nLabels(self):
      return self.nLabels

    """
   * Checks if the value of a specific label in a specific attribute matchs with a given value
   * </p>
   * @param variable Attribute which we are going to check
   * @param label Attribute's label we are going to check
   * @param value Value to be compared
   * @return int 1 = Don't care, [0.0,1.0] = another one.
    
    """
    def matching(self,variable_int,lable_int,value_double):
        if value_double < 0 or lable_int < 0:
            return 1
        else :
            return self.dataBase[variable_int][lable_int].fuzzification(value_double)
    """ 
    /**
     * Return a String representation of the Triangular Membership Functions of the variable and its label given as arguments. 
     * @param var Index of the variable given.
     * @param label Index of the label given.
     * @return String representation of the Triangular Membership Function.
     */
    public String print_triangle(int var, int label) {
    String cadena = new String("");

	Fuzzy d = this.dataBase[var][label];

    cadena = d.name + ": \t" + d.x0 + "\t" + d.x1 + "\t" + d.x3 + "\n";
    return cadena;
  }
    """
    def print_triangle(self,var_int_pass,lable_int_pass):
        cadena = ""
        fuzzy = self.dataBase[var_int_pass][lable_int_pass]

        cadena = fuzzy.name + ": \t" +fuzzy.x0 + "\t"+fuzzy.x1+"\t"+fuzzy.x3+"\n"
        return cadena

    """
    * It prints an attribute with its label in a string way
    * @param var Attribute to be printed
    * @param label Attribute's label to be printed
    * @return A string which represents the "string format" of the given input
   
    original function name is print. Changed it because python use print as keyword
    """
    def print_attribute(self,var_int_pass,lable_int_pass):
        return self.dataBase[var_int_pass][lable_int_pass].get_Name()

    """
       * It prints the whole database
       * @return The whole database
    
    """
    def print_string(self):

        string_all = "@Using Triangular Membership Functions as antecedent fuzzy sets"
        for i in range(0,self.n_variables):
            string_all = string_all + "\n\n @Number of Labels in Variable " + str(i+1) + ": " + self.nLabels[i]
            string_all = string_all + "\n" + self.names[i] + ":\n"
            for j in range(0,int(self.nLabels[i])):
                string_all = string_all + self.dataBase[i][j].name + ": (" + str(self.dataBase[i][j].x0) + "," + str(self.dataBase[i][j].x1) + "," + str(self.dataBase[i][j].x3) + ")\n"
        return string_all

    """
    * It stores the data base in a given file
    * @param filename Name for the database file
    """
    def save_file(self,file_name_pass):
        string_out = self.print_string()
        print("save lables print_string in file")
        file = open(file_name_pass,"w+")
        file.write(string_out)
        file.close()

    """
    # '''
    #      * It computes the membership degree for a input value
    #      * @param i int the input variable id
    #      * @param j int the fuzzy label id
    #      * @param X double the input value
    #      * @return double the membership degree
    #      */
    # '''
    def  membershipFunction(self,i, j, X):
            print("len(self.dataBase[0])"+str(len(self.dataBase)))
            value = self.dataBase[i][j].setX(X)
            print("Get value form Fuzzy setX is :" + str(value))
            return value
 
    # '''
    #      * It makes a copy of a fuzzy label
    #      * @param i int the input variable id
    #      * @param j int the fuzzy label id
    #      * @return Fuzzy a copy of a fuzzy label
    # '''
    def clone(self,i, j) :
            return self.dataBase[i][j]
    
    # '''
    #      * It prints the Data Base into an string
    #      * @return String the data base
    # '''
    def printString(self) :
            cadena =  "@Using Triangular Membership Functions as antecedent fuzzy sets\n"
            cadena += "@Number of Labels per variable: " + str(self.n_labels) + "\n"
            numrows=len(self.dataBase)
            print("numrows: " + str(numrows))
            numcols=len(self.dataBase[0])

            print("numrows: " + str(numrows) + "numcols:"+ str(numcols))
            if(self.dataBase.size!=0):
                print("cadena: "+cadena)
                for i in range(0, self.n_variables):
                    print("i = " + str(i))
                    print("cadena: " + cadena)
                    cadena += "\n" + self.names[i] + ":\n"
                    for j in range(0, self.n_labels):
                        print("i = " + str(i))
                        cadena += " L_" + str(int(j + 1)) + ": (" + str(self.dataBase[i][j].x0) +  "," + str(self.dataBase[i][j].x1) + "," + str(self.dataBase[i][j].x3) + ")\n"
            else:
                print("self.dataBase is None")

            return cadena

    # '''
    #      * It writes the Data Base into an output file
    #      * @param filename String the name of the output file
    # '''
    def writeFile(self,filename):

            file=open(filename, "w")
            outputString = self.printString()
            file.write(outputString)
            file.close()
    
    """
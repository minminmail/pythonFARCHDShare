
#***********************************************************************

	# This file is part of KEEL-software, the Data Mining tool for regression,
	# classification, clustering, pattern mining and so on.
    #
	# Copyright (C) 2004-2010
    #
	# F. Herrera (herrera@decsai.ugr.es)
    # L. Sánchez (luciano@uniovi.es)
    # J. Alcalá-Fdez (jalcala@decsai.ugr.es)
    # S. García (sglopez@ujaen.es)
    # A. Fernández (alberto.fernandez@ujaen.es)
    # J. Luengo (julianlm@decsai.ugr.es)
    #
	# This program is free software: you can redistribute it and/or modify
	# it under the terms of the GNU General Public License as published by
	# the Free Software Foundation, either version 3 of the License, or
	# (at your option) any later version.
    #
	# This program is distributed in the hope that it will be useful,
	# but WITHOUT ANY WARRANTY; without even the implied warranty of
	# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	# GNU General Public License for more details.
    #
	# You should have received a copy of the GNU General Public License
	# along with this program.  If not, see http://www.gnu.org/licenses/

#**********************************************************************/
from DataBase import DataBase
from RuleBase import RuleBase
from MyDataSet import MyDataSet
from apriori import apriori
from population import population
import time
import random
 # * <p>It contains the implementation of the Chi algorithm</p>
 # *
 # * @author Written by Jesus Alcala (University of Granada) 09/02/2011
 # * @version 1.0
 # * @since JDK1.5

class FARC_HD:

# MyDataSet
  train_myDataSet = None
  val_myDataSet = None
  test_myDataSet = None

#String variants
  outputTr=""
  outputTst=""
  fileDB=""
  fileRB=""
  fileTime=""
  fileHora=""
  data=""
  fileRules = ""
  evolution = ""
# long int variants
  rules_stage1 = None
  rules_stage2 = None
  rules_stage3 = None
  startTime = None
  total_time = None # long

  dataBase=None # DataBase object
  ruleBase=None # RuleBase object
  apriori_instance = None #Apriori
  pop = None #Population
#  int variants
  nLabels= None
  population_size = None
  depth = None
  k = None
  maxTrials = None
  typeInference = None
  BITS_GEN = None

#  double variants
  minsup = None
  maxconf = None
  alpha = None

  somethingWrong = False #to check if everything is correct.
 #  Default constructor

       # * It reads the data from the input files (training, validation and test) and parse all the parameters
       # * from the parameters array.
       # * @param parameters parseParameters It contains the input files, output files and parameters

  def __init__(self,parameters):
        print("__init__ of FARC_HD begin...")

        self.startTime = time.time()
        self.train_myDataSet = MyDataSet()
        self.val_myDataSet = MyDataSet()
        self.test_myDataSet = MyDataSet()

        try:
          print("Reading the training set: ")
          inputTrainingFile= parameters.getInputTrainingFiles()
          print("In Fuzzy Chi init method the training file is :" + inputTrainingFile)
          self.train_myDataSet.readClassificationSet(inputTrainingFile, True)
          print(" ********* train_myDataSet.myDataSet readClassificationSet finished !!!!!! *********")

          print("Reading the validation set: ")
          inputValidationFile=parameters.getValidationInputFile()
          self.val_myDataSet.readClassificationSet(inputValidationFile, False)
          print(" ********* val_myDataSet.myDataSet readClassificationSet finished !!!!!! *********")

          print("Reading the test set: ")
          self.test_myDataSet.readClassificationSet(parameters.getInputTestFiles(), False)
          print(" ********* test_myDataSet.myDataSet readClassificationSet finished !!!!!! *********")

        except IOError as ioError :
            print ("I/O error: "+ str(ioError))
            self.somethingWrong = True
        except Exception as e:
            print("Unexpected error:" + str(e))
            self.somethingWrong = True
        #
        #     #We may check if there are some numerical attributes, because our algorithm may not handle them:
        #     #somethingWrong = somethingWrong || train.hasNumericalAttributes();
        print(" ********* Three type of myDataSet readClassificationSet finished !!!!!! *********")
        self.somethingWrong = self.somethingWrong or self.train_myDataSet.hasMissingAttributes()

        self.outputTr = parameters.getTrainingOutputFile()
        self.outputTst = parameters.getTestOutputFile()

        self.fileDB = parameters.getOutputFile(0)
        self.fileRB = parameters.getOutputFile(1)

        self.data = parameters.getInputTrainingFiles()
        output_file_str= parameters.getOutputFile(1)
        print("output_file_str is " + output_file_str)
        last_index_slash= output_file_str.rindex('.txt')
        print("last_index_slash is " + str(last_index_slash))
        front_file_name = output_file_str[0:int(last_index_slash)]
        self.fileTime = front_file_name + "time.txt"
        self.fileHora = front_file_name + "hora.txt"
        self.fileRules = front_file_name + "rules.txt"

        # Now we parse the parameters

        seed = parameters.getParameter(0)[1]
        print("parameter 0 seed is :" + str(seed))

        self.nLabels = parameters.getParameter(1)[1]
        print("parameter 1 nLabels is :" + str(self.nLabels))

        self.minsup = parameters.getParameter(2)[1]
        print("parameter 2 minsup is :" + str(self.minsup))

        self.maxconf = parameters.getParameter(3)[1]
        print("parameter 3 maxconf is :" + str(self.maxconf))

        self.depth = parameters.getParameter(4)[1]
        print("parameter 4 Depth of the trees is :" + str(self.depth))

        self.k = parameters.getParameter(5)[1]
        print("parameter 5 k is :" + str(self.k))

        self.maxTrials = parameters.getParameter(6)[1]
        print("parameter 6 maxTrials is :" + str(self.maxTrials))

        self.population_size = parameters.getParameter(7)[1]
        print("parameter 7 population_size is :" + str(self.population_size))


        if int(self.population_size) % 2 >0:
            self.population_size = self.population_size + 1


        self.alpha = parameters.getParameter(8)[1]
        print("parameter 8 alpha is :" + str(self.alpha))

        self.BITS_GEN = parameters.getParameter(9)[1]
        print("parameter 9 BITS_GEN is :" + str(self.BITS_GEN))

        self.typeInference = parameters.getParameter(10)[1]
        print("parameter 10 typeInference is :" + str(self.typeInference))

        random.seed(seed)


            #It launches the algorithm
  def execute(self) :
    if self.somethingWrong : #We do not execute the program
      print("An error was found, the data-set have missing values")
      print("Please remove those values before the execution")
      print("Aborting the program")
      #We should not use the statement: System.exit(-1);
    else :
      #We do here the algorithm's operations
      print("No errors, Execute in FARCHD execute :")
      self.dataBase = DataBase(self.nLabels,self.train_myDataSet)
      self.ruleBase = RuleBase(self.dataBase,self.train_myDataSet,self.k,self.typeInference)
      print("dataBase, ruleBase initialized , Execute in FARCHD execute :")
      self.apriori_instance = apriori()
      self.apriori_instance.init_with_more_parameters(self.ruleBase,self.dataBase,self.train_myDataSet,self.minsup,self.maxconf,self.depth)
      self.apriori_instance.generate_RB()
      print("dataBase, ruleBase initialized , Execute in FARCHD execute :")

      self.rules_stage1 = self.apriori_instance.get_rules_stage1()
      print("FARC_HD,rules_stage1,is :" + str(self.rules_stage1))
      self.rules_stage2 = self.ruleBase.size()
      print("FARC_HD,rules_stage2,is :" + str(self.rules_stage2))

      print("self.ruleBase in FARC_HD execute, pass into population :" + str(self.ruleBase))
      pop = population(self.train_myDataSet,self.dataBase,self.ruleBase,self.population_size,self.BITS_GEN,self.maxTrials,self.alpha)
      pop.generation()

      print("Building classifier ......")
      self.ruleBase = pop.rulebase_get_bestRB()
      print("FARC_HD,rule stage3, FARC_HD ruleBase.size() is :" + str(self.ruleBase.size()))
      self.rules_stage3 = self.ruleBase.size()

      self.dataBase.save_file(self.fileDB)
      self.ruleBase.save_file(self.fileRB)

      self.doOutput(self.val_myDataSet,self.outputTr)
      self.doOutput(self.test_myDataSet,self.outputTst)

      self.total_time= time.time() -self.startTime
      self.write_time()
      self.write_rules()

      print(" FARC_HD algorithm is finished . ")
  """
     /**
     * Add all the rules generated by the classifier to fileRules file.
     */
  """
  def write_rules(self):

      string_out = "" + str(self.rules_stage1) + " " + str(self.rules_stage2) + " " + str(self.rules_stage3 )+ "\n"
      file_here = open(self.fileRules,'a+')
      file_here.write(string_out)
      file_here.close()


  #It add the runtime to fileHora file.)
  def write_time(self):
      aux = None
      second_here = None
      min_here = None
      hour_here = None
      string_out = ""+ str(self.total_time/1000) + "  " + self.data + "\n"

      file_hora = open(self.fileHora, "a+")
      file_hora.write(string_out)

      self.total_time = self.total_time /1000
      second_here = self.total_time % 60
      self.total_time = self.total_time /60
      min_here = self.total_time % 60

      hour_here = self.total_time / 60
      string_out = ""

      if hour_here < 10:
          string_out = string_out + "0"+ str(hour_here) + ":"
      else:
          string_out = string_out + str(hour_here) + ":"

      if min_here < 10:
          string_out = string_out + "0"+ str(min_here) + ":"
      else:
          string_out = string_out + str(min_here) + ":"

      if second_here < 10:
          string_out = string_out + "0"+ str(second_here)
      else:
          string_out = string_out + str(second_here)
      string_out = string_out + self.data +  "\n"
      file_here = open(self.fileHora,'a+')
      file_here.write(string_out)

  """
   * It generates the output file from a given dataset and stores it in a file
   * @param dataset myDataset input dataset
   * @param filename String the name of the file   
  """

  def doOutput(self,dataset, filename) :
      try:

          output_here = dataset.copyHeader() #we insert the header in the output file
          #We write the output for each example
          print("before loop in FARC_HD......")
          print("dataset.getnData()"+ str(dataset.getnData()))
          for i in range( 0, dataset.getnData()):
            #for classification:

            classOut = self.classificationOutput(dataset.getExample(i))

            output_here = output_here + dataset.getOutputAsStringWithPos(i) + " " + str(classOut) + "\n"

            #print("dataset.getOutputAsString(i) :" + str(dataset.getOutputAsStringWithPos(i)))
            #print("classificationOutput,classOut :" + str(classOut))

          print("before open file in FARC_HD......")
          file = open(filename,"w")
          file.write(output_here)
          file.close()
      except Exception as excep:
          print("There is exception in doOutput in FARC class !!! The exception is :" + str(excep))


       # * It returns the algorithm classification output given an input example
       # * @param example double[] The input example
       # * @return String the output generated by the algorithm
  def classificationOutput(self,example):
        output_string = "?"
          # Here we should include the algorithm directives to generate the
          # classification output from the input example
        classOut = self.ruleBase.FRM_one(example)
        if classOut >= 0:
            output_string = self.train_myDataSet.getOutputValue(classOut)
        print("In FARC_HD,classificationOutput,classOut :"+str(classOut)+",self.output :"+str(output_string))
        return output_string













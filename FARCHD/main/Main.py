
# /***********************************************************************
#
# 	This file is part of KEEL-software, the Data Mining tool for regression,
# 	classification, clustering, pattern mining and so on.
#
# 	Copyright (C) 2004-2010
#
# 	F. Herrera (herrera@decsai.ugr.es)
# 	L. Sánchez (luciano@uniovi.es)
# 	J. Alcalá-Fdez (jalcala@decsai.ugr.es)
# 	S. García (sglopez@ujaen.es)
# 	A. Fernandez (alberto.fernandez@ujaen.es)
# 	J. Luengo (julianlm@decsai.ugr.es)
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see http://www.gnu.org/licenses/
#
# **********************************************************************

# https://stackabuse.com/association-rule-mining-via-apriori-algorithm-in-python/

from ParseParameters import ParseParameters
from FARC_HD import FARC_HD
from os import listdir
from os.path import isfile,join
import sys
from pathlib import Path
import datetime

 # * <p>It reads the configuration file (data-set files and parameters) and launch the algorithm</p>
 # *
 # * @author Written by Alberto Fern谩ndez (University of Granada) 14/10/2007
 # * @version 1.0
 # * @since JDK1.5

class Main :

    config_files_folder=Path("C:\pythonAlgorithms\KeelSoftware-2018-04-09\Documentos\Experimentos\FARCHD\FARCHD\scripts\Fuzzy-FARCHD-C\iris")
    file_to_open = None
       # Default Constructor

               # * It launches the algorithm
               # * @param confFile String it is the filename of the configuration file.

    def execute(config_file):
        print("Main execute begin...")
        time_begin = datetime.datetime.now()
        parameters=ParseParameters()
        parameters.parseConfigurationFile(config_file)
        farc_hd =FARC_HD(parameters)
        farc_hd.execute()
        time_finish = datetime.datetime.now()
        run_time = time_finish - time_begin
        print("The execute finished and run time is : " + str(run_time))

    def executeMultiFiles(self,config_file):
            print("MaultiMain execute begin...")
            parameters = ParseParameters()
            parameters.parseConfigurationFile(config_file)
            farc_hd = FARC_HD(parameters)
            farc_hd.execute()

           # * Main Program
           # * @param args It contains the name of the configuration file
           # * Format:
           # * algorithm = ;algorithm name>
           # * inputData = "training file" "validation file" "test file"
           # * outputData = "training file" "test file"
           # *
           # * seed = value (if used)
           # Parameter1; value1
           # Parameter2&gt; value2


    if __name__=='__main__':
        print("Executing Algorithm.")

        print("sys.argv: " + sys.argv[1])
        execute(sys.argv[1])






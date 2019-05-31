
from os import listdir
from os.path import isfile,join
from Main import Main

class MultiMain:


    if __name__=='__main__':
        config_files_folder = "C:\pythonAlgorithms\KeelSoftware-2018-04-09\Documentos\Experimentos\FARCHD\FARCHD\scripts\Fuzzy-FARCHD-C\iris"
        con_files = listdir(config_files_folder)
        for file in con_files:
            whole_path_file = join(config_files_folder, file)
            main = Main()
            main.executeMultiFiles(whole_path_file)
            main=None
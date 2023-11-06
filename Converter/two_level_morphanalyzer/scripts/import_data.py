
import os
import os.path
import os
from tqdm import tqdm
from os import path
import shutil
path = 'C:/Users/User/PycharmProjects/kyrgyz_morph_analyzer/two_level_morphanalyzer/media/audios/'
from analyzer.models import Audios
all_files_in_directory = os.listdir(path)
#print(all_files_in_directory)
folder_name = ['01', '02']
def run():
        #Audios.objects.all().delete()
        for i in all_files_in_directory:
            # if i in folder_name and i == '01':
            #     all_files_in_directory2 = os.listdir(path+str(i))
            #     for j in all_files_in_directory2:
            #         allroot, created = Audios.objects.get_or_create(
            #             audio_file=str(i+"/"+j), super_visor='sup2', admin='admin2')
            #         print(allroot)
            #         print(created)
            if i in folder_name and i == '01':
                all_files_in_directory2 = os.listdir(path + str(i))
                for j in all_files_in_directory2:
                    allroot, created = Audios.objects.get_or_create(
                        audio_file=str(i+"/"+j), super_visor='sup1', admin='admin1')
                    print(allroot)
                    print(created)
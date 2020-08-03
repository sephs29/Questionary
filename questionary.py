#! python3.6    
#dlib-19.8.1-cp36-cp36m-win_amd64.whl works for 3.6python 64 bit

import os
import csv
import pandas as pd
from bing_images_download import googleimagesdownload
import cv2
import face_recognition
import pickle
import shutil
import random

class create_database():
    def get_player_list(self,filename): #'ipl2019.csv'
        playerdf = pd.read_csv(os.path.join(os.getcwd(), filename))
        return playerdf

    def download_images(self, directory_name, playername, num_img, is_face_repo=False):
        if is_face_repo:
            url = 'https://www.bing.com/images/search?q=%s' % playername.replace(' ', '%20')
            url += '&qft=&FORM=IRFLTR'
        else: 
            url = 'https://www.bing.com/images/search?q=%s' % playername.replace(' ', '%20')
            url += '&qft=&FORM=IRFLTR'
            #url = 'https://www.bing.com/images/search?q=%s' % playername.replace(' ', '%20')
            #url += '&qft=+filterui:license-L2_L3_L4&FORM=IRFLTR'#free to share and use commercially
       
        arguments = {"keywords": playername,
                    'prefix_keywords':'face',
                    "limit":num_img,
                    "format": 'jpg' or 'jpeg',
                    "prefix": playername,
                    #"print_urls": True,
                    #"usage_rights": "labeled-for-reuse",
                    'image_directory':playername,
                    'output_directory': directory_name,
                    #'extract_metadata': 'True',
                    # 'no_download':'X',
                    'url':url,
                    "chromedriver": os.path.join(os.getcwd(),"chromedriver_win32_1\chromedriver.exe")
                    } 
        response = googleimagesdownload()
        img_list = response.download(arguments)
        img_list = img_list[0]
        key = list(img_list.keys())
        img_list = img_list[key[0]]
        print('Download completed for',playername)
        
        return img_list

    def pickle_FaceRepo(self, playername):
        directory_name = 'FaceRepo'
        img_list = self.download_images(directory_name,playername,10,is_face_repo=True)
        print('Started generating pickle file for '+ playername)
        X_encodes = []
        y_name = []
        dir_path = os.path.join(os.getcwd() ,directory_name, playername)
        for i,img_name in enumerate(os.listdir(dir_path)):
        #for i,img_name in enumerate(img_list):  
            try:
                img = cv2.imread(os.path.join(dir_path, img_name))
                #img = cv2.imread(img_name)
                img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(img1, model="hog")
                if len(boxes) == 1:
                    encodings = face_recognition.face_encodings(img1, boxes)
                    for encoding in encodings:
                        X_encodes.append(encoding)
                        y_name.append(playername)
                    os.remove(os.path.join(dir_path, img_name))
                else:
                    os.remove(os.path.join(dir_path, img_name))
            except Exception as err_msg:
                print(err_msg)

        # save pickle files'
        subdir_path = os.path.join(os.getcwd(), 'PickleRepo')
        if not os.path.exists(subdir_path):
            os.makedirs(subdir_path)

        data = {"X_encodes": X_encodes, "y_name": y_name}
        pickle_filename = playername + '.pickle'
        f = open(os.path.join(os.getcwd(), 'PickleRepo', pickle_filename), "wb")
        f.write(pickle.dumps(data))
        f.close()
        print('Pickle file generated')

        try:
            # delete image from local system
            os.rmdir(os.path.join(os.getcwd() ,directory_name, playername))
            #os.remove(os.path.join(os.getcwd() ,directory_name))
            shutil.rmtree(os.path.join(os.getcwd() ,directory_name))

        except Exception as e:
            print(e)
            print("File ", playername, " could not be deleted")
        
    def read_picklefile(self, playername):
        dir_path = os.getcwd()
        pickle_filename = playername + '.pickle'
        data = pickle.loads(open(os.path.join(dir_path,'PickleRepo', pickle_filename), "rb").read())
        X_encodes = data['X_encodes']
        y_name = data['y_name']
        return X_encodes, y_name

    def recogniseface(self, X_encodes, y_name, img_file_path):
        img = cv2.imread(img_file_path)
        if img is not None:
            try:
                #img = cv2.imread(img_file_path)
                img1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Returns an array of bounding boxes of human faces in a image
                boxes = face_recognition.api.face_locations(img=img1, number_of_times_to_upsample=2, model="hog")

                # known_face_locations :the bounding boxes of each face if you already know them.
                # return the 128-dimension face encoding for each face in the image.
                encodings = face_recognition.api.face_encodings(face_image=img1, known_face_locations=boxes)
                if encodings and len(boxes) == 1:  # if has encoding values = True
                    for encoding in encodings:
                        player = y_name
                        # Compare a list of face encodings against a candidate encoding to see if they match.
                        matches = face_recognition.compare_faces(X_encodes, encoding)
                        if (max(matches)):
                            print('PLAYER PRESENT')
                            return 'True'
                        else:
                            answerfile = open("errorlog.txt", "a+")
                            answerfile.write(str('\n' + img_file_path))  # filename
                            answerfile.close()
                            print('PLAYER ABSENT')
                            return 'False'
                else:
                    print('empty encoding')
                    print(img_file_path)  # filename
                    #os.remove(os.path.join(img_file_path))

            except Exception as err_msg:
                print(err_msg)
                err_counter += 1
                print('error')
                print(err_counter)
    
    def select_imgfile(self, img_file_path,playername,X_encodes, y_playername):
        
        img = cv2.imread(img_file_path)
        face_locations = face_recognition.face_locations(img)
        #print(face_locations)
        if len(face_locations) == 1:
            X_encodes, y_playername = self.read_picklefile(playername)
            recognition = self.recogniseface(X_encodes, y_playername, img_file_path)
            if recognition:
                #if player present, rename the img file
                #oldimg_path = os.path.join(dir_path, img_name)
                img_path = img_file_path.rsplit("\\",1)[0]
                img_name = img_file_path.rsplit("\\",1)[1]
                img_name = img_name.split('.',)[0] + '.' +img_name.split('.',)[-1]
                print(img_name) 
                newimg_path = os.path.join(img_path ,img_name)
                os.rename(img_file_path,newimg_path)
            else:
                os.remove(os.path.join(img_file_path))
        else:
            os.remove(os.path.join(img_file_path))
    
    def finalrepocheck(self,directory_name,playername):
        dir_path = os.path.join(os.getcwd() ,directory_name, playername)
        img_list =os.listdir(dir_path)
        if len(img_list) < 1:
            shutil.rmtree(dir_path)
            return False
        else:
            return playername

    
    def create_pickleRepo(self,filename):
        playerdf = pd.read_csv(os.path.join(os.getcwd(), filename))
        #create_database = create_database()
        for player in playerdf['Player']:
            #create_database.download_facerepo(player)
            self.pickle_FaceRepo(player)

    def create_imageRepo(self,filename):
        directory_name = 'ImageRepo'
        playerdf = pd.read_csv(os.path.join(os.getcwd(), filename))
        newplayerdf  = pd.DataFrame(columns=playerdf.columns.values)

        for i,player in enumerate(playerdf['Player']):
            img_list = self.download_images(directory_name,player,10)
            X_encodes, y_name = self.read_picklefile(player)
            dir_path = os.path.join(os.getcwd(),directory_name, player)
            img_list = os.listdir(dir_path)
            for img_name in img_list:
                img_file_path = os.path.join(dir_path,img_name)
                self.select_imgfile(img_file_path,player,X_encodes,y_name)
            if self.finalrepocheck(directory_name,player):                
                newplayerdf = newplayerdf.append(playerdf.iloc[i,:])
            else:
                pass
        filepath = os.path.join(os.getcwd(),('new'+filename))
        newplayerdf.to_csv (filepath, index = False, header=True)


class get_data:

    def get_quesoptions(self,csvfilename):
        foldername = 'ImageRepo'

        quesdf = pd.read_csv(os.path.join(os.getcwd(), 'questions.csv'))
        tag = random.choice(quesdf['tag'])
        not_tag =random.choice([True,False])
        
        optionsdf = pd.read_csv(os.path.join(os.getcwd(), csvfilename))
        keyword = str(random.choice(optionsdf[tag]))        

        question = list(quesdf['question'][quesdf['tag']==tag])[0]
        queswords =set(['who','what','how','when','which','where','why'])
        question = question.split()
        question.extend([keyword,'?'])

        groups = optionsdf.groupby(by=tag).groups     
        grouplist = {str(k):v.tolist() for k, v in groups.items()}
        index = len(grouplist[keyword])    
        
        if not not_tag : #who belongs/is at <keyword>
            question = ' '.join(question)
            answer = optionsdf[optionsdf[tag] == keyword].sample(n=1)
            otheroptions = optionsdf[optionsdf[tag] != keyword].sample(n=3)
            options  = otheroptions.append(answer)
            answer,options = self.get_image(foldername,options)
                        
            

        elif not_tag and index >= 3: #not-questions eg: Not in 
        #and tag !='rank' 
            
            foundquesword = list(queswords.intersection(question))[0]
            i = question.index(foundquesword)
            question.insert(i+2, 'not')
            question = ' '.join(question)

            answer = optionsdf[optionsdf[tag] != keyword].sample(n=1)
            otheroptions = optionsdf[optionsdf[tag] == keyword].sample(n=3)
            options  = otheroptions.append(answer)
            answer,options = self.get_image(foldername,options)       

        else:#not_tag and tag == 'rank'
            question,options,answer = self.get_quesoptions(csvfilename) 


        return question,options,answer

    def get_image(self,foldername,options):
        #options  = options.sample(frac=1) #shuffle
        names = options['Player']    
        opindex = options.index
        options = {}
        for i,ele in enumerate(names):
            folderpath = os.path.join(os.getcwd(),foldername,ele)
            imgpath = os.path.join(folderpath,random.choice(os.listdir(folderpath)))
            options[i] = [opindex[i],ele,imgpath]
        answer = options[3]
        #shuffle
        values = list(options.values())
        random.shuffle(values)
        keys = list(options.keys())        
        options = dict(zip(keys, values))
        
        return answer,options
        


if __name__ == "__main__":
    filename= 'ipl2019.csv'
    obj = create_database()
    #obj.create_pickleRepo(filename)
    #obj.create_imageRepo(filename)

    #filename = 'new'+filename
    #qa = get_data()
    #qa.get_quesoptions(filename)
from imgpy import VocabImage as VocabImage
import pandas as pd
import os
import shutil#파일 통채로 옮기는 라이브러리 for moving train result
from ultralytics import YOLO
import torch

MasterDir = 'D:/vocabbooks'

class VocabBook():
    def __init__(self, book_name = 'MyVocab',#단어장 이름 -> 이걸로 폴더 만들어짐
                  bookdir = None, datadir = None, yamldir = None, labeldir = None,#각종 경로, ocr data있는 pdf 경로 추가 필요
                  vocab_mean_boundary = None, use_tesseract = False,#vocabmean boundary는 고정 좌우 좌표, use tesseract는 업데이트 하여 다양한 ocr 방법 쓰도록 수정
                    pretrained=True, patience=800 ,epochs=800, optimizer = 'Adam', save_period=100, imgsz=720, batch=8, lr0 = 0.001, lrf=0.001,#수정해서 따로 입력되도록 할것임
                    
                    autoProceed = True, data_in_pdf = False, ) -> None:
        


        self.book_name = book_name
        self.set_dir(book_name, bookdir, datadir, yamldir, labeldir)
        VocabImage.vocab_mean_boundary = vocab_mean_boundary#단어와 뜻의 경계선
        VocabImage.use_tesseract = use_tesseract
        

        self.checkTrain = False
        self.model = None
        self.bestModel = None

        self.imgClasses = {}
        
        
        if autoProceed:
            self.Process(data_in_pdf=data_in_pdf)

    def set_dir(self, book_name, bookdir, datadir, yamldir, labeldir):
        '''
        각종 경로 받아오기
        '''
        if not os.path.exists(MasterDir):
            os.mkdir(MasterDir)

        if bookdir == None:
            self.bookdir = MasterDir+'/'+book_name
            if not os.path.exists(self.bookdir):
                print(self.bookdir,"created")
                os.mkdir(self.bookdir)
            else:
                print(self.bookdir,"already exists!")
        else:
            self.bookdir = bookdir

        if datadir == None:
            self.datadir = bookdir+'/dataset'
            if not os.path.exists(self.datadir):
                print(self.datadir,"created")
                os.mkdir(self.datadir)
            else:
                print(self.datadir,"already exists!")
        else:
            self.datadir = datadir
        
        self.labeldir = labeldir
        self.yamldir = yamldir

    def Process(self, data_in_pdf):
        '''
        자동으로 모든 process를 진행하는 함수. 클래스 매개변수로 autoProceed가 True이면 진행되도록 한다.

        '''
        # if data_in_pdf:
        #     self.pdf_to_image()
        
        # if self.labeldir == None:
        #     self.label_data()

        # if self.yamldir == None:
        #     self.make_yaml()

        # self.train()
        # self.move_result()
        # self.get_best_model()

        self.best_model = YOLO('./best.pt')
        
        self.make_img_list()
        torch.cuda.empty_cache()
        self.predict()
        torch.cuda.empty_cache()
        self.run_ocrs()
        torch.cuda.empty_cache()
        self.extract_xls()

        
        

    def pdf_to_image(self):
        '''
        데이터셋이 pdf 형식일 경우 pdf의 이미지를 가져와 한 폴더안에 넣는 함수
        '''
        None
        
    def label_data(self):
        '''
        라벨 데이터가 없을 경우 직접 라벨링하는 기능을 호출하는 함수 (UI 구성에 따라 UI에 갈 함수일 수 도 있음)
        '''
        if self.labeldir == None:
            self.labeldir = self.bookdir+'/label'
            if not os.path.exists(self.labeldir):
                print(self.labeldir,"created")
                os.mkdir(self.labeldir)
        #-------------------------------
        #label codes here        
        #-------------------------------

        return self.labeldir

    def make_yaml(self):
        '''
        라벨 데이터와 라벨링된 파일의 경로를 가지고 yaml 파일을 만드는 함수
        미완성
        '''
        #구현
        if self.labeldir == None:
            self.label_data()
        
        if self.yamldir == None:
            os.mkdir(self.bookdir+'trainimg')
            self.yamldir = self.bookdir+'trainimg'
            if not os.path.exists(self.yamldir):
                print(self.yamldir,"created")
                os.mkdir(self.yamldir)            

        

        return self.yamldir
    
    def train(self):
        '''
        train 함수
        '''
        model = YOLO('yolov8n.pt')  # pretrained model
        model.train(data=self.yamldir, name=self.book_name, pretrained=True, patience=800 ,epochs=800, optimizer = 'Adam', save_period=100, imgsz=720, batch=8, lr0 = 0.001, lrf=0.001)

        result_dir = self.move_result()
        return result_dir

    def move_result(self):
        '''
        결과는 코드파일 주소의 ./runs/detect에 저장됨
        해당 프로젝트들에 해당되는 폴더를 리스트하고, 마지막 result 폴더 bookdir로 옮김
        해당 프로젝트 결과 폴더 중 옮기지 않은 나머지 result들은 삭제

        참고: train의 경우 결과가 bookname bookname2 bookname3... 순으로 저장됨
        exception에 의해 train이 중단되면 위처럼 여러 결과가 생길 수 있음
        '''
        temp_res_dir = './runs/detect'#train 결과 저장되는곳
        result_list = os.listdir(temp_res_dir)#해당 폴더 안 내용

        #해당 프로젝트가 아니면 대상에서 제외
        for foldername in result_list:
            if self.book_name not in foldername:
                result_list.remove(foldername)
            print(temp_res_dir+foldername)

        #마지막 result는 옮긴다
        self.result_dir = self.bookdir+'trainresult'
        shutil.move(temp_res_dir+result_list[-1], self.result_dir)

        #옮겨지지 않은 result들은 삭제
        for foldername in result_list[:-1]:
            if self.book_name in foldername:
                shutil.rmtree(temp_res_dir+foldername)

        return self.result_dir

    def get_best_model(self):
        '''
        train된 결과 중 best.pt를 가져오는것
        '''
        self.best_model = YOLO(self.result_dir+'/weights/best.pt')
        return self.best_model

    def make_img_list(self):
        '''
        
        '''
        files = os.listdir(self.datadir)
        for page, file in enumerate(files):
            img_dir = os.path.join(self.datadir, file)
            imgname = os.path.splitext(file)[0]
            imgCls = VocabImage(img_name = imgname, img_dir=img_dir, page=page+1)#file[0]는 0001.jpg -> 0001로 바뀜, dir은 주소
            self.imgClasses[imgname] = imgCls
        VocabImage.book_pages = len(self.imgClasses)

    def predict(self):
        predict_rslts = self.best_model.predict(self.datadir, save=False, save_txt=False, imgsz=720, conf=0.5)
        for predict_rslt in predict_rslts:
            cur_img = os.path.splitext(os.path.basename(predict_rslt.path))[0]
            clss = predict_rslt.boxes.cls.long().tolist()
            boxes = predict_rslt.boxes.xyxy.tolist()
            self.imgClasses[cur_img].predict(clss, boxes)

    def run_ocrs(self):
        '''
        각 vocab image의 ocr을 돌리고 결과 받아 df로 만들기
        '''
        self.text_datas = pd.DataFrame(columns=["chapter","page","image_name","idx_in_page","vocab", "meaning", "example","syn"])
        for img in self.imgClasses:
            #결과 return하도록 했으니 datas를 여기서 combine해도 됨
            pd_text_data = self.imgClasses[img].run_ocr()
            self.text_datas = pd.concat([self.text_datas, pd_text_data], ignore_index=True)
        return self.text_datas
    

    def extract_xls(self):
        '''
        df 엑셀로 변환해서 추출
        '''
        excel_dir = self.bookdir+'/'+self.book_name+'.xlsx'
        print('extracting result data to {}'.format(excel_dir))
        try:
            self.text_datas.to_excel(excel_dir,index=False)
        except:
            print('excel extraction fail')

            
    def get_dataset(self):
        return self.imgClasses



import cv2
import pytesseract
import easyocr
import pandas as pd




class VocabImage():
    label_class = {0:'vocab', 1:'meaning', 2:'example', 3:'syn', 4:'vboundary'}

    #좌우 바운더리 정보는 좀더 구체적으로 구현 필요할듯
    use_absolute_boundary = False
    vocab_mean_boundary = None
    left_boundary = 0
    right_boundary = None

    use_tesseract = False
    easyocr_reader = easyocr.Reader(['en', 'ko'], gpu=True)

    book_pages = None


    def __init__(self, img_name, img_dir = None, page = 0, chapter = 0) -> None:
        self.img_name = img_name
        self.chapter = chapter
        self.page = page
        #self.is_labelled = 
        self.img_dir = img_dir

        if self.vocab_mean_boundary != None:#전역 좌우 바운더리 설정 있을 경우에 설정
            self.set_ocr_boundary()
            
        self.text_data = {}
    
    def set_chapter(self, chapter):
        self.chapter = chapter

    def load_img(self):
        None
    
    

    def predict(self, clss, boxes):
        self.predict_classes = clss
        self.predict_boxes = boxes



    def draw_bbox(self):
        None

    def print_image(self):
        None

    def set_ocr_boundary(self):
        '''
        이미지마다 크기 다르므로 오른쪽 바운더리는 일일히 이미지별로 지정해야함
        '''
        self.use_absolute_boundary = True
        img = cv2.imread(self.img_dir)
        image_height, image_width, _ = img.shape
        self.vocab_right_boundary = image_width

    def run_ocr(self):
        #단어장 페이지가 아니면 안돌림
        if self.chapter == -1:
            return None
        
        print("running ocr - chapter: {}, page: {}/{}, image: {}".format(self.chapter, self.page, self.book_pages, self.img_name))
        mixed_text_data = []
        for i, cls in enumerate(self.predict_classes):
            if cls != 4:
                continue
            boundary_top = self.predict_boxes[i][1]
            boundary_bottom = self.predict_boxes[i][3]

            wordset = {}
            for j, box in enumerate(self.predict_boxes):
                if self.predict_classes[j] == 4:#해당 박스가 vboundary일경우
                    continue
                #left, top, right, bottom = box#xyxy형식
                #아래가 윗줄 round 기능 추가한 버전
                left, top, right, bottom =[int(round(val)) for val in box]
                
                if top < boundary_top or bottom > boundary_bottom:#해당 박스가 vboundary 안에 있지 않은경우
                    continue

                #절대 바운더리 사용 경우
                if self.use_absolute_boundary:
                    if self.predict_classes[j] == 0:
                        left = self.left_boundary
                        right = self.vocab_mean_boundary
                    else:
                        left = self.vocab_mean_boundary
                        right = self.right_boundary

                image = cv2.imread(self.img_dir)
                roi = image[top:bottom, left:right]
                if self.use_tesseract:
                    text = pytesseract.image_to_string(roi, lang='kor+eng')
                else:
                    ocr_rslt = self.easyocr_reader.readtext(roi,detail=0)
                    text = "".join(ocr_rslt)
                wordset[self.label_class[self.predict_classes[j]]] = text

            #결과 dict와 boundary top 묶는다.
            #boundary top으로 sort한다
            #sort된것을 text_data에 저장한다
            mixed_text_data.append((wordset, boundary_top))
            sorted_text_data = sorted(mixed_text_data, key=lambda x: x[1])
            self.text_data = [x[0] for x in sorted_text_data]
            
            pd_text_data = self.data_to_pd(self.text_data)

            
        return pd_text_data
    

    def data_to_pd(self, text_data):
        '''
        run ocr 함수에서 리스트로 된 텍스트 데이터를 pandas df 형태로 변환시키는 함수
        '''
        textdata_dicts = []

        img_info = self.get_img_info()
        for idx_in_page, txtdata in enumerate(text_data):
            textdata_dict = {"chapter": img_info[0],
                            "page": img_info[1],
                            "image_name": img_info[2],
                            "idx_in_page": idx_in_page,
                            "vocab": txtdata.get('vocab', ''),
                            "meaning": txtdata.get('meaning', ''),
                            "example": txtdata.get('example', ''),
                            "syn": txtdata.get('syn', '')
                            }
            textdata_dicts.append(textdata_dict)
        dfs = [pd.DataFrame([d]) for d in textdata_dicts]
        pd_text_data = pd.concat(dfs, ignore_index=True)
        return pd_text_data


        



    def edit_texts(self):
        None

    def get_img_info(self):
        return (self.chapter, self.page, self.img_name)

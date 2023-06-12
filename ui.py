import sys
import os

import threading


from vocabbook import VocabBook as VocabBook

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt, QEvent, QObject
from qtpy.QtGui import QPixmap


setup_ui = uic.loadUiType("setup.ui")[0]
set_chapter_ui = uic.loadUiType("set_chapter.ui")[0]

def check_valid_path(path, isfile):
    valid = True

    if path == None:
        valid = False
    elif not os.path.exists(path):
        valid = False
    else:
        if isfile:
            if not os.path.isfile(path):
                valid = False
        else:
            if not os.path.isdir(path):
                valid = False
    
    return valid






#화면을 띄우는데 사용되는 Class 선언
class qt_setup(QMainWindow, setup_ui) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)#ui 불러오기
        self.setchap = None#다음 window

        #default setting
        self.project_name = 'My project'
        self.load_data_type = 0# 0: imagedir, 1: pdf, 2: pdf(ocr)
        self.data_dir = {0:None, 1:None, 2:None}
        self.load_label_type = 0# 0: no label, 1: labeldir(only label), 2: labeldir(label+image), 3: yaml
        self.label_dir = {0:'No label is currently not working.', 1:None, 2:None, 3:None}

        #default line
        self.proj_name_line.setText(self.project_name)
        self.label_dir_line.setText(self.label_dir[self.load_label_type])


        self.set_events()

    def set_events(self):
        #combo boxes
        self.data_type_combo.currentIndexChanged.connect(self.data_type_combo_change)
        self.label_type_combo.currentIndexChanged.connect(self.label_type_combo_change)

        #버튼들
        self.load_data_button.clicked.connect(self.load_data_button_clicked)
        self.load_label_data_button.clicked.connect(self.load_label_button_clicked)
        self.continueButton.clicked.connect(self.continue_button_clicked)

    def data_type_combo_change(self, index):
        self.load_data_type = index
        self.data_dir_line.setText(self.data_dir[self.load_data_type])

    def label_type_combo_change(self, index):
        self.load_label_type = index    
        self.label_dir_line.setText(self.label_dir[self.load_label_type])

    def load_data_button_clicked(self):
        if self.load_data_type == 0:
            folderpath = QFileDialog.getExistingDirectory(self, '이미지가 있는 폴더를 선택하십시오')
            if folderpath:
                print(folderpath)
                self.data_dir[self.load_data_type] = folderpath
                self.data_dir_line.setText(folderpath)
            else:
                pass
        else:
            fname=QFileDialog.getOpenFileName(self,'','','pdf(*.pdf)')
            if fname[0]:
                print(fname[0])
                self.data_dir[self.load_data_type] = fname[0]
                self.data_dir_line.setText(fname[0])
            else:
                pass
        
    def load_label_button_clicked(self):
        if self.load_label_type == 0:
            #No label이기 때문에 사실 할 동작이 없음
            #self.label_dir[0] = None#그냥 Nolabel에 해당하는 dir 초기화시킴
            self.label_dir_line.setText(self.label_dir[0])
        elif self.load_label_type == 3:
            fname=QFileDialog.getOpenFileName(self,'','','yaml(*.yaml)')
            if fname[0]:
                print(fname[0])
                self.label_dir[self.load_label_type] = fname[0]
                self.label_dir_line.setText(fname[0])
            else:
                pass
        else:
            folderpath = QFileDialog.getExistingDirectory(self, '라벨 데이터가 있는 폴더를 선택하십시오')
            if folderpath:
                print(folderpath)
                self.label_dir[self.load_label_type] = folderpath
                self.label_dir_line.setText(folderpath)
            else:
                pass

    def continue_button_clicked(self):
        print("press_continue called")


        # if self.load_data_type == 0:
        #     if self.load_label_type == 0:
        #         myVocabBook = VocabBook(book_name = self.project_name, datadir=self.data_dir[self.load_data_type])
        #     elif self.load_label_type == 3:
        #         myVocabBook = VocabBook(book_name = self.project_name, datadir=self.data_dir[self.load_data_type], yamldir=self.label_dir[self.load_label_type])
        #     else:
        #         myVocabBook = VocabBook(book_name = self.project_name, datadir=self.data_dir[self.load_data_type], labeldir=self.label_dir[self.load_label_type])

        # else:
        #     if self.load_data_type == 2:
        #         data_in_pdf = True
        #     else:
        #         data_in_pdf = False
            
        #     if self.load_label_type == 0:
        #         myVocabBook = VocabBook(book_name = self.project_name, pdfdir=self.data_dir[self.load_data_type], data_in_pdf=data_in_pdf)
        #     elif self.load_label_type == 3:
        #         myVocabBook = VocabBook(book_name = self.project_name, pdfdir=self.data_dir[self.load_data_type], yamldir=self.label_dir[self.load_label_type], data_in_pdf=data_in_pdf)
        #     else:
        #         myVocabBook = VocabBook(book_name = self.project_name, pdfdir=self.data_dir[self.load_data_type], labeldir=self.label_dir[self.load_label_type], data_in_pdf=data_in_pdf)

        myVocabBook = VocabBook(book_name = self.project_name, datadir='D:/MVPtest')


        if self.setchap ==None:
            self.setchap = qt_setchap(myVocabBook, self)

        self.setchap.show()
        self.close()
        del self


    def check_valid_path(self, path, isfile):
        valid = True

        if path == None:
            valid = False
        elif not os.path.exists(path):
            valid = False
        else:
            if isfile:
                if not os.path.isfile(path):
                    valid = False
            else:
                if not os.path.isdir(path):
                    valid = False
        
        return valid




#화면을 띄우는데 사용되는 Class 선언
class qt_setchap(QMainWindow, set_chapter_ui):
    def __init__(self, myVocabBook, qt_setup):
        super().__init__()
        self.setupUi(self)#ui 불러오기
        self.set_focuspolicy()



        self.myVocabBook = myVocabBook
        self.myVocabBook.Setup_Process(self.myVocabBook.data_in_pdf)
        self.imgClsseskey = list(self.myVocabBook.imgClasses.keys())

        self.curpage = 0
        self.curchap = 0
        self.book_pages = len(self.imgClsseskey)
        self.chapterInfo = {}

        self.page_num_label.setText('/' + str(self.book_pages))
        self.change_image_by_page(self.curpage)

        qt_setup = None
        self.qt_train = None
        self.continueButton.clicked.connect(self.continue_button_clicked)

    def set_focuspolicy(self):
        self.picture_label.setFocusPolicy(Qt.NoFocus)
        self.page_label.setFocusPolicy(Qt.NoFocus)
        self.page_num_label.setFocusPolicy(Qt.NoFocus)
        self.current_chapter_label.setFocusPolicy(Qt.NoFocus)
        self.instruction_textBrowser.setFocusPolicy(Qt.NoFocus)
        self.continueButton.setFocusPolicy(Qt.NoFocus)

        self.page_spinbox.setFocusPolicy(Qt.ClickFocus)
        self.current_chapter_spinbox.setFocusPolicy(Qt.ClickFocus)
    
    def keyPressEvent(self, e):
        pressed = e.key()
        if pressed == 16777235:#up
            self.curchap += 1
            self.current_chapter_spinbox.setValue(self.curchap)
        elif pressed == 16777237:#down
            self.curchap -= 1
            self.current_chapter_spinbox.setValue(self.curchap)

        elif pressed == 16777234:#left
            if self.curpage > 0:
                self.curpage -= 1
                try:
                    temp = self.chapterInfo[self.imgClsseskey[self.curpage]]
                    if temp != -1:
                        self.curchap = temp
                except:
                    pass
                self.current_chapter_spinbox.setValue(self.curchap)
                self.page_spinbox.setValue(self.curpage)
                self.change_image_by_page(self.curpage)
        elif pressed == 16777236:#right
            if self.curpage < self.book_pages-1:
                self.chapterInfo[self.imgClsseskey[self.curpage]] = self.curchap
                self.curpage += 1
                try:
                    temp = self.chapterInfo[self.imgClsseskey[self.curpage]]
                    if temp != -1:
                        self.curchap = temp
                except:
                    pass
                self.current_chapter_spinbox.setValue(self.curchap)
                self.page_spinbox.setValue(self.curpage)
                self.change_image_by_page(self.curpage)

        elif pressed == 32:#space
            if self.curpage < self.book_pages-1:
                self.chapterInfo[self.imgClsseskey[self.curpage]] = -1
                self.curpage += 1
                try:
                    temp = self.chapterInfo[self.imgClsseskey[self.curpage]]
                    if temp != -1:
                        self.curchap = temp
                except:
                    pass
                self.curchap += 1
                self.current_chapter_spinbox.setValue(self.curchap)
                self.page_spinbox.setValue(self.curpage)
                self.change_image_by_page(self.curpage)

   
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not (self.page_spinbox.underMouse() or self.current_chapter_spinbox.underMouse()):
            self.page_spinbox.clearFocus()  # Clear focus from the spin box if clicked outside
            self.current_chapter_spinbox.clearFocus()

        super().mousePressEvent(event)  # Pass the event to the base class for default handling
    
    def change_image_by_page(self, page):
        self.change_image(self.myVocabBook.imgClasses[self.imgClsseskey[page]].img_dir)

    def change_image_by_filename(self, filename):
        self.change_image(self.myVocabBook.imgClasses[filename].img_dir)

    def change_image(self, imgdir):
        #pixmap = QPixmap("D:/MVP/1110011.jpg")  # Replace with the path to your new image
        #pixmap = QPixmap(self.myVocabBook.imgClasses['1110003'].img_dir)  # Replace with the path to your new image
        pixmap = QPixmap(imgdir)  # Replace with the path to your new image
        pixmap = pixmap.scaled(self.picture_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.picture_label.setPixmap(pixmap)

    def continue_button_clicked(self):
        
        self.myVocabBook.set_chapters(self.chapterInfo)
        for imgcls in self.myVocabBook.imgClasses:
            print(self.myVocabBook.imgClasses[imgcls].chapter)

        # if self.qt_train == None:
        #     self.qt_train = qt_setchap(self.myVocabBook, self)

        # self.qt_train.show()
        # self.close()
        # del self








if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = qt_setup() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()


'''
#check if data dir is valid directory or file
        if self.load_data_type == 0:
            if not check_valid_path(self.data_dir[self.load_data_type], True):



        #     if type(self.data_dir[self.load_data_type]) == None or not os.path.exists(self.data_dir[self.load_data_type]) or not os.path.isdir(self.data_dir[self.load_data_type]):
        #         print('a')
        #         QMessageBox.about(self, "Information", "This is an information message.")
        #         pass
        #     else:
        #         print('b')
        #         QMessageBox.about(self, "Information", "This is an information message.")
        #         #QMessageBox().about(self, "Wrong dir"  ,"Your data directory is not valid")
        # else:
        #     print("c")
            # if type(self.data_dir[self.load_data_type]) != None or (os.path.exists(self.data_dir[self.load_data_type]) and os.path.isfile(self.data_dir[self.load_data_type])):
            #     pass
            # else:
            #     QMessageBox().about(self, "Wrong dir"  ,"Your data file is not valid")

        # #check if label dir is valid directory or file
        # if self.load_label_type == 0:
        #     pass
        # elif self.load_label_type == 3:
        #     if os.path.exists(self.label_dir[self.load_label_type]) and os.path.isfile(self.label_dir[self.load_label_type]):
        #         pass
        #     else:
                
        #         QMessageBox().about("Wrong file"  ,"Your data file is not valid")
        # else:
        #     if os.path.exists(self.label_dir[self.load_label_type]) and os.path.isdir(self.label_dir[self.load_label_type]):
        #         pass
        #     else:
        #         QMessageBox().about("Wrong dir"  ,"Your data directory is not valid")
        


        #경고창
        #QMessageBox().about("창이름"  ,"메세지 내용")
'''
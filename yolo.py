from ultralytics import YOLO
import  yaml
import torch
from IPython.display import Image, clear_output
from glob import glob#리스트 정리용 라이브러리
from multiprocessing import freeze_support


import os




if __name__ == '__main__':
    freeze_support()
    try:
        # Load a model
        model = YOLO('yolov8n.pt')  # build a new model from scratch
        model.train(data="./mvp2.yaml", pretrained=True, patience=800 ,epochs=800, optimizer = 'Adam', save_period=100, imgsz=720, batch=8, lr0 = 0.001, lrf=0.001)  # train the model
    except Exception as e:
        #failList.append(1)
        print("An exception was raised:", e)

# if __name__ == '__main__':
#     freeze_support()
#     print({torch.__version__}, {torch.cuda.get_device_properties(0).name if torch.cuda.is_available() else "CPU"})


#     os.chdir(r'D:\OneDrive - 아주대학교\1st\CapDesign\code')
#     '''
#     # Load a model
#     model = YOLO("yolov8n.yaml")  # build a new model from scratch
#     model.train(data="./export-2023-03-24T15_46_56.209Z/export-2023-03-24T15_46_56.209Z.yaml", epochs=2000, patience=50, optimizer = 'Adam', save_period=100, imgsz=1080)  # train the model
#     '''
#     end_of_train = 0
#     failList = []

#     if 1 in failList or end_of_train == 0:
#         #cocotext dataset train test
#         # model = None
#         # try:
#         #     # Load a model
#         #     model = YOLO('yolov8n.pt')  # build a new model from scratch
#         #     #model.train(data="./export-2023-03-24T15_46_56.209Z/export-2023-03-24T15_46_56.209Z.yaml", pretrained=True, patience=0, epochs=6000, optimizer = 'Adam', save_period=100, imgsz=720, lr0 = 0.001, lrf=0.001)  # train the model
#         #     model.train(data='coco128.yaml', epochs=100, imgsz=1080, batch=8, workers=2)
#         # except Exception as e:
#         #     failList.append(1)
#         #     print("An exception was raised:", e)

#         model = None
#         try:
#             # Load a model
#             model = YOLO('yolov8n.pt')  # build a new model from scratch
#             model.train(data="./mvp2.yaml", pretrained=True, patience=800 ,epochs=800, optimizer = 'Adam', save_period=100, imgsz=720, batch=8, lr0 = 0.001, lrf=0.001)  # train the model
#         except Exception as e:
#             failList.append(1)
#             print("An exception was raised:", e)


#     if False:
#         model = None
#         try:
#             # Load a model
#             model = YOLO("./runs/detect/train/weights/last.pt")  # build a new model from scratch
#             model.train(data="./export-2023-03-24T15_46_56.209Z/export-2023-03-24T15_46_56.209Z.yaml", pretrained=True, patience=1000, epochs=6000, optimizer = 'Adam', save_period=100, imgsz=720, lr0 = 0.001, lrf=0.001)  # train the model
#             print("faillist: ", failList)
#         except Exception as e:
#             failList.append(2)
#             print("An exception was raised:", e)

#     if False:
#         model = None
#         try:
#             # Load a model
#             model = YOLO("./runs/detect/train2/weights/last.pt")  # build a new model from scratch
#             model.train(data="./export-2023-03-24T15_46_56.209Z/export-2023-03-24T15_46_56.209Z.yaml", pretrained=True, epochs=6000, optimizer = 'Adam', save_period=100, imgsz=720, lr0 = 0.001, lrf=0.001)  # train the model
#             print("faillist: ", failList)
#         except Exception as e:
#             failList.append(3)
#             print("An exception was raised:", e)
    
#     end_of_train = 1



#     #model.train(data="./export-2023-03-24T15_46_56.209Z/export-2023-03-24T15_46_56.209Z.yaml", epochs=2000, patience=200, optimizer = 'Adam', save_period=100, imgsz=960, lr0 = 0.001, lrf=0.001)  # train the model
#     #model.train(data="./export-2023-03-24T15_46_56.209Z/export-2023-03-24T15_46_56.209Z.yaml", epochs=2000, patience=200, imgsz=960)  # train the model
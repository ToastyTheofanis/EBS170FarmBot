from ultralytics import YOLO

best = "C:/Users/Irvin/Coding Projects/FarmBot-API-scripts-main/best.pt"
last_image = "C:/Users/Irvin/Coding Projects/FarmBot-API-scripts-main/Images"
model = YOLO(best)
results = model.predict(last_image, save=True, conf=0.8, show=True, save_txt=True)  
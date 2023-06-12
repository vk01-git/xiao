import cv2

# 加载人脸识别分类器
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# 加载图像
img = cv2.imread('test.jpg')

# 将图像转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 检测人脸
faces = face_cascade.detectMultiScale(gray, 1.3, 5)

# 在图像中标记人脸
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

# 显示图像
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

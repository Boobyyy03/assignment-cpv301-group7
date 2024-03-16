import numpy as np
import cv2
import sys
import os

FREQ_DIV = 5  # frequency divider for capturing training images
RESIZE_FACTOR = 4
NUM_TRAINING = 200


class TrainEigenFaces:
    def __init__(self):
        cascPath = "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(cascPath)
        self.face_dir = 'face_data'
        self.face_name = sys.argv[1]
        self.path = os.path.join(self.face_dir, self.face_name)
        if not os.path.isdir(self.path):
            os.mkdir(self.path)
        self.model = cv2.face.EigenFaceRecognizer_create()
        self.count_captures = 0
        self.count_timer = 0

    def capture_training_images(self):
        video_capture = cv2.VideoCapture(0)
        while True:
            self.count_timer += 1
            ret, frame = video_capture.read()
            inImg = np.array(frame)
            outImg = self.process_image(inImg)
            cv2.imshow('Video', outImg)

            # When everything is done, release the capture on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                video_capture.release()
                cv2.destroyAllWindows()
                return

    def comput_hist(self, img):
        hist = np.zeros((256,))
        row, colum = img.shape[:2]

        for i in range(row):
            for j in range(colum):
                hist[img[i][j]] += 1
        return hist

    def equalize_hist(self, img):
        hist = self.comput_hist(img)
        cumulator = np.zeros_like(hist, np.float64)
        for i in range(len(cumulator)):
            cumulator[i] = hist[:i].sum()
        new_hist = 255 * (cumulator - cumulator.min()) / (cumulator.max() - cumulator.min())
        row, colum = img.shape[:2]
        for i in range(row):
            for j in range(colum):
                img[i, j] = new_hist[img[i, j]]
        return img

    def gen_gaussian_kernel(self, k_size, sigma):
        center = k_size // 2
        x, y = np.mgrid[0 - center: k_size - center, 0 - center: k_size - center]
        kernal = 1 / (2 * np.pi * sigma) * np.exp(-(np.square(x) + np.square(y)) / (2 * np.square(sigma)))
        return kernal

    def gaussian_filter(self, img, k_size=3, sigma=1):
        h, w = img.shape[:2]
        output = np.zeros((h - 2, w - 2))
        kernal_met = self.gen_gaussian_kernel(k_size, sigma)
        for i in range(0, h - 2):
            for j in range(0, w - 2):
                value = np.sum(img[i:i + 3, j:j + 3] * kernal_met)
                output[i, j] = value
        return output.astype(np.uint8)

    def process_image(self, inImg):
        frame = cv2.flip(inImg, 1)
        resized_width, resized_height = (112, 92)
        if self.count_captures < NUM_TRAINING:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # gray_resized = cv2.resize(gray, (gray.shape[1]/RESIZE_FACTOR, gray.shape[0]/RESIZE_FACTOR))
            gray_eq = cv2.equalizeHist(gray)
            gray_resized = cv2.resize(gray_eq, (int(gray.shape[1] / RESIZE_FACTOR), int(gray.shape[0] / RESIZE_FACTOR)))

            faces = self.face_cascade.detectMultiScale(
                gray_resized,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            if len(faces) > 0:
                areas = []
                for (x, y, w, h) in faces:
                    areas.append(w * h)
                max_area, idx = max([(val, idx) for idx, val in enumerate(areas)])
                face_sel = faces[idx]

                x = face_sel[0] * RESIZE_FACTOR
                y = face_sel[1] * RESIZE_FACTOR
                w = face_sel[2] * RESIZE_FACTOR
                h = face_sel[3] * RESIZE_FACTOR

                face = gray[y:y + h, x:x + w]
                face_resized = cv2.resize(face, (resized_width, resized_height))
                img_no = sorted([int(fn[:fn.find('.')]) for fn in os.listdir(self.path) if fn[0] != '.'] + [0])[-1] + 1

                if self.count_timer % FREQ_DIV == 0:
                    cv2.imwrite('%s/%s.png' % (self.path, img_no), face_resized)
                    self.count_captures += 1
                    print ("Captured image: ", self.count_captures)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, self.face_name, (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
        elif self.count_captures == NUM_TRAINING:
            print ("Training data captured. Press 'q' to exit.")
            self.count_captures += 1

        return frame

    def eigen_train_data(self):
        imgs = []
        tags = []
        index = 0

        for (subdirs, dirs, files) in os.walk(self.face_dir):
            for subdir in dirs:
                img_path = os.path.join(self.face_dir, subdir)
                for fn in os.listdir(img_path):
                    path = img_path + '/' + fn
                    tag = index
                    new_img = cv2.imread(path, 0)
                    new_img = self.equalize_hist(new_img)
                    new_img = self.gaussian_filter(new_img, 3, 1)
                    imgs.append(new_img)
                    tags.append(int(tag))
                index += 1
        (imgs, tags) = [np.array(item) for item in [imgs, tags]]

        self.model.train(imgs, tags)
        self.model.save('eigen_trained_data.xml')
        print("Training completed successfully")
        return


if __name__ == '__main__':
    trainer = TrainEigenFaces()
    trainer.capture_training_images()
    trainer.eigen_train_data()
    print("Type in next user to train, or press Recognize")

import os
import face_recognition
from sklearn import svm

def load_training_data(train_dir):
    encodings = []
    names = []

    # Lặp qua tất cả các tệp trong thư mục train
    for file_name in os.listdir(train_dir):
        image_path = os.path.join(train_dir, file_name)

        # Kiểm tra xem file có phải là hình ảnh không
        if os.path.isfile(image_path) and image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Đọc hình ảnh
            image = face_recognition.load_image_file(image_path)
            
            # Trích xuất và mã hóa khuôn mặt nếu có
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                encoding = face_encodings[0]

                # Lấy tên của người từ tên tệp
                name = os.path.splitext(file_name)[0]

                # Thêm mã hóa và tên vào danh sách
                encodings.append(encoding)
                names.append(name)

    return encodings, names

if __name__ == "__main__":
    # Thư mục chứa dữ liệu huấn luyện
    train_dir = r'C:\Users\Administrator\Desktop\HoangTMSE171715_AIL303m_slot18_SVM\train'

    # Load dữ liệu huấn luyện từ thư mục
    encodings, names = load_training_data(train_dir)

    # Tạo và huấn luyện mô hình SVM
    clf = svm.SVC(gamma='scale')
    # clf.fit(encodings, names)

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from PIL import Image, ImageTk
from Capture import record
import time

# Tạo từ điển chứa tên sinh viên và số thẻ tương ứng
name_dict = {
    'Roll Number': 'Name of the Student',
    'SE171715': 'Minh Hoang',
    'Roll_01': '<Tên 01>',
    'Roll_02': '<Tên 02>',
    # Các số thẻ và tên sinh viên tương ứng sẽ được thêm vào ở đây...
}

# Hàm cập nhật danh sách điểm danh
def update_attendance():
    # Đọc dữ liệu từ tệp CSV
    with open('Attendance.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Xóa tất cả các hàng hiện có trong Treeview
    tree.delete(*tree.get_children())
    
    # Chèn dữ liệu mới từ tệp CSV vào Treeview
    for i, row in enumerate(data, 1):
        tree.insert('', 'end', values=(i,) + tuple(row))

    # Lấy tên sinh viên được thêm vào cuối cùng
    last_added_name = data[-1][0] if data else ''

    # Cập nhật nhãn với thông tin chi tiết của sinh viên cuối cùng được thêm vào
    try:
        name_label.config(text=format_student_details(name_dict[last_added_name], last_added_name))
    except KeyError:
        print("KeyError: last_added_name =", last_added_name)

    # Chọn hàng cuối cùng trong Treeview
    tree.selection_set(tree.get_children()[-1])

    # Đường dẫn của hình ảnh dựa trên tên sinh viên cuối cùng
    image_path = 'faces/{}.jpg'.format(last_added_name)
    try:
        # Load và điều chỉnh kích thước hình ảnh
        image = Image.open(image_path)
        image = image.resize((300, 300))
        # Chuyển đổi hình ảnh sang đối tượng PhotoImage của Tkinter
        photo = ImageTk.PhotoImage(image)
        # Hiển thị hình ảnh trong một Label của Tkinter
        image_label.config(image=photo)
        image_label.image = photo  # Giữ tham chiếu đến hình ảnh
    except Exception as e:
        messagebox.showinfo('Information', 'Your Attendance is marked!\nPress [esc] to return')

# Hàm theo dõi thay đổi trong tệp CSV
def detect_file_change():
    modified_time = os.path.getmtime('Attendance.csv')
    if modified_time > detect_file_change.last_modified_time:
        update_attendance()  # Cập nhật danh sách điểm danh trong GUI
        detect_file_change.last_modified_time = modified_time
    clock.config(text=time.strftime("Date: %d-%m-%Y\nTime: %I:%M:%S"), background='light steel blue')
    window.after(1000, detect_file_change)

# Tạo cửa sổ GUI
window = tk.Tk()
window.title("Attendance Recording System")
window.geometry("1500x1000")
window['bg'] = 'light steel blue'

# Label hiển thị thời gian
clock = tk.Label(window, background='white', foreground='black', font=('arial', 25, 'bold'), justify='left')
style = ttk.Style()
style.configure("Custom.Treeview", font=('Arial', 15))

# Tạo widget Treeview để hiển thị danh sách điểm danh
tree = ttk.Treeview(window, columns=('No.', 'Name', 'Time', 'Date'), show='headings', style='Custom.Treeview')
name_label = tk.Label(window, font=('Arial', 25), background='deep sky blue', fg='black', justify='left',
                      relief='solid', borderwidth=5)
atten_name = tk.Label(window, text='Attendance System', font=('Arial', 20), fg='black', relief='solid', borderwidth=5)

# Hàm định dạng chi tiết sinh viên
def format_student_details(name, roll_no):
    formatted_text = "Name    : {}\n".format(name)
    formatted_text += "Roll No  : {}\n".format(roll_no)
    formatted_text += "Branch  : CSE\n"
    formatted_text += "Section  : C"
    return formatted_text

def update_student_details(name, roll_no):
    student_details_text = format_student_details(name, roll_no)
    name_label.config(text=student_details_text)

# Label để hiển thị hình ảnh sinh viên
image_label = tk.Label(window, background='#34495e')
# Tạo nút để chạy hàm record() khi điểm danh
button = tk.Button(window, text="Take Attendance", command=record, background='green2', font=('Arial', 20, 'bold'),
                   fg='black', relief='solid', borderwidth=4)

# Thiết lập cấu trúc lưới cho các thành phần trong cửa sổ
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Cấu hình bố cục dạng lưới
atten_name.grid(row=0, column=0, sticky='n', pady=20)
image_label.grid(row=0, column=0, padx=2, pady=0)
student_details_label = ttk.Label(window, text="Student Details:", font=('Arial', 15, 'bold'),
                                   padding=(10, 10))
student_details_label.grid(row=0, column=0, padx=5, pady=2, sticky='s')
name_label.grid(row=1, column=0, padx=5, sticky='s')
tree.grid(row=0, column=1, sticky='ewns')

# Đặt trọng số hàng 1 thành 1, để nó chiếm không gian dọc còn lại
button.grid(row=2, column=0, padx=20, pady=20)
clock.grid(row=3, column=0, columnspan=3, padx=100, pady=3, sticky='w')

# Lấy thời gian sửa đổi cuối cùng của tệp CSV
detect_file_change.last_modified_time = os.path.getmtime('Attendance.csv')

# Cập nhật danh sách điểm danh ban đầu
update_attendance()

# Bắt đầu theo dõi thay đổi trong tệp CSV
detect_file_change()

# Bắt đầu vòng lặp chính của GUI
window.mainloop()

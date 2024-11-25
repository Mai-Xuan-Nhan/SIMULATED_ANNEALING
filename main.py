from ui import InventoryManagementApp  # Nhập lớp InventoryManagementApp từ file ui.py
import ttkbootstrap as ttkb  # Nhập thư viện ttkbootstrap, một thư viện giao diện người dùng đẹp và hiện đại, cải tiến từ tkinter

if __name__ == "__main__":  # Kiểm tra xem đoạn mã có đang được chạy trực tiếp hay không
    # Tạo cửa sổ chính của ứng dụng sử dụng ttkbootstrap với chủ đề "solar"
    root = ttkb.Window(themename="solar")  # Tạo một cửa sổ ứng dụng với chủ đề "solar"
    
    # Tạo đối tượng InventoryManagementApp và gắn vào cửa sổ root
    app = InventoryManagementApp(root)
    
    # Bắt đầu vòng lặp chính của giao diện người dùng
    root.mainloop()  # Chạy vòng lặp chính của ttkbootstrap (giao diện người dùng)

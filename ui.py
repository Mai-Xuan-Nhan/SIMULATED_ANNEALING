import ttkbootstrap as ttkb  # Thư viện giao diện hiện đại, cải tiến từ tkinter
from ttkbootstrap.constants import *  # Các hằng số giao diện (PRIMARY, SUCCESS, INFO, v.v.)
from tkinter import messagebox, Text  # Thư viện tkinter gốc: messagebox để hiển thị thông báo, Text để nhập/xuất văn bản
import csv  # Đọc file CSV
from knapsack_algorithm import simulated_annealing  # Hàm giải bài toán tối ưu hóa balo (knapsack)

class InventoryManagementApp:
    def __init__(self, root):
        # Thiết lập cửa sổ chính
        self.root = root
        self.root.title("Quản lý hàng tồn kho - Simulated Annealing")  # Tiêu đề ứng dụng

        self.items = []  # Danh sách các vật phẩm (lưu trữ dữ liệu nhập vào)
        self.run_count = 0  # Đếm số lần chạy thuật toán (hiển thị trong lịch sử)

        # Tạo hai khung chính: khung trái và khung phải
        left_frame = ttkb.Frame(self.root)  # Khung bên trái (nhập dữ liệu, nút điều khiển)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_frame = ttkb.Frame(self.root)  # Khung bên phải (hiển thị kết quả, lịch sử)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # ===========================
        # Khu vực bên trái (left_frame)
        # ===========================

        # Tiêu đề cho khu vực nhập liệu
        ttkb.Label(left_frame, text="Dữ liệu hàng tồn kho", bootstyle=INFO).pack(pady=10)

        # Bảng hiển thị dữ liệu vật phẩm
        self.tree = ttkb.Treeview(
            left_frame, columns=("Name", "Value", "Weight"), show="headings", bootstyle=SUCCESS
        )
        self.tree.heading("Name", text="Tên")  # Cột tên
        self.tree.heading("Value", text="Giá trị")  # Cột giá trị
        self.tree.heading("Weight", text="Trọng lượng")  # Cột trọng lượng
        self.tree.pack(pady=10, fill="both", expand=True)  # Hiển thị bảng

        # Nút tải dữ liệu từ CSV
        self.load_button = ttkb.Button(
            left_frame, text="Tải dữ liệu từ CSV", command=self.load_data_from_csv, bootstyle=PRIMARY
        )
        self.load_button.pack(pady=5)

        # Nhập dữ liệu thủ công
        entry_frame = ttkb.Frame(left_frame)  # Khung con để chứa các mục nhập dữ liệu
        entry_frame.pack(pady=10)

        # Nhập tên vật phẩm
        ttkb.Label(entry_frame, text="Tên vật phẩm:", bootstyle=INFO).grid(row=0, column=0)
        self.name_entry = ttkb.Entry(entry_frame)  # Ô nhập tên
        self.name_entry.grid(row=0, column=1)

        # Nhập giá trị
        ttkb.Label(entry_frame, text="Giá trị:", bootstyle=INFO).grid(row=1, column=0)
        self.value_entry = ttkb.Entry(entry_frame)  # Ô nhập giá trị
        self.value_entry.grid(row=1, column=1)

        # Nhập trọng lượng
        ttkb.Label(entry_frame, text="Trọng lượng:", bootstyle=INFO).grid(row=2, column=0)
        self.weight_entry = ttkb.Entry(entry_frame)  # Ô nhập trọng lượng
        self.weight_entry.grid(row=2, column=1)

        # Nút thêm vật phẩm
        self.add_button = ttkb.Button(
            entry_frame, text="Thêm vật phẩm", command=self.add_item, bootstyle=SUCCESS
        )
        self.add_button.grid(row=3, columnspan=2, pady=5)

        # Nút xóa toàn bộ dữ liệu
        self.clear_button = ttkb.Button(
            left_frame, text="Xóa Dữ Liệu", command=self.clear_data, bootstyle=DANGER
        )
        self.clear_button.pack(pady=5)

        # Nút xóa vật phẩm đã chọn
        self.delete_selected_button = ttkb.Button(
            left_frame, text="Xóa vật phẩm đã chọn", command=self.delete_selected_item, bootstyle=WARNING
        )
        self.delete_selected_button.pack(pady=5)

        # Nhập trọng lượng tối đa
        ttkb.Label(left_frame, text="Trọng lượng tối đa", bootstyle=INFO).pack()
        self.max_weight_entry = ttkb.Entry(left_frame, bootstyle=PRIMARY)  # Ô nhập trọng lượng tối đa
        self.max_weight_entry.pack()

        # Nút chạy thuật toán
        self.run_button = ttkb.Button(
            left_frame, text="Chạy thuật toán", command=self.run_algorithm, bootstyle=SUCCESS
        )
        self.run_button.pack(pady=10)

        # ===========================
        # Khu vực bên phải (right_frame)
        # ===========================

        # Hiển thị kết quả
        ttkb.Label(right_frame, text="Kết quả", bootstyle=INFO).pack(pady=10)
        self.result_text = Text(right_frame, height=10, width=50, state="disabled")  # Kết quả thuật toán
        self.result_text.pack(pady=10)

        # Hiển thị lịch sử giải pháp
        ttkb.Label(right_frame, text="Lịch sử giải pháp", bootstyle=INFO).pack()
        self.history_text = Text(right_frame, height=20, width=50, state="disabled")  # Lịch sử
        self.history_text.pack(pady=10)

    # ===========================
    # Hàm xử lý dữ liệu
    # ===========================

    def load_data_from_csv(self):
        """Tải dữ liệu từ file CSV."""
        file_path = "D:\SIMULATED_ANNEALING\data_100_unique.csv"  # Đường dẫn file CSV
        try:
            self.items.clear()  # Xóa danh sách hiện tại
            for item in self.tree.get_children():  # Xóa bảng hiển thị
                self.tree.delete(item)
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    name = row['Name']
                    value = int(row['Value'])
                    weight = int(row['Weight'])
                    if value < 0 or weight < 0:  # Bỏ qua nếu giá trị hoặc trọng lượng âm
                        continue
                    self.items.append((name, value, weight))  # Lưu vào danh sách items
                    self.tree.insert("", "end", values=(name, value, weight))  # Hiển thị lên bảng
        except FileNotFoundError:
            messagebox.showerror("Lỗi", f"Không tìm thấy tệp {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi đọc tệp CSV: {e}")

    def add_item(self):
        """Thêm vật phẩm vào danh sách."""
        name = self.name_entry.get()
        if not name:  # Kiểm tra nếu tên bị bỏ trống
            messagebox.showerror("Lỗi", "Tên vật phẩm không được để trống.")
            return
        try:
            value = int(self.value_entry.get())
            weight = int(self.weight_entry.get())
            if value < 0 or weight < 0:  # Kiểm tra giá trị và trọng lượng không được âm
                messagebox.showerror("Lỗi", "Giá trị và trọng lượng không được âm.")
                return
            self.items.append((name, value, weight))  # Lưu vào danh sách items
            self.tree.insert("", "end", values=(name, value, weight))  # Hiển thị lên bảng
            # Ghi vào file CSV
            self.save_data_to_csv()
            # Xóa dữ liệu nhập sau khi thêm
            self.name_entry.delete(0, "end")
            self.value_entry.delete(0, "end")
            self.weight_entry.delete(0, "end")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập giá trị và trọng lượng hợp lệ.")

    def clear_data(self):
        """Xóa toàn bộ dữ liệu."""
        self.items.clear()  # Xóa danh sách vật phẩm
        for item in self.tree.get_children():  # Xóa bảng hiển thị
            self.tree.delete(item)
        # Xóa dữ liệu trong các ô nhập liệu
        self.name_entry.delete(0, "end")
        self.value_entry.delete(0, "end")
        self.weight_entry.delete(0, "end")
        self.max_weight_entry.delete(0, "end")
        # Xóa nội dung kết quả và lịch sử
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, "end")
        self.result_text.config(state="disabled")
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, "end")
        self.history_text.config(state="disabled")

    def delete_selected_item(self):
        """Xóa vật phẩm được chọn trong Treeview."""
        selected_item = self.tree.selection()  # Lấy mục đang được chọn
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một vật phẩm để xóa.")
            return

        for item in selected_item:
            # Lấy dữ liệu của mục được chọn
            values = self.tree.item(item, "values")
            if values:
                name, value, weight = values
                # Xóa khỏi danh sách `self.items`
                self.items = [
                    i for i in self.items
                    if not (i[0] == name and i[1] == int(value) and i[2] == int(weight))
                ]
            # Xóa khỏi Treeview
            self.tree.delete(item)
        # Ghi lại toàn bộ danh sách vào file CSV
        self.save_data_to_csv()

    def run_algorithm(self):
        """Chạy thuật toán tối ưu hóa."""
        # Chuẩn bị dữ liệu đầu vào
        names = [item[0] for item in self.items]
        values = [item[1] for item in self.items]
        weights = [item[2] for item in self.items]
        try:
            max_weight = int(self.max_weight_entry.get())  # Lấy trọng lượng tối đa
            if max_weight < 0:  # Kiểm tra trọng lượng tối đa không được âm
                messagebox.showerror("Lỗi", "Trọng lượng tối đa không được âm.")
                return
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập trọng lượng tối đa hợp lệ.")
            return
        if not self.items:
            messagebox.showerror("Lỗi", "Danh sách vật phẩm trống. Vui lòng nhập dữ liệu.")
            return

        # Gọi thuật toán
        selected_items, history = simulated_annealing(names, values, weights, max_weight)

        # Tính tổng giá trị và trọng lượng
        total_value = sum(values[i] for i, name in enumerate(names) if name in selected_items)
        total_weight = sum(weights[i] for i, name in enumerate(names) if name in selected_items)

        # Hiển thị kết quả
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, "end")
        self.result_text.insert("end", f"Tổng giá trị: {total_value}\n")
        self.result_text.insert("end", f"Tổng trọng lượng: {total_weight}\n")
        self.result_text.insert("end", f"Vật phẩm chọn: {','.join(selected_items)}")
        self.result_text.config(state="disabled")

        # Hiển thị lịch sử giải pháp
        self.history_text.config(state="normal")
        self.history_text.insert("end", "\n".join(history))
        self.history_text.config(state="disabled")

    #Lưu lại dữ liệu sau khi thao tác thêm, xóa
    def save_data_to_csv(self):
        """Ghi toàn bộ dữ liệu vào file CSV."""
        file_path = "D:\Download\KnapsackApp_PY-main (1)\KnapsackApp_PY-main\data_100_unique.csv"
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                # Ghi tiêu đề cột
                writer.writerow(["Name", "Value", "Weight"])
                # Ghi từng dòng dữ liệu
                for item in self.items:
                    writer.writerow(item)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu dữ liệu vào file CSV: {e}")

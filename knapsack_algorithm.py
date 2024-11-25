import random  # Thư viện random để sinh số ngẫu nhiên
import math  # Thư viện math để tính toán các hàm toán học (như hàm exp)

def simulated_annealing(names, values, weights, max_weight, initial_temp=10000, cooling_rate=0.95, max_iter=1000):
    """Giải bài toán knapsack bằng thuật toán Simulated Annealing."""
    
    # Khởi tạo giải pháp ban đầu: ba lô rỗng (không chọn vật phẩm nào)
    current_solution = [0] * len(names)  # Biểu diễn nhị phân: 0 -> không chọn, 1 -> chọn
    current_value = 0  # Giá trị của giải pháp hiện tại
    current_weight = 0  # Trọng lượng của giải pháp hiện tại

    # Lịch sử các giải pháp để hiển thị cho việc trực quan hóa
    history = []

    # Hàm phụ để tính tổng giá trị và tổng trọng lượng của một giải pháp
    def get_value_weight(solution):
        total_value = sum(v for i, v in enumerate(values) if solution[i] == 1)  # Tổng giá trị của các vật phẩm được chọn
        total_weight = sum(w for i, w in enumerate(weights) if solution[i] == 1)  # Tổng trọng lượng của các vật phẩm được chọn
        return total_value, total_weight

    # Hàm sinh ra một giải pháp láng giềng bằng cách đảo ngược một vật phẩm ngẫu nhiên
    def neighbor(solution):
        new_solution = solution[:]  # Sao chép giải pháp hiện tại
        index = random.randint(0, len(solution) - 1)  # Chọn ngẫu nhiên một vật phẩm để thay đổi
        new_solution[index] = 1 - new_solution[index]  # Đảo ngược giá trị (chọn hoặc bỏ chọn vật phẩm)
        return new_solution

    # Khởi tạo nhiệt độ ban đầu
    temperature = initial_temp
    best_solution = current_solution[:]  # Giải pháp tốt nhất tìm được, bắt đầu bằng giải pháp ban đầu
    best_value, best_weight = get_value_weight(best_solution)  # Tính giá trị và trọng lượng của giải pháp tốt nhất

    for iteration in range(max_iter):
        # Sinh ra một giải pháp láng giềng
        new_solution = neighbor(current_solution)
        new_value, new_weight = get_value_weight(new_solution)  # Tính giá trị và trọng lượng của giải pháp láng giềng

        # Kiểm tra nếu giải pháp mới tốt hơn hoặc chấp nhận giải pháp tồi hơn theo quy tắc Simulated Annealing
        if new_weight <= max_weight and (new_value > current_value or random.random() < math.exp((new_value - current_value) / temperature)):
            current_solution = new_solution  # Chấp nhận giải pháp mới
            current_value = new_value  # Cập nhật giá trị giải pháp hiện tại
            current_weight = new_weight  # Cập nhật trọng lượng giải pháp hiện tại

            # Cập nhật giải pháp tốt nhất nếu giải pháp hiện tại tốt hơn
            if current_value > best_value:
                best_solution = current_solution[:]  # Lưu giải pháp tốt nhất
                best_value = current_value
                best_weight = current_weight

        # Lưu lịch sử của giải pháp tại mỗi vòng lặp để hiển thị
        selected_items = [names[i] for i, taken in enumerate(current_solution) if taken == 1]  # Lấy tên các vật phẩm được chọn
        history.append(f" {iteration}:  Value: {current_value}, Weight: {current_weight}, Temperature:{temperature} ")

        # Giảm nhiệt độ theo tỷ lệ làm mát
        temperature *= cooling_rate

    # Trả về giải pháp tốt nhất tìm được và lịch sử các giải pháp
    selected_items = [names[i] for i, taken in enumerate(best_solution) if taken == 1]  # Lấy các vật phẩm tốt nhất được chọn
    return selected_items, history

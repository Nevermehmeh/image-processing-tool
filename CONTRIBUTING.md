# Hướng dẫn Đóng góp

Cảm ơn bạn đã quan tâm đến việc đóng góp cho dự án Image Processor! Tài liệu này sẽ hướng dẫn bạn cách đóng góp một cách hiệu quả.

## Mã ứng xử

Trước tiên, hãy đảm bảo đọc và tuân thủ [Quy tắc ứng xử](CODE_OF_CONDUCT.md) của chúng tôi. Chúng tôi cam kết tạo ra một môi trường thân thiện và tôn trọng cho tất cả mọi người.

## Báo cáo lỗi

Khi báo cáo lỗi, vui lòng:

1. **Tìm kiếm trước** để đảm bảo lỗi chưa được báo cáo
2. Sử dụng template báo cáo lỗi có sẵn
3. Mô tả rõ ràng các bước để tái tạo lỗi
4. Bao gồm thông tin phiên bản, hệ điều hành và các thông tin liên quan

## Đề xuất tính năng mới

Chúng tôi luôn chào đón các đề xuất cải tiến. Khi đề xuất tính năng mới:

1. Giải thích rõ vấn đề mà tính năng này giải quyết
2. Mô tả chi tiết cách bạn muốn triển khai nó
3. Đề xuất các giải pháp thay thế (nếu có)
4. Bao gồm các ví dụ minh họa (nếu có thể)

## Quy trình đóng góp code

### 1. Fork repository

1. Fork repository này về tài khoản GitHub của bạn
2. Clone về máy tính cá nhân:
   ```bash
   git clone https://github.com/your-username/image_processor.git
   cd image_processor
   ```

### 2. Thiết lập môi trường phát triển

1. Tạo và kích hoạt môi trường ảo:
   ```bash
   # Trên Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # Trên macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Cài đặt các phụ thuộc:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. Tạo file cấu hình:
   ```bash
   cp .env.example .env
   ```
   Và cập nhật các biến môi trường cần thiết

4. Khởi tạo cơ sở dữ liệu:
   ```bash
   flask db upgrade
   ```

### 3. Tạo nhánh mới

Tạo một nhánh mới cho tính năng/sửa lỗi của bạn:
```bash
git checkout -b feature/your-feature-name
# hoặc
# git checkout -b bugfix/description-of-fix
```

### 4. Thực hiện thay đổi

1. Thực hiện các thay đổi cần thiết
2. Chạy kiểm tra:
   ```bash
   pytest
   ```
3. Đảm bảo code tuân thủ các quy tắc định dạng:
   ```bash
   black .
   isort .
   flake8 .
   ```
4. Cập nhật tài liệu nếu cần

### 5. Commit và push

1. Commit các thay đổi của bạn:
   ```bash
   git add .
   git commit -m "Mô tả ngắn gọn về thay đổi"
   ```
2. Push lên repository của bạn:
   ```bash
   git push origin your-branch-name
   ```

### 6. Tạo Pull Request

1. Truy cập repository gốc trên GitHub
2. Nhấn "Compare & pull request"
3. Điền đầy đủ thông tin theo template
4. Gắn nhãn phù hợp (bug, enhancement, documentation, v.v.)
5. Chờ phản hồi từ người bảo trì

## Hướng dẫn viết code

### Quy ước đặt tên

- **Biến và hàm**: Sử dụng `snake_case`
- **Lớp**: Sử dụng `PascalCase`
- **Hằng số**: Sử dụng `UPPER_CASE`
- **Module**: Sử dụng `snake_case`

### Tài liệu code

1. **Docstrings**: Tuân thủ theo chuẩn Google Python Style Guide
   ```python
   def example_function(param1, param2):
       """Mô tả ngắn gọn về hàm.

       Mô tả chi tiết hơn về chức năng của hàm, các tham số và giá trị trả về.

       Args:
           param1 (type): Mô tả tham số 1.
           param2 (type): Mô tả tham số 2.

       Returns:
           type: Mô tả giá trị trả về.

       Raises:
           ValueError: Mô tả khi nào lỗi được ném ra.
       """
   ```

2. **Comments**: Giải thích lý do tại sao hơn là mô tả cái gì

### Kiểm thử

- Viết test cho mọi tính năng mới
- Đảm bảo tỷ lệ bao phủ code cao (>=80%)
- Chạy tất cả các test trước khi tạo pull request

## Quy trình đánh giá code

1. Pull request sẽ được xem xét bởi ít nhất một người bảo trì
2. Có thể có phản hồi và yêu cầu thay đổi
3. Khi đã được phê duyệt, pull request sẽ được merge bởi người bảo trì

## Ghi công

Mọi đóng góp đều được ghi nhận trong [tài liệu đóng góp](CONTRIBUTORS.md).

## Câu hỏi?

Nếu bạn có bất kỳ câu hỏi nào, vui lòng mở một issue mới với nhãn `question`.

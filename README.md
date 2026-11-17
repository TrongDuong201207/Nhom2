[README.md](https://github.com/user-attachments/files/34962037/README.md)
# Student Grade System - Tuần 4 / Demo mốc 1

Dự án Django mẫu bám theo báo cáo Tuần 1-3: Django + SQLite, Custom User, quản lý Student, Course, CourseSection và Enrollment. Module `grading` đã có model và hàm tính điểm nền tảng để nối tiếp ở giai đoạn sau; giao diện nhập điểm/báo cáo chưa thuộc phạm vi demo mốc 1.

## 1. Yêu cầu
- Python 3.10+ (khuyến nghị Python 3.11/3.12)
- Django 5.2.x

## 2. Cài đặt trên Windows
```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## 3. Khởi tạo cơ sở dữ liệu
`AUTH_USER_MODEL = "accounts.User"` đã được khai báo trong `config/settings.py`. Giữ nguyên cấu hình này trước lần migrate đầu tiên.

```powershell
python manage.py makemigrations accounts students academics enrollments grading
python manage.py migrate
python manage.py createsuperuser
```

## 4. Tạo dữ liệu demo (tùy chọn)
Dùng dữ liệu giả lập, không nhập dữ liệu cá nhân thật. Đặt mật khẩu demo riêng tại máy local:
```powershell
python manage.py seed_demo --password "DemoOnly-2026!"
```
Tài khoản giáo vụ mẫu: `giaovu_demo`; mật khẩu là giá trị đã truyền sau `--password`.

## 5. Chạy ứng dụng
```powershell
python manage.py runserver
```
Mở `http://127.0.0.1:8000/`. Đăng nhập bằng tài khoản quản trị hoặc `giaovu_demo`.

## 6. Chức năng có trong mốc 1
- Đăng nhập/đăng xuất bằng Django Authentication; role `STUDENT`, `LECTURER`, `ACADEMIC_STAFF`, `ADMIN`.
- CRUD hồ sơ sinh viên, mã sinh viên duy nhất, kiểm tra email và trường bắt buộc.
- Quản lý danh mục Course; quản lý CourseSection, mở/đóng lớp.
- Gán sinh viên vào CourseSection; chỉ lớp `OPEN` nhận đăng ký; chống trùng bằng form/service và UNIQUE constraint ở CSDL.
- Dashboard đếm sinh viên, học phần, lớp và lượt đăng ký từ DB.
- `grading` có các model GradeComponent/Grade và hàm tính tổng kết theo trọng số; phần giao diện nhập điểm được dành cho giai đoạn tiếp theo.

## 7. Chạy kiểm thử
```powershell
python manage.py test students academics enrollments grading
```
Các test bao gồm mã sinh viên/học phần/lớp không trùng, role, đăng ký trùng, lớp đóng và phép tính 8.0×20% + 7.0×30% + 9.0×50% = 8.20.

## 8. Git
```powershell
git init
git branch -M main
git add .
git commit -m "feat: implement milestone 1 core CRUD and persistence"
```
Tạo remote trên GitHub/GitLab của nhóm, sau đó thêm URL thực tế và push. Không commit `.venv`, `.env`, `db.sqlite3`, mật khẩu hoặc dữ liệu cá nhân.

## 9. Lưu ý phạm vi
Đây là bộ mã khởi đầu cho demo mốc 1. Nhóm phải cài Django, chạy migration, chạy test, kiểm tra trên trình duyệt và chụp minh chứng trên máy của nhóm trước khi ghi nhận chức năng đã chạy thành công. Mật khẩu `SECRET_KEY` trong settings chỉ dành cho môi trường local; thay bằng biến môi trường khi triển khai.


## 10. Tuần 5 / Demo mốc 2
Xem `docs/HUONG_DAN_TUAN5.md` để cài đặt, cấu hình role, nhập điểm, tìm kiếm, thống kê, xuất CSV và chạy test.
- Bảng điểm: `/grading/`
- Điểm sinh viên: `/grading/my/`
- Tìm kiếm: `/grading/search/`
- Thống kê: `/grading/statistics/`
- Kiểm thử: `python manage.py test grading`

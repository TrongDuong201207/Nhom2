# HƯỚNG DẪN BỔ SUNG DEMO 2 – TUẦN 5
## Hệ thống quản lý sinh viên và điểm số

Phiên bản này phát triển trực tiếp từ source Demo mốc 1 người dùng cung cấp. Các model hiện có được tái sử dụng: `Student`, `Course`, `CourseSection`, `Enrollment`, `GradeComponent`, `Grade`. Không tạo lại dự án hoặc thay đổi tên ứng dụng.

## 1. Chức năng được bổ sung

### FR04 – Cấu hình thành phần điểm và nhập điểm
- Chọn lớp học phần để mở bảng điểm.
- Thêm thành phần điểm với tên, trọng số và thứ tự.
- Không cho tổng trọng số vượt quá 100%; chỉ khi tổng đúng 100% và sinh viên có đủ điểm thành phần mới tính điểm tổng kết.
- Nhập/sửa điểm cho từng sinh viên; điểm hợp lệ từ 0 đến 10, tối đa 2 chữ số thập phân.
- Điểm được lưu cùng người cập nhật và thời điểm cập nhật.
- Giảng viên chỉ được thao tác trên lớp có `teacher_user` đúng bằng tài khoản của mình.

### FR05 – Tìm kiếm và lọc kết quả
- Tìm theo mã sinh viên, họ tên, mã lớp hoặc tên học phần.
- Lọc theo học phần, học kỳ, năm học.
- Có thể kết hợp nhiều bộ lọc và xóa bộ lọc.
- Giảng viên chỉ nhìn thấy các lớp do mình phụ trách.

### FR06 – Thống kê và xuất CSV
- Tổng số lượt đăng ký trong tập dữ liệu đã lọc.
- Số lượt đã đủ điểm / chưa đủ điểm.
- Số đạt / chưa đạt; ngưỡng đạt mặc định là 4.00/10.
- Điểm trung bình và tỷ lệ đạt.
- Xuất kết quả CSV theo đúng bộ lọc đang áp dụng, hỗ trợ Excel bằng BOM UTF-8.

### Phân quyền
| Vai trò | Quyền trong Demo 2 |
|---|---|
| ADMIN / superuser | Quản trị toàn hệ thống, xem và quản lý mọi lớp/điểm |
| ACADEMIC_STAFF | Quản lý hồ sơ, học phần, lớp, đăng ký; xem tìm kiếm/thống kê toàn bộ; nhập điểm trong phạm vi lớp qua giao diện điểm |
| LECTURER | Chỉ xem lớp được phân công; cấu hình thành phần, nhập/sửa điểm lớp được phân công; tìm kiếm/thống kê/CSV trong phạm vi lớp đó |
| STUDENT | Chỉ xem điểm gắn với hồ sơ sinh viên liên kết tài khoản; không vào trang tìm kiếm nội bộ hoặc nhập điểm |

**Lưu ý:** tài khoản sinh viên phải được liên kết với hồ sơ tại trường `Student.user`. Tài khoản giảng viên phải được gán vào `CourseSection.teacher_user`.

## 2. Cài đặt trên Windows bằng VS Code

### Bước 1 – Sao lưu Demo 1
- Đóng server đang chạy.
- Sao chép thư mục dự án Demo 1 thành một bản dự phòng.
- Giải nén ZIP Tuần 5 vào một thư mục mới.
- Trong VS Code chọn `File > Open Folder`, mở thư mục có file `manage.py`.

Không chép riêng từng file vào một dự án khác nếu chưa đối chiếu; ZIP này đã gồm các file thay thế và file mới.

### Bước 2 – Tạo môi trường Python
Mở Terminal (PowerShell) tại thư mục chứa `manage.py`:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn chạy script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Cài Django:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Bước 3 – Tạo database
Source gốc được cung cấp không có thư mục migration được đóng gói. Tạo migration lần đầu:

```powershell
python manage.py makemigrations accounts students academics enrollments grading
python manage.py migrate
```

Nếu máy đã có database Demo 1 và migration cũ đã tồn tại, hãy sao lưu `db.sqlite3` trước; không xóa database đang có dữ liệu. Chạy `makemigrations` và `migrate` như trên để Django đối chiếu thay đổi.

### Bước 4 – Tạo tài khoản quản trị và dữ liệu mẫu
Nếu chưa có superuser:

```powershell
python manage.py createsuperuser
```

Tạo dữ liệu demo giả lập (tùy chọn):

```powershell
python manage.py seed_demo --password "DemoOnly-2026!"
```

Lệnh này tạo/cập nhật tài khoản giáo vụ `giaovu_demo`, học phần `CS101`, lớp `CS101-01`, 3 hồ sơ sinh viên và đăng ký mẫu. Mật khẩu mẫu chỉ dùng local; đổi thành mật khẩu riêng nếu cần. Nếu dữ liệu đã tồn tại, lệnh cập nhật tài khoản demo và không tạo bản ghi đăng ký trùng.

### Bước 5 – Kiểm tra và chạy
```powershell
python manage.py check
python manage.py test students academics enrollments grading
python manage.py runserver
```

Mở `http://127.0.0.1:8000/`.

Nếu `check` hoặc test báo lỗi, lưu toàn bộ thông báo Terminal và xử lý trước khi demo. Môi trường chạy hiện tại không đi kèm Django nên file ZIP được kiểm tra cú pháp Python, nhưng người dùng cần cài requirements và chạy test trên máy của mình.

## 3. Chuẩn bị tài khoản và dữ liệu phân quyền

### Tài khoản giảng viên
1. Vào `/admin/` bằng superuser.
2. Mở Users, tạo tài khoản mới.
3. Chọn `role = LECTURER`, bật `is_active`.
4. Vào Course sections, mở lớp học phần và gán `teacher_user` là tài khoản giảng viên.
5. Đăng xuất admin, đăng nhập tài khoản giảng viên. Tài khoản chỉ thấy lớp được gán.

### Tài khoản sinh viên
1. Trong `/admin/`, tạo User có `role = STUDENT`.
2. Mở Students, sửa hồ sơ sinh viên tương ứng.
3. Chọn trường `user` là tài khoản vừa tạo.
4. Đảm bảo sinh viên có Enrollment trong lớp học phần.
5. Đăng nhập tài khoản sinh viên và mở `/grading/my/`.

Không dùng cùng một tài khoản admin để chứng minh quyền sinh viên. Hãy đăng xuất và đăng nhập từng tài khoản riêng.

## 4. Cách cấu hình và nhập điểm

1. Đăng nhập bằng ADMIN, ACADEMIC_STAFF hoặc giảng viên được phân công.
2. Chọn menu `Quản lý điểm`.
3. Chọn lớp học phần.
4. Nhấn `Thêm thành phần điểm`.
5. Ví dụ tạo ba thành phần:
   - Bài tập: 20.00%
   - Giữa kỳ: 30.00%
   - Cuối kỳ: 50.00%
6. Kiểm tra tổng trọng số hiển thị đúng 100%.
7. Tại dòng sinh viên, chọn `Nhập / sửa điểm`.
8. Chọn thành phần điểm và nhập điểm, ví dụ 8.00; nhấn Lưu điểm.
9. Lặp lại cho các thành phần và sinh viên.

Ví dụ tính điểm:
`8.00 × 20% + 7.00 × 30% + 9.00 × 50% = 8.20`.

Nếu chưa đủ 100% trọng số hoặc thiếu điểm thành phần, hệ thống hiển thị “Chưa đủ điểm” thay vì tự đoán điểm tổng kết. Ngưỡng đạt ở thống kê hiện đặt 4.00; nếu đề cương môn học quy định ngưỡng khác, cần đổi hằng số trong `grading/views.py`.

## 5. Tìm kiếm, thống kê, CSV

- Mở `Tìm kiếm điểm`, nhập một phần mã/tên sinh viên hoặc lớp/học phần.
- Có thể thêm học phần, học kỳ, năm học.
- Nhấn Tìm kiếm để xem kết quả.
- Nhấn Xóa lọc để trở về toàn bộ phạm vi được phép.
- Nhấn Xuất CSV để tải `ket_qua_hoc_tap.csv`.
- Mở `Thống kê` để xem tổng số, đủ điểm, thiếu điểm, đạt, chưa đạt, điểm trung bình và tỷ lệ đạt theo phạm vi dữ liệu.

## 6. Bộ kiểm thử cần chạy và minh chứng

Chạy:

```powershell
python manage.py test grading
```

Các test hiện có kiểm tra phép tính có trọng số, tổng trọng số không hợp lệ và các tình huống quyền truy cập cơ bản: giảng viên đúng lớp được phép, giảng viên không được phân công bị từ chối, sinh viên xem trang điểm cá nhân, sinh viên không được vào trang tìm kiếm nội bộ.

Bảng kiểm thử thủ công nên ghi kết quả sau khi chạy trên máy:
| ID | Thao tác | Kết quả mong đợi |
|---|---|---|
| T16 | Thêm thành phần điểm hợp lệ | Lưu thành công |
| T17 | Thêm trọng số khiến tổng vượt 100% | Báo lỗi, không lưu |
| T18 | Nhập điểm 8.00 | Lưu thành công |
| T19 | Nhập điểm âm hoặc trên 10 | Báo lỗi |
| T20 | Đủ trọng số và đủ điểm | Tính điểm tổng kết |
| T21 | Thiếu thành phần điểm | Chưa đủ điểm |
| T22 | Tìm theo mã sinh viên | Chỉ hiện kết quả phù hợp |
| T23 | Lọc theo học phần/học kỳ/năm | Kết quả đúng bộ lọc |
| T24 | Xuất CSV | Tải file CSV, dữ liệu đúng bộ lọc |
| T25 | Mở thống kê | Số liệu khớp danh sách kết quả |
| T26 | Giảng viên mở lớp được phân công | Cho phép |
| T27 | Giảng viên mở lớp người khác | HTTP 403 |
| T28 | Sinh viên mở trang điểm cá nhân | Chỉ thấy hồ sơ liên kết |
| T29 | Sinh viên mở trang tìm kiếm nội bộ | HTTP 403 |
| T30 | Sinh viên thử truy cập URL nhập điểm | HTTP 403 |
| T31 | Giáo vụ truy cập tìm kiếm/thống kê | Cho phép |
| T32 | Người chưa đăng nhập mở trang điểm | Chuyển đến đăng nhập |

Chỉ đánh dấu Đạt sau khi thực sự chạy và quan sát. Chụp ảnh: bảng thành phần điểm 100%, bảng điểm có điểm tổng kết, kết quả tìm kiếm, trang thống kê, file CSV mở bằng Excel, giảng viên được phép/bị từ chối và trang “Điểm của tôi”.

## 7. Danh sách file chính được bổ sung/thay đổi

- `accounts/permissions.py`: decorator kiểm tra role và phân công giảng viên.
- `grading/forms.py`: form cấu hình thành phần điểm và nhập điểm.
- `grading/views.py`: bảng điểm, nhập/sửa điểm, tìm kiếm, thống kê, CSV, điểm cá nhân.
- `grading/urls.py`: các URL của module điểm.
- `grading/templatetags/grading_tags.py`: hiển thị điểm theo ID thành phần trong template.
- `templates/grading/`: giao diện cho các chức năng.
- `config/urls.py`: đăng ký URL `/grading/`.
- `templates/base.html`, `templates/dashboard.html`: menu và liên kết Demo 2.
- `academics/views.py`, `students/views.py`, `enrollments/views.py`: siết quyền thao tác quản trị.
- `grading/tests.py`: kiểm thử phân quyền bổ sung.

## 8. Giới hạn và lưu ý an toàn

- Đây là bản demo học tập, chưa phải hệ thống production.
- Ngưỡng đạt 4.00 chỉ là mặc định demo; cần xác nhận theo quy định môn học.
- Không đưa dữ liệu sinh viên thật lên hosting công khai khi chưa có biện pháp bảo vệ dữ liệu.
- Không commit mật khẩu, file `.env`, `db.sqlite3` hoặc dữ liệu thật lên Git.
- Người dùng cần tự chạy migrations, tests và xác minh giao diện. Không ghi trong báo cáo là đã kiểm thử thành công nếu chưa có ảnh/chứng cứ chạy thực tế.

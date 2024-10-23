# Dự án Wallet

## Hướng dẫn chạy dự án

### Để chạy dự án, sử dụng lệnh sau:

```bash
python app.py
```

### Quy tắc làm việc với Git
    - Trước khi thực hiện bất kỳ thay đổi nào, hãy đảm bảo thực hiện các bước sau:
        + Pull nhánh develop: Trước khi push code, bạn cần phải kéo (pull) nhánh develop về để đảm bảo rằng bạn đang làm việc trên phiên bản mới nhất.
```bash
    git checkout develop
    git pull origin develop
```

### Tạo nhánh mới: Khi bắt đầu một tính năng mới hoặc sửa lỗi, hãy tạo một nhánh mới từ nhánh develop. Tên nhánh nên theo cấu trúc sau:


```bash
git checkout -b feat/my-feature
```

### Push code: Khi đã hoàn thành công việc, hãy commit và push code lên nhánh của bạn. Lưu ý rằng bạn không được push lên nhánh master, develop, hoặc nhánh của người khác.

```bash
git add .
git commit -m "Mô tả ngắn gọn về thay đổi"
git push origin feat/my-feature
```
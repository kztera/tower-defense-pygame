BTL - Lập trình ứng dụng Python - K1N1 - 2425
---

## Thông tin nhóm:
- A41316 - Nguyễn Hữu Khoa
- A41594 - Lê Ngọc Hiếu

## Đề tài:

Phát triển Game bằng Python với thư viện Pygame

## Thông tin cơ bản/Ý tưởng ban đầu
- Thể loại: Thủ thành (Tower Defense)
- Loại game: Endless Game
- Cách chơi: Đặt căn cứ > Thu thập tài nguyên > Xây tháp bảo vệ căn cứ > Chiến đấu và nâng cấp

## Cách chơi:

Thu thập tài nguyên và xây dựng căn cứ, phòng thủ chống lại thây ma và giành vị trí số 1 trên bảng xếp hạng!

## Các chạy thử:

1. Tạo môi trường ảo:

```bash
python3 -m venv venv
```

2. Kích hoạt môi trường ảo:

```bash
source venv/bin/activate
```

3. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

4. Chạy game:

```bash
cd code
python main.py
```

## Các cơ chế nổi bật:

1. Snap to grid: Có thể dễ dàng xây dựng tháp bảo vệ trên lưới
2. Spawn system: Hệ thống sinh ra quái vật ngẫu nhiên theo cơ chế wave (ngày/đêm) tăng dần độ khó
3. Tấn công tự động: Tháp bảo vệ sẽ tự động tấn công quái vật gần nhất
4. Zombie AI: Quái vật sẽ tìm đường ngắn nhất để tấn công căn cứ

## Custom:

Để sử dụng map to hơn, có thể thay đổi `ASSET_PATH_MAP` trong file `asset_path.py` thành `map.tmx`
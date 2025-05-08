import qrcode

# GitHub 저장소 URL (사용자 지정)
github_url = "https://github.com/bang-min-gi/university_map-"  # 여기로 접속하는 QR 코드 생성

# QR 코드 생성
qr = qrcode.make(github_url)

# QR 코드 이미지 저장 경로
output_path = "C:\\Users\\ai06\\Desktop\\2학년1학기\\목요일 오전\\university_map_qr.png"

# QR 코드 이미지 저장
qr.save(output_path)
print(f"QR 코드 생성 완료: {output_path}")

import hashlib

def generate_password(password: str) -> str:
    # Băm mật khẩu bằng SHA-256 và trả về chuỗi hex
    hash_object = hashlib.sha256(password.encode('utf-8'))
    return hash_object.hexdigest()

def verify_pass(input_password: str, hashed_password_hex: str) -> bool:
    # Băm lại input và so sánh với chuỗi hex đã lưu
    return generate_password(input_password) == hashed_password_hex


# plain_password = "uf5s8"
# # hashed = generate_password(plain_password)
# hashed = "bc54a259ec5ff40806b521da9793d098320694ddd4053ab28d7a9c49b682bb4e"
# print("Hash:", hashed)

# # Kiểm tra
# print("Check đúng:", verify_pass(plain_password, hashed)) 
# # print("Check sai:", verify_pass("wrongpass", hashed))      # ❌ False

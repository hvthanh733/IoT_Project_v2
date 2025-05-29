from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    """Mã hóa mật khẩu bằng werkzeug"""
    return generate_password_hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """So sánh mật khẩu với mật khẩu đã mã hóa"""
    return check_password_hash(hashed_password, password)

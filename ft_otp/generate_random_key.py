import secrets

key = secrets.token_hex(32)  # 32 bytes × 2 hex digits each = 64 characters

with open("random_key.txt", "w") as file:
    file.write(key)
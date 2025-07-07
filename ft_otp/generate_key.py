import secrets

key = secrets.token_hex(32)  # 32 bytes × 2 hex digits each = 64 characters

with open("key.hex", "w") as file:
    file.write(key)
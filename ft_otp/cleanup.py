import os

files_to_delete = [
    "random_key.txt",
    "ft_otp.key",
    "encryption_key.key",
    "counter.json"
]

for filename in files_to_delete:
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Deleted: {filename}")
    else:
        print(f"File not found: {filename}")
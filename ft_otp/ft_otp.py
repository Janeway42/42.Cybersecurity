import os
import argparse
from cryptography.fernet import Fernet
import binascii
import re
import base64
import hmac
import hashlib
import struct
import time
import json
import qrcode
import pyotp

COUNTER_STATE = "counter.json"
generate_qr = False
user_code = -1

def hotp(base32_secret, counter, digits=6):
    # converts the base32 secret into raw binary bites
    key = base64.b32decode(base32_secret) 
    # encodes the counter into an 8-byte message for the hmac
    msg = struct.pack(">Q", counter)
    # generates the hmac hash using the secret in bytes and the counter in bytes
    # .digest() returns the raw binary hash
    hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()
    # takes the last byte of the hash and extracts the lowest 4 bits this gives a number between 0 and 15
    offset = hmac_hash[-1] & 0x0F
    # which is the used to choose a slice of the hash, convert it to an integer
    # then apllies "& 0x7FFFFFFF" to remove the most significant bit (force positive)
    # and then converts the full integer into a shorter numeric code
    code = (struct.unpack(">I", hmac_hash[offset:offset+4])[0] & 0x7FFFFFFF) % (10 ** digits)
    # .zfill adds zeros in front of the integer if necessary to reach the desired length 
    return str(code).zfill(digits)

def get_counter():
    time_step = int(time.time() // 30) # better time tracking than comparing time stamps
    remaining = int (30 - (time.time() % 30))

    if os.path.exists(COUNTER_STATE):
        with open (COUNTER_STATE, "r") as file:
            state = json.load(file)

        last_time_step = state.get("time step")
        counter = state.get("counter", 1)

        if time_step != last_time_step:
            counter += 1
            state["counter"] = counter
            state["time step"] = time_step

            with open(COUNTER_STATE, "w") as file:
                json.dump(state, file)
            
    else: 
        counter = 1
        state = {"counter": counter, "time step": time_step}

        with open(COUNTER_STATE, "w") as file:
            json.dump(state, file)
    
    return counter, remaining

def store_and_encript_key_file(file):
    if not os.path.isfile(file):
        return print(f"File '{file}' does not exist\n")
    
    try:
        with open(file, "r") as file:
            file_content = file.read()

            if len(file_content) < 64 and re.fullmatch(r"[0-9a-fA-F]+", file_content) == False:
                return print("Please provide a hexadecimal key of at least 54 characters\n")
            
            # create encryption key
            try: 
                # generate an encryption key
                encryption_key = Fernet.generate_key()
                cipher = Fernet(encryption_key)

                # save the encryption key
                with open("encryption_key.key", "wb") as key_file:
                    key_file.write(encryption_key)

            except Exception as e:
                print(f"Unable to create encryption key: {e}\n")

            # transform hex key so it can be encrypted by Fernet as it expects a 32-byte base64-encoded key
            raw_content_bytes = binascii.unhexlify(file_content)

            # encrypt data
            encrypted_key = cipher.encrypt(raw_content_bytes)

            # save encrypted data
            with open("ft_otp.key", "wb") as file:
                file.write(encrypted_key)
            print("Key was successfully saved in ft_otp.key.\n")

    except Exception as e:
        print(f"Unable to open file '{file}: {e}\n")

def generate_or_validate_one_time_password(encrypted_file, generate_qr, user_code):
    if not os.path.isfile(encrypted_file):
        return print(f"Encrypted file '{encrypted_file}' does not exist. Please encrypt and save key first\n")
    
    if not encrypted_file.lower().endswith('.key'):
        return print("File does not have the correct extension. Please verify provided data!\n")
    
    # decrypt key
    try:
        with open(encrypted_file, "rb") as file:
            encrypted_file_content = file.read()

            try: 
                with open("encryption_key.key", "r") as fernet_file:
                    fernet_key = fernet_file.read()

                    cipher = Fernet(fernet_key)
                    decrypted_file_content = cipher.decrypt(encrypted_file_content)

                    try: 
                        # HOTP requires a base32 encode key
                        base32_encoded_key = base64.b32encode(decrypted_file_content).decode("utf-8")
                        counter, remaining = get_counter()

                        if -1 != user_code:
                            totp = pyotp.TOTP(base32_encoded_key)
                            print(totp.verify(user_code)) 
                        elif (generate_qr):
                            qr = qrcode.make(f'otpauth://totp/OTPqr:Janeway?secret={base32_encoded_key}&issuer=OTPqr&counter={counter}')
                            qr.save("otp_qr.png")
                            print("QR code saved as otp_qr.png")
                            print(f"Time untill a new otp is generated: {remaining} seconds\n")

                        else:
                            otp = hotp(base32_encoded_key, counter)
                            print(f"\nOne time password succesfully generated: {otp}")
                            print(f"Time untill a new otp is generated: {remaining} seconds\n")


                    except Exception as e:
                        print(f"Unable to  decrypt file: {e}\n")

            except Exception as e:
                print(f"Unable to create one time password: {e}\n")
           
    except Exception as e:
        print(f"Unable to open provided key file '{file}: {e}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Script that ....."
        )
    parser.add_argument("-g", help="hexadecimal key")
    parser.add_argument("-k", help="encrypted hexadecimal file")
    parser.add_argument("-q", action="store_true", help="create a qr code for this otp")
    parser.add_argument("-v", help="To verify the code from the autheniticator")
    args = parser.parse_args()

    if args.q:
        generate_qr = True
    if args.v:
        user_code = args.v

    try:
        if args.g and args.k:
            print("Encript key or generate password please! One or the other!\n")
        elif args.g and args.q:
            print("No qr code for you yet! provide a hex key first!")
        elif args.g:
            store_and_encript_key_file(args.g)
        elif args.k:
            generate_or_validate_one_time_password(args.k, generate_qr, user_code)
    except Exception as e:
        print(f"Could not initialize ft_otp: {e}\n")

# ft_otp 
# mac/linux: use python3
# windows: use python

# Generate a random key: python3 generate_key.py  - or create a new file with your own hex key
# Run: python3 ft_otp.py -g=key.txt  - (or your file) to save and encrypt key 
# Run: python3 ft_otp.py -k=ft_otp.key  - to create a one time password  
# Run: python3 cleanup.py  - to start over


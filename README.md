# 42.Cybersecurity
42 cybersecurity piscine

Run: 
Check each project for instructions

42 The Network Assignment:

Arachnida:

- Spider: small program to automatically to extract all the images from a website, recursively, by
providing a url as a parameter.
    /spider [-rlp] URL
• Option -r : recursively downloads the images in a URL received as a parameter.
• Option -r -l [N] : indicates the maximum depth level of the recursive download.
If not indicated, it will be 5.
• Option -p [PATH] : indicates the path where the downloaded files will be saved. If not specified, ./data/ will be used.
The program will download the following extensions by default: .jpg/jpeg, .png, .gif, .bmp

- Scorpion: small program that receives image files as parameters and parses them for EXIF and other metadata, displaying them on the screen.
The program must at least be compatible with the same extensions that spider handles.
It display basic attributes such as the creation date, as well as EXIF data. 

ft_otp:

A program that stores an initial password in file and can generate a new one time password
every time it is requested.
Use of any library that facilitates the implementation of the algorithm is permitted, as long as it doesn’t do the dirty work, i.e. using a TOTP library is strictly prohibited. Of course, you can and should use a library or function that allows you to access system time.
• Program must take arguments:
◦ -g: The program receives as argument a hexadecimal key of at least 64 characters. The program stores this key safely in a file called ft_otp.key, which is encrypted.
◦ -k: The program generates a new temporary password based on the key given as argument and prints it on the standard output.
• Program must use the HOTP algorithm (RFC 4226).
• The generated one-time password must be random and must always contain the same format, i.e. 6 digits.
Bonus: 
- create a QR code with seed integration
- create a graphic interface
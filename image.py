from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from PIL import Image
import os
import struct

# Function to encrypt an image
def encrypt_image(image_path, key):
    # Load the image
    image = Image.open(image_path)
    image_bytes = image.tobytes()  # Convert image to bytes

    # Get the original image size and mode
    width, height = image.size
    mode = image.mode
    mode_len = len(mode)  # Length of the mode string

    # Generate a random initialization vector (IV)
    iv = os.urandom(16)

    # Create a cipher object using AES encryption in CFB mode
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the image bytes
    encrypted_bytes = encryptor.update(image_bytes) + encryptor.finalize()

    # Save the encrypted image, IV, width, height, and mode
    with open(image_path + ".enc", "wb") as enc_file:
        enc_file.write(iv)
        enc_file.write(struct.pack('>II', width, height))  # Save width and height
        enc_file.write(struct.pack('>B', mode_len))  # Save the length of mode string
        enc_file.write(mode.encode('utf-8'))  # Save mode
        enc_file.write(encrypted_bytes)

    print(f"Image encrypted and saved as {image_path}.enc")


# Function to decrypt an image
def decrypt_image(encrypted_image_path, key):
    # Read the encrypted image file
    with open(encrypted_image_path, "rb") as enc_file:
        iv = enc_file.read(16)  # Read the IV
        width, height = struct.unpack('>II', enc_file.read(8))  # Read width and height
        mode_len = struct.unpack('>B', enc_file.read(1))[0]  # Read the length of mode string
        mode = enc_file.read(mode_len).decode('utf-8')  # Read mode
        encrypted_bytes = enc_file.read()

    # Create a cipher object for decryption
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the image bytes
    decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()

    # Reconstruct the image from decrypted bytes
    image = Image.frombytes(mode, (width, height), decrypted_bytes)
    decrypted_image_path = encrypted_image_path.replace(".enc", "_decrypted.png")
    image.save(decrypted_image_path)

    print(f"Image decrypted and saved as {decrypted_image_path}")

# Example usage:
key = os.urandom(32)  # AES-256 key (32 bytes)
image_path = "images1.jpg"

# Encrypt the image
encrypt_image(image_path, key)

# Decrypt the image
decrypt_image(image_path + ".enc", key)

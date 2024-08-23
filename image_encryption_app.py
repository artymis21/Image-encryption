import streamlit as st
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from PIL import Image
import io
import os

# Set a constant encryption key (AES-256 key should be 32 bytes)
CONSTANT_KEY = bytes.fromhex('22cfb6899df21c6560d3f0dd975ee914b1922ca98e4d3ce8cd38a83f05bb825e')

# Function to encrypt an image
def encrypt_image(image_data):
    # Generate a random initialization vector (IV)
    iv = os.urandom(16)
    
    # Create a cipher object using AES encryption in CFB mode
    cipher = Cipher(algorithms.AES(CONSTANT_KEY), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the image bytes
    encrypted_bytes = encryptor.update(image_data) + encryptor.finalize()

    # Combine IV and encrypted bytes
    encrypted_data = iv + encrypted_bytes

    return encrypted_data

# Function to decrypt an image
def decrypt_image(encrypted_data):
    try:
        # Extract the IV and encrypted bytes
        iv = encrypted_data[:16]
        encrypted_bytes = encrypted_data[16:]

        # Create a cipher object for decryption
        cipher = Cipher(algorithms.AES(CONSTANT_KEY), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt the image bytes
        decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()

        return decrypted_bytes

    except Exception as e:
        st.error("Failed to decrypt the image. Please check the encryption key and data.")
        return None

# Streamlit UI
st.title("Image Encryption & Decryption")

# Upload an image for encryption
uploaded_image = st.file_uploader("Choose an image to encrypt", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Encrypt the image
    image_bytes = uploaded_image.read()
    encrypted_data = encrypt_image(image_bytes)

    # Save the encrypted data to a .txt file
    st.download_button(
        label="Download Encrypted Image",
        data=encrypted_data,
        file_name="encrypted_image.txt",
        mime="text/plain"
    )

# Upload a .txt file for decryption
uploaded_txt = st.file_uploader("Upload the encrypted .txt file", type=["txt"])

if uploaded_txt is not None:
    # Decrypt the image
    encrypted_data = uploaded_txt.read()
    decrypted_data = decrypt_image(encrypted_data)

    if decrypted_data:
        # Display the decrypted image
        st.image(decrypted_data)

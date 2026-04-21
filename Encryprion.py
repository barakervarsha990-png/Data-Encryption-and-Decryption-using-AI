import streamlit as st
import hashlib

# ---------------------------------------
# 🔑 KEY GENERATION FROM PASSWORD
# ---------------------------------------
def generate_key(password: str) -> int:
    hash_obj = hashlib.sha256(password.encode())
    return int(hash_obj.hexdigest(), 16) % 256


# ---------------------------------------
# 🔐 XOR ENCRYPTION (TEXT)
# ---------------------------------------
def encrypt_text(text, key):
    return ''.join(chr(ord(c) ^ key) for c in text)

def decrypt_text(cipher, key):
    return ''.join(chr(ord(c) ^ key) for c in cipher)


# ---------------------------------------
# 📁 FILE ENCRYPTION
# ---------------------------------------
def process_file(data, key):
    return bytes([b ^ key for b in data])


# ---------------------------------------
# 🚀 STREAMLIT UI
# ---------------------------------------
st.set_page_config(page_title="Encryption Tool", page_icon="🔐")

st.title("🔐 Data Encryption & Decryption Tool")
st.write("Simple password-based XOR encryption (educational use)")

# ==========================
# 🔑 PASSWORD INPUT
# ==========================
password = st.text_input("Enter Password", type="password")

if password:
    key = generate_key(password)
    st.success(f"Generated Key: {key}")
else:
    key = None
    st.warning("Please enter a password")

# ==========================
# 📝 TEXT SECTION
# ==========================
st.header("📝 Text Encryption")

text = st.text_area("Enter text")

col1, col2 = st.columns(2)

with col1:
    if st.button("Encrypt Text"):
        if text and key is not None:
            encrypted = encrypt_text(text, key)
            st.session_state["enc"] = encrypted
            st.success("Text Encrypted")
        else:
            st.error("Enter text and password")

with col2:
    if st.button("Decrypt Text"):
        if "enc" in st.session_state and key is not None:
            decrypted = decrypt_text(st.session_state["enc"], key)
            st.session_state["dec"] = decrypted
            st.success("Text Decrypted")
        else:
            st.error("Encrypt first or enter password")

st.text_area("Encrypted Output", st.session_state.get("enc", ""))
st.text_area("Decrypted Output", st.session_state.get("dec", ""))

# ==========================
# 📁 FILE SECTION
# ==========================
st.header("📁 File Encryption")

uploaded_file = st.file_uploader("Upload a file")

if uploaded_file and key is not None:
    file_data = uploaded_file.read()

    col3, col4 = st.columns(2)

    with col3:
        if st.button("Encrypt File"):
            encrypted_file = process_file(file_data, key)
            st.download_button(
                "Download Encrypted File",
                encrypted_file,
                file_name="encrypted.bin"
            )

    with col4:
        if st.button("Decrypt File"):
            decrypted_file = process_file(file_data, key)
            st.download_button(
                "Download Decrypted File",
                decrypted_file,
                file_name="decrypted_output"
            )

elif uploaded_file and key is None:
    st.error("Enter password first")

# ==========================
# ⚠️ FOOTER
# ==========================
st.caption("⚠ Educational project only. XOR encryption is not secure for real-world use.")
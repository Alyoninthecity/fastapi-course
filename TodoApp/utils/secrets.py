import secrets
import string

# Genera una stringa casuale di 32 byte (circa 44 caratteri in base64)
# Questo è il metodo più sicuro.
secure_key = secrets.token_urlsafe(32) 

print(f"Chiave generata (lunghezza {len(secure_key)}): {secure_key}")
# Esempio: '1yP-t5T_lQ7jR8z-4Xv6H3pA2qE9g0M_wBfVdCbYhUa...'
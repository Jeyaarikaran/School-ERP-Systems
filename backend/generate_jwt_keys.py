import rsa
import base64

# Generate a 2048-bit RSA key pair
public_key, private_key = rsa.newkeys(2048)

# Export them to PEM format
priv_pem = private_key.save_pkcs1(format='PEM').decode('utf-8')
pub_pem = public_key.save_pkcs1(format='PEM').decode('utf-8')

# Convert newlines to literal \n so they fit safely inside a .env file!
priv_env = priv_pem.replace('\n', '\\n')
pub_env = pub_pem.replace('\n', '\\n')

print("\n=== COPY AND PASTE THIS INTO YOUR .env FILE ===\n")
print(f'JWT_PRIVATE_KEY="{priv_env}"\n')
print(f'JWT_PUBLIC_KEY="{pub_env}"\n')
print("===============================================\n")

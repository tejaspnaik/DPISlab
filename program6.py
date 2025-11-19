import hashlib

# Easy hash function
def H(pwd, salt):
    return hashlib.sha256((salt + pwd).encode()).hexdigest()

# Users with their salts and stored hashes
users = {
    "alice": ("S1", H("apple123", "S1")),
    "bob":   ("X9", H("qwerty",  "X9")),
    "carol": ("ZZ", H("letmein", "ZZ")),
}

print("Stored (salt,hash) samples (truncated):")
for name, (salt, hashed) in users.items():
    print(" ", name, salt, hashed[:12] + "...")

# Small dictionary attacker tries
words = ["password", "123456", "qwerty", "apple123", "letmein"]

print("\nAttacker tries small dictionary...")
for name, (salt, stored_hash) in users.items():
    for w in words:
        if H(w, salt) == stored_hash:
            print(f"[ATTACKER] Cracked {name} -> {w}")
            break

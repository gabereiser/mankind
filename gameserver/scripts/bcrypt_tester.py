import bcrypt

salt = "changeme"

def main():
	secret = "password"
	v = bcrypt.hashpw(secret.encode(), bcrypt.gensalt(prefix=b"2a"))
	t = bcrypt.hashpw(secret.encode(), bcrypt.gensalt(prefix=b"2b"))
	print(f"V test is {bcrypt.checkpw(secret.encode(), v)}")
	print(f"T test is {bcrypt.checkpw(secret.encode(), t)}")

if __name__ == "__main__":
    main()
    


import hashlib, os, binascii

def hash_password(password):
	salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
	pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),salt, 100000)
	pwdhash = binascii.hexlify(pwdhash)
	return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
	salt = stored_password[:64]
	stored_password = stored_password[64:]
	pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'),salt.encode('ascii'),100000)
	pwdhash = binascii.hexlify(pwdhash).decode('ascii')
	return pwdhash == stored_password


#print(hash_password("4l3xis3schido"))
#print(hash_password("pru3baprof3sor"))
#s = 'dbed1d1417a60d4d705689cfb8f6051e25f4e089a8eadcff724b60eef5681bd320a5a462de9e66c73ac650c5d96dda3595da79a8feb69679feafa045e5dc44a96881a2441117dc22b5d9fbb11fed27807c13113221e4d477e7f2336212af5f56'
#b = verify_password(s,'pru3baprof3sor')
#print(b)
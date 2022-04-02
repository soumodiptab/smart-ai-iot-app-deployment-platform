import hashlib
ip_port = "127.0.0.1:9008"


def get_hash(inp_string):
    return hashlib.md5(inp_string.encode()).hexdigest()

print(get_hash(ip_port))

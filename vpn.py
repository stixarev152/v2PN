import uuid

def create_vpn_key():
    return "vpn://" + str(uuid.uuid4())

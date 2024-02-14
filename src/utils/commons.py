import hashlib, threading, time, uuid, bcrypt, hashlib


u8 = "utf-8"


def get_timestamp() -> int:
    return int(time.time())


def get_id() -> str:
    id = str(uuid.uuid4())
    return hashlib.sha256(id.encode()).hexdigest()


def run_on_thread(target: callable, *args, **kwargs):
    threading.Thread(target=target, args=args, kwargs=kwargs).start()


def hash_data(email: str) -> str:
    return hashlib.sha256(email.lower().encode(u8)).hexdigest()


def hash_bcrypt(password: str) -> str:
    return bcrypt.hashpw(password.encode(u8), bcrypt.gensalt()).decode(u8)


def verify_hash(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(u8), hashed_password.encode(u8))
    except:
        return False

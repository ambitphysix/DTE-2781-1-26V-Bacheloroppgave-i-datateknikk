import hashlib

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    if "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
        hash_object = hashlib.sha256(filename.encode())
        hashed_filename = (
            hash_object.hexdigest() + "." + filename.rsplit(".", 1)[1].lower()
        )
        return hashed_filename
    return None

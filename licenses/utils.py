import os
from uuid import uuid5

def path_and_rename(instance, filename: str):
    """
    Generates a new filename for an uploaded file.

    This function takes an instance (usually a model instance) and the original filename,
    and returns a new filename consisting of a UUID and the original file extension.
    The UUID is generated using the uuid5 function, with the instance's UUID as the namespace
    and the original filename as the name. The new filename is then joined with the upload path.

    Args:
        instance: The instance that the file is being uploaded for.
        filename: The original filename of the uploaded file.

    Returns:
        str: The new filename, consisting of the upload path and the generated filename.
    """
    upload_to = 'licenses/'
    ext = filename.split('.')[-1]
    filename = f'{uuid5(instance.id, filename).hex}.{ext}'
    return os.path.join(upload_to, filename)

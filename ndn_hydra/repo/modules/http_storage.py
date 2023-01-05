import os
import logging

class HttpStorage():
  def __init__(self, path):
    self.path = path
    self.logger = logging.getLogger()

  def store_bytes(self, file_name: str, data_bytes: bytes):
    file_name = file_name.lstrip('/')
    full_path = self.path + file_name
    # print("Path:", path)
    # print("file name:", file_name)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'wb') as f:
        f.write(data_bytes)

  def delete_file(self, file_name: str):
    file_name = file_name.lstrip('/')
    try:
      os.remove(self.path + file_name)
      self.logger.info(f"File {file_name} deleted.")
    except:
      pass
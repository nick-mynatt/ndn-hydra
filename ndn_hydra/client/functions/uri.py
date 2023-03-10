
import logging
import subprocess
from ndn.app import NDNApp
from ndn.encoding import FormalName, Component, Name, ContentType
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure

class HydraURIClient(object):
    def __init__(self, app: NDNApp, client_prefix: FormalName, repo_prefix: FormalName) -> None:
      """
      This client handles the inserting and fetching of file URIs.
      :param app: NDNApp.
      :param client_prefix: NonStrictName. Routable name to client.
      :param repo_prefix: NonStrictName. Routable name to remote repo.
      """
      self.app = app
      self.client_prefix = client_prefix
      self.repo_prefix = repo_prefix

    async def insert_URI(self, file_name: FormalName, uri: str) -> bool:
      """
      Insert a file associated with a file name to the remote repo.
      """
      # This is not the best way to insert files into the repo. Too bad!
      upload_prefix = self.repo_prefix + [Component.from_str("uri")] + [Component.from_str("upload")] + file_name
      data_name, meta_info, content = await self.app.express_interest(upload_prefix, app_param=uri.encode(), freshness_period=3000, content_type=ContentType.BLOB)

    async def fetch_URI(self, query: Name, path: str, node_name: str=None) -> str:
      """
      Express interest for URI of a file.
      """
      if not node_name:
          fetch_prefix = self.repo_prefix + [Component.from_str("uri")] + [Component.from_str("fetch")] + query
      else:
          fetch_prefix = self.repo_prefix + [Component.from_str("node")] + [Component.from_str(node_name)] + [Component.from_str("uri")] + query

      try:
          data_name, meta_info, content = await self.app.express_interest(fetch_prefix, can_be_prefix=True, must_be_fresh=True, lifetime=3000)
          if meta_info.content_type == ContentType.NACK:
            print("Distributed repo does not have that file.")
            return
          else:
            uri_str = bytes(content).decode()
            self.globus_download(uri_str, path)
            return

      except (InterestNack, InterestTimeout, InterestCanceled, ValidationFailure) as e:
          print("Query command received no data packet back")
          return
      
    def globus_download(self, uri: str, path: str, p: int=2):
      """
      Downloads a file using cmd globus-url-copy
      """
      try:
        if not uri.startswith('http://'):
           uri = 'http://' + uri
        if not path.startswith('file://'):
           path = 'file://' + path
        output = subprocess.run(f"globus-url-copy -p {p} -vb {uri} {path}", shell=True)
        stdout, stderr = output.stdout, output.stderr
        
      except Exception as e:
         print("Failed to download file from uri")
         print(e)
         return


import logging
from ndn.app import NDNApp
from ndn.encoding import FormalName, Component, Name, ContentType
from ndn.types import InterestNack, InterestTimeout, InterestCanceled, ValidationFailure
from ndn_hydra.repo.protocol.base_models import FileList, File

class HydraURIClient(object):
    def __init__(self, app: NDNApp, client_prefix: FormalName, repo_prefix: FormalName) -> None:
      """
      This client queries a node within the remote repo.
      :param app: NDNApp.
      :param client_prefix: NonStrictName. Routable name to client.
      :param repo_prefix: NonStrictName. Routable name to remote repo.
      """
      self.app = app
      self.client_prefix = client_prefix
      self.repo_prefix = repo_prefix

    async def get_uri(self, query: Name, node_name: str=None) -> str:
      """
      Form a certain query and request that info from a node.
      """
      if not node_name:
          named_query = self.repo_prefix + [Component.from_str("uri")] + query
      else:
          named_query = self.repo_prefix + [Component.from_str("node")] + [Component.from_str(node_name)] + [Component.from_str("uri")] + query

      try:
          data_name, meta_info, content = await self.app.express_interest(named_query, can_be_prefix=True, must_be_fresh=True, lifetime=3000)
          if meta_info.content_type == ContentType.NACK:
            print("Distributed repo does not have that file.")
            return
          else:
            uris_str = bytes(content).decode()
            uris = uris_str.split(" ")
            print("URIs to download file from:", uris)
            return

      except (InterestNack, InterestTimeout, InterestCanceled, ValidationFailure) as e:
          print("Query command received no data packet back")
          return

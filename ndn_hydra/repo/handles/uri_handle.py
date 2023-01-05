# -------------------------------------------------------------
# NDN Hydra URI Handle
# -------------------------------------------------------------
#  @Project: NDN Hydra
#  @Date:    2022-11-08
#  @Authors: Please check AUTHORS.rst
#  @Source-Code:   https://github.com/justincpresley/ndn-hydra
#  @Documentation: https://ndn-hydra.readthedocs.io
#  @Pip-Library:   https://pypi.org/project/ndn-hydra
# -------------------------------------------------------------

import asyncio as aio
import logging
from ndn.app import NDNApp
from ndn.encoding import Name, ContentType, Component
from ndn.storage import Storage
from ndn_hydra.repo.modules.global_view import GlobalView
from ndn_hydra.repo.protocol.base_models import FileList, File

class URIHandle(object):
    """
    URIHandle processes URI interests.
    """
    def __init__(self, app: NDNApp, global_view: GlobalView, config: dict):
        """
        :param app: NDNApp.
        :param global_view: Global View.
        :param config: All config Info.
        """
        self.app = app
        self.global_view = global_view
        self.node_name = config['node_name']
        self.repo_prefix = config['repo_prefix']

        self.logger = logging.getLogger()

        self.command_comp = "/uri"
        self.node_comp = "/node"

        self.listen(Name.from_str(self.repo_prefix + self.command_comp))
        self.listen(Name.from_str(self.repo_prefix + self.node_comp  + self.node_name + self.command_comp))

    def listen(self, prefix):
        """
        This function needs to be called for prefix of all data stored.
        :param prefix: NonStrictName.
        """
        self.app.route(prefix)(self._on_interest)
        self.logger.info(f'URI handle: listening to {Name.to_str(prefix)}')

    def unlisten(self, prefix):
        """
        :param name: NonStrictName.
        """
        aio.ensure_future(self.app.unregister(prefix))
        self.logger.info(f'IP handle: stop listening to {Name.to_str(prefix)}')

    def _on_interest(self, int_name, int_param, _app_param):
        print("URI HANDLE: _on_interest called")
        file_name = Name.to_str(int_name[2:])
        print("File name:", file_name)
        if not file_name:
            return
        print("Getting file from globalview:", file_name)
        try:
            node_to_URI_dic = self.global_view.get_file_URIs(file_name)
        except:
            print("File not found.")
            return
        print("Node to uri dic:", node_to_URI_dic)
        uris = list(node_to_URI_dic.values())
        print(uris)
        uris_str = " ".join(uris) # convert list to str for bytes encoding
        print("URI:", uris)

        if uris:
            self.app.put_data(int_name, content=bytes(uris_str.encode()), freshness_period=3000, content_type=ContentType.BLOB)
        else:
            self.app.put_data(int_name, content=None, freshness_period=3000, content_type=ContentType.NACK)

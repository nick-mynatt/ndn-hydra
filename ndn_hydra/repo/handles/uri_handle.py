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
        self.listen(Name.from_str(self.repo_prefix + self.command_comp + '/upload'))
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
        file_name = Name.to_str(int_name[2:]).split('/params')[0]
        
        if '/upload' in file_name:
            file_name = file_name.lstrip('/upload')
            uri = bytes(_app_param).decode()
            print("Storing file", file_name, "with uri", uri)
            self.global_view.store_file(file_name, node_name=self.node_name, uri=uri)
            self.app.put_data(int_name, content=bytes('Worked'.encode()), freshness_period=3000, content_type=ContentType.BLOB)
        else:
            file_name = file_name.lstrip('/')
            node_to_URI_dic = self.global_view.get_file_URIs(file_name)
            uris = list(node_to_URI_dic.values())
            uris_str = " ".join(uris) # convert list to str for bytes encoding
            content = bytes(uris_str.encode())
            if uris:
                self.app.put_data(int_name, content=content, freshness_period=3000, content_type=ContentType.BLOB)
            else:
                self.app.put_data(int_name, content=None, freshness_period=3000, content_type=ContentType.NACK)

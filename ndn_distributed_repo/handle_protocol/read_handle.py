import asyncio as aio
import logging
from secrets import choice
from ..data_storage import DataStorage
from ..global_view import GlobalView
from ndn.app import NDNApp
from ndn.encoding import Name, tlv_var, ContentType, Component
from ndn_python_repo import Storage


class ReadHandle(object):
    """
    ReadCommandHandle processes ordinary interests, and return corresponding data if exists.
    """
    def __init__(self, app: NDNApp, data_storage: DataStorage, global_view: GlobalView, config: dict):
        """
        :param app: NDNApp.
        :param storage: Storage.
        """
        self.app = app
        self.data_storage = data_storage
        self.global_view = global_view
        self.session_id = config['session_id']
        self.repo_prefix = config['repo_prefix']

        self.normal_serving_comp = "/fetch"
        self.personal_serving_comp = "/id"

        self.listen(Name.from_str(self.repo_prefix + self.normal_serving_comp))
        self.listen(Name.from_str(self.repo_prefix + self.personal_serving_comp  + "/" + self.session_id))

    def listen(self, prefix):
        """
        This function needs to be called for prefix of all data stored.
        :param prefix: NonStrictName.
        """
        self.app.route(prefix)(self._on_interest)
        logging.info(f'Read handle: listening to {Name.to_str(prefix)}')

    def unlisten(self, prefix):
        """
        :param name: NonStrictName.
        """
        aio.ensure_future(self.app.unregister(prefix))
        logging.info(f'Read handle: stop listening to {Name.to_str(prefix)}')

    def _on_interest(self, int_name, int_param, _app_param):
        """
        Repo should not respond to any interest with MustBeFresh flag set.
        Repo will:
        - Reply with data of its own
        - Nack if data can not be found within the repo
        - Reply with a redirect to another node
        Assumptions:
        - A file will always have a on list not empty
        - A node on the on list will have the file in complete form
        """
        if int_param.must_be_fresh:
            return
        # get rid of the security part if any on the int_name
        file_name = self._get_file_name_from_interest(Name.to_str(int_name[:-1]))
        best_id = self._best_id_for_file(file_name)
        segment_comp = "/" + Component.to_str(int_name[-1])

        if best_id == self.session_id:
            if segment_comp == "/seg=0":
                print(f'[cmd][FETCH] serving data to client')

            # serve content from my storage
            storage_content = self.data_storage.get_v(file_name + segment_comp)
            final_id = Component.from_number(int(self.global_view.get_insertion_by_file_name(file_name)["packets"])-1, Component.TYPE_SEGMENT)
            self.app.put_data(int_name, content=storage_content, content_type=ContentType.BLOB, final_block_id=final_id)
            logging.info(f'Read handle: served data {Name.to_str(int_name)}')
            return
        elif best_id == None:
            if segment_comp == "/seg=0":
                print(f'[cmd][FETCH] nacked client due to no file in repo')

            # nack due to lack of avaliability
            self.app.put_data(int_name, content=None, content_type=ContentType.NACK)
            logging.info(f'Read handle: data not found {Name.to_str(int_name)}')
            return
        else:
            if segment_comp == "/seg=0":
                print(f'[cmd][FETCH] linked to another node in the repo')

            # create a link to a node who has the content
            new_name = self.repo_prefix + self.personal_serving_comp + "/" + best_id + file_name
            link_content = bytes(new_name.encode())
            final_id = Component.from_number(int(self.global_view.get_insertion_by_file_name(file_name)["packets"])-1, Component.TYPE_SEGMENT)
            self.app.put_data(int_name, content=link_content, content_type=ContentType.LINK, final_block_id=final_id)
            logging.info(f'Read handle: redirected {Name.to_str(int_name)}')
            return

    def _get_file_name_from_interest(self, int_name):
        file_name = int_name[len(self.repo_prefix):]
        if file_name[0:len(self.normal_serving_comp)] == self.normal_serving_comp:
            return file_name[len(self.normal_serving_comp):]
        else:
            return file_name[(len(self.personal_serving_comp)+len("/" + self.session_id)):]

    def _best_id_for_file(self, file_name: str):
        file_info = self.global_view.get_insertion_by_file_name(file_name)
        if file_info != None:
            on_list = file_info["stored_bys"]
            if file_info["is_deleted"] == True or not on_list:
                return None
            if self.session_id in on_list:
                return self.session_id
            else:
              return choice(on_list)
        return None
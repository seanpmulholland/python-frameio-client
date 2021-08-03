import os
import mimetypes

from .service import Service
from .projects import Project

from ..lib import FrameioUploader, FrameioDownloader, constants, Reference

class Asset(Service):
  def _build_asset_info(self, filepath):
    full_path = os.path.abspath(filepath)

    file_info = {
        "filepath": full_path,
        "filename": os.path.basename(full_path),
        "filesize": os.path.getsize(full_path),
        "mimetype": mimetypes.guess_type(full_path)[0]
    }

    return file_info

  @Reference(operation="#getAsset")
  def get(self, asset_id):
    """
    Get an asset by id.

    Args:
      asset_id (string): The asset id.
    """
    endpoint = '/assets/{}'.format(asset_id)
    return self.client._api_call('get', endpoint)

  @Reference(operation="#getAssets")
  def get_children(self, asset_id, include=[], slim=False, **kwargs):
    """
    Get a folder.

    Args:
      asset_id (string): The asset id.
    
    :Keyword Arguments:
      includes (list): List of includes you would like to add.

    Example::
    
      client.assets.get_children(
        asset_id='1231-12414-afasfaf-aklsajflaksjfla',
        includes=['review_links','cover_asset','creator','presentation']
      )
    """
    endpoint = '/assets/{}/children'.format(asset_id)
<<<<<<<

=======


    if slim == True:
      query_params = ''

      # Include children
      query_params += '?' + 'include=children,creator'

      # Only fields
      query_params += '&' + 'only_fields=' + ','.join(constants.asset_excludes['only_fields'])

      # # Drop includes
      query_params += '&' + 'drop_includes=' + ','.join(constants.asset_excludes['drop_includes'])

      # # Hard drop fields
      query_params += '&' + 'hard_drop_fields=' + ','.join(constants.asset_excludes['hard_drop_fields'])

      # Excluded fields
      # query_params += '&' + 'excluded_fields=' + ','.join(constants.asset_excludes['excluded_fields'])

      # # Sort by inserted_at
      # query_params += '&' + 'sort=-inserted_at'

      endpoint += query_params

      # print("Final URL", endpoint)    

    if len(include) > 0:
      endpoint += '&include={}'.format(include.join(','))

    return self.client._api_call('get', endpoint, kwargs)

    if len(include) > 0:
      endpoint += '?include={}'.format(include.join(','))

>>>>>>>
    return self.client._api_call('get', endpoint, kwargs)

  @Reference(operation="#createAsset")
  def create(self, parent_asset_id, **kwargs):
    """
    Create an asset.

    Args:
      parent_asset_id (string): The parent asset id.

    :Keyword Arguments:
      (optional) kwargs: additional request parameters.

    Example::

      client.assets.create(
        parent_asset_id="123abc",
        name="ExampleFile.mp4",
        type="file",
        filetype="video/mp4",
        filesize=123456
      )
    """
    endpoint = '/assets/{}/children'.format(parent_asset_id)
    return self.client._api_call('post', endpoint, payload=kwargs)
  
<<<<<<<

=======
  @Reference(operation="#createAsset")
  def create_folder(self, parent_asset_id, name="New Folder"):
    """
    Create a new folder.

    Args:
      parent_asset_id (string): The parent asset id.
      name (string): The name of the new folder.

    Example::

      client.assets.create_folder(
        parent_asset_id="123abc",
        name="ExampleFile.mp4",
      )
    """
    endpoint = '/assets/{}/children'.format(parent_asset_id)
    return self.client._api_call('post', endpoint, payload={"name": name, "type":"folder"})

  @Reference(operation="#createAsset")
>>>>>>>
  def from_url(self, parent_asset_id, name, url):
    """
    Create an asset from a URL.

    Args:
      parent_asset_id (str): The parent asset id.
      name (str): The filename.
      url (str): The remote URL.

    Example::

      client.assets.from_url(
        parent_asset_id="123abc",
        name="ExampleFile.mp4",
        type="file",
        url="https://"
      )
    """
    
    payload = {
      "name": name,
      "type": "file",
      "source": {
        "url": url
      }
    }

    endpoint = '/assets/{}/children'.format(parent_asset_id)
    return self.client._api_call('post', endpoint, payload=payload)

  @Reference(operation="#updateAsset")
  def update(self, asset_id, **kwargs):
    """
    Updates an asset

    Args:
      asset_id (string): the asset's id

    :Keyword Arguments:
      kwargs (optional): fields and values you wish to update

    Example::

      client.assets.update("adeffee123342", name="updated_filename.mp4")
    """
    endpoint = '/assets/{}'.format(asset_id)
    return self.client._api_call('put', endpoint, kwargs)

  @Reference(operation="#copyAsset")
  def copy(self, destination_folder_id, **kwargs):
    """
    Copy an Asset

    Args:
      destination_folder_id (str): The id of the folder you want to copy into.
    
    :Keyword Arguments:
      id (str): The id of the asset you want to copy.

    Example::

      client.assets.copy("adeffee123342", id="7ee008c5-49a2-f8b5-997d-8b64de153c30")
    """
    endpoint = '/assets/{}/copy'.format(destination_folder_id)
    return self.client._api_call('post', endpoint, kwargs)

<<<<<<<
  def bulk_copy(self, destination_folder_id, asset_list=[], copy_comments=False):
=======
  @Reference(operation="#batchCopyAsset")
  def bulk_copy(self, destination_folder_id, asset_list, copy_comments=False):
>>>>>>>
    """Bulk copy assets

    Args:
      destination_folder_id (string): The id of the folder you want to copy into.
    
    :Keyword Arguments:
      asset_list (list): A list of the asset IDs you want to copy.
      copy_comments (boolean): Whether or not to copy comments: True or False.

    Example::

      client.assets.bulk_copy("adeffee123342", 
        asset_list=[
          "7ee008c5-49a2-f8b5-997d-8b64de153c30",
          "7ee008c5-49a2-f8b5-997d-8b64de153c30"
        ],
        copy_comments=True
      )
    """
    
    payload = {"batch": []}
    new_list = list()

    if copy_comments:
      payload['copy_comments'] = "all"

    for asset in asset_list:
      payload['batch'].append({"id": asset})

    endpoint = '/batch/assets/{}/copy'.format(destination_folder_id)
    return self.client._api_call('post', endpoint, payload)

  @Reference(operation="#deleteAsset")
  def delete(self, asset_id):
    """
    Delete an asset

    Args:
      asset_id (string): the asset's id
    """
    endpoint = '/assets/{}'.format(asset_id)
    return self.client._api_call('delete', endpoint)

  def _upload(self, asset, file):
    """
    Upload an asset. The method will exit once the file is uploaded.

    Args:
      asset (object): The asset object.
      file (file): The file to upload.

    Example::

      client._upload(asset, open('example.mp4'))
    """

    uploader = FrameioUploader(asset, file)
    uploader.upload()

  # def upload_folder(sFelf, destination_id, folderpath):
  #   try:
  #     if os.path.isdir(folderpath):
  #       # Good it's a directory, we can keep going
  #       pass

  #   except OSError:
  #     if not os.path.exists(folderpath):
  #       sys.exit("Folder doesn't exist, exiting...")

  def build_asset_info(self, filepath):
    full_path = os.path.abspath(filepath)

    file_info = {
        "filepath": full_path,
        "filename": os.path.basename(full_path),
        "filesize": os.path.getsize(full_path),
        "mimetype": mimetypes.guess_type(full_path)[0]
    }

    return file_info

  def upload(self, destination_id, filepath, asset=None):
    """
    Upload a file. The method will exit once the file is downloaded.

    Args:
      destination_id (uuid): The destination Project or Folder ID.
      filepath (string): The locaiton of the file on your local filesystem \
        that you want to upload.

    Example::

      client.assets.upload('1231-12414-afasfaf-aklsajflaksjfla', "./file.mov")
    """

    # Check if destination is a project or folder
    # If it's a project, well then we look up its root asset ID, otherwise we use the folder id provided
    # Then we start our upload

    try:
        # First try to grab it as a folder
        folder_id = self.get(destination_id)['id']
    except Exception as e:
        # Then try to grab it as a project
        folder_id = Project(self.client).get_project(destination_id)['root_asset_id']
    finally:
      file_info = self.build_asset_info(filepath)

      if not asset:
        try:
          asset = self.create(folder_id,  
              type="file",
              name=file_info['filename'],
              filetype=file_info['mimetype'],
              filesize=file_info['filesize']
          )

        except Exception as e:
            print(e)

        try:
          with open(file_info['filepath'], "rb") as fp:
            self._upload(asset, fp)

        except Exception as e:
            print(e)

    return asset

  def download(self, asset, download_folder, prefix=None, multi_part=False, concurrency=5):
    """
    Download an asset. The method will exit once the file is downloaded.

    Args:
      asset (object): The asset object.
      download_folder (path): The location to download the file to.

    Example::

      client.assets.download(asset, "~./Downloads")
    """
    downloader = FrameioDownloader(asset, download_folder, prefix, multi_part, concurrency)
    return downloader.download_handler()
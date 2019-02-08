from gettext import gettext as _
from logging import getLogger
from os import path

from django.db import models

from pulpcore.plugin.models import Content, Remote, Publisher


log = getLogger(__name__)


class FileContent(Content):
    """
    The "file" content type.

    Content of this type represents a collection of 0 or more files uniquely
    identified by path and SHA256 digest.

    Fields:
        relative_path (str): The file relative path.
        digest (str): The SHA256 HEX digest.
    """

    TYPE = 'file'

    relative_path = models.TextField(null=False)
    digest = models.TextField(null=False)

    class Meta:
        unique_together = (
            'relative_path',
            'digest'
        )

    @staticmethod
    def init_from_relative_path(relative_path):
        """

        :param relative_path:
        :return:
        """
        

class FileRemote(Remote):
    """
    Remote for "file" content.
    """

    TYPE = 'file'

    def get_remote_artifact_url(self, relative_path=None):
        """
        Get the full URL for a RemoteArtifact from a relative path.

        This method returns the URL for a RemoteArtifact by concatinating the Remote's url and the
        relative path.located in the Remote. Plugin writers are expected to override this method
        when a more complex algorithm is needed to determine the full URL.

        Args:
            relative_path (str): The relative path of a RemoteArtifact

        Raises:
            ValueError: If relative_path starts with a '/'.

        Returns:
            str: A URL for a RemoteArtifact available at the Remote.
        """
        if path.isabs(relative_path):
            raise ValueError(_("Relative path can't start with '/'. {0}").format(relative_path))
        return path.join(self.url, relative_path)

    def get_remote_artifact_content_type(self, relative_path=None):
        """
        Get the type of content that should be available at the relative path.

        Args:
            relative_path (str): The relative path of a RemoteArtifact

        Returns:
            Class: FileContent
        """
        return FileContent


class FilePublisher(Publisher):
    """
    Publisher for "file" content.
    """

    TYPE = 'file'
    manifest = models.TextField()

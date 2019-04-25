# coding: utf-8
"""
Base constants and standard exceptions
"""

# Directory in which homefront will cache data, under the pelican cache
CACHE_SUBDIR = "_homefront/"


class HomefrontException(Exception):
    """
    Generic exception raised by Homefront.
    """
    pass


class Error(HomefrontException):
    """
    An error raised by homefront which prevented an operation to succeed.
    """
    pass

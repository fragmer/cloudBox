# cloudBox is copyright 2012 - 2013 the cloudBox team.
# cloudBox is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSE" file in the "docs" folder of the
# cloudBox Package.

"""
Constants for World Servers.
"""

ERROR_HEADER_MISMATCH = 0
ERROR_UNSUPPORTED_LEVEL_VERSION = 1
ERROR_REQUIRED_FIELDS_MISSING = 2


SUPPORTED_LEVEL_FORMATS = {
    "ClassicWorld": ("cloudbox.world.formats.cw", "ClassicWorldWorldFormat"),
}
import platform

from maya import mel


PLATFORM_SEPARATOR = ':' if platform.system() == 'Darwin' else ';'


def get_environment_variable(variable_name):
    """
    Get a list of the values for an environment variable
    @param variable_name:
    @return:
    """
    result = mel.eval('getenv "%s"' % variable_name).split(PLATFORM_SEPARATOR)
    return [x for x in result if x != '']


def set_environment_variable(variable_name, value_list):
    """
    Set an environment variable with a list of values
    @param variable_name:
    @param value_list:
    """
    mel.eval('putenv "%s" "%s"' % (variable_name, PLATFORM_SEPARATOR.join(value_list)))

import logging

# Get an instance of a logger
from src.photogallery import settings

logger = logging.getLogger("django")


# Parse the db variables from a heroku db env variable
def parse_db_variable(var_string):
    import re

    if not var_string:
        return []

    regex = r'.*\/\/(\w+):(\w+)@([A-Za-z0-9\-\.]+):(\d{4})\/(\w+)'

    logger.info("Parse db variable: {}".format(var_string))
    m = re.match(regex, var_string)
    if m:
        return m.groups()
    return list()


def load_env(env_file):
    with open(env_file, 'r') as f:
        for line in f:
            if "=" in line:
                env_var = line.split("=")
                setattr(settings, env_var[0], env_var[1].rstrip())

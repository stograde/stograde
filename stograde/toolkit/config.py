from datetime import datetime, timedelta
from configparser import ConfigParser
from appdirs import AppDirs
import os

_dirs = AppDirs('stograde', 'StoDevX')


class Config:
    _filename = os.path.join(_dirs.user_config_dir, 'stograde.ini')
    _config = ConfigParser()

    def __init__(self):
        # load the config file
        loaded_files = self._config.read(self._filename)
        # create the config file if it doesn't exist
        if not loaded_files:
            self._setup()

    def _setup(self):
        # create the config dir
        os.makedirs(_dirs.user_config_dir, exist_ok=True)
        # initialize with default values
        self._config['general'] = {}
        self.set_last_update_check()
        # save the file b/c it didn't exist
        self.save_config()

    def get_last_update_check(self):
        value = self._config.get('general', 'last_update_check', fallback=str(datetime.now()))
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')

    def set_last_update_check(self):
        self._config.set('general', 'last_update_check', str(datetime.now()))
        self.save_config()

    def needs_update_check(self):
        return self.get_last_update_check() < datetime.now() - timedelta(minutes=15)

    def save_config(self):
        with open(self._filename, 'w') as outfile:
            self._config.write(outfile)


conf = Config()

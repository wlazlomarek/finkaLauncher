import os
import socket
import winreg
import platform

import eel
from loguru import logger

from read_conf_ini import ParseConfigIni


log_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents\\FinkaLauncher\\')
ini_file = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents\\FinkaLauncher\\finka_config.ini')


if os.path.exists(log_path):
    files = os.listdir(log_path)
    for file in files:
        if file.startswith('finkaLauncher_'):
            try:
                os.remove(os.path.join(log_path, file))
            except Exception as error:
                raise error
    logger.add(os.path.join(log_path, 'finkaLauncher_{time}.log'))
else:
    try:
        os.mkdir(log_path)
        logger.add(os.path.join(log_path, 'finkaLauncher_{time}.log'))
    except Exception as error:
        raise error

logger.info(f'Building UI')
eel.init('www')


class MachineInformation:
    def __init__(self):
        self.uname = platform.uname()
        self.releaseId = self.get_ReleaseId()

        data = f"({self.uname}, winver='{self.releaseId}'"
        logger.info(f'Collecting windows specyfication: {data[14:]}')

    def get_ReleaseId(self):
        key = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion'
        val = 'ReleaseID'

        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as key:
            releaseId = int(winreg.QueryValueEx(key, val)[0])

        return releaseId


class FinkaLauncher:
    def __init__(self, ini_conf:dict):
        self.externalIP = ini_conf['externalIP']
        self.localIP = ini_conf['localIP']
        self.firebird_port = int(ini_conf['firebird_port'])
        self.rdp_port = int(ini_conf['rdp_port'])

        # FK
        self.finkafk_local_path = ini_conf['finkafk_local_path']
        self.finkafk_remote_path = ini_conf['finkafk_remote_path']

        # KPR
        self.finkakpr_local_path = ini_conf['finkakpr_local_path']
        self.finkakpr_remote_path = ini_conf['finkakpr_remote_path']

        # PLACE
        self.finkaplace_local_path = ini_conf['finkaplace_local_path']
        self.finkaplace_remote_path = ini_conf['finkaplace_remote_path']

        # STW
        self.finkastw_local_path = ini_conf['finkastw_local_path']
        self.finkastw_remote_path = ini_conf['finkastw_remote_path']

    def check_flags(self):
        flags = {
            'internet_connection': ['google.com', '80'],
            'localFlag': [self.localIP, self.firebird_port],
            'externalFlag': [self.externalIP, self.firebird_port],
            'rdp_port': [self.externalIP, self.rdp_port]
        }

        new_flags = {}

        for key in flags:
            ip = flags.get(key)[0]
            port = flags.get(key)[1]
            new_flags[key] = [ip, port, self.check_server_port(ip, port)]

        self.internet_connection = new_flags.get('internet_connection')[2]
        if self.internet_connection:
            logger.info(f'Internet connection status: Available')
        else:
            logger.error(f'Internet connection: Not available')

        self.localFlag = new_flags.get('localFlag')[2]
        if self.localFlag:
            logger.info(f'localConnection ({self.localIP}) / firebird_port ({self.firebird_port}): Available')
        else:
            logger.warning(f'localConnection ({self.localIP}) / firebird_port ({self.firebird_port}): Not available')

        self.externalFlag = new_flags.get('externalFlag')[2]
        if self.externalFlag:
            logger.info(f'externalConnection ({self.externalIP}) / firebird_port ({self.firebird_port}): Available')
        else:
            logger.warning(f'externalConnection ({self.externalIP})  / firebird_port ({self.firebird_port}): Not available')

        self.rdp_portFlag = new_flags.get('rdp_port')[2]
        if self.rdp_portFlag:
            logger.info(f'Rdp port ({self.rdp_port}): Available')
        else:
            logger.error(f'RDP port ({self.rdp_port}): Not available')

    @staticmethod
    def check_server_port(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try:
            s.connect((ip, int(port)))
            s.shutdown(socket.SHUT_RDWR)
            return True
        except:
            return False
        finally:
            s.close()


@eel.expose
def check_network_adapter():
    p = os.popen('netsh interface show interface').read()
    if 'Connected' in p:
        logger.info(f'Network Card: Working')
        server_location()
        return True
    else:
        logger.error(f'Network Card: Disabled!')
        eel.network_adapter()
        return False


def server_location():
    finka.check_flags()
    if finka.internet_connection:
        eel.change_color_green_ic_js()
        if finka.externalFlag and finka.rdp_portFlag:
            eel.change_color_green_ss_js()
        elif finka.localFlag:
            eel.change_color_green_ss_js()
        else:
            eel.change_color_red_ss_js()  # jest internet ale nie możliwa jest praca lokalna oraz zdalna
    else:
        if finka.localFlag:
            eel.change_color_red_ic_green_ss_js_quite_not()
        else:
            eel.change_color_red_id_red_ss_one_not()  # nie ma internetu oraz nie możliwa jest praca lokalna oraz zdalna

@eel.expose
def showLog():
    if os.path.exists(log_path):
        try:
            log = os.listdir(log_path)
            os.startfile(os.path.join(log_path, log[0]))
        except FileNotFoundError:
            logger.error(f'Log file not found...')


@eel.expose
def finkaFK():
    logger.info(f'\nFinka-FK clicked')
    if check_network_adapter():
        if finka.localFlag:
            logger.info(f'Running local Finka-FK')
            try:
                os.startfile(finka.finkafk_local_path)
            except FileNotFoundError:
                logger.error(f'Finka FK local file not found...')
        elif finka.externalFlag:
            logger.info(f'Running external Finka-FK')
            try:
                os.startfile(finka.finkafk_remote_path)
            except FileNotFoundError:
                logger.error(f'Finka FK external file not found...')


@eel.expose
def finkaPLACE():
    logger.info(f'\nFinka-PLACE clicked')
    if check_network_adapter():
        if finka.localFlag:
            logger.info(f'Running local Finka-PLACE')
            try:
                os.startfile(finka.finkaplace_local_path)
            except FileNotFoundError:
                logger.error(f'Finka PLACE local file not found...')
        elif finka.externalFlag:
            logger.info(f'Running external Finka-PLACE')
            try:
                os.startfile(finka.finkaplace_remote_path)
            except FileNotFoundError:
                logger.error(f'Finka PLACE external file not found...')


@eel.expose
def finkaSTW():
   logger.info(f'\nFinka-STW clicked')
   if check_network_adapter():
        if finka.localFlag:
            logger.info(f'Running local Finka-STW')
            try:
                os.startfile(finka.finkastw_local_path)
            except FileNotFoundError:
                logger.error(f'Finka STW local file not found...')
        elif finka.externalFlag:
            logger.info(f'Running external Finka-STW')
            try:
                os.startfile(finka.finkastw_remote_path)
            except FileNotFoundError:
                logger.error(f'Finka STW external file not found...')


@eel.expose
def finkaKPR():
    logger.info(f'\nFinka-KPR clicked')
    if check_network_adapter():
        if finka.localFlag:
            logger.info(f'Running local Finka-KPR')
            try:
                os.startfile(finka.finkakpr_local_path)
            except FileNotFoundError:
                logger.error(f'Finka KPR local file not found...')
        elif finka.externalFlag:
            logger.info(f'Running external Finka-KPR')
            try:
                os.startfile(finka.finkakpr_remote_path)
            except FileNotFoundError:
                logger.error(f'Finka KPR external file not found...')


if __name__ == '__main__':
    machine = MachineInformation()
    ini_c = ParseConfigIni()
    finka = FinkaLauncher(ini_c.parse_ini(ini_file))
    eel.init('src\www')
    eel.start('index.html', size=(400, 620), options={'port': 2208}, suppress_error=True)
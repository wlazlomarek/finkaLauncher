import configparser

class ParseConfigIni:
    
    def __init__(self) -> None:
        pass

    def parse_ini(self, ini_file):
        config = configparser.ConfigParser()
        config.read(ini_file)

        self.externalIP = config.get('NETWORK', 'externalip')
        self.localIP = config.get('NETWORK', 'localip')
        self.firebird_port = int(config.get('NETWORK', 'firebird_port'))
        self.rdp_port = int(config.get('NETWORK', 'rdp_port'))

        # FK
        self.finkafk_local_path = config.get('EXE_PATH', 'finka_fk_exe')
        self.finkafk_remote_path = config.get('RDP_PATH', 'finka_fk_rdp')

        # KPR
        self.finkakpr_local_path = config.get('EXE_PATH', 'finka_kpr_exe')
        self.finkakpr_remote_path = config.get('RDP_PATH', 'finka_kpr_rdp')

        # PLACE
        self.finkaplace_local_path = config.get('EXE_PATH', 'finka_place_exe')
        self.finkaplace_remote_path = config.get('RDP_PATH', 'finka_place_rdp')
        
        # STW
        self.finkastw_local_path = config.get('EXE_PATH', 'finka_stw_exe')
        self.finkastw_remote_path = config.get('RDP_PATH', 'finka_stw_rdp')

        return vars(self)


if __name__ == '__main__':
    cnf = ParseConfigIni(r'src\finka_config.ini')
    cnf.parse_ini()

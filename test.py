import configparser
config = configparser.ConfigParser()
config.read('config.ini')
datetime = config['datetime']['timestr']
print (datetime)

def update_ini():
    """Updates the time and date for .ini file"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    timestr = time.strftime("%Y%m%d-%I%M%S %p")
    try:
        config.set('datetime', 'timestr', timestr)
        with open("config.ini", 'w+') as cfgfile:
            config.write(cfgfile)
        return str(config["datetime"]["timestr"])
    except config.NoSectionError:
        # Create non-existent section
        config.add_section('datetime')
        config.set('datetime', 'timestr', timestr)
        with open("config.ini", 'w+') as cfgfile:
            config.write(cfgfile)
        return str(config["datetime"]["timestr"])

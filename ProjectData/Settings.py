config = {}
def GetSettings():
    with open("ProjectData/Settings.config", "r") as f:
        for line in f:
            key, value = line.strip().split("=")
            config[key] = value
    return config

def GetSetting(setting):
    config = GetSettings()
    return config[setting]


def EditSetting(setting, value):
    config[setting] = value
    with open("ProjectData/Settings.config", "w") as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")


#print(GetSetting("email-adress"))
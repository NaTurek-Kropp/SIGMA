config = {}
def GetSettings():
    with open("ProjectData/Settings.config", "r") as f:
        for line in f:
            key, value = line.strip().split("=")
            config[key] = value
    return config

def GetSubSettings():
    with open("ProjectData/SubSettings.config", "r") as f:
        for line in f:
            key, value = line.strip().split("=")
            config[key] = value
    return config

def GetSubSetting(setting):
    config = GetSubSettings()
    return config[setting]


def GetSetting(setting):
    config = GetSettings()
    return config[setting]

def EditSetting(setting, value):
    with open("ProjectData/Settings.config", "r") as f:
        lines = f.readlines()
    with open("ProjectData/Settings.config", "w") as f:
        for line in lines:
            key, _ = line.strip().split("=")
            if key == setting:
                f.write(f"{key}={value}\n")
            else:
                f.write(line)

def EditSubSetting(setting, value):
    with open("ProjectData/SubSettings.config", "r") as f:
        lines = f.readlines()
    with open("ProjectData/SubSettings.config", "w") as f:
        for line in lines:
            key, _ = line.strip().split("=")
            if key == setting:
                f.write(f"{key}={value}\n")
            else:
                f.write(line)


#print(GetSetting("email-adress"))

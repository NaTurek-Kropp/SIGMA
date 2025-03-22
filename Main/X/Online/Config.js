import { readFileSync } from 'fs';
import { join } from 'path';

const config = {};

function getSettings() {
    const settingsPath = join(__dirname, 'Online', 'API.config');
    const data = readFileSync(settingsPath, 'utf-8');
    const lines = data.split('\n');

    lines.forEach(line => {
        const [key, value] = line.trim().split('=');
        if (key && value) {
            config[key] = value;
        }
    });

    return config;
}

function getSetting(setting) {
    const settings = getSettings();
    return settings[setting];
}


export default { getSettings, getSetting};
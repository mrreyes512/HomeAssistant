import logging
import re
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from datetime import timedelta
from telnetlib import Telnet
from homeassistant.const import (CONF_NAME, CONF_DISPLAY_OPTIONS, CONF_HOST, CONF_PORT, CONF_USERNAME, CONF_PASSWORD)
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=1)

DEFAULT_PORT = 23
DEFAULT_NAME = 'Draytek'
DEFAULT_TIMEOUT = 5

SENSOR_TYPES = {
    'Running_Mode' : ['Running_Mode', None, 'mdi:lan-connect'],
    'State' : ['State', None, 'mdi:water'],
    'DS_Actual_Rate' : ['DS_Actual_Rate', 'Mbps', 'mdi:arrow-down-bold-circle-outline'],
    'US_Actual_Rate' : ['US_Actual_Rate', 'Mbps', 'mdi:arrow-up-bold-circle-outline'],
    'DS_Attainable_Rate' : ['DS_Attainable_Rate', 'Mbps', 'mdi:arrow-down-bold-circle-outline'],
    'US_Attainable_Rate' : ['US_Attainable_Rate', 'Mbps', 'mdi:arrow-up-bold-circle-outline'],
    'DS_Path_Mode' : ['DS_Path_Mode', None, 'mdi:arrow-down-bold-circle-outline'],
    'US_Path_Mode' : ['US_Path_Mode', None, 'mdi:arrow-up-bold-circle-outline'],
    'DS_Interleave_Depth' : ['DS_Interleave_Depth', None, 'mdi:arrow-down-bold-circle-outline'],
    'US_Interleave_Depth' : ['US_Interleave_Depth', None, 'mdi:arrow-up-bold-circle-outline'],
    'NE_Current_Attenuation' : ['NE_Current_Attenuation', 'dB', 'mdi:signal-variant'],
    'Cur_SNR_Margin' : ['Cur_SNR_Margin', 'dB', 'mdi:signal-variant'],
    'DS_Actual_PSD' : ['DS_Actual_PSD', 'dB', 'mdi:arrow-down-bold-circle-outline'],
    'US_Actual_PSD' : ['US_Actual_PSD', 'dB', 'mdi:arrow-up-bold-circle-outline'],
    'NE_Rcvd_Cells' : ['NE_Rcvd_Cells', None, 'mdi:counter'],
    'NE_Xmitted_Cells' : ['NE_Xmitted_Cells', None, 'mdi:counter'],
    'NE_CRC_Count' : ['NE_CRC_Count', None, 'mdi:counter'],
    'FE_CRC_Count' : ['FE_CRC_Count', None, 'mdi:counter'],
    'NE_ES_Count' : ['NE_ES_Count', None, 'mdi:counter'],
    'FE_ES_Count' : ['FE_ES_Count', None, 'mdi:counter'],
    'Xdsl_Reset_Times' : ['Xdsl_Reset_Times', None, 'mdi:counter'],
    'Xdsl_Link_Times' : ['Xdsl_Link_Times', None, 'mdi:counter'],
    'ITU_Version_0' : ['ITU_Version_0', None, 'mdi:counter'],
    'ITU_Version_1' : ['ITU_Version_1', None, 'mdi:counter'],
    'ADSL_Firmware_Version' : ['ADSL_Firmware_Version', None, 'mdi:counter'],
    'Power_Management_Mode' : ['Power_Management_Mode', None, 'mdi:counter'],
    'Test_Mode' : ['Test_Mode', None, 'mdi:counter'],
    'Far_Current_Attenuation' : ['Far_Current_Attenuation', None, 'mdi:signal-variant'],
    'Far_SNR_Margin' : ['Far_SNR_Margin', None, 'mdi:signal-variant'],
    'CO_ITU_Version_0' : ['CO_ITU_Version_0', None, 'mdi:counter'],
    'CO_ITU_Version_1' : ['CO_ITU_Version_1', None, 'mdi:counter'],
    'DSLAM_Chipset_Vendor' : ['DSLAM_Chipset_Vendor', None, 'mdi:counter'],
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_DISPLAY_OPTIONS, default=SENSOR_TYPES):
        [vol.In(SENSOR_TYPES)],
})

ICON = 'mdi:router-wireless'

ADSL_STATUS_REGEX = re.compile(
         r'.*:\s(.*)State\s*:\s(.*)' +
         r'\s*.*?:\s(.*?)bps.*?:\s(.*?)bps' +
         r'\s*.*?:\s(.*?)bps.*?:\s(.*?)bps' +
         r'\s*.*?:\s(.*?)US.*?:\s(.*)' +
         r'\s*.*?:\s(.*?)US.*?:\s(.*)' +
         r'\s*.*?:\s(.*?)dB.*?:\s(.*)dB' +
         r'\s*.*?:\s(.*?)dB.*?:\s(.*)dB' +
         r'\s*.*?:\s(.*?)NE.*?:\s(.*)' +
         r'\s*.*?:\s(.*?)FE.*?:\s(.*)' +
         r'\s*.*?:\s(.*?)FE.*?:\s(.*)' +
         r'\s*.*?:\s(.*?)Xdsl Link.*?:\s(.*)' +
         r'\s*.*?:\s(.*?)ITU.*?:\s(.*)' +
         r'\s*.*?:\s(.*)' +
         r'\s*.*?:\s(.*)' +
         r'\s*.*?:\s(.*)' +
         r'\s.*' +
         r'\s*.*?:\s(.*?)dB.*?:\s(.*)dB' +
         r'\s*.*?:\s(.*?)CO.*?:\s(.*)' +
         r'\s*.*?:\s<\s(.*)\s>'
)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    name = config.get(CONF_NAME)
    host = config.get(CONF_HOST)
    port = config.get(CONF_PORT)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    data = DraytekData(host, port, username, password, CONF_DISPLAY_OPTIONS)
    dev = []

    for variable in config[CONF_DISPLAY_OPTIONS]:
        dev.append(DraytekSensor(config, data, variable))

    add_devices(dev)


class DraytekSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, config, data, sensor_types):
        """Initialize a HDDTemp sensor."""
        self.data = data
        self._name = '{0}_{1}'.format(config.get(CONF_NAME),
                                      SENSOR_TYPES[sensor_types][0])

        self._unit_of_measurement = SENSOR_TYPES[sensor_types][1]
        self.type = sensor_types
        self._state = None
        self.update()


    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return SENSOR_TYPES[self.type][1] \
            if self.type in SENSOR_TYPES else None

    @property
    def icon(self):
        """Return the icon."""
        return SENSOR_TYPES[self.type][2] \
            if self.type in SENSOR_TYPES else None

    def update(self):
        """Get the latest data from modem and update the states."""
        self.data.update()

        if self.data.status is  None:
            #self._state = "OK"
            _LOGGER.error('No Data Received')
            return
        else:
            self.details = ADSL_STATUS_REGEX.search(self.data.status)
            if self.type == 'Running_Mode':
                self._state = self.details.group(1)
            elif self.type == 'State':
                self._state = self.details.group(2)
            elif self.type == 'DS_Actual_Rate':
                self._state = float(self.details.group(3)) / 1000000
            elif self.type == 'US_Actual_Rate':
                self._state = float(self.details.group(4)) / 1000000
            elif self.type == 'DS_Attainable_Rate':
                self._state = float(self.details.group(5)) / 1000000
            elif self.type == 'US_Attainable_Rate':
                self._state = float(self.details.group(6)) / 1000000
            elif self.type == 'DS_Path_Mode':
                self._state = self.details.group(7)
            elif self.type == 'US_Path_Mode':
                self._state = self.details.group(8)
            elif self.type == 'DS_Interleave_Depth':
                self._state = float(self.details.group(9))
            elif self.type == 'US_Interleave_Depth':
                self._state = float(self.details.group(10))
            elif self.type == 'NE_Current_Attenuation':
                self._state = float(self.details.group(11))
            elif self.type == 'Cur_SNR_Margin':
                self._state = float(self.details.group(12))
            elif self.type == 'DS_Actual_PSD':
                self._state = float(self.details.group(13).replace(" ", ""))
            elif self.type == 'US_Actual_PSD':
                self._state = float(self.details.group(14).replace(" ", ""))
            elif self.type == 'NE_Rcvd_Cells':
                self._state = float(self.details.group(15))
            elif self.type == 'NE_Xmitted_Cells':
                self._state = float(self.details.group(16))
            elif self.type == 'NE_CRC_Count':
                self._state = float(self.details.group(17))
            elif self.type == 'FE_CRC_Count':
                self._state = float(self.details.group(18))
            elif self.type == 'NE_ES_Count':
                self._state = float(self.details.group(19))
            elif self.type == 'FE_ES_Count':
                self._state = float(self.details.group(20))
            elif self.type == 'Xdsl_Reset_Times':
                self._state = float(self.details.group(21))
            elif self.type == 'Xdsl_Link_Times':
                self._state = float(self.details.group(22))
            elif self.type == 'ITU_Version_0':
                self._state = self.details.group(23)
            elif self.type == 'ITU_Version_1':
                self._state = self.details.group(24)
            elif self.type == 'ADSL_Firmware_Version':
                self._state = self.details.group(25)
            elif self.type == 'Power_Management_Mode':
                self._state = self.details.group(26)
            elif self.type == 'Test_Mode':
                self._state = self.details.group(27)
            elif self.type == 'Far_Current_Attenuation':
                self._state = float(self.details.group(28).replace(" ", ""))
            elif self.type == 'Far_SNR_Margin':
                self._state = float(self.details.group(29).replace(" ", ""))
            elif self.type == 'CO_ITU_Version_0':
                self._state = self.details.group(30)
            elif self.type == 'CO_ITU_Version_1':
                self._state = self.details.group(31)
            elif self.type == 'DSLAM_Chipset_Vendor':
                self._state = self.details.group(32)
            else:
                self._state = self.details.group(2)

class DraytekData(object):
    """Get the latest data from modem and update the states."""

    def __init__(self, host, port, username, password, CONF_DISPLAY_OPTIONS):
        """Initialize the data object."""
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.data = None

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Connect to modem via telnet to gather status."""
        try:
            connection = Telnet(
                self.host, self.port, timeout=DEFAULT_TIMEOUT)
            connection.read_until(b"Account:")
            connection.write((self.username + "\n").encode('ascii'))
            connection.read_until(b"Password: ")
            connection.write((self.password + "\n").encode('ascii'))
            connection.read_until(b">")
            connection.write(("adsl status\n").encode('ascii'))
            self.status = connection.read_until(b">").decode('ascii')

        except ConnectionRefusedError:
            _LOGGER.error('Draytek is not available at %s:%s', self.host, self.port)
            self.data = None


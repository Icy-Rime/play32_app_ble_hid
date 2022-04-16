from ubluetooth import UUID, BLE, FLAG_READ, FLAG_WRITE, FLAG_NOTIFY
from machine import unique_id
from micropython import const
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)
_IRQ_GATTS_INDICATE_DONE = const(20)
_IRQ_MTU_EXCHANGED = const(21)
_IRQ_L2CAP_ACCEPT = const(22)
_IRQ_L2CAP_CONNECT = const(23)
_IRQ_L2CAP_DISCONNECT = const(24)
_IRQ_L2CAP_RECV = const(25)
_IRQ_L2CAP_SEND_READY = const(26)
_IRQ_CONNECTION_UPDATE = const(27)
_IRQ_ENCRYPTION_UPDATE = const(28)
_IRQ_GET_SECRET = const(29)
_IRQ_SET_SECRET = const(30)

# https://www.bilibili.com/read/cv15067064/
MAX_IRQ_EVENT = 8
HIDS = (                              # Service description: describes the service and how we communicate
    UUID(0x1812),                     # Human Interface Device
    (
        (UUID(0x2A4A), FLAG_READ),       # HID information
        (UUID(0x2A4B), FLAG_READ),       # HID report map
        (UUID(0x2A4C), FLAG_WRITE),      # HID control point
        (UUID(0x2A4D), FLAG_READ | FLAG_NOTIFY, ((UUID(0x2908), 1),)),  # HID report / reference
        (UUID(0x2A4D), FLAG_READ | FLAG_WRITE,  ((UUID(0x2908), 1),)),  # HID report / reference
        (UUID(0x2A4E), FLAG_READ | FLAG_WRITE), # HID protocol mode
    ),
)
SERVICES = (HIDS,)

# https://developer.nordicsemi.com/nRF5_SDK/nRF51_SDK_v4.x.x/doc/html/group___b_l_e___a_p_p_e_a_r_a_n_c_e_s.html
# use little-endian
TYPE_MEDIA_CONTROL = b"\xC0\x03"
TYPE_KEYBOARD = b"\xC1\x03"
TYPE_GAMEPAD = b"\xC3\x03"

# [    # Report Description: describes what we communicate
#     # Report ID 1: Advanced buttons
#     0x05, 0x0C,       # Usage Page (Consumer)
#     0x09, 0x01,       # Usage (Consumer Control)
#     0xA1, 0x01,       # Collection (Application)
#     0x85, 0x01,       #     Report Id (1)
#     #buttons
#     0x15, 0x00,       #     Logical minimum (0)
#     0x25, 0x01,       #     Logical maximum (1)
#     0x75, 0x01,       #     Report Size (1)
#     0x95, 0x01,       #     Report Count (1)
#     0x09, 0xCD,       #     Usage (Play/Pause)
#     0x81, 0x06,       #     Input (Data,Value,Relative,Bit Field)
#     0x09, 0xE2,       #     Usage (Mute)
#     0x81, 0x06,       #     Input (Data,Value,Relative,Bit Field)
#     0x09, 0x40,       #     Usage (Menu)
#     0x81, 0x06,       #     Input (Data,Value,Relative,Bit Field)
#     0x09, 0x9A,       #     Usage (Home)
#     0x81, 0x06,       #     Input (Data,Value,Relative,Bit Field)
#     0x09, 0xB5,       #     Usage (Scan Next Track)
#     0x81, 0x06,       #     Input (Data,Value,Relative,Bit Field)
#     0x09, 0xB6,       #     Usage (Scan Previous Track)
#     0x81, 0x06,       #     Input (Data,Value,Relative,Bit Field)
#     0x09, 0xE9,       #     Usage (Volume Up)
#     0x81, 0x06,       #     Input (Data,Value,Relative,Bit Field)
#     0x09, 0xEA,       #     Usage (Volume Down)
#     0x81, 0x06,       #     Input (Data,Value,Relative,Bit Field)
#     0xC0              # End Collection
# ]
_REPORT_MAP_MEDIA_CONTROL = b"\x05\x0c\t\x01\xa1\x01\x85\x01\x15\x00%\x01u\x01\x95\x01\t\xcd\x81\x06\t\xe2\x81\x06\t@\x81\x06\t\x9a\x81\x06\t\xb5\x81\x06\t\xb6\x81\x06\t\xe9\x81\x06\t\xea\x81\x06\xc0"
# https://docs.microsoft.com/en-us/windows-hardware/drivers/hid/hid-clients
# [    # Report Description: describes what we communicate
#     0x05, 0x01,      # USAGE_PAGE (Generic Desktop)
#     0x09, 0x06,      # USAGE (Keyboard)
#     0xa1, 0x01,      # COLLECTION (Application)
#     0x85, 0x01,      #     REPORT_ID (1)
#     # MODIFIER 1BYTE
#     0x75, 0x01,      #     Report Size (1)
#     0x95, 0x08,      #     Report Count (8)
#     0x05, 0x07,      #     Usage Page (Key Codes)
#     0x19, 0xE0,      #     Usage Minimum (224)
#     0x29, 0xE7,      #     Usage Maximum (231)
#     0x15, 0x00,      #     Logical Minimum (0)
#     0x25, 0x01,      #     Logical Maximum (1)
#     0x81, 0x02,      #     Input (Data, Variable, Absolute); Modifier byte
#     # RESERVED 1BYTE
#     0x75, 0x08,      #     Report Size (8)
#     0x95, 0x01,      #     Report Count (1)
#     0x81, 0x01,      #     Input (Constant); Reserved byte
#     # LEDS(OUTPUT)
#     0x75, 0x01,      #     Report Size (1)
#     0x95, 0x05,      #     Report Count (5)
#     0x05, 0x08,      #     Usage Page (LEDs)
#     0x19, 0x01,      #     Usage Minimum (1)
#     0x29, 0x05,      #     Usage Maximum (5)
#     0x91, 0x02,      #     Output (Data, Variable, Absolute); LED report
#     0x95, 0x01,      #     Report Count (1)
#     0x75, 0x03,      #     Report Size (3)
#     0x91, 0x01,      #     Output (Constant); LED report padding
#     # KEYCODE
#     0x75, 0x08,      #     Report Size (8)
#     0x95, 0x06,      #     Report Count (6)
#     0x15, 0x00,      #     Logical Minimum (0)
#     0x25, 0x65,      #     Logical Maximum (101)
#     0x05, 0x07,      #     Usage Page (Key Codes)
#     0x19, 0x00,      #     Usage Minimum (0)
#     0x29, 0x65,      #     Usage Maximum (101)
#     0x81, 0x00,      #     Input (Data, Array); Key array (6 bytes)
#     0xc0             # END_COLLECTION
# ]
_REPORT_MAP_KEYBOARD = b"\x05\x01\t\x06\xa1\x01\x85\x01u\x01\x95\x08\x05\x07\x19\xe0)\xe7\x15\x00%\x01\x81\x02u\x08\x95\x01\x81\x01u\x01\x95\x05\x05\x08\x19\x01)\x05\x91\x02\x95\x01u\x03\x91\x01u\x08\x95\x06\x15\x00%e\x05\x07\x19\x00)e\x81\x00\xc0"
[    # Report Description: describes what we communicate
    0x05, 0x01,                    # USAGE_PAGE (Generic Desktop)
    0x09, 0x04,                    # USAGE (Joystick)
    0xa1, 0x01,                    # COLLECTION (Application)
    0x85, 0x01,                    #   REPORT_ID (1)
    0xa1, 0x00,                    #   COLLECTION (Physical)
    # sticks
    0x09, 0x30,                    #     USAGE (X)
    0x09, 0x31,                    #     USAGE (Y)
    0x75, 0x08,                    #     REPORT_SIZE (8)
    0x95, 0x02,                    #     REPORT_COUNT (2)
    0x15, 0x81,                    #     LOGICAL_MINIMUM (-127)
    0x25, 0x7f,                    #     LOGICAL_MAXIMUM (127)
    0x81, 0x02,                    #     INPUT (Data,Var,Abs)
    # buttons
    0x05, 0x09,                    #     USAGE_PAGE (Button)
    0x75, 0x01,                    #     REPORT_SIZE (1)
    0x95, 0x08,                    #     REPORT_COUNT (8)
    0x19, 0x01,                    #     USAGE_MINIMUM (Button 1)
    0x29, 0x08,                    #     USAGE_MAXIMUM (Button 8)
    0x25, 0x01,                    #     LOGICAL_MAXIMUM (1)
    0x15, 0x00,                    #     LOGICAL_MINIMUM (0)
    0x81, 0x02,                    #     Input (Data, Variable, Absolute)
    0xc0,                          #   END_COLLECTION
    0xc0                           # END_COLLECTION
]
_REPORT_MAP_GAMEPAD = b"\x05\x01\t\x04\xa1\x01\x85\x01\xa1\x00\t0\t1u\x08\x95\x02\x15\x81%\x7f\x81\x02\x05\tu\x01\x95\x08\x19\x01)\x08%\x01\x15\x00\x81\x02\xc0\xc0"

def _ad_data(type, data):
    size = len(data) + 1
    return bytes([size, type]) + bytes(data)

class HID:
    def __init__(self, name=None, hid_type=TYPE_KEYBOARD):
        self._ble = BLE()
        if type(name) != str:
            name = "PLAY32_" + hex(int.from_bytes(unique_id(), "big"))[-4:].upper()
        self.name = name
        self.hid_type = hid_type
        self.handles = tuple()
        self.conn_handle = None

    def _bt_irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            # A central has connected to this peripheral.
            conn_handle, addr_type, addr = data
            self.conn_handle = conn_handle
            self.stop_advertise()
        elif event == _IRQ_CENTRAL_DISCONNECT:
            # A central has disconnected from this peripheral.
            self.conn_handle = None
            self.start_advertise()

    def init(self, report_map):
        ble = self._ble
        ble.active(True)
        ble.config(gap_name=self.name)
        ble.config(mtu=23)
        self.handles = ble.gatts_register_services(SERVICES)
        adv_data = _ad_data(0x01, b"\x05") # low power device flag
        adv_data += _ad_data(0x03, b"\x12\x18") # HID 0x1812
        adv_data += _ad_data(0x19, self.hid_type) # Appearance
        resp_data = _ad_data(0x09, self.name.encode("utf8")) # Name
        ble.gap_advertise(100_000, adv_data=adv_data, resp_data=resp_data)
        (h_info, h_rep_map, _, __, h_d_rep_in, ___, h_d_rep_out, h_model,) = self.handles[0]
        ble.gatts_write(h_info, b"\x01\x01\x00\x03") # HID info: ver=1.1, country=0, flags=wakeup+normal
        ble.gatts_write(h_d_rep_in, b"\x01\x01") # HID reference: id=1, type=input
        ble.gatts_write(h_d_rep_out, b"\x01\x02") # HID reference: id=1, type=output
        ble.gatts_write(h_model, b"\x01") # HID Protocol Model: 0=Boot Model, 1=Report Model
        ble.gatts_write(h_rep_map, report_map)    # HID input report map
        ble.irq(self._bt_irq)
    
    def stop_advertise(self):
        self._ble.gap_advertise(None)

    def start_advertise(self):
        self._ble.gap_advertise(100_000) # re-use data in the init function.

    def report(self, report_data):
        if self.conn_handle == None:
            return # no-op
        self._ble.gatts_notify(self.conn_handle, self.handles[0][3], report_data)

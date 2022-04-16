import hal_screen, hal_keypad, ble_hid
from play32sys import app
from play32hw import cpu
from ui.dialog import dialog
from ui.select import select_menu

def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def main(app_name, *args, **kws):
    hal_screen.init()
    hal_keypad.init()
    # app_name is app`s dir name in fact.
    sel = select_menu("Please select device type", "HID MODE", ["Keyboard", "Media Control", "Gamepad"])
    if sel < 0:
        app.reset_and_run_app("")
    if sel == 0:
        dialog("D-Pad: Arrow Keys\nA: ENTER\nB: ESCAPE\n\nHard reset to exit. Screen will be turned off.")
    if sel == 1:
        dialog("UP and DOWN: Volume\nLEFT and RIGHT: Track\nA: Play/Pause\nB: Mute\n\nHard reset to exit. Screen will be turned off.")
    if sel == 2:
        dialog("Hard reset to exit. Screen will be turned off.")
    hal_screen.get_framebuffer().fill(0)
    hal_screen.refresh()
    if sel == 0:
        main_loop_keyboard()
    if sel == 1:
        main_loop_media()
    if sel == 2:
        main_loop_gamepad()
    app.reset_and_run_app("")

def main_loop_keyboard():
    hid = ble_hid.HID("Play32_Keyboard", ble_hid.TYPE_KEYBOARD)
    hid.init(ble_hid._REPORT_MAP_KEYBOARD)
    keys = [0x00] * 6
    kmap = [
        0x28, # A: ENTER
        0x29, # B: ESCAPE
        0x52, # UP: UpArrow
        0x51, # DOWN: DownArrow
        0x50, # LEFT: LeftArrow
        0x4F, # RIGHT: RightArrow
    ]
    while True:
        for event in hal_keypad.get_key_event():
            event_type, key = hal_keypad.parse_key_event(event)
            if event_type == hal_keypad.EVENT_KEY_PRESS:
                keys[key] = kmap[key]
            if event_type == hal_keypad.EVENT_KEY_RELEASE:
                keys[key] = 0
            hid.report(b"\x00\x00"+bytes(keys))

def main_loop_media():
    hid = ble_hid.HID("Play32_Media", ble_hid.TYPE_MEDIA_CONTROL)
    hid.init(ble_hid._REPORT_MAP_MEDIA_CONTROL)
    byte = 0
    bit_pos_map = [
        0, # A: Play/Pause
        1, # B: Mute
        6, # UP: vol Volume Up
        7, # DOWN: vol Volume Down
        5, # LEFT: Previous Track
        4, # RIGHT: Next Track
    ]
    while True:
        for event in hal_keypad.get_key_event():
            event_type, key = hal_keypad.parse_key_event(event)
            if event_type == hal_keypad.EVENT_KEY_PRESS:
                byte = set_bit(byte, bit_pos_map[key])
            if event_type == hal_keypad.EVENT_KEY_RELEASE:
                byte = clear_bit(byte, bit_pos_map[key])
            hid.report(bytes([byte]))

def main_loop_gamepad():
    hid = ble_hid.HID("Play32_Gamepad", ble_hid.TYPE_GAMEPAD)
    hid.init(ble_hid._REPORT_MAP_GAMEPAD)
    byte = 0
    while True:
        for event in hal_keypad.get_key_event():
            event_type, key = hal_keypad.parse_key_event(event)
            if event_type == hal_keypad.EVENT_KEY_PRESS:
                byte = set_bit(byte, key)
            if event_type == hal_keypad.EVENT_KEY_RELEASE:
                byte = clear_bit(byte, key)
            hid.report(bytes([byte]))
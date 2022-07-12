import machine
import sdcard
import utime
import uos
import os

cs_pin = 9
sck_pin = 10
mosi_pin = 11
miso_pin = 12
analog_pin = 26

number_of_emg_sensors = 3
number_of_analog_channels = 14
mount_path = '/sd'
log_path = "{}{}".format(mount_path, '/log.csv')


pot_read = machine.ADC(analog_pin)
pot_select_pins = list([machine.Pin(pin_number, machine.Pin.OUT) for pin_number in range(4)])

try:
    spi = machine.SPI(1,
                      baudrate=1000000,
                      polarity=0,
                      phase=0,
                      bits=8,
                      firstbit=machine.SPI.MSB,
                      sck=machine.Pin(sck_pin),
                      mosi=machine.Pin(mosi_pin),
                      miso=machine.Pin(miso_pin))

    sd = sdcard.SDCard(spi, machine.Pin(cs_pin))

    vfs = uos.VfsFat(sd)
    uos.mount(vfs, mount_path)

    with open(log_path, 'w') as log_opend:
        channels_names = ','.join(list(['channel_{}'.format(channel_number) for channel_number in range(number_of_analog_channels)])) + '\n'
        log_opend.write(channels_names)
    print("Found SD card")
except Exception as error:
    pass

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

while True:
    dataset = []
    for current_channel in range(number_of_analog_channels):
        for index, current_pot in enumerate(pot_select_pins):
            current_pot.value(current_channel >> index & 1)
        current_pot_value = pot_read.read_u16()
        dataset.append(str(current_pot_value))
    dataset_str = ','.join(dataset) + '\n'
    with open(log_path, 'a+') as log_opend:
        log_opend.write(dataset_str)
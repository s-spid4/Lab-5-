# Lab 5 – Timing Game using DS3231 RTC and SW1 (GP10)
# Author: Sebastian & Tomas (simplified beginner version)

from machine import Pin, I2C
import time

# --- Setup I2C and DS3231 ---
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
RTC_ADDR = 0x68

# --- Use SW1 (GP10) as button ---
button = Pin(10, Pin.IN, Pin.PULL_DOWN)

# --- Helper: convert BCD to decimal ---
def bcd_to_dec(bcd):
    return (bcd // 16) * 10 + (bcd % 16)

# --- Read seconds from DS3231 ---
def get_seconds():
    data = i2c.readfrom_mem(RTC_ADDR, 0x00, 1)
    return bcd_to_dec(data[0] & 0x7F)

print("=== Timing Game ===")
print("Press SW1 to start, then again after 15 seconds.")
print("Press Ctrl+C to stop.\n")

# --- Open log file ---
log = open("log.txt", "a")

counting = False
start_time = 0

try:
    while True:
        if button.value() == 1:
            time.sleep(0.25)  # debounce
            if not counting:
                # Start timing
                start_time = get_seconds()
                counting = True
                print("Started! Count 15 seconds...")
            else:
                # Stop timing
                end_time = get_seconds()
                counting = False

                elapsed = end_time - start_time
                if elapsed < 0:
                    elapsed += 60

                print("You counted:", elapsed, "seconds")

                # Log to file
                log.write(f"{elapsed}\n")
                log.flush()
                print("Saved to log.txt\n")

            # Wait until button released
            while button.value() == 1:
                time.sleep(0.05)

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nProgram stopped.")

finally:
    log.close()
    print("Log file closed.")
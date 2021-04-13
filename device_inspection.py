"""
Run this script to check the system devices on your computer and set proper index to your main script.

!python device_inspection.py
"""
import pyaudio


def main():
    p = pyaudio.PyAudio()
    print("Number of device: ", p.get_device_count())
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        print(
            "Index: {} has device name: {}".format(
                device_info["index"], device_info["name"]
            )
        )


if __name__ == "__main__":
    main()

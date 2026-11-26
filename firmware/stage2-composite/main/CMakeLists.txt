# SPDX-License-Identifier: MIT
# With CONFIG_USB_DEVICE_UAC_AS_PART=y the usb_device_uac component does not add its own descriptors and TinyUSB configuration:
# the project must. This mirrors what the component's own CMakeLists does when AS_PART is off, but with OUR files in ./tusb.
idf_component_register(SRCS "main.c"
                       INCLUDE_DIRS "." "tusb")

# find the TinyUSB component (a local one, or the one fetched from the component registry)
idf_build_get_property(build_components BUILD_COMPONENTS)
if(tinyusb IN_LIST build_components)
    set(tinyusb_name tinyusb)           # a local component
else()
    set(tinyusb_name espressif__tinyusb) # the managed component
endif()

idf_component_get_property(tusb_lib ${tinyusb_name} COMPONENT_LIB)
target_include_directories(${tusb_lib} PUBLIC "${COMPONENT_DIR}/tusb")
target_sources(${tusb_lib} PUBLIC "${COMPONENT_DIR}/tusb/usb_descriptors.c")

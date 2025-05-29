#!/bin/bash

# Prerequisite check(s) for module.
check() {
    # Return 255 to only include the module, if another module requires it.
    return 0
}

installkernel() {
    # Filesystem (vfat) and codepages required to mount the ESP
    hostonly="" instmods vfat nls_cp437 nls_iso8859-1 nls_utf8
}

install() {
    inst_multiple \
        "$systemdsystemunitdir"/initrd-pcr-signature.service \
        "$systemdutildir"/system-generators/boot-efi-generator \
        /usr/libexec/initrd-pcr-signature \
        dd tr

    $SYSTEMCTL -q --root "$initdir" enable initrd-pcr-signature.service
}

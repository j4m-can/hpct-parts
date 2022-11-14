# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# manager.py

from charms.operator_libs_linux.v0 import passwd
from charms.operator_libs_linux.v1 import apt, systemd


class Manager:

    packages = []
    systemd_services = []

    def __init__(self):
        pass

    def configure(self):
        pass

    def disable(self):
        """Disable services."""

        for name in self.systemd_services:
            systemd.service_pause(name)

    def enable(self):
        """Enable services."""

        for name in self.systemd_services:
            systemd.service_resume(name)

    def install(self):
        """Install packages."""

        if self.packages:
            try:
                apt.update()
                apt.add_package(self.packages)
            except:
                raise Exception(f"failed to install package ({name})")

    def is_enabled(self):
        """Check enabled status of services."""

        if self.systemd_services:
            for name in self.systemd_services:
                if not _systemctl("is-enabled", name, quiet=True):
                    return False

        return True

    def is_installed(self):
        """Check packages are installed."""

        if self.packages:
            for name in self.packages:
                if not self.apt.DebianPackage.from_installed_package(name).present:
                    return False

        return True

    def is_running(self):
        """Check running/active status of services."""

        if self.systemd_services:
            for name in self.systemd_services:
                if not systemd.service_running(name):
                    return False

        return True

    def restart(self):
        """Restart servers/services."""

        self.stop()
        self.start()

    def start(self):
        """Start services."""

        for name in self.systemd_services:
            systemd.service_start(name)

    def stop(self):
        """Stop services."""

        for name in self.systemd_services:
            systemd.service_stop(name)

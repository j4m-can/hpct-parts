# Copyright 2022 Canonical Ltd.
# See LICENSE file for licensing details.
#
# manager.py

from charms.operator_libs_linux.v0 import passwd
from charms.operator_libs_linux.v1 import apt, snap, systemd


class Manager:

    packages = []
    systemd_services = []
    snaps = []

    def __init__(self):
        pass

    def configure(self):
        pass

    def disable(self):
        """Disable services."""

        for name in self.systemd_services:
            systemd.service_pause(name)

        if self.snaps:
            pass

    def enable(self):
        """Enable services."""

        for name in self.systemd_services:
            systemd.service_resume(name)

        if self.snaps:
            pass

    def install(self):
        """Install packages."""

        if self.packages:
            try:
                apt.update()
                apt.add_package(self.packages)
            except:
                raise Exception(f"failed to install package ({name})")

        if self.snaps:
            try:
                cache = snap.SnapCache()
                for d in self.snaps:
                    _snap = cache[d["name"]]
                    _snap.ensure(
                        d["version"],
                        classic=d.get("classic", False),
                        channel=d.get("channel", ""),
                        cohort=d.get("cohort", ""),
                    )
                snap.hold_refresh()
            except:
                raise Exception(f"failed to install snap ({d['name']})")

    def is_enabled(self):
        """Check enabled status of services."""

        if self.systemd_services:
            for name in self.systemd_services:
                if not _systemctl("is-enabled", name, quiet=True):
                    return False

        if self.snaps:
            cache = snap.SnapCache()
            for d in self.snaps:
                name = d["name"]
                _snap = cache[name]
                for svcname in d.get("services", []):
                    if not _snap.service[svcname]["enabled"]:
                        return False

        return True

    def is_installed(self):
        """Check packages are installed."""

        if self.packages:
            for name in self.packages:
                if not self.apt.DebianPackage.from_installed_package(name).present:
                    return False

        if self.snaps:
            cache = snap.SnapCache()
            for d in self.snaps:
                name = d["name"]
                _snap = cache[name]
                if not _snap.present:
                    return False

        return True

    def is_running(self):
        """Check running/active status of services."""

        if self.systemd_services:
            for name in self.systemd_services:
                if not systemd.service_running(name):
                    return False

        if self.snaps:
            cache = snap.SnapCache()
            for d in snaps:
                name = d["name"]
                _snap = cache[name]
                for svcname in d.get("services", []):
                    if not _snap.service[svcname]["active"]:
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

        for name in self.snaps:
            snap.start(name)

    def stop(self):
        """Stop services."""

        for name in self.systemd_services:
            systemd.service_stop(name)

        for name in self.snaps:
            snap.stop(name)

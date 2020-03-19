#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © ${year} ${dev_name} ${dev_email}
#
# Distributed under terms of the GPL license.
"""Operator Charm main library."""
# Load modules from lib directory
import sys
sys.path.append('lib')

from ops.charm import CharmBase  # noqa:E402
from ops.framework import StoredState  # noqa:E402
from ops.model import (  # noqa:E402
    ActiveStatus,
    BlockedStatus,
    MaintenanceStatus
)

""" -- Example relation interface for MySQL:
from interfaces import (
    MySQLInterfaceRequires
)
"""


class ${class}(CharmBase):
    """Class reprisenting this Operator charm."""

    state = StoredState()

    def __init__(self, *args):
        """Initialize charm and configure states and events to observe."""
        super().__init__(*args)
        # -- standard hook observation
        self.framework.observe(self.on.install, self.on_install)
        self.framework.observe(self.on.start, self.on_start)
        self.framework.observe(self.on.config_changed, self.on_config_changed)
        # -- initialize states --
        self.state.set_default(installed=False)
        self.state.set_default(configured=False)
        self.state.set_default(started=False)
        # -- example action observation
        # self.framework.observe(self.on.example_action, self)
        # -- example relation / interface observation, disabled by default
        # self.framework.observe(self.on.db_relation_changed, self)
        # self.mysql = MySQLInterfaceRequires(self, 'db')

    def on_install(self, event):
        """Handle install state."""
        self.unit.status = MaintenanceStatus("Installing charm software")
        # Perform install tasks
        self.unit.status = MaintenanceStatus("Install complete")
        self.model._backend.juju_log("INFO", "Install of software complete")
        self.state.installed = True

    def on_config_changed(self, event):
        """Handle config changed."""

        if not self.state.installed:
            self.model._backend.juju_log(
                "ERROR", "Config changed called before install complete."
            )
            self.unit.status = MaintenanceStatus(
                "Install not completed, not configuring."
            )

            return

        if self.state.started:
            # Stop if necessary for reconfig
            self.model._backend.juju_log("INFO", "Stopping for configuration")
            pass
        # Configure the software
        self.model._backend.juju_log("INFO", "Configuring")
        self.state.configured = True

    def on_start(self, event):
        """Handle start state."""

        if not self.state.configured:
            self.model._backend.juju_log(
                "ERROR", "Install called before configuration complete."
            )

            self.unit.status = MaintenanceStatus(
                "Configure not completed, not starting."
            )

            return

        self.unit.status = MaintenanceStatus("Starting charm software")
        # Start software
        self.unit.status = ActiveStatus("Unit is ready")
        self.state.started = True

    # -- Example relation interface for MySQL, not observed by default:
    # def on_db_relation_changed(self, event):
    #     """Handle an example db relation's change event."""
    #     self.password = event.relation.data[event.unit].get("password")
    #     self.unit.status = MaintenanceStatus("Configuring database")
    #     if self.mysql.is_ready:
    #         event.log("Database relation complete")
    #     self.state._db_configured = True

    # def on_example_action(self, event):
    #     """Handle the example_action action."""
    #     event.log("Hello from the example action.")
    #     event.set_results({"success": "true"})


if __name__ == "__main__":
    main(CloudstatsCharm)

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © ${year} ${dev_name} ${dev_email}
#
# Distributed under terms of the GPL license.
"""Operator Charm main library."""
# Load modules from $CHARM_DIR/lib
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
        self.unit = self.framework.model.unit
        # -- standard hook observation
        self.framework.observe(self.on.start, self)
        self.framework.observe(self.on.config_changed, self)
        # -- example action observation
        self.framework.observe(self.on.example_action, self)
        # -- example relation / interface observation, disabled by default
        # self.framework.observe(self.on.db_relation_changed, self)
        # self.mysql = MySQLInterfaceRequires(self, 'db')

    def on_start(self, event):
        """Handle start state."""
        # do things on start, like install packages
        # once done, mark state as done
        self.unit.status = MaintenanceStatus("Installing charm software")
        # perform installation and common configuration bootstrap tasks
        self.unit.status = MaintenanceStatus("Software installed, performing configuration")
        self.state._started = True

    def on_config_changed(self, event):
        """Handle config changed hook."""
        # if software is installed and DB related, configure software
        if self.state._started and self.state._db_configured:
            # configure your software
            self.example_config = self.model.config['example_config']
            event.log("Install of software complete")
            self.unit.status = ActiveStatus("Software installed and configured")
            self.state._configured = True
        elif self.state._started:
            event.log("Waiting on configuration to run, and DB to be related.")
            self.unit.status = BlockedStatus("Waiting for MySQL to be related")
        else:
            event.log("Waiting on installation to complete.")

    # -- Example relation interface for MySQL, not observed by default:
    def on_db_relation_changed(self, event):
        """Handle an example db relation's change event."""
        self.password = event.relation.data[event.unit].get("password")
        self.unit.status = MaintenanceStatus("Configuring database")
        if self.mysql.is_ready:
            event.log("Database relation complete")
        self.state._db_configured = True

    def on_example_action(self, event):
        """Handle the example_action action."""
        event.log("Hello from the example action.")
        event.set_results({"success": "true"})

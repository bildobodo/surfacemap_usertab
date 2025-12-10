import os
import linuxcnc

from qtpy import uic
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget

from qtpyvcp.plugins import getPlugin
from qtpyvcp.utilities import logger
from qtpyvcp.actions.machine_actions import issue_mdi

LOG = logger.getLogger(__name__)

STATUS = getPlugin('status')
TOOL_TABLE = getPlugin('tooltable')

INI_FILE = linuxcnc.ini(os.getenv('INI_FILE_NAME'))


class UserTab(QWidget):
    def __init__(self, parent=None):
        super(UserTab, self).__init__(parent)
        ui_file = os.path.splitext(os.path.basename(__file__))[0] + ".ui"
        uic.loadUi(os.path.join(os.path.dirname(__file__), ui_file), self)
        
        # Connect input field signals to update LinuxCNC parameters
        self.surface_scan_x0_3050.editingFinished.connect(self.update_parameters)
        self.surface_scan_x1_3051.editingFinished.connect(self.update_parameters)
        self.surface_scan_y0_3052.editingFinished.connect(self.update_parameters)
        self.surface_scan_y1_3053.editingFinished.connect(self.update_parameters)
        self.surface_scan_xprobes_3054.editingFinished.connect(self.update_parameters)
        self.surface_scan_yprobes_3055.editingFinished.connect(self.update_parameters)
        self.probe_fast_fr_3056.editingFinished.connect(self.update_parameters)
        self.probe_slow_fr_3057.editingFinished.connect(self.update_parameters)
        self.surface_scan_safez_3058.editingFinished.connect(self.update_parameters)
        self.surface_scan_depthz_3059.editingFinished.connect(self.update_parameters)
        
        # Also connect the button to update parameters
        self.update_surface_scan_params.clicked.connect(self.update_parameters)
    
    def update_parameters(self):
        """Write GUI input values to LinuxCNC numbered parameters using issue_mdi"""
        try:
            # Get values from input fields, using 0.0 as default if empty
            x0 = float(self.surface_scan_x0_3050.text() or 0.0)
            x1 = float(self.surface_scan_x1_3051.text() or 0.0)
            y0 = float(self.surface_scan_y0_3052.text() or 0.0)
            y1 = float(self.surface_scan_y1_3053.text() or 0.0)
            xprobes = float(self.surface_scan_xprobes_3054.text() or 2.0)
            yprobes = float(self.surface_scan_yprobes_3055.text() or 2.0)
            fast_fr = float(self.probe_fast_fr_3056.text() or 100.0)
            slow_fr = float(self.probe_slow_fr_3057.text() or 20.0)
            safez = float(self.surface_scan_safez_3058.text() or 5.0)
            depthz = float(self.surface_scan_depthz_3059.text() or 10.0)
            
            # Write to LinuxCNC numbered parameters #3050-#3059
            # These are persistent parameters that will be saved to the var file
            issue_mdi(f"#3050 = {x0}")
            issue_mdi(f"#3051 = {x1}")
            issue_mdi(f"#3052 = {y0}")
            issue_mdi(f"#3053 = {y1}")
            issue_mdi(f"#3054 = {xprobes}")
            issue_mdi(f"#3055 = {yprobes}")
            issue_mdi(f"#3056 = {fast_fr}")
            issue_mdi(f"#3057 = {slow_fr}")
            issue_mdi(f"#3058 = {safez}")
            issue_mdi(f"#3059 = {depthz}")
            
            LOG.info(f"Surface scan parameters updated: x0={x0}, x1={x1}, y0={y0}, y1={y1}, "
                    f"xprobes={xprobes}, yprobes={yprobes}, fast_fr={fast_fr}, slow_fr={slow_fr}, "
                    f"safez={safez}, depthz={depthz}")
        except ValueError as e:
            LOG.error(f"Error updating surface scan parameters: {e}")
        except Exception as e:
            LOG.error(f"Unexpected error updating surface scan parameters: {e}")

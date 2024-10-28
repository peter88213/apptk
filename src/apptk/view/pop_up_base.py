"""Provide an abstract popup window base class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/apptk
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from abc import abstractmethod
from apptk.view.view_component_base import ViewComponentBase
import tkinter as tk


class PopUpBase(ViewComponentBase, tk.Toplevel):
    OFFSET = 300

    @abstractmethod
    def __init__(self, model, view, controller, **kw):
        ViewComponentBase.__init__(self, model, view, controller)
        tk.Toplevel.__init__(self, **kw)
        __, x, y = self._ui.root.geometry().split('+')
        windowGeometry = f'+{int(x)+self.OFFSET}+{int(y)+self.OFFSET}'
        self.geometry(windowGeometry)
        self.grab_set()
        self.focus()

    def disable_menu(self):
        """Disable UI widgets when no project is open."""
        pass

    def enable_menu(self):
        """Enable UI widgets when a project is open."""
        pass

    def lock(self):
        """Inhibit changes on the model."""
        pass

    def refresh(self):
        """Refresh the view after model change."""
        pass

    def unlock(self):
        """Enable changes on the model."""
        pass


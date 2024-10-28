"""Provide an abstract view component base class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/apptk
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from abc import ABC, abstractmethod


class ViewComponentBase(ABC):

    @abstractmethod
    def __init__(self, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller

    def disable_menu(self):
        """Disable UI widgets, e.g. when no project is open."""
        pass

    def enable_menu(self):
        """Enable UI widgets, e.g. when a project is opened."""
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


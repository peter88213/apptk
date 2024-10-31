"""Provide an abstract view component base class.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/apptk
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from abc import ABC, abstractmethod


class ViewComponentBase(ABC):
    """A node in the view composite structure.
    
    Sub-view instances of the same class can be registered and unregistered.
    
    Passes down the following commands to the sub-views:
        - refresh
        - lock/unlock
        - emable/disable menu    
    """

    @abstractmethod
    def __init__(self, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        self._viewComponents = []
        # applying the Composite design pattern

    def disable_menu(self):
        """Disable UI widgets, e.g. when no project is open."""
        for viewComponent in self._viewComponents:
            viewComponent.disable_menu()

    def enable_menu(self):
        """Enable UI widgets, e.g. when a project is opened."""
        for viewComponent in self._viewComponents:
            viewComponent.enable_menu()

    def lock(self):
        """Inhibit changes on the model."""
        for viewComponent in self._viewComponents:
            viewComponent.lock()

    def refresh(self):
        """Refresh all view components."""
        for viewComponent in self._viewComponents:
            viewComponent.refresh()

    def register_view(self, viewComponent):
        """Add a view object to the composite list.
        
        Positional arguments:
            viewComponent -- Reference to a ViewComponentBase subclass instance.
        """
        if not viewComponent in self._viewComponents:
            self._viewComponents.append(viewComponent)

    def unlock(self):
        """Enable changes on the model."""
        for viewComponent in self._viewComponents:
            viewComponent.unlock()

    def unregister_view(self, viewComponent):
        """Revove a view object from the component list.
        
        Positional arguments:
            viewComponent -- Reference to a ViewComponentBase subclass instance.
        """
        if viewComponent in self._viewComponents:
            self._viewComponents.remove(viewComponent)


"""Provide a view base class for a MVC framework.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/apptk
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from abc import ABC, abstractmethod
from tkinter import messagebox

import tkinter as tk


class ViewBase(ABC):

    @abstractmethod
    def __init__(self, model, controller, title):
        """Create a composite structure for view components."""
        self._mdl = model
        self._ctrl = controller
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self._ctrl.on_quit)
        self.root.title(title)
        self.title = title
        self._mdl.register_client(self)
        self._viewComponents = []
        self.infoWhatText = ''
        self.infoHowText = ''

    def ask_yes_no(self, text, title=None):
        """Query yes or no with a pop-up box.
        
        Positional arguments:
            text -- question to be asked in the pop-up box. 
            
        Optional arguments:
            title -- title to be displayed on the window frame.            
        """
        if title is None:
            title = self.title
        return messagebox.askyesno(title, text)

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

    def on_quit(self):
        """Gracefully close the user interface."""
        self.root.quit()

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

    def set_info(self, message):
        """Set a buffered message for display in any info area.
        
        Positional arguments:
            message -- message to be buffered.
        """
        self.infoWhatText = message

    def set_status(self, message):
        """Set a buffered message for display in any status area.
        
        Positional arguments:
            message -- message to be buffered.
            
        Replace error/notification markers, if any.
        """
        if message.startswith('!'):
            message = f'Error: {message.split("!", maxsplit=1)[1].strip()}'
        elif message.startswith('#'):
            message = f'Notification: {message.split("#", maxsplit=1)[1].strip()}'
        self.infoHowText = message

    def show_error(self, message, title=None):
        """Display an error message box.
        
        Positional arguments:
            message -- error message to be displayed.
            
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showerror(title, message)

    def show_info(self, message, title=None):
        """Display an informational message box.
        
        Positional arguments:
            message -- informational message to be displayed.
            
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showinfo(title, message)

    def show_warning(self, message, title=None):
        """Display a warning message box.
        
        Optional arguments:
            title -- title to be displayed on the window frame.
        """
        if title is None:
            title = self.title
        messagebox.showwarning(title, message)

    def start(self):
        """Start the Tk main loop.
        
        Note: This can not be done in the constructor method.
        """
        self.root.mainloop()

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


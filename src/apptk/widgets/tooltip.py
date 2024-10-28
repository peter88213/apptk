"""Tools for displaying tool-tips.

This includes:
 * an abstract base-class for different kinds of tooltips
 * a simple text-only Tooltip class
 
This is a slightly modified variant of the idlelib.tooltip module.

idlelib code:
Copyright (c) 2001-2024 Python Software Foundation; All Rights Reserved
https://github.com/python/cpython/blob/main/LICENSE

Modifications for the use with apptk:
For further information see https://github.com/peter88213/apptk

- Change the tkinter import to avoid namespace issues when packaging.
- Replace some tk constants with simple strings.

"""
import tkinter as tk


class TooltipBase:
    """abstract base class for tooltips"""

    def __init__(self, anchor_widget):
        """Create a tooltip.

        anchor_widget: the widget next to which the tooltip will be shown

        Note that a widget will only be shown when showtip() is called.
        """
        self.anchor_widget = anchor_widget
        self.tipwindow = None

    def __del__(self):
        self.hidetip()

    def showtip(self):
        """display the tooltip"""
        if self.tipwindow:
            return
        self.tipwindow = tw = tk.Toplevel(self.anchor_widget)
        # show no border on the top level window
        tw.wm_overrideredirect(1)
        try:
            # This command is only needed and available on Tk >= 8.4.0 for OSX.
            # Without it, call tips intrude on the typing process by grabbing
            # the focus.
            tw.tk.call("::tk::unsupported::MacWindowStyle", "style", tw._w,
                       "help", "noActivates")
        except tk.TclError:
            pass

        self.position_window()
        self.showcontents()
        self.tipwindow.update_idletasks()  # Needed on MacOS -- see #34275.
        self.tipwindow.lift()  # work around bug in Tk 8.5.18+ (issue #24570)

    def position_window(self):
        """(re)-set the tooltip's screen position"""
        x, y = self.get_position()
        root_x = self.anchor_widget.winfo_rootx() + x
        root_y = self.anchor_widget.winfo_rooty() + y
        self.tipwindow.wm_geometry("+%d+%d" % (root_x, root_y))

    def get_position(self):
        """choose a screen position for the tooltip"""
        # The tip window must be completely outside the anchor widget;
        # otherwise when the mouse enters the tip window we get
        # a leave event and it disappears, and then we get an enter
        # event and it reappears, and so on forever :-(
        #
        # Note: This is a simplistic implementation; sub-classes will likely
        # want to override this.
        return 20, self.anchor_widget.winfo_height() + 1

    def showcontents(self):
        """content display hook for sub-classes"""
        # See ToolTip for an example
        raise NotImplementedError

    def hidetip(self):
        """hide the tooltip"""
        # Note: This is called by __del__, so careful when overriding/extending
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            try:
                tw.destroy()
            except tk.TclError:  # pragma: no cover
                pass


class OnHoverTooltipBase(TooltipBase):
    """abstract base class for tooltips, with delayed on-hover display"""

    def __init__(self, anchor_widget, hover_delay=1000):
        """Create a tooltip with a mouse hover delay.

        anchor_widget: the widget next to which the tooltip will be shown
        hover_delay: time to delay before showing the tooltip, in milliseconds

        Note that a widget will only be shown when showtip() is called,
        e.g. after hovering over the anchor widget with the mouse for enough
        time.
        """
        super().__init__(anchor_widget)
        self.hover_delay = hover_delay

        self._after_id = None
        self._id1 = self.anchor_widget.bind("<Enter>", self._show_event)
        self._id2 = self.anchor_widget.bind("<Leave>", self._hide_event)
        self._id3 = self.anchor_widget.bind("<Button>", self._hide_event)

    def __del__(self):
        try:
            self.anchor_widget.unbind("<Enter>", self._id1)
            self.anchor_widget.unbind("<Leave>", self._id2)  # pragma: no cover
            self.anchor_widget.unbind("<Button>", self._id3)  # pragma: no cover
        except tk.TclError:
            pass
        super().__del__()

    def _show_event(self, event=None):
        """event handler to display the tooltip"""
        if self.hover_delay:
            self.schedule()
        else:
            self.showtip()

    def _hide_event(self, event=None):
        """event handler to hide the tooltip"""
        self.hidetip()

    def schedule(self):
        """schedule the future display of the tooltip"""
        self.unschedule()
        self._after_id = self.anchor_widget.after(self.hover_delay,
                                                  self.showtip)

    def unschedule(self):
        """cancel the future display of the tooltip"""
        after_id = self._after_id
        self._after_id = None
        if after_id:
            self.anchor_widget.after_cancel(after_id)

    def hidetip(self):
        """hide the tooltip"""
        try:
            self.unschedule()
        except tk.TclError:  # pragma: no cover
            pass
        super().hidetip()


class Hovertip(OnHoverTooltipBase):
    "A tooltip that pops up when a mouse hovers over an anchor widget."

    def __init__(self, anchor_widget, text, hover_delay=1000):
        """Create a text tooltip with a mouse hover delay.

        anchor_widget: the widget next to which the tooltip will be shown
        hover_delay: time to delay before showing the tooltip, in milliseconds

        Note that a widget will only be shown when showtip() is called,
        e.g. after hovering over the anchor widget with the mouse for enough
        time.
        """
        super().__init__(anchor_widget, hover_delay=hover_delay)
        self.text = text

    def showcontents(self):
        label = tk.Label(self.tipwindow, text=self.text, justify='left',
                      background="#ffffe0", relief='solid', borderwidth=1)
        label.pack()


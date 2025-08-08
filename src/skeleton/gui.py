"""
Graphical user interface for the skeleton project using wxPython.
"""

import sys
import threading
from typing import Optional

try:
    import wx
    import wx.lib.agw.aui as aui
    WX_AVAILABLE = True
except ImportError:
    wx = None
    WX_AVAILABLE = False

# Handle both relative and absolute imports
try:
    from .core import SkeletonApp
    from .utils import setup_logging, get_version
except ImportError:
    # If running as __main__, try absolute imports
    try:
        from skeleton.core import SkeletonApp
        from skeleton.utils import setup_logging, get_version
    except ImportError:
        # Last resort - add parent directory to path
        import os
        from pathlib import Path
        parent_dir = Path(__file__).parent.parent.parent / "src"
        sys.path.insert(0, str(parent_dir))
        
        from skeleton.core import SkeletonApp
        from skeleton.utils import setup_logging, get_version


if WX_AVAILABLE:
    class SkeletonFrame(wx.Frame):
        """Main application frame."""
        
        def __init__(self):
            super().__init__(
                None,
                title=f"Skeleton Project v{get_version()}",
                size=(800, 600)
            )
            
            self.app_instance = None
            self.setup_ui()
            self.setup_menubar()
            self.setup_statusbar()
            self.center_on_screen()
            
        def setup_ui(self):
            """Set up the user interface."""
            # Create main panel
            self.panel = wx.Panel(self)
            
            # Create sizer for layout
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            
            # Title label
            title_label = wx.StaticText(
                self.panel,
                label="Skeleton Project",
                style=wx.ALIGN_CENTER
            )
            title_font = title_label.GetFont()
            title_font.SetPointSize(16)
            title_font.SetWeight(wx.FONTWEIGHT_BOLD)
            title_label.SetFont(title_font)
            
            # Information text
            info_text = wx.StaticText(
                self.panel,
                label="This is a skeleton Python project with GUI interface.\n"
                      "Use this as a template for your own projects.",
                style=wx.ALIGN_CENTER
            )
            
            # Control buttons
            button_sizer = wx.BoxSizer(wx.HORIZONTAL)
            
            self.run_button = wx.Button(self.panel, label="Run Application")
            self.status_button = wx.Button(self.panel, label="Show Status")
            
            button_sizer.Add(self.run_button, 0, wx.ALL, 5)
            button_sizer.Add(self.status_button, 0, wx.ALL, 5)
            
            # Output text area
            self.output_text = wx.TextCtrl(
                self.panel,
                style=wx.TE_MULTILINE | wx.TE_READONLY,
                size=(-1, 200)
            )
            
            # Layout
            main_sizer.Add(title_label, 0, wx.ALL | wx.CENTER, 10)
            main_sizer.Add(info_text, 0, wx.ALL | wx.CENTER, 10)
            main_sizer.Add(button_sizer, 0, wx.ALL | wx.CENTER, 10)
            main_sizer.Add(
                wx.StaticText(self.panel, label="Output:"),
                0, wx.ALL | wx.EXPAND, 5
            )
            main_sizer.Add(self.output_text, 1, wx.ALL | wx.EXPAND, 5)
            
            self.panel.SetSizer(main_sizer)
            
            # Bind events
            self.run_button.Bind(wx.EVT_BUTTON, self.on_run_application)
            self.status_button.Bind(wx.EVT_BUTTON, self.on_show_status)
            
        def setup_menubar(self):
            """Set up the menu bar."""
            menubar = wx.MenuBar()
            
            # File menu
            file_menu = wx.Menu()
            file_menu.Append(wx.ID_EXIT, "E&xit\tCtrl+Q", "Exit the application")
            menubar.Append(file_menu, "&File")
            
            # Help menu
            help_menu = wx.Menu()
            help_menu.Append(wx.ID_ABOUT, "&About\tF1", "About this application")
            menubar.Append(help_menu, "&Help")
            
            self.SetMenuBar(menubar)
            
            # Bind menu events
            self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_EXIT)
            self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)
            
        def setup_statusbar(self):
            """Set up the status bar."""
            self.statusbar = self.CreateStatusBar(2)
            self.statusbar.SetStatusText("Ready", 0)
            self.statusbar.SetStatusText(f"v{get_version()}", 1)
            
        def center_on_screen(self):
            """Center the window on the screen."""
            self.Center()
            
        def log_to_output(self, message: str):
            """Add a message to the output text area."""
            wx.CallAfter(self._append_to_output, message)
            
        def _append_to_output(self, message: str):
            """Append message to output (called from main thread)."""
            self.output_text.AppendText(f"{message}\n")
            
        def on_run_application(self, event):
            """Handle run application button click."""
            self.statusbar.SetStatusText("Running...", 0)
            self.log_to_output("Starting application...")
            
            # Run app in separate thread to avoid blocking GUI
            def run_app():
                try:
                    if self.app_instance is None:
                        self.app_instance = SkeletonApp({"debug": False})
                    
                    result = self.app_instance.run()
                    if result == 0:
                        self.log_to_output("Application completed successfully!")
                    else:
                        self.log_to_output(f"Application failed with exit code: {result}")
                        
                except Exception as e:
                    self.log_to_output(f"Error running application: {str(e)}")
                    
                finally:
                    wx.CallAfter(self.statusbar.SetStatusText, "Ready", 0)
            
            thread = threading.Thread(target=run_app)
            thread.daemon = True
            thread.start()
            
        def on_show_status(self, event):
            """Handle show status button click."""
            if self.app_instance is None:
                self.app_instance = SkeletonApp()
                
            status = self.app_instance.get_status()
            
            status_msg = f"App: {status['app_name']}\n"
            status_msg += f"Version: {status['version']}\n"
            status_msg += f"Debug: {status['debug']}\n"
            
            self.log_to_output("Current Status:")
            self.log_to_output(status_msg)
            
        def on_exit(self, event):
            """Handle exit menu item."""
            self.Close()
            
        def on_about(self, event):
            """Handle about menu item."""
            about_info = wx.adv.AboutDialogInfo()
            about_info.SetName("Skeleton Project")
            about_info.SetVersion(get_version())
            about_info.SetDescription(
                "A skeleton Python project ready for PyPI distribution\n"
                "and executable packaging."
            )
            about_info.SetCopyright("(C) 2024 Your Name")
            about_info.AddDeveloper("Your Name")
            
            wx.adv.AboutBox(about_info)


    class SkeletonWxApp(wx.App):
        """Main wxPython application class."""
        
        def OnInit(self):
            """Initialize the application."""
            frame = SkeletonFrame()
            frame.Show()
            return True

else:
    # Dummy classes when wxPython is not available
    class SkeletonFrame:
        """Dummy frame class when wxPython is not available."""
        pass
        
    class SkeletonWxApp:
        """Dummy app class when wxPython is not available."""
        pass


def main() -> int:
    """
    Main entry point for the GUI application.
    
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    if not WX_AVAILABLE:
        print("Error: wxPython is not installed.")
        print("Install it with: pip install wxpython")
        print("")
        print("On macOS, you might need to use:")
        print("  pip install -U wxpython")
        print("")
        print("On Linux, you might need to install system dependencies first:")
        print("  sudo apt-get install libgtk-3-dev libwebkitgtk-3.0-dev")
        print("  pip install wxpython")
        return 1
        
    # Set up basic logging
    setup_logging(level="INFO")
    
    # Create and run the wxPython application
    app = SkeletonWxApp()
    app.MainLoop()
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 
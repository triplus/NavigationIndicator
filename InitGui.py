# Navigation indicator for FreeCAD
# Copyright (C) 2016  triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA


def navigationIndicator():
    """
    Navigation indicator for FreeCAD.
    """
    import FreeCAD as App
    import FreeCADGui as Gui
    from PySide import QtGui
    from PySide import QtCore

    icon = """<svg xmlns="http://www.w3.org/2000/svg" height="64" width="64">
               <path d="m39.075 4.9998c5.2101 0 9.4337 4.2602 9.4337
                        9.5154v27.826c0 7.8515-7.3914 16.659-16.509
                        16.659-9.1177
                        0-16.509-8.7965-16.509-16.645v-27.84c0-5.2552
                        4.9959-9.5154 9.4459-9.5154h14.138z"
                        stroke="#2e3436" stroke-width="6" fill="none"/>
               <path d="m33.886 15.11v13.084a1.8868 1.9032 0 0 1 -3.7735
                        0v-13.084a1.8868 1.9032 0 1 1 3.7735 0z"
                        stroke="#2e3436" stroke-width="4" fill="none"/>
              </svg>"""

    navIcon = QtGui.QPixmap()
    navIcon.loadFromData(icon)

    def onStart():
        """
        Add navigation indicator to the status bar.
        """
        statusBar = mw.statusBar()
        paramGet = App.ParamGet("User parameter:BaseApp/Preferences/View")

        navStyle = {
            "OpenInventor": "Gui::InventorNavigationStyle",
            "CAD": "Gui::CADNavigationStyle",
            "Blender": "Gui::BlenderNavigationStyle",
            "MayaGesture": "Gui::MayaGestureNavigationStyle",
            "Touchpad": "Gui::TouchpadNavigationStyle",
            "Gesture": "Gui::GestureNavigationStyle",
            "OpenCascade": "Gui::OpenCascadeNavigationStyle"}

        navStyleSort = [
            "OpenInventor",
            "CAD",
            "Blender",
            "MayaGesture",
            "Touchpad",
            "Gesture",
            "OpenCascade"]

        def setDefault():
            """
            Set default navigation style.
            """
            style = False
            menu.blockSignals(True)
            defaultStyle = paramGet.GetString("NavigationStyle")

            for i in navStyle:
                if navStyle[i] == defaultStyle:
                    for a in menu.actions():
                        if a.text() == i:
                            style = True
                            menu.setDefaultAction(a)
                            indicator.setDefaultAction(a)
                        else:
                            pass
                else:
                    pass

                if style:
                    undefined.setVisible(False)
                else:
                    undefined.setVisible(True)
                    undefined.setEnabled(True)
                    menu.setDefaultAction(undefined)
                    indicator.setDefaultAction(undefined)

            menu.blockSignals(False)

        indicator = QtGui.QToolButton(statusBar)
        indicator.setAutoRaise(True)
        indicator.setObjectName("NavInd_Button")
        indicator.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        indicator.setStyleSheet("QToolButton::menu-indicator {image: none}")
        indicator.setPopupMode(QtGui.QToolButton
                               .ToolButtonPopupMode
                               .InstantPopup)

        menu = QtGui.QMenu(indicator)
        indicator.setMenu(menu)

        def onMenu(action):
            """
            Set navigation style when an option from the menu is selected.
            """
            style = False

            if action.data() != "Undefined":
                style = True
                menu.setDefaultAction(action)
                indicator.setDefaultAction(action)
                paramGet.SetString("NavigationStyle", action.data())
            else:
                pass

            if style:
                undefined.setVisible(False)
            else:
                undefined.setVisible(True)
                undefined.setEnabled(True)
                menu.setDefaultAction(undefined)
                indicator.setDefaultAction(undefined)

        menu.triggered.connect(onMenu)

        for i in navStyleSort:
            if i in navStyle:
                action = QtGui.QAction(menu)
                action.setText(i)
                action.setIcon(navIcon)
                action.setData(navStyle[i])
                action.setObjectName("NavInd_" + i)
                menu.addAction(action)
            else:
                pass

        undefined = QtGui.QAction(menu)
        undefined.setIcon(navIcon)
        undefined.setText("Undefined")
        undefined.setData("Undefined")
        undefined.setObjectName("NavInd_Undefined")
        toolTip = "A navigation style set is not recognized by navigation indicator."
        undefined.setToolTip(toolTip)
        menu.addAction(undefined)

        setDefault()
        statusBar.insertPermanentWidget(0, indicator)
        statusBar.insertPermanentWidget(0, statusBar.children()[2])

    def onMessageChanged():
        """
        Start navigation indicator after activity in status bar is detected.
        """
        statusBar.messageChanged.disconnect(onMessageChanged)
        onStart()

    mw = Gui.getMainWindow()

    # Single instance
    if mw.findChild(QtGui.QToolButton, "NavInd_Button"):
        pass
    else:
        statusBar = mw.statusBar()
        statusBar.messageChanged.connect(onMessageChanged)

navigationIndicator()

# Navigation indicator for FreeCAD
# Copyright (C) 2016, 2017  triplus @ FreeCAD
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

"""Navigation indicator for FreeCAD."""


def navigationIndicator():
    """Navigation indicator."""

    import FreeCAD as App
    import FreeCADGui as Gui
    from PySide import QtGui
    from PySide import QtCore
    import NavigationIndicatorPath

    mw = Gui.getMainWindow()
    statusBar = mw.statusBar()
    timer = NavigationIndicatorPath.timer()
    path = NavigationIndicatorPath.path() + "/Resources/icons/"
    p = App.ParamGet("User parameter:BaseApp/Preferences/View")

    ttUndefined = "Navigation style not recognized."

    ttCAD = str("""
        <p align='center'><b>CAD</b> navigation style</p>
        <table>
            <tr>
                <th>Select</th>
                <th>Zoom</th>
                <th>Rotate</th>
                <th>Rotate</th>
                <th>Pan</th>
            </tr>
            <tr>
                <td><img align='center' src='""" + path + """NavigationCAD_Select.svg'></td>
                <td><img align='center' src='""" + path + """NavigationCAD_Zoom.svg'></td>
                <td><img align='center' src='""" + path + """NavigationCAD_Rotate.svg'></td>
                <td><img align='center' src='""" + path + """NavigationCAD_RotateAlt.svg'></td>
                <td><img align='center' src='""" + path + """NavigationCAD_Pan.svg'></td>
            </tr>
        </table>""")

    style = {
        "OpenInventor": "Gui::InventorNavigationStyle",
        "CAD": "Gui::CADNavigationStyle",
        "Blender": "Gui::BlenderNavigationStyle",
        "MayaGesture": "Gui::MayaGestureNavigationStyle",
        "Touchpad": "Gui::TouchpadNavigationStyle",
        "Gesture": "Gui::GestureNavigationStyle",
        "OpenCascade": "Gui::OpenCascadeNavigationStyle"}

    indicator = QtGui.QToolButton(statusBar)
    indicator.setAutoRaise(True)
    indicator.setObjectName("Indicator_Navigation")
    indicator.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
    indicator.setPopupMode(QtGui.QToolButton
                           .ToolButtonPopupMode
                           .InstantPopup)

    menu = QtGui.QMenu(indicator)
    indicator.setMenu(menu)

    a0 = QtGui.QAction(menu)
    a0.setIcon(QtGui.QIcon(path + "NavigationUndefined.svg"))
    a0.setText("Undefined")
    a0.setData("Undefined")
    a0.setObjectName("Indicator_NavigationUndefined")
    a0.setToolTip(ttUndefined)

    a1 = QtGui.QAction(menu)
    a1.setIcon(QtGui.QIcon(path + "NavigationOpenInventor.svg"))
    a1.setText("OpenInventor")
    a1.setObjectName("Indicator_NavigationOpenInventor")
    a1.setData("Gui::InventorNavigationStyle")

    a2 = QtGui.QAction(menu)
    a2.setIcon(QtGui.QIcon(path + "NavigationCAD.svg"))
    a2.setText("CAD")
    a2.setToolTip(ttCAD)
    a2.setObjectName("Indicator_NavigationCAD")
    a2.setData("Gui::CADNavigationStyle")

    a3 = QtGui.QAction(menu)
    a3.setIcon(QtGui.QIcon(path + "NavigationBlender.svg"))
    a3.setText("Blender")
    a3.setObjectName("Indicator_NavigationBlender")
    a3.setData("Gui::BlenderNavigationStyle")

    a4 = QtGui.QAction(menu)
    a4.setIcon(QtGui.QIcon(path + "NavigationMayaGesture.svg"))
    a4.setText("MayaGesture")
    a4.setObjectName("Indicator_NavigationMayaGesture")
    a4.setData("Gui::MayaGestureNavigationStyle")

    a5 = QtGui.QAction(menu)
    a5.setIcon(QtGui.QIcon(path + "NavigationTouchpad.svg"))
    a5.setText("Touchpad")
    a5.setObjectName("Indicator_NavigationTouchpad")
    a5.setData("Gui::TouchpadNavigationStyle")

    a6 = QtGui.QAction(menu)
    a6.setIcon(QtGui.QIcon(path + "NavigationGesture.svg"))
    a6.setText("Gesture")
    a6.setObjectName("Indicator_NavigationGesture")
    a6.setData("Gui::GestureNavigationStyle")

    a7 = QtGui.QAction(menu)
    a7.setIcon(QtGui.QIcon(path + "NavigationOpenCascade.svg"))
    a7.setText("OpenCascade")
    a7.setObjectName("Indicator_NavigationOpenCascade")
    a7.setData("Gui::OpenCascadeNavigationStyle")

    menu.addAction(a0)
    menu.addAction(a1)
    menu.addAction(a2)
    menu.addAction(a3)
    menu.addAction(a4)
    menu.addAction(a5)
    menu.addAction(a6)
    menu.addAction(a7)

    def onMenu(action):
        """Set navigation style on selection."""

        s = False

        if action.data() != "Undefined":
            s = True
            menu.setDefaultAction(action)
            indicator.setDefaultAction(action)
            p.SetString("NavigationStyle", action.data())
        else:
            pass

        if s:
            a0.setVisible(False)
        else:
            a0.setVisible(True)
            a0.setEnabled(True)
            menu.setDefaultAction(a0)
            indicator.setDefaultAction(a0)

    menu.triggered.connect(onMenu)

    def setCurrent():
        """Set navigation style on start and on interval."""

        s = False
        current = p.GetString("NavigationStyle")

        menu.blockSignals(True)

        if current:
            for i in style:
                if style[i] == current:
                    for a in menu.actions():
                        if a.text() == i:
                            s = True
                            menu.setDefaultAction(a)
                            indicator.setDefaultAction(a)
                        else:
                            pass
                else:
                    pass
        else:
            s = True
            menu.setDefaultAction(a2)
            indicator.setDefaultAction(a2)

        if s:
            a0.setVisible(False)
        else:
            a0.setVisible(True)
            a0.setEnabled(True)
            menu.setDefaultAction(a0)
            indicator.setDefaultAction(a0)

        menu.blockSignals(False)

    statusBar.addPermanentWidget(indicator)
    statusBar.addPermanentWidget(statusBar.children()[2])

    setCurrent()

    timer.timeout.connect(setCurrent)
    timer.start(10000)


navigationIndicator()

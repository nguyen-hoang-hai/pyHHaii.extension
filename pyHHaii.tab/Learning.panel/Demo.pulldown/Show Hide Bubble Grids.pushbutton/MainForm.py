import clr
import System
import string
from rpw.ui.forms import Alert

# Importing necessary references for Revit and Windows Forms
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms.DataVisualization')

import System.Drawing
import System.Windows.Forms
import os
from System.Drawing import Icon  # Import Icon class
import System.Diagnostics  # Open Link when press Button

from System.Drawing import *
from System.Windows.Forms import *

# Adding a reference to the system to use List
clr.AddReference('System')
from System.Collections.Generic import List

"""---------------------------Get active document and view from Revit------------------------"""
doc = __revit__.ActiveUIDocument.Document
view = doc.ActiveView
uidoc = __revit__.ActiveUIDocument
"""-------------------------------------------------------------------------------------------"""


class MainForm(Form):
    def __init__(self):
        self.InitializeComponent()

    def InitializeComponent(self):
        # Get the directory of the running script
        script_dir = os.path.dirname(__file__)
        image_path = os.path.join(script_dir, "Logo.png")
        icon_path = os.path.join(script_dir, "icon.ico")

        # Load custom icon
        self.Icon = Icon(icon_path)

        resources = System.Resources.ResourceManager("Show_Hide_Bubble.MainForm",
                                                     System.Reflection.Assembly.GetExecutingAssembly())

        self._LeftBox = System.Windows.Forms.CheckBox()
        self._Topbox = System.Windows.Forms.CheckBox()
        self._Rigthbox = System.Windows.Forms.CheckBox()
        self._Botbox = System.Windows.Forms.CheckBox()
        self._OKbutton = System.Windows.Forms.Button()
        self._Cancelbutton = System.Windows.Forms.Button()
        self._helplabel = System.Windows.Forms.LinkLabel()
        self._pictureBox1 = System.Windows.Forms.PictureBox()
        self._showbutton = System.Windows.Forms.RadioButton()
        self._hidebutton = System.Windows.Forms.RadioButton()
        self._pictureBox1.BeginInit()
        self.SuspendLayout()

        # LeftBox
        self._LeftBox.Location = System.Drawing.Point(6, 106)
        self._LeftBox.Name = "LeftBox"
        self._LeftBox.Size = System.Drawing.Size(104, 24)
        self._LeftBox.TabIndex = 0
        self._LeftBox.Text = "Left"
        self._LeftBox.UseVisualStyleBackColor = True
        self._LeftBox.CheckedChanged += self.LeftBoxCheckedChanged

        # Topbox
        self._Topbox.Location = System.Drawing.Point(116, 12)
        self._Topbox.Name = "Topbox"
        self._Topbox.Size = System.Drawing.Size(104, 24)
        self._Topbox.TabIndex = 0
        self._Topbox.Text = "Top"
        self._Topbox.UseVisualStyleBackColor = True
        self._Topbox.CheckedChanged += self.TopboxCheckedChanged

        # Rigthbox
        self._Rigthbox.Location = System.Drawing.Point(267, 106)
        self._Rigthbox.Name = "Rigthbox"
        self._Rigthbox.Size = System.Drawing.Size(104, 24)
        self._Rigthbox.TabIndex = 0
        self._Rigthbox.Text = "Right"
        self._Rigthbox.UseVisualStyleBackColor = True
        self._Rigthbox.CheckedChanged += self.RigthboxCheckedChanged

        # Botbox
        self._Botbox.Location = System.Drawing.Point(116, 207)
        self._Botbox.Name = "Botbox"
        self._Botbox.Size = System.Drawing.Size(104, 24)
        self._Botbox.TabIndex = 0
        self._Botbox.Text = "Bottom"
        self._Botbox.UseVisualStyleBackColor = True
        self._Botbox.CheckedChanged += self.BotboxCheckedChanged

        # OKbutton
        self._OKbutton.BackColor = System.Drawing.Color.FromArgb(255, 128, 0)
        self._OKbutton.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                                  System.Drawing.GraphicsUnit.Point, 0)
        self._OKbutton.Location = System.Drawing.Point(332, 96)
        self._OKbutton.Name = "OKbutton"
        self._OKbutton.Size = System.Drawing.Size(85, 34)
        self._OKbutton.TabIndex = 1
        self._OKbutton.Text = "OK"
        self._OKbutton.UseVisualStyleBackColor = False
        self._OKbutton.Click += self.OKbuttonClick

        # Cancelbutton
        self._Cancelbutton.BackColor = System.Drawing.Color.FromArgb(255, 128, 0)
        self._Cancelbutton.DialogResult = System.Windows.Forms.DialogResult.Cancel
        self._Cancelbutton.Font = System.Drawing.Font("Microsoft Sans Serif", 10, System.Drawing.FontStyle.Regular,
                                                      System.Drawing.GraphicsUnit.Point, 0)
        self._Cancelbutton.Location = System.Drawing.Point(332, 173)
        self._Cancelbutton.Name = "Cancelbutton"
        self._Cancelbutton.Size = System.Drawing.Size(85, 34)
        self._Cancelbutton.TabIndex = 1
        self._Cancelbutton.Text = "Cancel"
        self._Cancelbutton.UseVisualStyleBackColor = False
        self._Cancelbutton.Click += self.CancelbuttonClick

        # helplabel
        self._helplabel.Location = System.Drawing.Point(10, 231)
        self._helplabel.Name = "helplabel"
        self._helplabel.Size = System.Drawing.Size(100, 23)
        self._helplabel.TabIndex = 2
        self._helplabel.TabStop = True
        self._helplabel.Text = "Help"
        self._helplabel.TextAlign = System.Drawing.ContentAlignment.MiddleLeft
        self._helplabel.LinkClicked += self.HelplabelLinkClicked

        # pictureBox1
        self._pictureBox1.Image = Image.FromFile(image_path)
        self._pictureBox1.Location = System.Drawing.Point(60, 42)
        self._pictureBox1.Name = "pictureBox1"
        self._pictureBox1.Size = System.Drawing.Size(201, 159)
        self._pictureBox1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
        self._pictureBox1.TabIndex = 3
        self._pictureBox1.TabStop = False
        self._pictureBox1.Click += self.PictureBox1Click

        # showbutton
        self._showbutton.Checked = True
        self._showbutton.Location = System.Drawing.Point(329, 12)
        self._showbutton.Name = "showbutton"
        self._showbutton.Size = System.Drawing.Size(104, 24)
        self._showbutton.TabIndex = 4
        self._showbutton.TabStop = True
        self._showbutton.Text = "SHOW"
        self._showbutton.UseVisualStyleBackColor = True
        self._showbutton.CheckedChanged += self.ShowbuttonCheckedChanged

        # hidebutton
        self._hidebutton.Location = System.Drawing.Point(329, 42)
        self._hidebutton.Name = "hidebutton"
        self._hidebutton.Size = System.Drawing.Size(104, 24)
        self._hidebutton.TabIndex = 5
        self._hidebutton.Text = "HIDE"
        self._hidebutton.UseVisualStyleBackColor = True
        self._hidebutton.CheckedChanged += self.HidebuttonCheckedChanged

        # MainForm
        self.AcceptButton = self._OKbutton
        self.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink
        self.CancelButton = self._Cancelbutton
        self.ClientSize = System.Drawing.Size(445, 263)
        self.Controls.Add(self._hidebutton)
        self.Controls.Add(self._showbutton)
        self.Controls.Add(self._pictureBox1)
        self.Controls.Add(self._helplabel)
        self.Controls.Add(self._Cancelbutton)
        self.Controls.Add(self._OKbutton)
        self.Controls.Add(self._Botbox)
        self.Controls.Add(self._Rigthbox)
        self.Controls.Add(self._Topbox)
        self.Controls.Add(self._LeftBox)
        self.Name = "MainForm"
        self.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
        self.Text = "Show Hide Bubble"
        self._pictureBox1.EndInit()
        self.ResumeLayout(False)
        self.PerformLayout()


    # Event Handlers
    def LeftBoxCheckedChanged(self, sender, e):
        pass


    def TopboxCheckedChanged(self, sender, e):
        pass


    def RigthboxCheckedChanged(self, sender, e):
        pass


    def BotboxCheckedChanged(self, sender, e):
        pass


    def HelplabelLinkClicked(self, sender, e):
        System.Diagnostics.Process.Start("https://www.youtube.com/@paper.engineer")


    def OKbuttonClick(self, sender, e):
        """OK Button"""
        # CheckBox values
        left_box = self._LeftBox.Checked
        right_box = self._Rigthbox.Checked
        top_box = self._Topbox.Checked
        bot_box = self._Botbox.Checked

        hide_checked = self._hidebutton.Checked
        show_checked = self._showbutton.Checked

        if not (left_box or right_box or top_box or bot_box):  # Ensure at least one is checked
            TaskDialog.Show("Warning", "You must select at least one direction.")
            return  # Stop further execution if no box is checked
        else:
            self.DialogResult = System.Windows.Forms.DialogResult.OK
            self.Close()


    def ShowbuttonCheckedChanged(self, sender, e):
        pass


    def HidebuttonCheckedChanged(self, sender, e):
        pass


    def CancelbuttonClick(self, sender, e):
        self.Close()


    def PictureBox1Click(self, sender, e):
        pass

﻿import wx
import configparser
import os
import sys
from functions import *


class Settings:
	def __init__(self):

		AppData = os.getenv("AppData")
		AppData = AppData + "/" + "WikiSearch"

		if not os.path.exists(AppData):
			os.mkdir(AppData)

		filename = "Settingss.ini"
		self.path = AppData + "/" + filename

		self.config = configparser.ConfigParser()

		self.DefaultSettings = {
		"language": "English",
		"activ escape": "False",
		"results number": "20",
		"random articles number": "20",
		"auto update": "True",
		"close message": "True",
		"search language": "English",
		"wepviewer": "0"
				}

	def WriteSettings(self, **NewSettings):

		try:
			self.config.read(self.path, encoding='utf-8')
		except:
			pass

		try:
			self.config.add_section("default")
		except configparser.DuplicateSectionError:
			pass

		for Setting in NewSettings:
			self.config.set("default", Setting, NewSettings[Setting])

		with open(self.path, "w", encoding='utf-8') as config_file:
			self.config.write(config_file)

	def ReadSettings(self):

		try:
			self.config.read(self.path, encoding='utf-8')
		except:
			self.WriteSettings(**self.DefaultSettings)

		CurrentSettings = self.DefaultSettings.copy()

		for Setting in CurrentSettings:
			try:
				CurrentSettings[Setting] = self.config.get("default", Setting)
			except:
				DefaultSetting = {Setting: self.DefaultSettings[Setting]}
				self.WriteSettings(**DefaultSetting)

		return CurrentSettings

#end of class

#Set language for Settings Dialog
_ = SetLanguage(Settings().ReadSettings())

# Create Settings Dialog
class SettingsDialog(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, title=_("Program Settings"), size=(400, 500))
		#make window in center.
		self.Center()
		#make window Minimum size.
		self.Maximize(False)
		self.CurrentSettings = Settings().ReadSettings()

		# Creating panel
		Panel = wx.Panel(self)



		# Creating ComboBox for languages
		wx.StaticText(Panel, -1, _("Choose language:"), pos=(15,120), size=(380, 30))
		self.ProgramLanguage = wx.ComboBox(Panel, -1, choices=['Arabic', 'English', 'Español', 'Français',], pos=(15, 150), size=(120, 40), style=wx.CB_READONLY+wx.CB_SORT)
		self.ProgramLanguage.Value = self.CurrentSettings["language"]

		#creating RadioBox to chews Favorite  view.
		self.viewer = wx.RadioBox(Panel, -1, label=_("Choose your prefered view:"), choices=[_("Normal View"), _("Web View(Not recommended)")], pos=(10 , 20), size=(350,80), style=wx.RB_SINGLE)
		self.viewer.Selection = int(self.CurrentSettings["wepviewer"])

		# Creating SpinCtrl for Results Number
		wx.StaticText(Panel, -1, _("Select the number of results:"), pos=(140,120), size=(380, 30))
		self.NumberResults = wx.SpinCtrl(Panel, -1, "20", min=1, max=100, style=wx.SP_ARROW_KEYS, pos=(160, 150), size=(50, 20))
		self.NumberResults.Value = self.CurrentSettings["results number"]

		# Creating SpinCtrl for random article Number
		wx.StaticText(Panel, -1, _("Select the number of random articles:"), pos=(10,260), size=(380, 30))
		self.random_articles_number = wx.SpinCtrl(Panel, -1, "20", min=1, max=100, style=wx.SP_ARROW_KEYS, pos=(30, 290), size=(50, 20))
		self.random_articles_number.Value = self.CurrentSettings["random articles number"]

		# Creating Check Boxes
		self.VerificationMsg = wx.CheckBox(Panel, -1, label=_("Show Close message when at least an article is open"), pos=(10, 180), size=(380, 30))
		if self.CurrentSettings["close message"] == "True":
			self.VerificationMsg.Value = True

		self.AutoUpdate = wx.CheckBox(Panel, -1, label=_("Check for updates automatically"), pos=(10, 205), size=(380, 30))
		if self.CurrentSettings["auto update"] == "True":
			self.AutoUpdate.Value = True

		self.CloseArticleWithScape = wx.CheckBox(Panel, -1, label=_("Close the article via the Escape key"), pos=(10, 230), size=(380, 30))
		if self.CurrentSettings["activ escape"] == "True":
			self.CloseArticleWithScape.Value = True

		# Create Buttons
		self.SaveSettings = wx.Button(Panel, -1, _("&Save changes"), pos=(10,400), size=(100,30))
		self.SaveSettings.SetDefault()
		self.GoBack = wx.Button(Panel, wx.ID_CANCEL, _("&Cancel"), pos=(120,400), size=(80,30))

		self.hotKeys = wx.AcceleratorTable([
			(wx.ACCEL_ALT, ord("S"), self.SaveSettings.GetId()),
			(wx.ACCEL_CTRL, ord("W"), self.GoBack.GetId()),
		])
		Panel.SetAcceleratorTable(self.hotKeys)

		#event for Save Settings button
		self.SaveSettings.Bind(wx.EVT_BUTTON, self.OnSaveSettings)

		#Show settings dialog
		self.Show()

	#Save Settings function
	def OnSaveSettings(self, event):

		NewSettings = {
		"language": self.ProgramLanguage.Value,
		"results number": str(self.NumberResults.Value),
		"random articles number": str(self.random_articles_number.Value),
		"close message": str(self.VerificationMsg.Value),
		"auto update": str(self.AutoUpdate.Value),
		"activ escape": str(self.CloseArticleWithScape.Value),
		"search language": self.CurrentSettings["search language"],
		"wepviewer": str(self.viewer.Selection)
}

		Settings().WriteSettings(**NewSettings)

		if NewSettings["language"] != self.CurrentSettings["language"]:
			ConfirmRestartProgram = wx.MessageDialog(self, _("""You must restart the program for the new language to take effect.
Do you want to restart the program now?"""), _("Confirm"), style=wx.YES_NO+wx.YES_DEFAULT+wx.ICON_WARNING+wx.ICON_QUESTION)
			ConfirmRestartProgram.SetYesNoLabels(_("&Yes"), _("&No"))
			if ConfirmRestartProgram.ShowModal() == wx.ID_YES:
				os.execv(sys.executable, ['python'] + sys.argv)
			else:
				self.Destroy()

		self.Destroy()

#end of class


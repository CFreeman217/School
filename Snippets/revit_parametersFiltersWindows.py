# import clr
# import sys
# 
# clr.AddReference('RevitAPI')
# from Autodesk.Revit.DB import *
# 
# clr.AddReference('RevitAPIUI')
# clr.AddReference('RevitServices')
# import RevitSerivces
# from RevitSerivces.Persistence import DocumentManager
# from RevitServices.Transactions import TransactionManager
# 
# clr.AddReference('ProtoGeometry')
# from Autodesk.DesignScript.Geometry import *
# 
# doc = DocumentManager.Instance.CurrentDBDocument
# app = DocumentManager.Instance.CurrentUIApplication.Application
# 
# uiapp = DocumentManager.Instance.CurrentUIApplication
# 
# elements = IN[0]
# parameter = IN[1]
# 
# outList = []
# familyType = []
# 
# # Get all of the shared parameters of the elements
# for i in UnwrapElement(elements):
# 	for j in i.Parameters:
# 		if j.IsShared and j.Definition.Name == parameter:
# 			parameterValue = i.get_Parameter(j.GUID)
# 			outList.append(parameterValue.AsString())
# 
# # Get the Element ID of the elements
# for i in UnwrapElement(IN[0]):
# 	id = i.GetTypeId()
# 	if id == ElementId.InvalidElementId:
# 		familyType.append(none)
# 	else:
# 		familyType.append(doc.GetElement(id))
# 
# # Get the bult in parameter Type Mark.
# builtInParamType = BuiltInParameter.All_MODEL_TYPE_MARK
# for i in UnwrapElement(familyType):
# 	typeMark = i.get_Parameter(builtInParamType)
# 	outList.append(typeMark.AsString())
# 	
# OUT = outlist

# # Set the text parameter 'APZ Status' to 'Setting a Parameter'
# for i in UnwrapElement(elements):
# 	p = i.LookupParameter("APZ Status")
# 	TransactionManager.Instance.EnsureInTransaction(doc)
# 	p.Set("Setting a Parameter")
# 	TransactionManager.Instance.TransactionTaskDone()




import clr
clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

import System
from System.Collections.Generic import *

doc = DocumentManager.Instance.CurrentDBDocument

# Get all of the elements of class 'Wall' in the current Document
collector = FilteredElementCollector(doc)
ofClass = collector.OfClass(Wall).ToElements()

# Get the items of class 'Wall' in the ActiveView
ActiveView = FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(Wall).ToElements()
OUT = ofClass

# Get elements of a category OST_Walls
BuiltInCategory = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

# Do a search of elements in the document
wallList = []
for w in BuiltInCategory:
	# Collect all of the walls with family name 'SW48'
	if w.Name.Equals('SW48'):
		wallList.append(w)
OUT = wallList

# Lambda expression version for collecting the same information as above
walls = list(filter(lambda x : x.Name.Equals('SW48'),BuiltInCategory))

builtInCats = List[BuiltInCategory]()
builtInCats.Add(BuiltInCategory.OST_Doors)
builtInCats.Add(BuiltInCategory.OST_Walls)
# Slower filter. Why would you use this?
filter = ElementMultiCategoryFilter(builtInCats)

elements = FilteredElementCollector(doc).WherePasses(filter).ToElements()

OUT = elements



import clr

clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
import System

from System.Windows.Forms import *
from System.Drawing import *

# Create a class form

class CreateWindow(Form):
	
	def __init__(self)
	
		# Create the form
		self.Name = "Create Window"
		self.Text = "Window Text"
		self.Size = Size(500,150)
		self.CenterToScreen()
	
		self.values[]
	
		# Create label for sheet name
		labelSheetName = Label(Text = "Sheet Name")
		LabelSheetName.Parent = self
		labelSheetName = Location = Point(30,20)
	
		# Create label for sheet number
		labelSheetNumber = Label(Text = "Sheet Number")
		labelSheetNumber.Parent = self
		labelSheetNumber.Location = Point(30,50)
	
		# Create Textbox for Sheet Name
		self.textboxSheetName = TextBox()
		self.textboxSheetName.Parent = self
		self.textboxSheetName.Text = "Populated name Text"
		self.textboxSheetName.Location = Point(150,20)
		self.textboxSheetName.Width = 150
	
		# Create Textbox for Sheet Number
		self.textboxSheetNumber = TextBox()
		self.textboxSheetNumber.Parent = self
		self.textboxSheetNumber.Text = "Populated number Text"
		self.textboxSheetNumber.Location = Point(150,50)
		self.textboxSheetNumber.Width = 150
	
		# Create button
		button = Button()
		button.Parent = self
		button.Text = "ButtonText"
		button.Location = Point(400,60)
	
		# Register Event for button
		button.Click += self.ButtonClicked
	
	def ButtonClicked(self, sender, args):
		if sender.Click:
			self.values.append(self.textboxSheetName.Text)
			self.values.append(self.textboxSheetNumber.Text)
			self.Close()
	
if IN [0]:
	form = CreateWindow()
	Application.Run(form)
	
	OUT = form.values
	
	
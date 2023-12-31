import clr

clr.AddReferenceByPartialName('PresentationCore')
clr.AddReferenceByPartialName('AdWindows')
clr.AddReferenceByPartialName("PresentationFramework")
clr.AddReferenceByPartialName('System')
clr.AddReferenceByPartialName('System.Windows.Forms')

from Autodesk.Revit import DB
from Autodesk.Revit import UI
import Autodesk
import Autodesk.Windows as aw

uiapp = __revit__
uidoc = uiapp.ActiveUIDocument
doc = uiapp.ActiveUIDocument.Document

import sys
sys.path.append("C:\Users\dolan.klock\OneDrive - HOK\desktop\OneDrive Sharing\PythonResources\Revit")

from pyrevit import forms
import math
from GetSetParameters import *
from System.Collections.Generic import List
from pyrevit import *
import pyrevit
import Schedules

# CODE BELOW HERE #

__author__ = "Dolan Klock"

# Tooltip
__doc__ = "Used as container file of classes and functions"


class ElementToCopy(forms.TemplateListItem):
    @property
    def name(self):
        return GetParameter.get_type_name(self)


class GetElementsFromDoc(object):

    @staticmethod
    def all_sheets(document):
        """

        :param document (Document) revit document to retrieve elements from
        :param elements_only (bool) if false, the method will get and return all view types. If True, method
        will get and return all views in document
        :returns
        """
        all_elements = DB.FilteredElementCollector(document).OfCategory(DB.BuiltInCategory.OST_Sheets).WhereElementIsNotElementType()
        return all_elements
       

    @staticmethod
    def all_views(document, elements_only=False):
        """

        :param document (Document) revit document to retrieve elements from
        :param elements_only (bool) if false, the method will get and return all view types. If True, method
        will get and return all views in document
        :returns (FilteredElementCollector)
        """
        all_types = DB.FilteredElementCollector(document).OfClass(DB.ViewFamilyType)
        if elements_only:
            all_elements = DB.FilteredElementCollector(document).OfCategory(DB.BuiltInCategory.OST_Views). \
                WhereElementIsNotElementType()
            return all_elements
        return all_types

    @staticmethod
    def all_floors(document, elements_only=False):
        """

        :param document (Document) revit document to retrieve elements from
        :param elements_only (bool) if false, the method will get and return all view types. If True, method
        will get and return all views in document
        :returns
        """
        all_types = DB.FilteredElementCollector(document).OfClass(DB.Floors)
        if elements_only:
            all_elements = DB.FilteredElementCollector(document).OfCategory(DB.BuiltInCategory.OST_Floors). \
                WhereElementIsNotElementType()
            return all_elements
        return all_types

    @staticmethod
    def all_walls(document, elements_only=False):
        """

        :param document (Document) revit document to retrieve elements from
        :param elements_only (bool) if false, the method will get and return all view types. If True, method
        will get and return all views in document
        :returns
        """
        all_types = DB.FilteredElementCollector(document).OfClass(DB.Walls)
        if elements_only:
            all_elements = DB.FilteredElementCollector(document).OfCategory(DB.BuiltInCategory.OST_Walls). \
                WhereElementIsNotElementType()
            return all_elements
        return all_types


    @staticmethod
    def all_dimensions(document, elements_only=False):
        all_types = DB.FilteredElementCollector(document).OfClass(DB.DimensionType)
        # if elements_only:
        #     all_elements = DB.FilteredElementCollector(document).OfCategory(DB.BuiltInCategory.OST_Dimensions).\
        #         WhereElementIsNotElementType()
        #     return all_elements
        return all_types

    @staticmethod
    def all_text(document, elements_only=False):
        """

        :param document (Document) revit document to retrieve elements from
        :param elements_only (bool) if false, the method will get and return all view types. If True, method
        will get and return all views in document
        :returns
        """
        all_types = DB.FilteredElementCollector(document).OfClass(DB.TextNoteType)
        if elements_only:
            all_elements = DB.FilteredElementCollector(document).OfCategory(DB.BuiltInCategory.OST_TextNotes). \
                WhereElementIsNotElementType()
            return all_elements
        return all_types

    @staticmethod
    def all_rooms_placed(document):
        all_rooms_collector = DB.FilteredElementCollector(document).OfCategory(DB.BuiltInCategory.OST_Rooms).WhereElementIsNotElementType()
        all_rooms_placed = [room for room in all_rooms_collector if room.LookupParameter("Area").AsDouble() > 0]
        return all_rooms_placed


class UITaskDialog:

    @staticmethod
    def task_dialog_two_options(title="", option_one_name="", option_two_name=""):
        td = Autodesk.Revit.UI.TaskDialog(title)
        td.CommonButtons = Autodesk.Revit.UI.TaskDialogCommonButtons.Ok
        td.AddCommandLink(Autodesk.Revit.UI.TaskDialogCommandLinkId.CommandLink1, option_one_name)
        td.AddCommandLink(Autodesk.Revit.UI.TaskDialogCommandLinkId.CommandLink2, option_two_name)
        result = td.Show()
        return result


def get_link_doc():
    """
    This function generates a UI of all of the linked models in the host model and returns selected linked model
    """
    revit_links = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_RvtLinks).ToElements()
    if len(revit_links) == 0:
        forms.alert("There are no linked Revit models inside this model")
        sys.exit()
    rvt_link_instances = [rvt_link for rvt_link in revit_links if isinstance(rvt_link, DB.RevitLinkInstance)]
    input_rvt_link_instance = forms.SelectFromList.show(rvt_link_instances, multiselect=False, name_attr="Name")
    link_doc = input_rvt_link_instance.GetLinkDocument()
    return link_doc


def pick_category(doc):
    """
    Lists all categories from document and prompts for user to select one from list
    :param doc: (Document) the document you want to get categories from
    :return (Category) returns the chosen category
    """
    all_categories = doc.Settings.Categories
    input_category = forms.SelectFromList.show(all_categories, multiselect=False, name_attr="Name")
    return input_category


def pick_element_type(doc, category):
    """

    """
    built_in_category = category.BuiltInCategory
    filter_element_collector = DB.FilteredElementCollector(doc).OfCategory(built_in_category).WhereElementIsElementType()
    # all_types = [e for e in filter_element_collector]
    all_types_names = [ElementToCopy(e_type) for e_type in filter_element_collector]
    input_element_type = forms.SelectFromList.show(all_types_names, multiselect=True)
    return input_element_type


def pick_element_type_of_class(types):
    """

    """
    all_types_names = [ElementToCopy(e_type) for e_type in types]
    input_element_type = forms.SelectFromList.show(all_types_names, multiselect=True)
    return input_element_type


def copy_from_doc(items_to_copy, from_doc, to_doc):
    """

    """
    types_copy_collection = List[DB.ElementId]()
    for type in items_to_copy:
        types_copy_collection.Add(type.Id)
    with pyrevit.revit.Transaction("Copy elements from document"):
        DB.ElementTransformUtils.CopyElements(from_doc,
                                              types_copy_collection,
                                              to_doc,
                                              None,
                                              DB.CopyPasteOptions()
                                              )

def get_titleblocks_from_sheet(sheet, doc):
    "Thanks to Erik Frits for this function ! https://www.learnrevitapi.com/blog/get-titleblock-from-sheet-views/"
    # type:(ViewSheet, Document) -> list
    """Function to get TitleBlocks from the given ViewSheet.
    :param sheet: ViewSheet that has TitleBlock
    :param doc:   Document instance of the Project
    :return:      list of TitleBlocks that are placed on the given Sheet."""

    # RULE ARGUMENTS
    rule_value         = sheet.SheetNumber
    param_sheet_number = DB.ElementId(DB.BuiltInParameter.SHEET_NUMBER)
    f_pvp              = DB.ParameterValueProvider(param_sheet_number)
    evaluator          = DB.FilterStringEquals()
    # CREATE A RULE (Method has changed in Revit API in 2022)
    f_rule = DB.FilterStringRule(f_pvp, evaluator, rule_value)
    # CREATE A FILTER
    tb_filter = DB.ElementParameterFilter(f_rule)
    # GET TITLEBLOCKS
    tb = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_TitleBlocks) \
        .WhereElementIsNotElementType().WherePasses(tb_filter).ToElements()
    return list(tb)
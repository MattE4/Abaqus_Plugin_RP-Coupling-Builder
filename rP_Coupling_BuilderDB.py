from abaqusConstants import *
from abaqusGui import *
from kernelAccess import mdb, session
import os

thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)


###########################################################################
# Class definition
###########################################################################

class RP_Coupling_BuilderDB(AFXDataDialog):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form):

        # Construct the base class.
        #

        AFXDataDialog.__init__(self, form, 'Create RP + Coupling',
            self.OK|self.APPLY|self.CANCEL, DIALOG_ACTIONS_SEPARATOR)
            

        okBtn = self.getActionButton(self.ID_CLICKED_OK)
        okBtn.setText('OK')
            

        applyBtn = self.getActionButton(self.ID_CLICKED_APPLY)
        applyBtn.setText('Apply')
            
        AFXTextField(p=self, ncols=27, labelText='Name prefix: ', tgt=form.kw_nameKw, sel=0)
        GroupBox_1 = FXGroupBox(p=self, text='Reference Point', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        pickHf = FXHorizontalFrame(p=GroupBox_1, opts=0, x=0, y=0, w=0, h=0,
            pl=0, pr=0, pt=0, pb=0, hs=DEFAULT_SPACING, vs=DEFAULT_SPACING)
        # Note: Set the selector to indicate that this widget should not be
        #       colored differently from its parent when the 'Color layout managers'
        #       button is checked in the RSG Dialog Builder dialog.
        pickHf.setSelector(99)
        label = FXLabel(p=pickHf, text='Select faces: ' + ' (None)', ic=None, opts=LAYOUT_CENTER_Y|JUSTIFY_LEFT)
        pickHandler = RP_Coupling_BuilderDBPickHandler(form, form.kw_facesKw, 'Select faces: ', FACES, MANY, label)
        icon = afxGetIcon('select', AFX_ICON_SMALL )
        FXButton(p=pickHf, text='\tPick Items in Viewport', ic=icon, tgt=pickHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=2, pr=2, pt=1, pb=1)
        FXCheckButton(p=GroupBox_1, text='Create set with Reference Point', tgt=form.kw_set_pointKw, sel=0)
        FXCheckButton(p=GroupBox_1, text='Create surface with selected faces', tgt=form.kw_set_couplingKw, sel=0)
        GroupBox_2 = FXGroupBox(p=self, text='Coupling', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        FXCheckButton(p=GroupBox_2, text='Create Coupling', tgt=form.kw_couplingKw, sel=0)
        ComboBox_1 = AFXComboBox(p=GroupBox_2, ncols=0, nvis=1, text='Coupling type:', tgt=form.kw_coupling_typeKw, sel=0)
        ComboBox_1.setMaxVisible(10)
        ComboBox_1.appendItem(text='Distributing')
        ComboBox_1.appendItem(text='Kinematic')
        GroupBox_4 = FXGroupBox(p=self, text='Enforce specific RP coordinates', opts=FRAME_GROOVE|LAYOUT_FILL_X)
        FXCheckButton(p=GroupBox_4, text='X-coordinate', tgt=form.kw_xKw, sel=0)
        AFXTextField(p=GroupBox_4, ncols=15, labelText='X-value: ', tgt=form.kw_x_valueKw, sel=0)
        FXCheckButton(p=GroupBox_4, text='Y-coordinate', tgt=form.kw_yKw, sel=0)
        AFXTextField(p=GroupBox_4, ncols=15, labelText='Y-value: ', tgt=form.kw_y_valueKw, sel=0)
        FXCheckButton(p=GroupBox_4, text='Z-coordinate', tgt=form.kw_zKw, sel=0)
        AFXTextField(p=GroupBox_4, ncols=15, labelText='Z-value: ', tgt=form.kw_z_valueKw, sel=0)
        l = FXLabel(p=GroupBox_4, text='Note: You can also change coords via Tree', opts=JUSTIFY_LEFT)


###########################################################################
# Class definition
###########################################################################

class RP_Coupling_BuilderDBPickHandler(AFXProcedure):

        count = 0

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def __init__(self, form, keyword, prompt, entitiesToPick, numberToPick, label):

                self.form = form
                self.keyword = keyword
                self.prompt = prompt
                self.entitiesToPick = entitiesToPick # Enum value
                self.numberToPick = numberToPick # Enum value
                self.label = label
                self.labelText = label.getText()

                AFXProcedure.__init__(self, form.getOwner())

                RP_Coupling_BuilderDBPickHandler.count += 1
                self.setModeName('RP_Coupling_BuilderDBPickHandler%d' % (RP_Coupling_BuilderDBPickHandler.count) )

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def getFirstStep(self):

                return  AFXPickStep(self, self.keyword, self.prompt, 
                    self.entitiesToPick, self.numberToPick, sequenceStyle=TUPLE)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def getNextStep(self, previousStep):

                self.label.setText( self.labelText.replace('None', 'Picked') )
                return None

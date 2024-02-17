from abaqusGui import *
from abaqusConstants import ALL
import osutils, os


###########################################################################
# Class definition
###########################################################################

class RP_Coupling_Builder_plugin(AFXForm):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, owner):
        
        # Construct the base class.
        #
        AFXForm.__init__(self, owner)
        self.radioButtonGroups = {}

        self.cmd = AFXGuiCommand(mode=self, method='P_C_function',
            objectName='rP_Coupling_Builder_kernel', registerQuery=False)
        pickedDefault = ''
        self.kw_nameKw = AFXStringKeyword(self.cmd, 'kw_name', True, 'Coupling-')
        self.kw_facesKw = AFXObjectKeyword(self.cmd, 'kw_faces', TRUE, pickedDefault)
        self.kw_set_pointKw = AFXBoolKeyword(self.cmd, 'kw_set_point', AFXBoolKeyword.TRUE_FALSE, True, False)
        self.kw_set_couplingKw = AFXBoolKeyword(self.cmd, 'kw_set_coupling', AFXBoolKeyword.TRUE_FALSE, True, False)
        self.kw_couplingKw = AFXBoolKeyword(self.cmd, 'kw_coupling', AFXBoolKeyword.TRUE_FALSE, True, True)
        self.kw_coupling_typeKw = AFXStringKeyword(self.cmd, 'kw_coupling_type', True, 'Distributing')
        self.kw_xKw = AFXBoolKeyword(self.cmd, 'kw_x', AFXBoolKeyword.TRUE_FALSE, True, False)
        self.kw_x_valueKw = AFXFloatKeyword(self.cmd, 'kw_x_value', True, 0)
        self.kw_yKw = AFXBoolKeyword(self.cmd, 'kw_y', AFXBoolKeyword.TRUE_FALSE, True, False)
        self.kw_y_valueKw = AFXFloatKeyword(self.cmd, 'kw_y_value', True, 0)
        self.kw_zKw = AFXBoolKeyword(self.cmd, 'kw_z', AFXBoolKeyword.TRUE_FALSE, True, False)
        self.kw_z_valueKw = AFXFloatKeyword(self.cmd, 'kw_z_value', True, 0)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        import rP_Coupling_BuilderDB
        return rP_Coupling_BuilderDB.RP_Coupling_BuilderDB(self)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def doCustomChecks(self):

        # Try to set the appropriate radio button on. If the user did
        # not specify any buttons to be on, do nothing.
        #
        for kw1,kw2,d in self.radioButtonGroups.values():
            try:
                value = d[ kw1.getValue() ]
                kw2.setValue(value)
            except:
                pass
        return True

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def okToCancel(self):

        # No need to close the dialog when a file operation (such
        # as New or Open) or model change is executed.
        #
        return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Register the plug-in
#
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='Tools ME|RP + Coupling', 
    object=RP_Coupling_Builder_plugin(toolset),
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    kernelInitString='import rP_Coupling_Builder_kernel',
    applicableModules=['Assembly','Step','Interaction', 'Load'],
    version='1.0',
    author='Matthias Ernst, Dassault Systemes Germany',
    description='Plugin to create RP in center of selected face(s) and optionally a coupling. '\
                'Supported in A/CAE 2016 or higher. Selection of geometric surfaces is required. '\
                'Always confirm selection with DONE button or middle mouse button before pressing Apply or OK.'\
                '\n\nThis is not an official Dassault Systemes product.',
    helpUrl='N/A'
)

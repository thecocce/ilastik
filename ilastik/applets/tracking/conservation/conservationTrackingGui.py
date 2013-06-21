from PyQt4 import uic, QtGui
import os
import logging
import sys
import traceback
from ilastik.applets.tracking.base.trackingBaseGui import TrackingBaseGui

logger = logging.getLogger(__name__)
traceLogger = logging.getLogger('TRACE.' + __name__)

class ConservationTrackingGui( TrackingBaseGui ):     
    
    withMergers = True
    
    def _setMergerLegend(self, labels, selection):   
        for i in range(1,len(labels)+1):
            if i <= selection:
                labels[i-1].setVisible(True)
            else:
                labels[i-1].setVisible(False)
    
    def _loadUiFile(self):
        # Load the ui file (find it in our own directory)
        localDir = os.path.split(__file__)[0]
        self._drawer = uic.loadUi(localDir+"/drawer.ui")
        
        parameters = self.topLevelOperatorView.Parameters.value        
        if 'maxDist' in parameters.keys():
            self._drawer.maxDistBox.setValue(parameters['maxDist'])
        if 'maxObj' in parameters.keys():
            self._drawer.maxObjectsBox.setValue(parameters['maxObj'])
        if 'divThreshold' in parameters.keys():
            self._drawer.divThreshBox.setValue(parameters['divThreshold'])
        if 'avgSize' in parameters.keys():
            self._drawer.avgSizeBox.setValue(parameters['avgSize'][0])
        if 'withTracklets' in parameters.keys():
            self._drawer.trackletsBox.setChecked(parameters['withTracklets'])
        if 'sizeDependent' in parameters.keys():
            self._drawer.sizeDepBox.setChecked(parameters['sizeDependent'])
        if 'divWeight' in parameters.keys():
            self._drawer.divWeightBox.setValue(parameters['divWeight'])
        if 'transWeight' in parameters.keys():
            self._drawer.transWeightBox.setValue(parameters['transWeight'])
        if 'withDivisions' in parameters.keys():
            self._drawer.divisionsBox.setChecked(parameters['withDivisions'])
        if 'withOpticalCorrection' in parameters.keys():
            self._drawer.opticalBox.setChecked(parameters['withOpticalCorrection'])
        if 'withClassifierPrior' in parameters.keys():
            self._drawer.classifierPriorBox.setChecked(parameters['withClassifierPrior'])
        if 'withMergerResolution' in parameters.keys():
            self._drawer.mergerResolutionBox.setChecked(parameters['withMergerResolution'])
        if 'borderAwareWidth' in parameters.keys():
            self._drawer.bordWidthBox.setValue(parameters['borderAwareWidth'])
#        if 'cplex_timeout' in parameters.keys():
#            self._drawer.timeoutBox.setText(parameters['cplex_timeout']          
        
        return self._drawer

    def initAppletDrawerUi(self):
        super(ConservationTrackingGui, self).initAppletDrawerUi()        
        
        self.mergerLabels = [self._drawer.merg1,
                             self._drawer.merg2,
                             self._drawer.merg3,
                             self._drawer.merg4,
                             self._drawer.merg5,
                             self._drawer.merg6,
                             self._drawer.merg7]
        for i in range(len(self.mergerLabels)):
            self._labelSetStyleSheet(self.mergerLabels[i], self.mergerColors[i+1])
        
        self._onMaxObjectsBoxChanged()
        self._drawer.maxObjectsBox.valueChanged.connect(self._onMaxObjectsBoxChanged)                

    def _onMaxObjectsBoxChanged(self):
        self._setMergerLegend(self.mergerLabels, self._drawer.maxObjectsBox.value())
        
    def _onTrackButtonPressed( self ):        
        maxDist = self._drawer.maxDistBox.value()
        maxObj = self._drawer.maxObjectsBox.value()        
        divThreshold = self._drawer.divThreshBox.value()
        
        from_t = self._drawer.from_time.value()
        to_t = self._drawer.to_time.value()
        from_x = self._drawer.from_x.value()
        to_x = self._drawer.to_x.value()
        from_y = self._drawer.from_y.value()
        to_y = self._drawer.to_y.value()        
        from_z = self._drawer.from_z.value()
        to_z = self._drawer.to_z.value()        
        from_size = self._drawer.from_size.value()
        to_size = self._drawer.to_size.value()        
        
        self.time_range =  range(from_t, to_t + 1)
        avgSize = [self._drawer.avgSizeBox.value()]
                
        withTracklets = self._drawer.trackletsBox.isChecked()
        sizeDependent = self._drawer.sizeDepBox.isChecked()
        hardPrior = self._drawer.hardPriorBox.isChecked()
        classifierPrior = self._drawer.classifierPriorBox.isChecked()
        divWeight = self._drawer.divWeightBox.value()
        transWeight = self._drawer.transWeightBox.value()
        withDivisions = self._drawer.divisionsBox.isChecked()        
        withOpticalCorrection = self._drawer.opticalBox.isChecked()
        withMergerResolution = self._drawer.mergerResolutionBox.isChecked()
        borderAwareWidth = self._drawer.bordWidthBox.value()

        ndim=3
        if (to_z - from_z == 0):
            ndim=2
        
        try:
            self.mainOperator.track(
                time_range = self.time_range,
                x_range = (from_x, to_x + 1),
                y_range = (from_y, to_y + 1),
                z_range = (from_z, to_z + 1),
                size_range = (from_size, to_size + 1),
                x_scale = self._drawer.x_scale.value(),
                y_scale = self._drawer.y_scale.value(),
                z_scale = self._drawer.z_scale.value(),
                maxDist=maxDist,         
                maxObj = maxObj,               
                divThreshold=divThreshold,
                avgSize=avgSize,                
                withTracklets=withTracklets,
                sizeDependent=sizeDependent,
                divWeight=divWeight,
                transWeight=transWeight,
                withDivisions=withDivisions,
                withOpticalCorrection=withOpticalCorrection,
                withClassifierPrior=classifierPrior,
                ndim=ndim,
                withMergerResolution=withMergerResolution,
                borderAwareWidth = borderAwareWidth
                )
        except Exception:            
            ex_type, ex, tb = sys.exc_info()
            traceback.print_tb(tb)            
            QtGui.QMessageBox.critical(self, "Error", "Exception(" + str(ex_type) + "): " + str(ex), QtGui.QMessageBox.Ok)
            return                     
        
        self._drawer.exportButton.setEnabled(True)
        self._drawer.exportTifButton.setEnabled(True)
#        self._drawer.lineageTreeButton.setEnabled(True)
        
        self._setLayerVisible("Objects", False)
            
            

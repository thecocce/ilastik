from PyQt4.QtGui import QColor, QPixmap, QIcon, QItemSelectionModel
from PyQt4.QtCore import QAbstractTableModel, Qt, QModelIndex, pyqtSignal

class Label:
    def __init__(self, name, color):
        self.name = name
        self.color = color
    def __repr__(self):
        return "<Label name=%s, color=%r>" % (self.name, self.color)

class LabelListModel(QAbstractTableModel):
    orderChanged = pyqtSignal()
    labelSelected = pyqtSignal(int)
    
    def __init__(self, labels = [], parent = None):
        QAbstractTableModel.__init__(self, parent)
        self._labels = labels
        self._selectionModel = QItemSelectionModel(self)
        
        def onSelectionChanged(selected, deselected):
            self.labelSelected.emit(selected[0].indexes()[0].row())
        self._selectionModel.selectionChanged.connect(onSelectionChanged)
    
    def __len__(self):
        return len(self._labels)
    
    def __getitem__(self, i):
        return self._labels[i]
     
    def selectedRow(self):
        selected = self._selectionModel.selectedRows()
        if len(selected) == 1:
            return selected[0].row()
        return -1
    
    def selectedIndex(self):
        row = self.selectedRow()
        if row >= 0:
            return self.index(self.selectedRow())
        else:
            return QModelIndex()
            
    def rowCount(self, parent=None):
        return len(self._labels)
    
    def columnCount(self, parent):
        return 3

    def data(self, index, role):
        if role == Qt.EditRole and index.column() == 0:
            return self._labels[index.row()].color
        if role == Qt.EditRole and index.column() == 1:
            return self._labels[index.row()].name
        
        if role == Qt.ToolTipRole and index.column() == 0:
            return "Hex code : " + self._labels[index.row()].color.name() + "\n DoubleClick to change"
        if role == Qt.ToolTipRole and index.column() == 1:
            return self._labels[index.row()].name + "\n DoubleClick to rename"
        if role == Qt.ToolTipRole and index.column() == 2:
            return "Delete " + self._labels[index.row()].name
        
        if role == Qt.DecorationRole and index.column() == 0:
            row = index.row()
            value = self._labels[row]
            pixmap = QPixmap(26, 26)
            pixmap.fill(value.color)
            icon = QIcon(pixmap)
            return icon
        
        if role == Qt.DisplayRole and index.column() == 1:
            row = index.row()
            value = self._labels[row]
            return value.name

    def flags(self, index):
        if  index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        elif  index.column() == 1:
            return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        elif  index.column() == 2:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        
    def setData(self, index, value, role = Qt.EditRole):
        if role == Qt.EditRole  and index.column() == 0:
            row = index.row()
            color = QColor(value)
            if color.isValid():
                self._labels[row].color = color
                self.dataChanged.emit(index, index)
                return True
            
        if role == Qt.EditRole  and index.column() == 1:
            row = index.row()
            name = value
            self._labels[row].name = name
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRow(self, position, object, parent = QModelIndex()):
        self.beginInsertRows(parent, position, position)
        self._labels.insert(position, object)
        self.endInsertRows()
        return True

    def removeRow(self, position, parent = QModelIndex()):
        self.beginRemoveRows(parent, position, position)
        value = self._labels[position]
        print "removing row: ", value
        self._labels.remove(value)     
        self.endRemoveRows()
        return True
    
    
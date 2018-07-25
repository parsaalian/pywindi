import PyIndi
from windi import *

INDI_TYPES = ['number', 'switch', 'text', 'light', 'blob']

class DeviceHandler:
    _context = None
    _device = None
    def __init__(self, context, device, **kwargs):
        self._context = context
        self._device = device
        self.setProperty('CONNECTION', [True, False])


    def wait_for_property(self, propertyName):
        self._context.wait_for_property(self._device.getDeviceName(), propertyName)


    # Change the given property of device.
    #
    # @param propertyName {String} - the name of the property to change. -> e.g. "CONNECTION" or "connection" (case insensitive)
    # @param newSubProperties {Dictionary} - a dictionary that changing values are values of it. key can be index or name of sub-property. You can only change sub-properties that you need.
    # e.g. setProperty('connection', {0: True, 'disconect': False}) - change the connection of device.
    def setProperty(self, propertyName, newSubProperties):
        self.wait_for_property(propertyName)
        try:
            getattr(self, '_set' + INDI_TYPES[self._device.getProperty(propertyName).getType()].title())(propertyName, newSubProperties)
        except Exception as e:
            print(e)


    # Get the value of the given property.
    #
    # @param propertName {String} - the name of the property to get. -> e.g. "CONNECTION" or "connection" (case insensitive)
    # @param subProperty {Boolean} - True is sub-property of property is wanted.
    # @param index {Number|String} - index or name of sub-property.
    # @param object {Boolean} - True if object of sub-property is wanted, not content of it.
    def getProperty(self, propertyName, subProperty=False, index=None, object=False):
        self.wait_for_property(propertyName)
        try:
            return getattr(self, '_get' + INDI_TYPES[self._device.getProperty(propertyName).getType()].title())(propertyName, subProperty, index, object)
        except Exception as e:
            print(e)



    #######################################################
    ######################  setters  ######################
    #######################################################
    # Set values for switch properties.
    #
    # @param propertyName {String} - name of property to change, which is a switch.
    # @param newSubs {List} - new values for properties.
    def _setSwitch(self, propertyName, newSubs):
        switch = self._device.getSwitch(propertyName)
        for i in range(len(newSubs)):
            if newSubs[i] is not None:
                switch[i].s = PyIndi.ISS_ON if newSubs[i] == True else PyIndi.ISS_OFF
        self._context.sendNewSwitch(switch)


    # Set values for text properties.
    #
    # @param propertyName {String} - name of property to change, which is a text.
    # @param newSubs {List} - new values for properties.
    def _setText(self, propertyName, newSubs):
        text = self._device.getText(propertyName)
        for i in range(len(newSubs)):
            if newSubs[i] is not None:
                text[i].text = newSubs[i]
        self._context.sendNewText(text)


    # Set values for number properties.
    #
    # @param propertyName {String} - name of property to change, which is a switch.
    # @param newSubs {List} - new values for properties.
    def _setNumber(self, propertyName, newSubs):
        number = self._device.getNumber(propertyName)
        for i in range(len(newSubs)):
            if newSubs[i] is not None:
                number[i].value = newSubs[i]
        self._context.sendNewNumber(number)


    ###########################################################################

    #######################################################
    ######################  getters  ######################
    #######################################################
    # Get the value of switch propeties.
    #
    # @param propertyName {String} - name of property to get, which is a switch.
    # @param subProperty {Boolean} - True is sub-property of property is wanted.
    # @param index {Number|String} - index or name of sub-property.
    # @param object {Boolean} - True if object of sub-property is wanted, not content of it.
    def _getSwitch(self, propertyName, subProperty=False, index=None, object=False):
        if not subProperty:
            return self._device.getSwitch(propertyName)
        index = index if isinstance(index, int) else self._getIndexInProperty(device, propertyName, index)
        if object:
            return self._device.getSwitch(propertyName)[index]
        return self._device.getSwitch(propertyName)[index].s == PyIndi.ISS_ON


    # Get the value of text propeties.
    #
    # @param propertyName {String} - name of property to get, which is a text.
    # @param subProperty {Boolean} - True is sub-property of property is wanted.
    # @param index {Number|String} - index or name of sub-property.
    # @param object {Boolean} - True if object of sub-property is wanted, not content of it.
    def _getText(self, propertyName, subProperty=False, index=None, object=False):
        if not subProperty:
            return self._device.getText(propertyName)
        index = index if isinstance(index, int) else self._getIndexInProperty(device, propertyName, index)
        if object:
            return self._device.getText(propertyName)[index]
        return self._device.getText(propertyName)[index].text


    # Get the value of number propeties.
    #
    # @param propertyName {String} - name of property to get, which is a number.
    # @param subProperty {Boolean} - True is sub-property of property is wanted.
    # @param index {Number|String} - index or name of sub-property.
    # @param object {Boolean} - True if object of sub-property is wanted, not content of it.
    def _getNumber(self, propertyName, subProperty=False, index=None, object=False):
        if not subProperty:
            return self._device.getNumber(propertyName)
        index = index if isinstance(index, int) else self._getIndexInProperty(device, propertyName, index)
        if object:
            return self._device.getNumber(propertyName)[index]
        return self._device.getNumber(propertyName)[index].value


    # Get the value of blob propeties.
    #
    # @param propertyName {String} - name of property to get, which is a blob.
    # @param subProperty {Boolean} - True is sub-property of property is wanted.
    # @param index {Number|String} - index or name of sub-property.
    # @param object {Boolean} - True if object of sub-property is wanted, not content of it.
    def _getBlob(self, propertyName, subProperty=False, index=None, object=False):
        if not subProperty:
            return self._device.getBLOB(propertyName)
        index = index if isinstance(index, int) else self._getIndexInProperty(device, propertyName, index)
        if object:
            return self._device.getBLOB(propertyName)[index]
        return self._device.getBLOB(propertyName)[index]

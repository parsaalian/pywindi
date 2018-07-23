import PyIndi
# Agent class controls the properties of a device (or none).
#
class Agent:
    _client = None
    _device = None
    _properties = {}
    _names = {}
    def __init__(self, client=None):
        self._client = client
        self._device = client.device
        try:
            self._setPropertyList(device)
        except Exception:
            pass


    def setClient(self, client):
        self._client = client

    def getClient(self):
        return self._client


    # Create a dictionary of properties, property types and sub-propeties.
    #
    # @param device {PyIndi.Device} - device to create properties for.
    def _setPropertyList(self, device=None):
        for property in device.getProperties():
            type = property.getType()
            type = "Text" if type == PyIndi.INDI_TEXT else \
                ("Number" if type == PyIndi.INDI_NUMBER else \
                ("Switch" if type == PyIndi.INDI_SWITCH else \
                ("BLOB" if type == PyIndi.INDI_BLOB else "Light")))
            list = [type]
            subProperties = eval('property.get' + type + '()')
            for sub in subProperties:
                list.append(sub.name.upper().replace(' ', '_'))
            self._properties[property.getName().upper().replace(' ', '_')] = list
            self._names[property.getName().upper().replace(' ', '_')] = property.getName()


    # Returns index of a sub-property in property.
    #
    # @param propertyName {String} - the name of property to find sub-property in.
    # @param subPropertyName {String} - the name of sub-property to find index of.
    def _getIndexInProperty(self, propertyName, subPropertyName):
        return self._properties[propertyName.upper().replace(' ', '_')].index(subPropertyName.upper().replace(' ', '_')) - 1


    # Returns type of property.
    #
    # @param propertyName {String} - the name of property to find type of.
    def _getPropertyType(self, propertyName):
        return self._properties[propertyName.upper().replace(' ', '_')][0]


    # Returns the real name of property in IndiClient.
    #
    # @param propertyName {String} - the name of property to find the real name of.
    def _getRealPropertyName(self, propertyName):
        return self._names[propertyName.upper().replace(' ', '_')]


    def getProperties(self):
        return self._properties

    ############################################ Before connection ##########################################

    # TODO: Changing properties before connecting to the device, such as port and ...

    ############################################ After connection ###########################################
    # Change the given property of device.
    #
    # @param propertyName {String} - the name of the property to change. -> e.g. "CONNECTION" or "connection" (case insensitive)
    # @param newSubProperties {Dictionary} - a dictionary that changing values are values of it. key can be index or name of sub-property. You can only change sub-properties that you need.
    # e.g. setProperty('connection', {0: True, 'disconect': False}) - change the connection of device.
    def setProperty(self, propertyName, newSubProperties):
        newSubs = [None for i in range(len(self._properties[propertyName.upper().replace(' ', '_')]) - 1)]
        for i in newSubProperties:
            if isinstance(i, int):
                newSubs[i] = newSubProperties[i]
            else:
                newSubs[self._getIndexInProperty(propertyName, i)] = newSubProperties[i]
        print(newSubs)
        try:
            eval('self._set' + self._getPropertyType(propertyName).lower().title() + '(self._getRealPropertyName(propertyName), newSubs)')
        except NameError:
            print('Unavailable type of property.')


    # Get the value of the given property.
    #
    # @param propertName {String} - the name of the property to get. -> e.g. "CONNECTION" or "connection" (case insensitive)
    # @param subProperty {Boolean} - True is sub-property of property is wanted.
    # @param index {Number|String} - index or name of sub-property.
    # @param object {Boolean} - True if object of sub-property is wanted, not content of it.
    def getProperty(self, propertyName, subProperty=False, index=None, object=False):
        try:
            return eval('self._get' + self._getPropertyType(propertyName).lower().title() + '(self._getRealPropertyName(propertyName), subProperty, index, object)')
        except NameError:
            print('Unavailable type of property.')


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
        self._client.sendNewSwitch(switch)


    # Set values for text properties.
    #
    # @param propertyName {String} - name of property to change, which is a text.
    # @param newSubs {List} - new values for properties.
    def _setText(self, propertyName, newSubs):
        text = self._device.getText(propertyName)
        for i in range(len(newSubs)):
            if newSubs[i] is not None:
                text[i].text = newSubs[i]
        self._client.sendNewText(text)


    # Set values for number properties.
    #
    # @param propertyName {String} - name of property to change, which is a switch.
    # @param newSubs {List} - new values for properties.
    def _setNumber(self, propertyName, newSubs):
        number = self._device.getNumber(propertyName)
        for i in range(len(newSubs)):
            if newSubs[i] is not None:
                number[i].value = newSubs[i]
        self._client.sendNewNumber(number)


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
        index = index if isinstance(index, int) else self._getIndexInProperty(propertyName, index)
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
        index = index if isinstance(index, int) else self._getIndexInProperty(propertyName, index)
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
        index = index if isinstance(index, int) else self._getIndexInProperty(propertyName, index)
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
        index = index if isinstance(index, int) else self._getIndexInProperty(propertyName, index)
        if object:
            return self._device.getBLOB(propertyName)[index]
        return self._device.getBLOB(propertyName)[index]

# Agent class controls the properties of a device (or none).
#
class Agent:
    device = None
    def __init__(self, device=None):
        self.device = device


    def setDevice(self, device):
        self.device = device


    def getDevice(self):
        return self.device
    ############################################ Before connection ##########################################

    # TODO: Changing properties before connecting to the device, such as port and ...

    ############################################ After connection ###########################################
    # Change the given property of device.
    #
    # @param propertyName {String} - the name of the property to change. -> e.g. "CONNECTION" or "connection" (case insensitive)
    # @param type {String} - type of the changing property: 1. switch - 2. text - 3. number - 4. blob
    # @param *args {Boolean|String|Number|Blob} - new values for the property depends on type. Boolean for switch, Text for text and Number for number.
    def setProperty(self, propertyName, type, *args):
        try:
            eval('self.__set' + type.lower().title() + '(propertyName, *args)'))
        except NameError:
            print('Unavailable type of property.')


    # Get the value of the given property.
    #
    # @param propertName {String} - the name of the property to get. -> e.g. "CONNECTION" or "connection" (case insensitive)
    # @param type {String} - type of the changing property: 1. switch - 2. text - 3. number - 4. blob.
    # @param index {Number} - the index of the sub property.
    def getProperty(self, propertyName, type, index=None):
        try:
            eval('self.__get' + type.lower().title() + '(propertyName, index=None)'))
        except NameError:
            print('Unavailable type of property.')


    #######################################################
    ######################  setters  ######################
    #######################################################
    # Set values for switch properties.
    #
    # @param propertyName {String} - name of property to change, which is a switch.
    # @param *args {Boolean} - new values for properties.
    def __setSwitch(self, propertyName, *args):
        switch = self.device.getSwitch(propertyName.replace(' ', '_').upper())
        for i in range(len(args)):
            switch[i].s = PyIndi.ISS_ON if args[i] == True else PyIndi.ISS_OFF
        self.sendNewSwitch(switch)


    # Set values for text properties.
    #
    # @param propertyName {String} - name of property to change, which is a text.
    # @param *args {String} - new values for properties.
    def __setText(self, propertyName, *args):
        text = self.device.getText(propertyName.replace(' ', '_').upper())
        for i in range(len(args)):
            text[i].text = args[i]
        self.sendNewText(text)


    # Set values for number properties.
    #
    # @param propertyName {String} - name of property to change, which is a switch.
    # @param *args {Number} - new values for properties.
    def __setNumber(self, propertyName, *args):
        number = self.device.getNumber(propertyName.replace(' ', '_').upper())
        for i in range(len(args)):
            number[i].value = args[i]
        self.sendNewNumber(number)


    ###########################################################################

    #######################################################
    ######################  getters  ######################
    #######################################################
    # Get the value of switch propeties.
    #
    # @param propertyName {String} - name of property to get, which is a switch.
    # @para, index {Number} - the index of the sub property.
    def __getSwitch(self, propertyName, index):
        return self.device.getSwitch(propertyName.replace(' ', '_').upper())[index].s


    # Get the value of text propeties.
    #
    # @param propertyName {String} - name of property to get, which is a text.
    # @para, index {Number} - the index of the sub property.
    def __getText(self, propertyName, index):
        return self.device.getText(propertyName.replace(' ', '_').upper())[index].text


    # Get the value of number propeties.
    #
    # @param propertyName {String} - name of property to get, which is a number.
    # @para, index {Number} - the index of the sub property.
    def __getNumber(self, propertyName, index):
        return self.device.getNumber(propertyName.replace(' ', '_').upper())[index].values


    # Get the value of blob propeties.
    #
    # @param propertyName {String} - name of property to get, which is a blob.
    # @para, index {Number} - the index of the sub property.
    def __getBLOB(self, propertyName, index):
        return self.device.getBLOB(propertyName.replace(' ', '_').upper())[index]

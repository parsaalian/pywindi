import PyIndi

INDI_TYPES = ['number', 'switch', 'text', 'light', 'blob']

class Windevice:
    _winclient = None
    _device = None

    def __init__(self, winclient, device, **kwargs):
        self._winclient = winclient
        self._device = device
        for name, value in kwargs.items():
            self.set_property(name, value)
        self.set_property('CONNECTION', [True, False])


    def wait_for_property(self, property_name):
        self._winclient.wait_for_property(self._device.getDeviceName(), property_name)


    # Change the given property of device.
    #
    # @param property_name {String} - the name of the property to change. -> e.g. "CONNECTION" or "connection" (case insensitive)
    # @param new_sub_properties {List} - a list that changing values are in it. None if value is not meant to change.
    # e.g. set_property('CONNECTION', [True,  False]) - change the connection of device.
    def set_property(self, property_name, new_sub_properties):
        self.wait_for_property(property_name)
        try:
            getattr(self, '_set_' + INDI_TYPES[self._device.getProperty(property_name).getType()])(property_name, new_sub_properties)
        except Exception as e:
            print(e)


    # Get the value of the given property.
    #
    # @param propertName {String} - the name of the property to get. -> e.g. "CONNECTION" or "connection" (case insensitive)
    # @param sub_property {Boolean} - True is sub-property of property is wanted.
    # @param index {Number} - index of sub-property.
    # @param object {Boolean} - True if object of sub-property is wanted, not content of it.
    def get_property(self, property_name, sub_property=False, index=None, object=False):
        self.wait_for_property(property_name)
        try:
            return getattr(self, '_get_' + INDI_TYPES[self._device.getProperty(property_name).getType()])(property_name, sub_property, index, object)
        except Exception as e:
            print(e)



    #######################################################
    ######################  setters  ######################
    #######################################################
    # Set values for switch properties.
    #
    # @param property_name {String} - name of property to change, which is a switch.
    # @param new_subs {List} - new values for properties.
    def _set_switch(self, property_name, new_subs):
        switch = self._device.getSwitch(property_name)
        for i in range(len(new_subs)):
            if new_subs[i] is not None:
                switch[i].s = PyIndi.ISS_ON if new_subs[i] == True else PyIndi.ISS_OFF
        self._winclient.sendNewSwitch(switch)


    # Set values for text properties.
    #
    # @param property_name {String} - name of property to change, which is a text.
    # @param new_subs {List} - new values for properties.
    def _set_text(self, property_name, new_subs):
        text = self._device.getText(property_name)
        for i in range(len(new_subs)):
            if new_subs[i] is not None:
                text[i].text = new_subs[i]
        self._winclient.sendNewText(text)


    # Set values for number properties.
    #
    # @param property_name {String} - name of property to change, which is a switch.
    # @param new_subs {List} - new values for properties.
    def _set_number(self, property_name, new_subs):
        number = self._device.getNumber(property_name)
        for i in range(len(new_subs)):
            if new_subs[i] is not None:
                number[i].value = new_subs[i]
        self._winclient.sendNewNumber(number)


    ###########################################################################

    #######################################################
    ######################  getters  ######################
    #######################################################
    # Get the value of switch propeties.
    #
    # @param property_name {String} - name of property to get, which is a switch.
    # @param sub_property {Boolean} - True is sub-property of property is wanted.
    # @param index {Number} - index of sub-property.
    # @param object {Boolean} - True if object of sub-property is wanted, not content of it.
    def _get_switch(self, property_name, sub_property=False, index=None, object=False):
        if not sub_property:
            return self._device.getSwitch(property_name)
        if object:
            return self._device.getSwitch(property_name)[index]
        return self._device.getSwitch(property_name)[index].s == PyIndi.ISS_ON


    # Get the value of text propeties.
    #
    # @param property_name {String} - name of property to get, which is a text.
    # @param sub_property {Boolean} - True is sub-property of property is wanted.
    # @param index {Number} - index of sub-property.
    # @param object {Boolean} - True if object of sub-property is wanted, not content of it.
    def _get_text(self, property_name, sub_property=False, index=None, object=False):
        if not sub_property:
            return self._device.getText(property_name)
        if object:
            return self._device.getText(property_name)[index]
        return self._device.getText(property_name)[index].text


    # Get the value of number propeties.
    #
    # @param property_name {String} - name of property to get, which is a number.
    # @param sub_property {Boolean} - True is sub-property of property is wanted.
    # @param index {Number} - index of sub-property.
    # @param object {Boolean} - True if object of sub-property is wanted, not content of it.
    def _get_number(self, property_name, sub_property=False, index=None, object=False):
        if not sub_property:
            return self._device.getNumber(property_name)
        if object:
            return self._device.getNumber(property_name)[index]
        return self._device.getNumber(property_name)[index].value


    # Get the value of blob propeties.
    #
    # @param property_name {String} - name of property to get, which is a blob.
    # @param sub_property {Boolean} - True is sub-property of property is wanted.
    # @param index {Number} - index of sub-property.
    # @param object {Boolean} - True if object of sub-property is wanted, not content of it.
    def _get_blob(self, property_name, sub_property=False, index=None, object=False):
        if not sub_property:
            return self._device.getBLOB(property_name)
        if object:
            return self._device.getBLOB(property_name)[index]
        return self._device.getBLOB(property_name)[index]

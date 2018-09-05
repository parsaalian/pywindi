import PyIndi

INDI_TYPES = ['number', 'switch', 'text', 'light', 'blob']

class Windevice:
    def __init__(self, winclient, device, **kwargs):
        '''Set client, device and initial properties for device.

        :param winclient: client of the device.
        :param device: device of the windevice to change properties.
        :params **kwargs: the initial value for properties, such as device port
                          and ...
        '''
        self._winclient = winclient
        self._device = device
        #: set the initial values.
        for name, value in kwargs.items():
            self.set_property(name, value)
        #: connects the device.
        self.set_property('CONNECTION', [True, False])


    def wait_for_property(self, property_name):
        #: waits until the proprty is given to the client. if
        #: anything is change before this, you will get exception.
        self._winclient.wait_for_property(self._device.getDeviceName(), property_name)


    def get_name(self):
        return self._device.getDeviceName()


    def get_properties(self):
        return self._device.getProperties()


    # TODO: make the generator in a way that a map of property name and its normalize
    #       name is available.

    def set_property(self, property_name, new_sub_properties):
        '''Change the given property of device.

        :param property_name: the name of the property to change.
                              e.g. "CONNECTION" or "connection" (case sensitive)
        :param new_sub_properties: a list that changing values are in it.
                                   None if value is not meant to change.
                                   e.g. set_property('CONNECTION', [True,  False])
                                   -> change the connection of device.
        '''
        self.wait_for_property(property_name)
        try:
            #: set the property due to its type.
            getattr(self, '_set_' + INDI_TYPES[self._device.getProperty(property_name).getType()])(property_name, new_sub_properties)
        except Exception as e:
            print(e)



    def get_property(self, property_name, sub_property=False, index=None, object=False):
        '''Get the value of the given property.

        :param property_name: the name of the property to get.
                              e.g. "CONNECTION" or "connection" (case sensitive)
        :param sub_property: True is sub-property of property is wanted.
        :param index: index of sub-property.
        :param object: True if object of sub-property is wanted, not content of it.
        '''
        self.wait_for_property(property_name)
        try:
            #: get the property due to its type.
            return getattr(self, '_get_' + INDI_TYPES[self._device.getProperty(property_name).getType()])(property_name, sub_property, index, object)
        except Exception as e:
            print(e)



    #######################################################
    ######################  setters  ######################
    #######################################################
    def _set_switch(self, property_name, new_subs):
        switch = self._device.getSwitch(property_name)
        for i in range(len(new_subs)):
            if new_subs[i] is not None:
                switch[i].s = PyIndi.ISS_ON if new_subs[i] == True else PyIndi.ISS_OFF
        self._winclient.sendNewSwitch(switch)


    def _set_text(self, property_name, new_subs):
        text = self._device.getText(property_name)
        for i in range(len(new_subs)):
            if new_subs[i] is not None:
                text[i].text = new_subs[i]
        self._winclient.sendNewText(text)


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
    def _get_switch(self, property_name, sub_property=False, index=None, object=False):
        if not sub_property:
            return self._device.getSwitch(property_name)
        if object:
            return self._device.getSwitch(property_name)[index]
        return self._device.getSwitch(property_name)[index].s == PyIndi.ISS_ON


    def _get_text(self, property_name, sub_property=False, index=None, object=False):
        if not sub_property:
            return self._device.getText(property_name)
        if object:
            return self._device.getText(property_name)[index]
        return self._device.getText(property_name)[index].text


    def _get_number(self, property_name, sub_property=False, index=None, object=False):
        if not sub_property:
            return self._device.getNumber(property_name)
        if object:
            return self._device.getNumber(property_name)[index]
        return self._device.getNumber(property_name)[index].value


    def _get_blob(self, property_name, sub_property=False, index=None, object=False):
        if not sub_property:
            return self._device.getBLOB(property_name)
        if object:
            return self._device.getBLOB(property_name)[index]
        return self._device.getBLOB(property_name)[index]

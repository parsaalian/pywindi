class SBIG_CCD(Windevice):
	def __init__(self, winclient, indi_device):
		super().__init__(winclient, indi_device)


	def set_connection(self, **kwargs):
		properties_list = [connect, disconnect]
		self.set_global_property(CONNECTION, properties_list, **kwargs)


	def set_driver_info(self, **kwargs):
		properties_list = [driver_name, driver_exec, driver_version, driver_interface]
		self.set_global_property(DRIVER_INFO, properties_list, **kwargs)


	def set_polling_period(self, **kwargs):
		properties_list = [period_ms]
		self.set_global_property(POLLING_PERIOD, properties_list, **kwargs)


	def set_simulation(self, **kwargs):
		properties_list = [enable, disable]
		self.set_global_property(SIMULATION, properties_list, **kwargs)


	def set_config_process(self, **kwargs):
		properties_list = [config_load, config_save, config_default]
		self.set_global_property(CONFIG_PROCESS, properties_list, **kwargs)


	def set_active_devices(self, **kwargs):
		properties_list = [active_telescope, active_focuser, active_filter, active_skyquality]
		self.set_global_property(ACTIVE_DEVICES, properties_list, **kwargs)


	def set_device_port_type(self, **kwargs):
		properties_list = [ethernet, usb_1, usb_2, usb_3, usb_4, lpt_1, lpt_2, lpt_3]
		self.set_global_property(DEVICE_PORT_TYPE, properties_list, **kwargs)


	def set_debug(self, **kwargs):
		properties_list = [enable, disable]
		self.set_global_property(DEBUG, properties_list, **kwargs)


	def set_ccd_exposure(self, **kwargs):
		properties_list = [ccd_exposure_value]
		self.set_global_property(CCD_EXPOSURE, properties_list, **kwargs)


	def set_ccd_abort_exposure(self, **kwargs):
		properties_list = [abort]
		self.set_global_property(CCD_ABORT_EXPOSURE, properties_list, **kwargs)


	def set_ccd_frame(self, **kwargs):
		properties_list = [x, y, width, height]
		self.set_global_property(CCD_FRAME, properties_list, **kwargs)


	def set_ccd_binning(self, **kwargs):
		properties_list = [hor_bin, ver_bin]
		self.set_global_property(CCD_BINNING, properties_list, **kwargs)


	def set_fits_header(self, **kwargs):
		properties_list = [fits_observer, fits_object]
		self.set_global_property(FITS_HEADER, properties_list, **kwargs)


	def set_guider_exposure(self, **kwargs):
		properties_list = [guider_exposure_value]
		self.set_global_property(GUIDER_EXPOSURE, properties_list, **kwargs)


	def set_guider_abort_exposure(self, **kwargs):
		properties_list = [abort]
		self.set_global_property(GUIDER_ABORT_EXPOSURE, properties_list, **kwargs)


	def set_guider_frame(self, **kwargs):
		properties_list = [x, y, width, height]
		self.set_global_property(GUIDER_FRAME, properties_list, **kwargs)


	def set_ccd_temperature(self, **kwargs):
		properties_list = [ccd_temperature_value]
		self.set_global_property(CCD_TEMPERATURE, properties_list, **kwargs)


	def set_ccd_info(self, **kwargs):
		properties_list = [ccd_max_x, ccd_max_y, ccd_pixel_size, ccd_pixel_size_x, ccd_pixel_size_y, ccd_bitsperpixel]
		self.set_global_property(CCD_INFO, properties_list, **kwargs)


	def set_guider_info(self, **kwargs):
		properties_list = [ccd_max_x, ccd_max_y, ccd_pixel_size, ccd_pixel_size_x, ccd_pixel_size_y, ccd_bitsperpixel]
		self.set_global_property(GUIDER_INFO, properties_list, **kwargs)


	def set_guider_binning(self, **kwargs):
		properties_list = [hor_bin, ver_bin]
		self.set_global_property(GUIDER_BINNING, properties_list, **kwargs)


	def set_ccd_compression(self, **kwargs):
		properties_list = [ccd_compress, ccd_raw]
		self.set_global_property(CCD_COMPRESSION, properties_list, **kwargs)


	def set_ccd1(self, **kwargs):
		properties_list = [ccd1]
		self.set_global_property(CCD1, properties_list, **kwargs)


	def set_guider_compression(self, **kwargs):
		properties_list = [guider_compress, guider_raw]
		self.set_global_property(GUIDER_COMPRESSION, properties_list, **kwargs)


	def set_ccd2(self, **kwargs):
		properties_list = [ccd2]
		self.set_global_property(CCD2, properties_list, **kwargs)


	def set_telescope_timed_guide_ns(self, **kwargs):
		properties_list = [timed_guide_n, timed_guide_s]
		self.set_global_property(TELESCOPE_TIMED_GUIDE_NS, properties_list, **kwargs)


	def set_telescope_timed_guide_we(self, **kwargs):
		properties_list = [timed_guide_w, timed_guide_e]
		self.set_global_property(TELESCOPE_TIMED_GUIDE_WE, properties_list, **kwargs)


	def set_ccd_frame_type(self, **kwargs):
		properties_list = [frame_light, frame_bias, frame_dark, frame_flat]
		self.set_global_property(CCD_FRAME_TYPE, properties_list, **kwargs)


	def set_ccd_frame_reset(self, **kwargs):
		properties_list = [reset]
		self.set_global_property(CCD_FRAME_RESET, properties_list, **kwargs)


	def set_guider_frame_type(self, **kwargs):
		properties_list = [frame_light, frame_bias, frame_dark, frame_flat]
		self.set_global_property(GUIDER_FRAME_TYPE, properties_list, **kwargs)


	def set_ccd_cfa(self, **kwargs):
		properties_list = [cfa_offset_x, cfa_offset_y, cfa_type]
		self.set_global_property(CCD_CFA, properties_list, **kwargs)


	def set_ccd_rapid_guide(self, **kwargs):
		properties_list = [enable, disable]
		self.set_global_property(CCD_RAPID_GUIDE, properties_list, **kwargs)


	def set_guider_rapid_guide(self, **kwargs):
		properties_list = [enable, disable]
		self.set_global_property(GUIDER_RAPID_GUIDE, properties_list, **kwargs)


	def set_telescope_type(self, **kwargs):
		properties_list = [telescope_primary, telescope_guide]
		self.set_global_property(TELESCOPE_TYPE, properties_list, **kwargs)


	def set_wcs_control(self, **kwargs):
		properties_list = [wcs_enable, wcs_disable]
		self.set_global_property(WCS_CONTROL, properties_list, **kwargs)


	def set_upload_mode(self, **kwargs):
		properties_list = [upload_client, upload_local, upload_both]
		self.set_global_property(UPLOAD_MODE, properties_list, **kwargs)


	def set_upload_settings(self, **kwargs):
		properties_list = [upload_dir, upload_prefix]
		self.set_global_property(UPLOAD_SETTINGS, properties_list, **kwargs)


	def set_ccd_exposure_loop(self, **kwargs):
		properties_list = [loop_on, loop_off]
		self.set_global_property(CCD_EXPOSURE_LOOP, properties_list, **kwargs)


	def set_ccd_exposure_loop_count(self, **kwargs):
		properties_list = [frames]
		self.set_global_property(CCD_EXPOSURE_LOOP_COUNT, properties_list, **kwargs)


	def set_ccd_product(self, **kwargs):
		properties_list = [name, id]
		self.set_global_property(CCD_PRODUCT, properties_list, **kwargs)


	def set_ccd_fan(self, **kwargs):
		properties_list = [fan_on, fan_off]
		self.set_global_property(CCD_FAN, properties_list, **kwargs)


	def set_ccd_cooler(self, **kwargs):
		properties_list = [cooler_on, cooler_off]
		self.set_global_property(CCD_COOLER, properties_list, **kwargs)


	def set_ccd_cooler_power(self, **kwargs):
		properties_list = [ccd_cooler_value]
		self.set_global_property(CCD_COOLER_POWER, properties_list, **kwargs)


	def set_cfw_connection(self, **kwargs):
		properties_list = [connect, disconnect]
		self.set_global_property(CFW_CONNECTION, properties_list, **kwargs)


	def set_cfw_type(self, **kwargs):
		properties_list = [cfw1, cfw2, cfw3, cfw4, cfw5, cfw6, cfw7, cfw8, cfw9, cfw10, cfw11, cfw12, cfw13, cfw14, cfw15, cfw16]
		self.set_global_property(CFW_TYPE, properties_list, **kwargs)

class ProtocolParser:
	def __init__(self, process_address_data_change_callback, sync_callback ):
		self.__state = "WAIT_FOR_SYNC"
		self.__sync_byte_count = 0
		self.__address = 0
		self.__count = 0
		self.__data = 0
		self.data_change_callback = process_address_data_change_callback
		self.sync_callback = sync_callback
		
	def process_byte(self, c):
		if self.__state == "ADDRESS_LOW":
			self.__address = c
			self.__state = "ADDRESS_HIGH"
		elif self.__state == "ADDRESS_HIGH":
			self.__address += c*256
			if self.__address != 0x5555:
				self.__state = "COUNT_LOW"
			else:
				self.__state = "WAIT_FOR_SYNC"
		elif self.__state == "COUNT_LOW":
			self.__count = c
			self.__state = "COUNT_HIGH"
		elif self.__state == "COUNT_HIGH":
			self.__count += 256*c
			self.__state = "DATA_LOW"
		elif self.__state == "DATA_LOW":
			self.__data = c
			self.__count -= 1
			self.__state = "DATA_HIGH"
		elif self.__state == "DATA_HIGH":
			self.__data += 256*c
			self.__count -= 1
			self.data_change_callback(self.__address, self.__data)
			self.__address += 2
			if self.__count == 0:
				self.__state = "ADDRESS_LOW"
			else:
				self.__state = "DATA_LOW"
			
			
		if c == 0x55:
			self.__sync_byte_count += 1
		else:
			self.__sync_byte_count = 0
		
		if self.__sync_byte_count == 4:
			self.__state = "ADDRESS_LOW"
			self.__sync_byte_count = 0
			self.sync_callback()

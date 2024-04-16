class Node:
  def __init__(self, value, time_stamp, content):
        self.value = value
        self.time_stamp = time_stamp
        self.infection_status = False
        self.content = content
  
  def get_value(self):
    return self.value

  def get_time_stamp(self):
    return self.time_stamp
  
  def set_time_stamp(self, value, time_stamp): 
    self.time_stamp = time_stamp

  def set_value(self, value):
    self.value = value

  def get_infection_status(self):
    return self.infection_status
  
  def infected(self):
    self.infection_status = True

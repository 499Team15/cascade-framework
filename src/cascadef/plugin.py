import networkx as nx
import matplotlib.pyplot as plt
import datetime

class Node:
  def __init__(self, value, time_stamp):
    self.value = value
    self.time_stamp = time_stamp
  
  def get_value(self):
    return self.value

  def get_time_stamp(self):
    return self.time_stamp
  
  def set_time_stamp(self, value, time_stamp): 
    self.time_stamp = time_stamp


  def set_value(self, value):
    self.value = value

import queue

class Process:
  def __init__(self, id, duration, arrival_time, deadline=0, pages = 2):
    self.id = id
    self.duration = duration 
    self.arrival_time = arrival_time
    self.deadline = deadline
    self.pages = pages

  def __lt__(self,other):
    return self.deadline < other.deadline
  
  def __repr__(self) -> str:
    return str(self.id)
import queue

class Process:
  def __init__(self, id, duration, arrival_time, deadline=0):
    self.id = id
    self.duration = duration
    self.arrival_time = arrival_time
    self.deadline = deadline

  def __lt__(self,other):
    return self.deadline < other.deadline
import pyglet

from Process import Process
class Grid:
  def __init__(self, memory):
    self.square_size = 40
    self.font_size = int(self.square_size * 0.4)
    self.border_size = 2
    if memory == "RAM":
      self.label_text = "RAM"
      self.num_rows = 5
      self.num_cols = 10
      self.grid_width = self.num_cols * self.square_size
      self.grid_x = (1366 - self.grid_width) // 2 + 400  # Push grid 1 to the right by 400 pixels
    
    else:
      self.label_text = "Disk"
      self.num_rows = 10
      self.num_cols = 12
      self.grid_width = self.num_cols * self.square_size
      self.grid_x = (1366 - self.grid_width) // 2 - 350
    
    self.grid_height = self.num_rows * self.square_size
    self.grid_y = ((768 - self.grid_height) // 2) + 150 

    # Nessa matriz temos em cada posicao o id do processo alocado
    # self.pages_allocation = [[0] * self.num_cols for _ in range(self.num_rows)]
    self.pagination_FIFO_replacement_row = 0
    self.pagination_FIFO_replacement_col = 0

  def draw_grid(self):

    label = pyglet.text.Label(
        self.label_text,
        font_name='Arial',
        font_size=24,
        x=self.grid_x + self.grid_width//2,  # Center the label horizontally
        y=self.grid_y + self.grid_height + 5,
        anchor_x='center',
        color=(0, 0, 0, 255) 
    )
    label.draw()

    address = 0
    for row in range(self.num_rows):
      for col in range(self.num_cols):
        # Calculate the position of each square in grid 1
        square_x = self.grid_x + col * self.square_size
        square_y = self.grid_y + row * self.square_size

        square = pyglet.shapes.Rectangle(
            x=square_x,
            y=square_y,
            width=self.square_size,
            height=self.square_size,
            color=(255, 255, 255)
        )

        # Set the border color to black
        border_color = (0, 0, 0)

        # Draw the border of the square
        
        border_x = square_x - self.border_size
        border_y = square_y - self.border_size
        border_width = self.square_size + 2 * self.border_size
        border_height = self.square_size + 2 * self.border_size

        # Draw the border
        pyglet.shapes.Rectangle(
        x=border_x, y=border_y, width=border_width, height=border_height, color=border_color
        ).draw()

        # Draw the square
        square.draw()

        border_x = square_x - self.border_size
        border_y = square_y - self.border_size
        border_width = self.square_size + 2 * self.border_size
        border_height = self.square_size + 2 * self.border_size


        # Draw number in the top left corner with decreased font size in black
        small_font_size = int(self.font_size * 0.6)
        small_label = pyglet.text.Label(
            str(address),
            font_name='Arial',
            font_size=small_font_size,
            x=border_x + self.border_size,
            y=border_y + border_height - self.border_size,
            anchor_x='left',
            anchor_y='top',
            color=(0, 0, 0, 255)  # Set the text color to black
        )
        address += 1
        small_label.draw()


  def desalocate_address(self,row,col,processes_pagination_status,pages_allocation):
    square_x = self.grid_x + col * self.square_size
    square_y = self.grid_y + row* self.square_size

    border_x = square_x - self.border_size
    border_y = square_y - self.border_size
    border_width = self.square_size + 2 * self.border_size
    border_height = self.square_size + 2 * self.border_size

    border_color = (0, 0, 0)
    # Draw the border
    pyglet.shapes.Rectangle(
    x=border_x, y=border_y, width=border_width, height=border_height, color=border_color
    ).draw()


    # draw square
    square = pyglet.shapes.Rectangle(
      x=square_x,
      y=square_y,
      width=self.square_size,
      height=self.square_size,
      color=(255, 255, 255)
    ).draw()

    small_font_size = int(self.font_size * 0.6)
    small_label = pyglet.text.Label(
      str(row*10 + col),
      font_name='Arial',
      font_size=small_font_size,
      x=border_x + self.border_size,
      y=border_y + border_height - self.border_size,
      anchor_x='left',
      anchor_y='top',
      color=(0, 0, 0, 255)  # Set the text color to black
    ).draw()

    removed_process_page = pages_allocation[abs(row - (self.num_rows - 1))][col] 
    processes_pagination_status[removed_process_page] -= 1

  def pagination_FIFO(self, current_process,processes_pagination_status,pages_allocation,page_order):
    row,col = 0,0

    for i,past_page in enumerate(page_order):
      row,col = past_page[0],past_page[1]

      if pages_allocation[abs(row - (self.num_rows - 1))][col] != current_process.id:
        page_order.pop(i)
        break
      

    # Remove a pag que estava na posicao e adiciona a do current_process
    self.desalocate_address(row,col,processes_pagination_status,pages_allocation)

    self.allocate_page(current_process.id,row,col)
    pages_allocation[abs(row - (self.num_rows-1))][col] = current_process.id
    processes_pagination_status[current_process.id] += 1 
    page_order.append((row,col))

  def pagination_LRU(self,current_process,processes_pagination_status,pages_allocation,page_order):

    if len(page_order) == 0:
      return
      

    i = 0
    pages = 1
    while pages <= len(page_order):
      
      row,col = page_order[i][0],page_order[i][1]

      if pages_allocation[abs(row - (self.num_rows - 1))][col] == current_process.id:

        referenced_page = page_order.pop(i)
        page_order.append(referenced_page)
      else:
        i += 1
      pages += 1

    least_recently_used_page = page_order.pop(0)
    row,col = least_recently_used_page[0],least_recently_used_page[1]
    
     # Remove a pag que estava na posicao e adiciona a do current_process
    self.desalocate_address(row,col,processes_pagination_status,pages_allocation)

    self.allocate_page(current_process.id,row,col)
    pages_allocation[abs(row - (self.num_rows-1))][col] = current_process.id
    processes_pagination_status[current_process.id] += 1 
    page_order.append((row,col))
    pass
    
  def draw_processes_pages(self, processes, current_index, pagination_algorithm):
    
    page_order = []
    total_processes = max(processes[:current_index],key=lambda p: p.id).id

    
    processes_pagination_status = [0] * (total_processes+1)
    pages_allocation = [[0] * self.num_cols for _ in range(self.num_rows)]

    for current_process in processes[:current_index]:

      # se ja alocamos tds as paginas desse processo não queremos alocar denovo
      if processes_pagination_status[current_process.id] == current_process.pages:
        
        # colocamos no final da fila as pags do processo referenciado
        if pagination_algorithm == "LRU":
          i = 0
          pages = 1
          while pages <= len(page_order):
            
            row,col = page_order[i][0],page_order[i][1]

            if pages_allocation[abs(row - (self.num_rows - 1))][col] == current_process.id:

              referenced_page = page_order.pop(i)
              page_order.append(referenced_page)
            else:
              i += 1
            pages += 1
        continue
      
      # So queremos alocar as paginas que estao faltando
      missing_pages = current_process.pages - processes_pagination_status[current_process.id]
     
      for _ in range(missing_pages):
        # Se não conseguimos alocar uma pag do processo precisamos fazer uma paginação

        if not self.find_page_address(current_process.id,pages_allocation,processes_pagination_status,page_order):
            
          # chama algum algoritmo de paginação
          
          # self.pagination_FIFO(current_process,processes_pagination_status,pages_allocation,page_order)
          self.pagination_LRU(current_process,processes_pagination_status,pages_allocation,page_order)
    

  def find_page_address(self,process_id,pages_allocation,processes_pagination_status,page_order):
    for i in range(self.num_rows):
      for j in range(self.num_cols):     
        # se for 0 significa que n tem paginas alocadas na posicao [i][j]
        # abs(i - (self.num_rows-1)) correção por causa da indexação da matriz desenhada com matriz do python
        if not pages_allocation[abs(i - (self.num_rows-1))][j]:
          self.allocate_page(process_id,i,j)
          page_order.append((i,j))
          pages_allocation[abs(i - (self.num_rows-1))][j] = process_id
          processes_pagination_status[process_id] += 1
          return True
  
    return False
     
  def allocate_page(self,process_id, row, col):
   
    square_x = self.grid_x + col * self.square_size
    square_y = self.grid_y + row * self.square_size
    
    label = pyglet.text.Label(
      str(process_id),
      font_name='Arial',
      font_size=self.font_size,
      x=square_x + self.square_size // 2,
      y=square_y + self.square_size // 2,
      anchor_x='center',
      anchor_y='center',
      color=(0, 0, 0, 255)  # Set the text color to black
    )
    label.draw()

  
      

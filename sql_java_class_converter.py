class SqlJavaConverter:
  def convert_to_carmel_case(self, value: str):
    s = value.replace("_", " ")
    s = s.split()
    
    if len(s) == 0:
      return value
    else:
      return s[0] + ''.join(i.capitalize() for i in s[1:])
    
  def get_col_info(self, value: str, i: int):
    col_info = ''
    if i == 0:
      col_info = "@Column(name = \"{}\"".format(value[1:len(value) - 1])
    
    if i == 1 and value.__contains__('varchar'):
      col_info = col_info + ", length = {}".format(value[10:len(value) - 1])
    elif i == 1 and value.split(']')[0][1:] == 'char':
      col_info = col_info + ", length = {}".format(value[7:len(value) - 1])
    
    if (i == 2 or i == 3) and value.__contains__('NOT'):
      col_info = col_info + ', nullable = false'
      
    return col_info
    
  def convert(self):
    file = open('sql.txt', 'r')
    file2 = open('java_code.txt', 'w')
    lines = file.readlines()
    
    final_code = ''
    
    for line in lines:
      line_items = line.strip().split(" ")
      
      col_info = ''
      for i in range(len(line_items)):
        col_info = col_info + self.get_col_info(line_items[i], i)
        
      col_info = col_info + ')'
      
      field_info = 'private '
      if line_items[1].__contains__('char'):
        field_info = field_info + 'String ' + self.convert_to_carmel_case(line_items[0][1:len(line_items[0]) - 1])
      elif line_items[1].__contains__('numeric'):
        field_info = field_info + 'BigInteger ' + self.convert_to_carmel_case(line_items[0][1:len(line_items[0]) - 1])
      elif line_items[1].__contains__('datetime'):
        field_info = field_info + 'LocalDateTime ' + self.convert_to_carmel_case(line_items[0][1:len(line_items[0]) - 1])
      elif line_items[1].__contains__('timestamp'):
        field_info = field_info + 'LocalDateTime ' + self.convert_to_carmel_case(line_items[0][1:len(line_items[0]) - 1])
      
      field_info = field_info + ';'
      
      final_code = final_code + "{}\n{}\n\n".format(col_info, field_info)

    file2.writelines(final_code)
    file2.close()
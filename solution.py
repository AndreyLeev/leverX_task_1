from DataHandler import DataHandler
from JSONHandler import JSONHandler
from XMLHandler import XMLHandler


class DataTransfer():

    def __init__(self):
        self._in_data_handler = None
        self._out_data_handler = None
    
    in_data_handler = property()
    out_data_handler = property()
    
    @in_data_handler.setter
    def in_data_handler(self, value):
        self._in_data_handler = value

    @out_data_handler.setter
    def out_data_handler(self, value):
        self._out_data_handler = value

    def read_rooms(self, filename):
        self.rooms = self._in_data_handler.load(filename)

    def read_students(self, filename):
        self.students = self._in_data_handler.load(filename)

    def write_to_file(self, filename):
        self._out_data_handler.dump(self.data, filename)

    def handle_data(self):
        rooms_dict = {i['id']: {'name': i['name'], 'students':[]} for i in self.rooms}
        for student in self.students:
            room_for_stud = rooms_dict.get(student.get('room'))
            if room_for_stud is not None:
                room_for_stud.get('students').append(student)
        self.data = [{'id':i[0], **i[1]} for i in rooms_dict.items()]


def main(students_filename, rooms_filename, out_format):
    handler = DataTransfer()
    handler.in_data_handler = JSONHandler()  

    if out_format == 'json':
        handler.out_data_handler = JSONHandler()  
    elif out_format == 'xml':
        handler.out_data_handler = XMLHandler()
    else: 
        return
         
    try:
        handler.read_rooms(rooms_filename)
        handler.read_students(students_filename)    
    except FileNotFoundError as e:
        print(e)
        return

    handler.handle_data()  
    handler.write_to_file('out.'+out_format)


if __name__ == '__main__':

    import argparse  
    parser = argparse.ArgumentParser(description='Process some json files.')
    parser.add_argument('students_file_path',
                        type=str,
                        help='Path to the students file.')
    parser.add_argument('rooms_file_path',
                        type=str,
                        help='Input path to the students file.')
    parser.add_argument('out_format',
                        type=str,
                        help='Choice the output format') 
    args = parser.parse_args()
    
    main(args.students_file_path, args.rooms_file_path, args.out_format)

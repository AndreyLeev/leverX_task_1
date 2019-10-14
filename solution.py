from DataHandler import DataHandler
from JSONHandler import JSONHandler
from XMLHandler import XMLHandler


class DataTransfer():

    def read_rooms(self, handler, filename):
        self.rooms = handler.load(filename)

    def read_students(self, handler, filename):
        self.students = handler.load(filename)

    def write_to_file(self, handler, filename):
        handler.dump(self.data, filename)

    def handle_data(self):
        rooms_dict = {i['id']: {'name': i['name'], 'students':[]} for i in self.rooms}
        for student in self.students:
            room_for_stud = rooms_dict.get(student.get('room'))
            if room_for_stud is not None:
                room_for_stud.get('students').append(student)
        self.data = [{'id':i[0], **i[1]} for i in rooms_dict.items()]


def main(students_filename, rooms_filename, out_format):
    
    handler = DataTransfer()
     
    try:
        handler.read_rooms(JSONHandler, rooms_filename)
        handler.read_students(JSONHandler, students_filename)    
    except FileNotFoundError as e:
        return

    handler.handle_data()

    if out_format == 'json':
        handler.write_to_file(JSONHandler, 'out.'+out_format)
    elif out_format == 'xml':
         handler.write_to_file(XMLHandler, 'out.'+out_format)
    else: 
        return  
    

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

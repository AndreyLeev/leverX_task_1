import json 
import argparse  

from lxml import etree as xml
from abc import ABC, abstractmethod 


class DataHandler(ABC):
    @abstractmethod
    def load(self, data):
        pass

    @abstractmethod
    def dump(self, data):
        pass
    
    @abstractmethod
    def write(self, data, filename):
        pass

    @abstractmethod
    def read(self, filename):
        pass


class JSONHandler(DataHandler):
    def load(self, data):
        return json.loads(data) 
        
    def dump(self, data):
        return json.dumps(data, indent=2)
    
    def write(self, data, filename):
        with open(filename, 'w') as f:
            f.write(self.dump(data))

    def read(self, filename):
        with open(filename, 'r') as f:
            return self.load(f.read())


class XMLHandler(DataHandler):
    def load(self, data):
        raise NotImplementedError()
    
    def read(self, filename):
        raise NotImplementedError()

    def dump(self, data):
        root = xml.Element('rooms')
        for el in data:
            room = xml.Element('room')
            root.append(room)

            room_id = xml.SubElement(room, 'id')
            room_id.text = str(el.get('id')) 
            
            room_name = xml.SubElement(room, 'name')
            room_name.text = str(el.get('name')) 

            room_students = xml.SubElement(room, 'students')
            for student in el.get('students'):
                stud = xml.SubElement(room_students, 'student')
                stud_id = xml.SubElement(stud, 'id')
                stud_id.text = str(student.get('id'))
                stud_name = xml.SubElement(stud, 'name')
                stud_name.text = str(student.get('name'))   
                stud_id = xml.SubElement(stud, 'room')
                stud_id.text = str(student.get('room'))   
        
        tree = xml.ElementTree(root)
        return tree
    
    def write(self, data, filename):
        tree = self.dump(data)
        tree.write(filename, pretty_print=True)
     

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
        self.rooms = self._in_data_handler.read(filename)

    def read_students(self, filename):
        self.students = self._in_data_handler.read(filename)

    def write_to_file(self, filename):
        self._out_data_handler.write(self.data, filename)

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

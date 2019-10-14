from lxml import etree as xml

from DataHandler import DataHandler


class XMLHandler(DataHandler):
    def load(self, data):
        raise NotImplementedError()

    def dump(self, data, filename):
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
        tree.write(filename, pretty_print=True)
        
     
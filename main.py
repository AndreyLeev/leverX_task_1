import logging

import DataLoader as dl
import DataHandler as dh
import Factory

DATA_LOADERS = {
    'json': dl.JSONLoader,
}
DATA_HANDLERS = {
    'json': dh.JSONHandler,
    'xml': dh.XMLHandler,
}

data_loader_factory = Factory.ObjectFactory()
data_handler_factory = Factory.ObjectFactory()

for key, builder in DATA_LOADERS.items():
    data_loader_factory.register_builder(key, builder)

for key, builder in DATA_HANDLERS.items():
    data_handler_factory.register_builder(key, builder)


def get_union_data(rooms, students):
    rooms_dict = {i['id']: {'name': i['name'], 'students':[]} for i in rooms}
    for student in students:
        room_for_stud = rooms_dict.get(student.get('room'))
        if room_for_stud is not None:
            room_for_stud.get('students').append(student)
    union_data = [{'id':i[0], **i[1]} for i in rooms_dict.items()]
    return union_data
    

def main(students_filename, rooms_filename, out_format):
    in_format = 'json'
    out_filename = 'out.'+out_format

    loader = data_loader_factory.create(in_format)
    handler = data_handler_factory.create(out_format)
    
    try:
        rooms = loader.load(rooms_filename) 
        students = loader.load(students_filename)
    except FileNotFoundError as e:
        logging.error(e)
        return

    union_data = get_union_data(rooms, students)
    handler.write(union_data, out_filename)


def create_argparser():
    
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
    return parser 


if __name__ == '__main__':
    parser = create_argparser()
    args = parser.parse_args()
    main(args.students_file_path, args.rooms_file_path, args.out_format)
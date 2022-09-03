#!/usr/bin/python3
"""Module console
Serves as the entry point of the command interpreter"""
import models
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
import cmd
classes = {'Amenity': Amenity, 'City': City, 'Place': Place, 'State': State,
                'User': User, 'BaseModel': BaseModel, 'Review': Review}

class HBNBCommand(cmd.Cmd):
    """Class for the command interpreter"""
    prompt = "(hbnb) "

    def do_quit(self, line):
        """Quit command to exit the program\n"""
        return True

    def do_EOF(self, line):
        """Handles End of File character\n"""
        print()
        return True

    def emptyline(self):
        """Ensures the last nonempty command is not repeated\n"""
        pass

    def do_create(self, line):
        """Creates a new instance and saves it to JSON file
        on success: returns id
        else: returns an error msg\n"""

        o = None
        if line is None or line == "":
            print("** class name missing **")
        else:
            for k, v in classes.items():
                if line == k:
                    o = v()
                    o.save()
                    print(o.id)
                    break
            if line != k:
                print("** class doesn't exist **")
                

    def do_show(self, line):
        """Prints the string representation of an instance based\
 on class name and id\n"""
        if line is None or line == "":
            print("** class name missing **")
        else:
            words = line.split()
            for k, v in classes.items():
                if words[0] == k:
                    if len(words) < 2:
                        print("** instance id missing **")
                        break
                    else:
                        key = "{}.{}".format(words[0], words[1])
                        if key not in storage.all():
                            print("** no instance found **")
                            break
                        else:
                            print(storage.all()[key])
                            break
            if words[0] != k:
                print("** class doesn't exist **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id\n"""
        if line is None or line == "":
            print("** class name missing **")
        else:
            words = line.split(' ')
            for k, v in classes.items():
                if words[0] == k:
                    if len(words) < 2:
                        print("** instance id missing **")
                        break
                    else:
                        key = "{}.{}".format(words[0], words[1])
                        if key not in storage.all():
                            print("** no instance found **")
                            break
                        else:
                            del(storage.all()[key])
                            storage.save()
                            break
            if words[0] != k:
                print("** class doesn't exist **")

    def do_all(self, line):
        """Prints all string representation of all instances\
 given a class name or not\n"""
        if line != "":
            words = line.split(' ')
            for k, v in classes.items():
                if words[0] == k:
                    o_list = [str(obj) for key, obj in storage.all().items()
                            if type(obj).__name__ == words[0]]
                    print(o_list)
                    break
        else:
            o_list = [str(obj) for key, obj in storage.all().items()]
            print(o_list)

    def do_update(self, line):
        """Updates an instance based on the class name and id\n"""
        if line == "":
            print("** class name missing **")
        else:
            words = line.split(' ')
            for k, v in classes.items():
                if words[0] == k:
                    if len(words) < 2:
                        print("** instance id missing **")
                        break
                    else:
                        key = "{}.{}".format(words[0], words[1])
                        if key not in storage.all():
                            print("** no instance found **")
                            break
                        else:
                            if len(words) < 3:
                                print("** attribute name missing **")
                                break
                            elif len(words) < 4:
                                print("** value missing **")
                                break
                            else:
                                setattr(storage.all()[key], words[2], words[3])
                                storage.all()[key].save()
                                break
            if words[0] != k:
                print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()

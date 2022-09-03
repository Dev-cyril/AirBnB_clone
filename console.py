#!/usr/bin/python3
"""Module console
Serves as the entry point of the command interpreter"""

from models import storage
import json
import cmd
import re


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

        if line is None or line == "":
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            o = storage.classes()[line]()
            o.save()
            print(o.id)

    def do_show(self, line):
        """Prints the string representation of an instance based\
 on class name and id\n"""
        if line is None or line == "":
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id\n"""
        if line is None or line == "":
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del(storage.all()[key])
                    storage.save()

    def do_all(self, line):
        """Prints all string representation of all instances\
 given a class name or not\n"""
        if line != "":
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                o_list = [str(obj) for key, obj in storage.all().items()
                          if type(obj).__name__ == words[0]]
                print(o_list)
        else:
            o_list = [str(obj) for key, obj in storage.all().items()]
            print(o_list)

    def do_update(self, line):
        """Updates an instance based on the class name and id\n"""
        if line == "":
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[0] not in storage.classes():
                print("** class doesn't exit **")
            elif len(words) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[0], words[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    if len(words) < 3:
                        print("** attribute name missing **")
                    elif len(words) < 4:
                        print("** value missing **")
                    else:
                        setattr(storage.all()[key], words[2], words[3])
                        storage.all()[key].save()

    def precmd(self, line):
        """Reconfigures string to the acceptable prompt formats
        ex. <c_name>.show(<id>) translate to show <class name> <id> """
        p = r"^(\w*)\.(\w+)(?:\(([^)]*)\))$"
        m = re.search(p, line)
        if not m:
            return line

        c_name = m.group(1)
        method = m.group(2)
        arg = m.group(3)
        string = False
        command = f"{method} {c_name}"
        if arg != "":
            id_arg = re.search('^"([^"]*)"(?:, (.*))?$', arg)
            if not id_arg:
                return line
            uuid = id_arg.group(1)
            string = id_arg.group(2)
            command += f" {uuid}"

        if method == 'update' and string:
            is_dict = re.search(r"^{.*}$", string)
            if is_dict:
                try:
                    a_dict = json.loads(string.replace("'", '"'))
                except (ValueError, Exception):
                    return line
                else:
                    return self.update_dict(command, a_dict)
            is_atr = re.search(r'^(?:"([^"]*)")?(?:, "?([^"]*)"?)?$', string)
            if is_atr:
                command += f" {is_atr.group(1) or ''} {is_atr.group(2) or ''}"

        return command

    def update_dict(self, line, a_dict):
        """Helper method for update() with a dictionary."""
        if line == "":
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[1] not in storage.classes():
                print("** class doesn't exit **")
            elif len(words) < 3:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(words[1], words[2])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    for k, v in a_dict.items():
                        setattr(storage.all()[key], k, v)
                    storage.all()[key].save()
        return ""


if __name__ == '__main__':
    HBNBCommand().cmdloop()

#!/usr/bin/python3
"""Module console
Serves as the entry point of the command interpreter"""

import json
import re
from models import storage
import cmd


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
            for k, v in storage.classes().items():
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
            for k, v in storage.classes().items():
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
            for k, v in storage.classes().items():
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

    def do_count(self, line):
        """retrieves the number of instances of a class"""
        if line is not None:
            words = line.split(' ')
        if not words[0]:
            print("** class name missing **")
        elif words[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            matches = [
                k for k in storage.all() if k.startswith(
                    words[0] + '.')]
            print(len(matches))

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
            for k, v in storage.classes().items():
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
                                cast = None
                                if not re.search('^".*"$', words[3]):
                                    if '.' in words[3]:
                                        cast = float
                                    else:
                                        cast = int
                                else:
                                    words[3] = words[3].replace('"', '')
                                try:
                                    words[3] = cast(words[3])
                                except (TypeError, ValueError):
                                    pass  # fine, stay a string
                                setattr(storage.all()[key], words[2],
                                        words[3])
                                storage.all()[key].save()
                                break
            if words[0] != k:
                print("** class doesn't exist **")

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
        command = "{} {}".format(method, c_name)
        if arg != "":
            id_arg = re.search('^"([^"]*)"(?:, (.*))?$', arg)
            if not id_arg:
                return line
            uuid = id_arg.group(1)
            string = id_arg.group(2)
            command += " {}".format(uuid)

        if method == ('update') and string:
            is_dict = re.search(r"^{.*}$", string)
            if is_dict:
                try:
                    a_dict = json.loads(string.replace("'", '"'))
                except (ValueError, Exception):
                    return line
                else:
                    return self.update_dict(command, a_dict)
            is_atr = re.search(r'^(?:"([^"]*)")?(?:, (.*))?$', string)
            if is_atr:
                command += " {} {}".format(is_atr.group(1) or '',
                                           is_atr.group(2) or '')
        self.onecmd(command)
        return command

    def default(self, line):
        """Catch commands if nothing else matches then."""
        # print("DEF:::", line)
        self.precmd(line)

    def update_dict(self, line, a_dict):
        """Helper method for the update() with a dictionary."""
        if line == "":
            print("** class name missing **")
        else:
            words = line.split(' ')
            if words[1] not in storage.classes():
                print("** class doesn't exist **")
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

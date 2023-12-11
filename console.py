#!/usr/bin/python3
"""Defines the HBNB"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def spliting(arg):
    c_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if c_braces is None:
        if brackets is None:
            return [n.strip(",") for n in split(arg)]
        else:
            y = split(arg[:brackets.span()[0]])
            rr = [n.strip(",") for n in y]
            rr.append(brackets.group())
            return rr
    else:
        y = split(arg[:c_braces.span()[0]])
        rr = [n.strip(",") for n in y]
        rr.append(c_braces.group())
        return rr


class HBNBCommand(cmd.Cmd):
    """Defines Hbnb cmd"""

    prompt = "(hbnb) "
    __classes = {
            "BaseModel",
            "User",
            "Place",
            "City",
            "Amenity",
            "State",
            "Review"
    }

    def emptyline(self):
        """Do nothing"""
        pass

    def default(self, arg):
        """Default"""
        ar = {
                "all": self.do_all,
                "count": self.do_count,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            a = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", a[1])
            if match is not None:
                c = [a[1][:match.span()[0]], match.group()[1:-1]]
                if c[0] in ar.keys():
                    ca = "{} {}".format(a[0], c[1])
                    return ar[c[0]](ca)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """command to exit"""
        return True

    def do_EOF(self, arg):
        """exit"""
        print("")
        return True

    def do_create(self, arg):
        """Create a new class"""
        a = spliting(arg)
        if len(a) == 0:
            print("** class name missing **")
        elif a[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(a[0])().id)
            storage.save()

    def do_show(self, arg):
        """ Prints the strin"""
        a = spliting(arg)
        ser_obj = storage.all()
        if len(a) == 0:
            print("** class name missing **")
        elif a[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(a) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(a[0], a[1]) not in ser_obj:
            print("** no instance found **")
        else:
            print(ser_objs["{}.{}".format(a[0], a[1])])

    def do_destroy(self, arg):
        """Deletes an instance"""
        a = spliting(arg)
        ser_obj = storage.all()
        if len(a) == 0:
            print("** class name missing **")
        elif a[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(a) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(a[0], a[1]) not in ser_obj.keys():
            print("** no instance found **")
        else:
            del ser_obj["{}.{}".format(a[0], a[1])]
            storage.save()

    def do_all(self, arg):
        """Prints all string"""
        a = spliting(arg)
        if len(a) > 0 and a[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            o = []
            for jj in storage.all().values():
                if len(a) > 0 and a[0] == jj.__class__.__name__:
                    o.append(jj.__str__())
                elif len(a) == 0:
                    o.append(jj.__str__())
            print(o)

    def do_count(self, arg):
        """gives the number of users"""
        a = spliting(arg)
        cc = 0
        for o in storage.all().values():
            if a[0] == o.__class__.__name__:
                cc += 1
        print(cc)

    def do_update(self, arg):
        """Updates an instance"""
        a = spliting(arg)
        ser_obj = storage.all()

        if len(a) == 0:
            print("** class name missing **")
            return False
        if a[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(a) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(a[0], a[1]) not in ser_obj.keys():
            print("** no instance found **")
            return False
        if len(a) == 2:
            print("** attribute name missing **")
            return False
        if len(a) == 3:
            try:
                type(eval(a[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(a) == 4:
            o = ser_obj["{}.{}".format(a[0], a[1])]
            if a[2] in o.__class__.__dict__.keys():
                v = type(o.__class__.__dict__[a[2]])
                o.__dict__[a[2]] = v(a[3])
            else:
                o.__dict__[a[2]] = a[3]
        elif type(eval(a[2])) == dict:
            o = ser_obj["{}.{}".format(a[0], a[1])]
            for kk, vv in eval(a[2]).items():
                if (kk in o.__class__.__dict__.keys() and
                            type(o.__class__.__dict__[kk]) in {str, int, float}):
                    v = type(o.__class__.__dict__[kk])
                    o.__dict__[kk] = v(vv)
                else:
                    o.__dict__[kk] = vv
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()

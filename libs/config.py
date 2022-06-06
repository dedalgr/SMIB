# -*- coding:utf-8 -*-
'''
Created on 27.04.2018 г.

@author: dedal
'''
# -*- coding:utf-8 -*-

import ConfigParser


class ConfWarning(ConfigParser.Error):
    pass


class ConfError(ConfigParser.Error):
    pass


class NotConfigFile(Exception):
    pass

class ConfigWithCoder(ConfigParser.ConfigParser):
    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        if self._defaults:
            fp.write("[%s]\n" % "DEFAULT")
            for (key, value) in self._defaults.items():
                fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key == "__name__":
                    continue
                if (value is not None) or (self._optcre == self.OPTCRE):
                    if type(value) == unicode:
                        value = ''.join(value).encode('utf-8')
                    else:
                        value = str(value)
                    value = value.replace('\n', '\n\t')
                    key = " = ".join((key, value))
                fp.write("%s\n" % (key))
            fp.write("\n")

class ConfFile():
    '''
    Работа с конфигурационен файл!

    Функции:
        __init__(confName)
        update_option(section, **option)
        add_section(section)
        add_option(section, **option)
        get(section, option = None, return_type = None)
        add_comment(section, comment)

    '''

    def __init__(self, confName, make_new=False):
        '''
        Параметри на инстанцията:
            self.parser
            self.file_name
        '''
        # Създава парсер
        if make_new == True:
            file(confName, 'a').close()

        self.parser = ConfigParser.ConfigParser(allow_no_value=True)
        try:
            var = open(confName, 'r')  # @UnusedVariable
        except IOError as e:
            raise NotConfigFile, e
        self.file_name = confName

    def update_option(self, section, **option):
        '''
        Променя опция в секция

        Използване:
            conf.update_option('section', Option='value')

        Връща:
            True
        '''
        self.parser.read(self.file_name)

        for i in option.keys():
            var = self.parser.has_option(section, i)
            if var == True:
                self.parser.set(section, i, option[i])

            else:
                raise ConfError, 'Option %s not exist!' % (i)
        myfile = open(self.file_name, 'w')
        self.parser.write(myfile)
        myfile.close()
        return True

    def add_section(self, section):
        '''
        Добавяне на секция!

        Използване:
            conf.add_section('SectionName')

        Връща:
            True
        '''
        self.parser.read(self.file_name)
        var = self.parser.has_section(section)
        if var == False:
            self.parser.add_section(section)
            myfile = open(self.file_name, 'w')
            self.parser.write(myfile)
            myfile.close()
            return True
        else:
            raise ConfWarning, 'Section %s already exist!' % (section)

    def add_option(self, section, **option):
        '''
        Добавя опция в секция!

        Използване:
            conf.add_option('Section', Option='value')

        Връща:
            True
        '''
        try:
            self.parser.read(self.file_name)
            for i in option.keys():
                var = self.parser.has_option(section, i)
                if var == False:
                    self.parser.set(section, i, option[i])
                    myfile = open(self.file_name, 'w')
                    self.parser.write(myfile)
                    myfile.close()

                else:
                    raise ConfWarning, 'Option %s already exist!' % (i)
        except UnboundLocalError:
            raise ConfError, 'Section %s is mising.' % (section)

        return True

    def get(self, section, option=None, return_type=None):
        '''
        Взима опция от конфиг файла!

        Използване:
            a = conf.get('test', 'name', return_type='float')
            По подразбиране return_type = стринг

            return_type приема:
                None, ini, float, bool, str
        Връща:
            в зависимост от подадения return_type
            връща стринг, цяло число, число с плаваща запетая
            или True, False

            Ако няма подадена опция връща речник във формат
            {'Option':'value'}
        '''
        self.parser.read(self.file_name)
        if option == None and return_type == None:
            var = self.parser.items(section)
            res = {}
            for i in var:
                res[i[0]] = i[1]
            return res
        elif option == None and return_type != None:
            raise ConfError, 'Not have selected option!'
        elif option != None and return_type == None:
            return self.parser.get(section, option)
        elif option != None and return_type == 'str':
            return self.parser.get(section, option)
        elif option != None and return_type == 'int':
            return self.parser.getint(section, option)
        elif option != None and return_type == 'float':
            return self.parser.getfloat(section, option)
        elif option != None and return_type == 'bool':
            return self.parser.getboolean(section, option)
        elif (return_type != 'int' or return_type != 'float' or return_type != 'bool'
              or return_type != None):
            raise ConfError, ('''Invalid return_type %s.
            Type must be (int, bool, float or None)''' % (return_type))

    def has_section(self, section):
        # self.parser.read(self.file_name)
        return self.parser.has_section(section)

    def has_option(self, section, option):
        self.parser.read(self.file_name)
        return self.parser.has_option(section, option)

    def remove_section(self, section):
        self.parser.read(self.file_name)
        if self.has_section(section) == False:
            raise ConfError, 'Section %s is mising.' % (section)
        else:
            self.parser.remove_section(section)
            myfile = open(self.file_name, 'w')
            self.parser.write(myfile)
            myfile.close()
        return True

    def remove_option(self, section, option):
        if self.has_option(section, option) == False:
            raise ConfError, 'Option %s is mising.' % (option)
        else:
            self.parser.remove_option(section, option)
            myfile = open(self.file_name, 'w')
            self.parser.write(myfile)
            myfile.close()
        return True

    def remove(self, section, option=None):

        if option == None:
            return self.remove_section(section)
        else:
            if self.has_option(section, option) == False:
                raise ConfError, 'Option %s is mising.' % (option)
            else:
                return self.remove_option(section, option)

    def add_comment(self, section, comment):
        '''
        Добавя коментари във конфиг файла!

        Използване:
            conf.add_comment('section', 'comment')

        Връща:
            True
        '''
        self.parser.read(self.file_name)
        if type(comment) == unicode:
            comment = ''.join(comment).encode('utf-8')
        self.parser.set(section, '\n;%s' % (comment))
        myfile = open(self.file_name, 'w')
        self.parser.write(myfile)
        myfile.close()
        return True


# if __name__ == '__main__':
    # CONF = ConfFile('/home/dedal/Colibri/SMIB/1_4/smib.conf')
    # print CONF.remove('SAS', 'aft')

class Log:
    """
    Provides a facility for indent-formatted console output which can be disabled/enabled.
    The indent and unindent methods control the indent level.  Strings printed with the
    record method will be printed indented, including if there are newlines in the strings.
    The output_stream argument of __init__ (as well as the set_output_stream method) can be
    specified as None to disable output.
    """
    def __init__ (self, output_stream):
        self.__output_stream = output_stream
        self.__indent_level = 0
        self.__just_printed_newline = False
    
    def output_stream (self):
        """Return the current output stream.  A return value of None indicates no output stream."""
        return self.__output_stream
    
    def set_output_stream (self, out):
        """Specify something that has a write method (e.g. sys.stdout), or None to disable output."""
        self.__output_stream = out
    
    def indent_level (self):
        """Returns the current indent level."""
        return self.__indent_level
    
    def record (self, string):
        """Prints the given string to the log, indenting as necessary."""
        if len(string) > 0:
            tabs = '\t'*self.__indent_level
            leading_tabs = tabs if self.__just_printed_newline else ''
            indented_string = leading_tabs + string[:-1].replace('\n', '\n'+tabs) + string[-1]
            if self.__output_stream != None:
                self.__output_stream.write(indented_string)
            self.__just_printed_newline = indented_string[-1] == '\n'
    
    def indent (self):
        """Increases the indent level of the log."""
        if not self.__just_printed_newline:
            self.__output_stream.write('\n')
            self.__just_printed_newline = True
        self.__indent_level += 1
    
    def unindent (self):
        """Decreases the indent level of the log."""
        assert self.__indent_level > 0, 'Tried to Log.unindent too many times.'
        if not self.__just_printed_newline:
            self.__output_stream.write('\n')
            self.__just_printed_newline = True
        self.__indent_level -= 1

    @staticmethod
    def run_unit_test ():
        import cStringIO
        output_stream = cStringIO.StringIO()
        log = Log(output_stream)
        log.record('A\n')
        log.indent()
        log.record('B\nC')
        log.record('D\nE\n')
        log.record('F\n\n\nG')
        log.indent()
        log.record('H\n')
        log.unindent()
        log.record('I\n')
        log.unindent()
        log.record('J')
        assert output_stream.getvalue() == 'A\n\tB\n\tCD\n\tE\n\tF\n\t\n\t\n\tG\n\t\tH\n\tI\nJ', 'Unit test failed.'
        # If it reached this point, the test passed.

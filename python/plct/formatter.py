import optparse, textwrap

# code for formatting optparse
class IndentedHelpFormatterWithNL(optparse.IndentedHelpFormatter):
    def format_description(self, description):
        if not description: return ""
        desc_width = self.width - self.current_indent
        indent = " "*self.current_indent
        # the above is still the same
        bits = description.split('\n')
        formatted_bits = [
            textwrap.fill(bit,
            desc_width,
            initial_indent=indent,
            subsequent_indent=indent)
            for bit in bits]
        result = "\n".join(formatted_bits) + "\n"
        return result

    def format_option_strings(self, option):
        if self.short_first:
            opts = option._short_opts + option._long_opts
        else:
            opts = option._long_opts + option._short_opts
        str = ", ".join(opts)

        if option.takes_value():
            metavar = option.metavar or option.dest.upper()
            str += " %s" % metavar

        return str

    def format_option(self, option):
        # The help for each option consists of two parts:
        #   * the opt strings and metavars
        #   eg. ("-x", or "-fFILENAME, --file=FILENAME")
        #   * the user-supplied help string
        #   eg. ("turn on expert mode", "read data from FILENAME")
        #
        # We put the help string on a second line.
        #   -fFILENAME, --file=FILENAME
        #       read data from FILENAME
        result = []
        opts = self.option_strings[option]
        opt_width = self.help_position - self.current_indent - 2
        opts = "%*s%s\n" % (self.current_indent, "", opts)
        indent_first = self.current_indent+2
        result.append(opts)
        if option.help:
            help_text = self.expand_default(option)
            help_lines = []
            for para in help_text.split("\n"):
##                help_lines.extend(textwrap.wrap(para, self.help_width))
                help_lines = textwrap.wrap(para, self.help_width)
                result.extend(["%*s%s\n" % (indent_first, "", line)
                               for line in help_lines])
        elif opts[-1] != "\n":
            result.append("\n")
        return "".join(result)

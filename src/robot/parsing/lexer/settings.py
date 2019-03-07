class Settings(object):
    names = ()
    aliases = {}
    multi_use = ()

    def __init__(self):
        self.settings = {n: False for n in self.names}

    def validate(self, name):
        upper = name.upper()    # TODO: Non-ASCII spaces
        if upper in self.aliases:
            upper = self.aliases[upper]
        if upper not in self.settings:
            raise ValueError("Invalid setting '%s'." % name)  # TODO: Hints?
        if self.settings[upper] and upper not in self.multi_use:
            raise ValueError("Setting '%s' allowed only once." % name)
        self.settings[upper] = True

    def reset(self):
        self.__init__()


class TestCaseFileSettings(Settings):
    names = (
        'DOCUMENTATION',
        'SUITE SETUP',
        'SUITE TEARDOWN',
        'METADATA',
        'TEST SETUP',
        'TEST TEARDOWN',
        'TEST TEMPLATE',
        'TEST TIMEOUT',
        'FORCE TAGS',
        'DEFAULT TAGS',
        'LIBRARY',
        'RESOURCE',
        'VARIABLES'
    )
    aliases = {
        'TASK SETUP': 'TEST SETUP',
        'TASK TEARDOWN': 'TEST TEARDOWN',
        'TASK TEMPLATE': 'TEST TEMPLATE',
        'TASK TIMEOUT': 'TEST TIMEOUT',
    }
    multi_use = (
        'METADATA',
        'LIBRARY',
        'RESOURCE',
        'VARIABLES'
    )


# FIXME: Implementation missing. Need to check what settings are supported.
class InitFileSettings(Settings):
    pass


class ResourceFileSettings(Settings):
    names = (
        'DOCUMENTATION',
        'LIBRARY',
        'RESOURCE',
        'VARIABLES'
    )
    multi_use = (
        'LIBRARY',
        'RESOURCE',
        'VARIABLES'
    )


class TestCaseSettings(Settings):
    names = (
        'DOCUMENTATION',
        'SETUP',
        'TEARDOWN',
        'TEMPLATE',
        'TIMEOUT',
        'TAGS'
    )

    def __init__(self, parent):
        Settings.__init__(self)
        self.parent = parent

    def validate(self, name):
        Settings.validate(self, name[1:-1].strip())

    @property
    def template_set(self):
        # FIXME: Should look at the values as well
        return (self.settings['TEMPLATE'] or
                self.parent.settings['TEST TEMPLATE'])


class KeywordSettings(Settings):
    names = (
        'DOCUMENTATION',
        'ARGUMENTS',
        'TEARDOWN',
        'TIMEOUT',
        'TAGS',
        'RETURN'
    )

    def validate(self, name):
        Settings.validate(self, name[1:-1].strip())

class Environment:
    """Stores all name-value bindings: variables, functions, classes."""

    def __init__(self, enclosing=None):
        """The global environment has no enclosing environment, thus its enclosing is None.
        Otherwise, enclosing is the environment enclosing the current environment"""
        self.enclosing = enclosing
        self.bindings = {}

    def define(self, name, value):
        """Adds new identifier/name to environment."""
        self.bindings[name] = value

    def assign(self, name, value):
        """Updates existing identifier/name in (enclosing) environment."""
        name_in_scope = name in self.bindings
        if name_in_scope:
            self.bindings[name] = value
            return

        non_global_env = self.enclosing is not None
        if non_global_env:
            self.enclosing.assign(name, value)
            return

        print(
            "Can't (re-)assign undefined variable {}. Define thus: var {}; or var {} = <value>;".format(
                name, name, name
            )
        )

    def get(self, name):
        """Retrieves existing identifier/name from (enclosing) environment."""
        name_in_scope = name in self.bindings
        if name_in_scope:
            value = self.bindings.get(name)
            value_not_set = value is None
            if value_not_set:
                # can only get values that have been assigned or initialized.
                print(
                    "Can't access uninitialized/unassigned variable {}. Initialize thus: {} = <value>".format(
                        name, name
                    )
                )

            return value

        non_global_env = self.enclosing is not None
        if non_global_env:
            return self.enclosing.get(name)

        print(
            "Can't get undefined variable {}. Define thus: var {}; or var {} = <value>;".format(
                name, name, name
            )
        )

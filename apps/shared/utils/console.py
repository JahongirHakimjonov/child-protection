from django.core import management


class Console(management.BaseCommand):
    def get_stdout(self):
        base_command = management.BaseCommand()
        return base_command.stdout

    def get_style(self):
        base_command = management.BaseCommand()
        return base_command.style

    def success(self, message):
        self.get_stdout().write(self.get_style().SUCCESS(message))

    def error(self, message):
        self.get_stdout().write(self.get_style().ERROR(message))

    def log(self, message):
        self.get_stdout().write(
            self.get_style().ERROR(
                "\n====================\n{}\n====================\n".format(message)
            )
        )

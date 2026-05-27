import sys


class cryptoException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(str(error_message))
        self.error_message = self.get_detailed_error_message(
            error_message,
            error_detail
        )

    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()

        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno

            return (
                f"Error occurred in python script: [{file_name}] "
                f"line number: [{line_number}] "
                f"error message: [{error_message}]"
            )

        return str(error_message)

    def __str__(self):
        return self.error_message
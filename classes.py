import datetime


# Class for customer data
class DataForm:
    def __init__(self, priority_number, customer_name, transaction_type, additional_remarks):
        self.priority = priority_number
        self.name = customer_name
        self.date = str(datetime.datetime.now())
        self.transaction = transaction_type
        self.remarks = additional_remarks

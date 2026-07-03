class Transaction:

    def __init__(

        self,

        transaction_id,

        transaction_type,

        amount,

        description,

        category,

        transaction_date

    ):

        self.transaction_id = transaction_id

        self.transaction_type = transaction_type

        self.amount = amount

        self.description = description

        self.category = category

        self.transaction_date = transaction_date


    def __str__(self):

        return (

            f"ID: {self.transaction_id} | "

            f"{self.transaction_type.title()} - "

            f"£{self.amount:.2f} - "

            f"{self.description} "

            f"({self.category}) "

            f"[{self.transaction_date}]"

        )
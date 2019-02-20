class House():
    """
        House class that corresponds to the essential information of a house.
        It could be mapped as a row of the table in the database.
    """

    def __init__(self, id, streetAddress=None, status=None, date=None, lastListedPrice=None,
                 numBed=None, numBath=None, size=None):
        self.id = id
        self.streetAddress = streetAddress
        self.status = status
        self.date = date
        self.lastListedPrice = lastListedPrice
        self.numBed = numBed
        self.numBath = numBath
        self.size = size

class Config:
    """ What user wants to switch on or off

    currently only if median shall be produced
    """

    def __init__(self):
        self.do_median_computation = False
        # Ensure events are triggered

    def request_median_computation(self, request: bool):
        self.do_median_computation = request

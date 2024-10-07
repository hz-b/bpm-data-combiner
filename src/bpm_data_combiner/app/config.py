from ..bl.event import Event


class Config:
    """ What user wants to switch on or off

    currently only if median shall be produced
    """

    def __init__(self):
        self.on_median_computation_request = Event(name="median-computation")
        self.do_median_computation = False
        # Ensure events are triggered
        self.request_median_computation(self.do_median_computation)

    def request_median_computation(self, request: bool):
        self.do_median_computation = request
        self.on_median_computation_request.trigger(self.do_median_computation)
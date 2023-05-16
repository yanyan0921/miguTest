class TestCaseInfo(object):

    def __init__(self, test_id = "", name = "", owner = "", result = "Failed", start = "", end = "", error_info = ""):
        self.id = test_id
        self.name = name
        self.owner = owner
        self.result = result
        self.start = start
        self.end = end
        self.info = error_info
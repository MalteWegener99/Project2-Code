class Sample:
    '''
    Container for saving a sample in time
    time: uint: YearE3 + day
    '''
    def __init__(self, name, time, pos, mat):
        self.name = name
        self.time = time
        self.pos = pos
        self.mat = mat

    def __str__(self):
        return "{} was on position {} on {} \r\n with deviations: \r\n{}"\
                .format(self.name, self.xyz, self.time, self.mat)

class Sample_conv:
    '''
    Container for saving a sample in time
    time: uint: YearE3 + day
    '''
    def __init__(self, name, time, pos, err):
        self.name = name
        self.time = time
        self.pos = pos
        self.err = err

    def __str__(self):
        return "{} was on position {} on {} \r\n with deviations: \r\n{}"\
                .format(self.name, self.xyz, self.time, self.err)
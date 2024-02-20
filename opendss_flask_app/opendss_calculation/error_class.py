class NoConvergedError(Exception):
    """计算不收敛时抛出的异常"""
    def __init__(self, hour):
        self.hour = hour
        self.message = f'第{hour}个小时的计算不收敛'
        super().__init__(self.message)
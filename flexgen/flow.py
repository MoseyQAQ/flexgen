

'''
class设计：
flow定义了一次active learning的基本流程：模型训练（training）、模型评估（test）、采样（sample）、标记（label）；

1. init函数：定义这次迭代的基本信息
    接受参数：   training_list: list[Train对象]，需要执行的训练任务列表
                test_list: list[Test对象]，需要执行的测试任务列表
                sample_list: list[Sample对象]，需要执行的采样任务列表
                label_list: Label对象
    init函数执行时，自动读取working path下的record.flexgen文件，它记录了上次迭代运行的信息

2. run：执行一次迭代，按照training、test、sample、label的顺序执行任务列表中的任务
    run函数执行时，会自动执行training_list中的训练任务，然后执行test_list中的测试任务，然后执行sample_list中的采样任务，最后执行label任务
    每次执行任务时，都会将任务的信息记录到record.flexgen文件中

3. load_record：读取record.flexgen文件，获取上次迭代的信息


'''

class Flow:
    def __init__(self) -> None:
        raise NotImplementedError
    
    def load_record(self) -> None:
        raise NotImplementedError
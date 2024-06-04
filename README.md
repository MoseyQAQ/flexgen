# flexgen
A flexible machine learning potential generator.

TODO：

1. arch. design (flex, and expandable). I plan use DPDispachter
2. achieve a standard DPGEN workflow
3. support new sample methods (e.g. ASE,vacancy, classical potential MD sample) and configurations select methods.
4. support new label methods (DPA2)


软件运行设计：
在当前工作目录下，执行python3 myflow.py来执行一次迭代；

myflow.py中实例化了Flow对象，规定了一次迭代应该如何运行。

首先程序会先检测上次迭代是否正常运行完成。若完成，则开始新的一轮迭代，若没有完成，则继续上一轮进行。

对于新的迭代，按照顺序执行：sample，label，train，test（如果是第一次迭代，则执行：train，test，sample，label，train，test）
其中：sample规定了如何采样（基于ASE脚本、DPA2、LMP），label规定了用什么label（VASP ABACUS DPA2），train规定了如何训练（基于DeepMD-kit），test规定了如何测试（基于ASE traj），test是可跳过的
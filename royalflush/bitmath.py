#!/usr/bin/env python
# -*- coding: utf-8 -*-

def last_bit(x):
    """求最后一位是0还是1
    解: 跟1求 位与
    """
    return x & 1

def last_k_bit(x, k):
    """求倒数第k位是0还是1
    解: 跟100...0 (k-1个0) 求位与, 看是不是等于0
    """
    return (x & 1 << (k - 1)) == 0

def is_two_power(x):
    """检查是否是2的整数幂
    解: 跟 -1 的值求 位与, 如果为0说明是
    """
    return (x & (x - 1)) == 0

def howmany_one(x):
    """求一共有多少位是1
    解: 利用 x &= x - 1 每次消除一位最后的1的特性
    """
    ans = 0
    while x:
        ans += 1
        x &= x - 1
    return ans

def howmany_different(x, y):
    """求有多少位不相同
    解: 先位异或, 然后求1的个数
    """
    difference = x ^ y
    ans = 0
    while difference:
        ans += 1
        difference &= difference - 1
    return ans

def create_bitmap(array):
    """生成集合的bitmap
    Example:
        Array = [1, 3, 5]
        Bitmap = 10101
    """
    x = 0
    for i in array:
        x += 1 << (i-1)
    return x

def parse_bitmap(x):
    """根据bitmap, 解析出集合
    Example:
        Bitmap = 10101
        Array = [1, 3, 5]
    """
    array = list()
    counter = 1
    while x:
        if x & 1:
            array.append(counter)
        x = x >> 1
        counter += 1
    return array

def union_bitmap(x, y):
    """求x, y的交集, x, y是集合各自的bitmap
    """
    return x | y

def intersect_bitmap(x, y):
    """求并集, x, y是集合各自的bitmap
    """
    return x & y

def difference_bitmap(x, y):
    """从x中丢弃所有y中的元素, x, y是集合各自的bitmap
    """
    return x & (~ y)


if __name__ == "__main__":
    from angora.GADGET import Timer
    import random
    
    timer = Timer()
    complexity = 1000
    
    x = set([1, 7, 8, 19, 24])
    y = set([5, 8, 19, 33, 67])
    x1 = create_bitmap(x)
    y1 = create_bitmap(y)
    
    timer.start()
    for i in range(1000):
        x.difference(y)
    timer.timeup()
    
    timer.start()
    for i in range(1000):
        x1 & (~ y1)
    timer.timeup()
    
    x = random.randint(0, 2**32)
    timer.start()
    for i in range(complexity):
        last_bit(x)
    timer.stop()
    print("last_bit elapse %.6f seconds" % timer.elapse)
    
    x = random.randint(0, 2**32)
    timer.start()
    for i in range(complexity):
        last_k_bit(x, 44)
    timer.stop()
    print("last_k_bit elapse %.6f seconds" % timer.elapse)
    
    x = random.randint(0, 2**32)
    timer.start()
    for i in range(complexity):
        howmany_one(x)
    timer.stop()
    print("howmany_one elapse %.6f seconds" % timer.elapse)
    
    x = 8237548927358942735
    y = 1738575893482930758
    timer.start()
    for i in range(complexity):
        howmany_different(x, y)
    timer.stop()
    print("howmany_different elapse %.6f seconds" % timer.elapse)
    
    array = [1, 6, 17, 22, 37, 48]
    timer.start()
    for i in range(complexity):
        create_bitmap(array)
    timer.stop()
    print("create_bigmap elapse %.6f seconds" % timer.elapse)
    
    x = random.randint(0, 2**32)
    timer.start()
    for i in range(complexity):
        parse_bitmap(x)
    timer.stop()
    print("parse_bitmap elapse %.6f seconds" % timer.elapse)
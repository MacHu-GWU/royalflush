
temp = """
    <div> 
        <img src="%s.png">
        <input type="radio" name="c_%s" value="0" checked="checked" />不用
        <input type="radio" name="c_%s" value="1" />手牌
        <input type="radio" name="c_%s" value="2" />公牌
        <img src="%s.png">
        <input type="radio" name="c_%s" value="0" checked="checked" />不用
        <input type="radio" name="c_%s" value="1" />手牌
        <input type="radio" name="c_%s" value="2" />公牌
        <img src="%s.png">
        <input type="radio" name="c_%s" value="0" checked="checked" />不用
        <input type="radio" name="c_%s" value="1" />手牌
        <input type="radio" name="c_%s" value="2" />公牌
        <img src="%s.png">
        <input type="radio" name="c_%s" value="0" checked="checked" />不用
        <input type="radio" name="c_%s" value="1" />手牌
        <input type="radio" name="c_%s" value="2" />公牌
    </div>
"""
for i in range(2, 14+1):
    a = list()
    
    a.append(i*4+1)
    a.append(i*4+1)
    a.append(i*4+1)
    a.append(i*4+1)
    a.append(i*4+2)
    a.append(i*4+2)
    a.append(i*4+2)
    a.append(i*4+2)
    a.append(i*4+3)
    a.append(i*4+3)
    a.append(i*4+3)
    a.append(i*4+3)
    a.append(i*4+4)
    a.append(i*4+4)
    a.append(i*4+4)
    a.append(i*4+4)
    print(temp % tuple(a))
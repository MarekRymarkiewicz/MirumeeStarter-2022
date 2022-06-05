def backward_string_by_word(text: str) -> str:
    if len(text) == 0:
        return ''
    
    words = text.split()
    
    result = words[0][::-1]
    if len(words) == 1:
        return result
    text = text.lstrip(result)
    
    for word in words[1::]:
        result += text[:text.find(text.lstrip()):]
        result += word[::-1]
        text = text.lstrip()
        text = text.lstrip(word)
        
    return result
    


if __name__ == '__main__':
    print("Example:")
    print(backward_string_by_word('123 abc'))

    # These "asserts" are used for self-checking and not for an auto-testing
    assert backward_string_by_word('') == ''
    assert backward_string_by_word('world') == 'dlrow'
    assert backward_string_by_word('hello world') == 'olleh dlrow'
    assert backward_string_by_word('hello   world') == 'olleh   dlrow'
    assert backward_string_by_word('welcome to a game') == 'emoclew ot a emag'
    print("Coding complete? Click 'Check' to earn cool rewards!")
def price_processing(price):
    
    # length = len(price)
    # int(length/3)
    arr = ([price[::-1][i:i + 3] for i in range(0, len(price[::-1]), 3)])
    arr = list(reversed(arr))
    price = '.'.join(arr)
    return price
    
    
    
    

price_processing('1300200')
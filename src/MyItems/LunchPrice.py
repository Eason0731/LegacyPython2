import os

def CalcPrice(OPrice,People,DFee,Discount):
    print "The price after discount is : " + str( float(OPrice) + float(DFee)/float(People) - float(Discount)/float(People) )

if __name__ == '__main__':
    while 1:
        OPrice = raw_input("Please input original price: ")
        if OPrice.isalpha():
            print "It is not a number , pleae input again"
        elif not OPrice.strip():
            print "Cannot input empty infos , pleae input again"
        else:
            break

    while 1:
        People = raw_input("Please input number of people: ")
        if People.isalpha():
            print "It is not a number , pleae input again"
        elif not People.strip():
            print "Cannot input empty infos , pleae input again"
        else:
            break

    while 1:
        DFee = raw_input("Please input delivery fee: ")
        if DFee.isalpha():
            print "It is not a number , pleae input again"
        elif not DFee.strip():
            print "Cannot input empty infos , pleae input again"
        else:
            break

    while 1:
        Discount = raw_input("Please input total discount price: ")
        if Discount.isalpha():
            print "It is not a number , pleae input again"
        elif not Discount.strip():
            print "Cannot input empty infos , pleae input again"
        else:
            break
    
    CalcPrice(OPrice,People,DFee,Discount)
        

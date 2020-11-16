def generate_item(Barcode = 0,Name = "",Volume = 0,Type = "",Amount = 0):
    item ={
            "Barcode": Barcode,
            "Name": Name,
            "Volume": Volume,
            "Type": Type,
            "Amount": Amount
    }
    return item


def generate_item_for_regestry(Barcode = 0,Name = "",Volume = 0,Type = "",Amount = 0):
        item= {}
        item[str(Barcode)] ={
            "Barcode": Barcode,
            "Name": Name,
            "Volume": Volume,
            "Type": Type,
            "Amount": Amount
        }
        return item
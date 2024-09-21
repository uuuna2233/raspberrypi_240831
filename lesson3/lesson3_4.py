id1 = 4
def test(id1=id1, id2=4, *, id3=3):
    # global id1
    print(id1/id2)

test(id2=2)
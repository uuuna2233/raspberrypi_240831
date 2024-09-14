import widget

while True:
    kg=0  #清除變數
    cm=0  #清除變數

    cm,kg = widget.input_data() 
    bmi = widget.calculate_bmi(cm,kg)
    status = widget.get_status(bmi)
    
    print(f'身高={cm},體重={kg}')
    print(f'bmi={bmi}')
    print(status)

    
    play_again = input("還要繼續嗎?(y,n)")
    if play_again in ["N","n"]:
        break

print('程式結束')

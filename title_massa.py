import sys
import traceback

def title_m(ttext, price, discont ):
    list_else = []  # список штучных товаров
    try:
           # словарь с результатами для товаров с массой
        if ttext[-2:] == 'кг' and ttext[-3:-2] == ' ' and ttext[-6:-5] == ' ' and ttext[-12:-5] != ' шт по ':  # 30 кг
            massa = float(ttext[-5:-2].strip().replace(',', '.'))
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','if1', 'price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-2:] == 'кг' and ttext[-3:-2] != ' ' and ttext[-4:-3] == ' 'and ttext[-11:-5] != 'шт по ':         # 3кг
            massa = float(ttext[-3:-2].strip().replace(',', '.'))
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','elif2',price_kg, price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-3:] == 'кг.' and ttext[-4:-3] != ' ' and ttext[-11:-5] != 'шт по ' and ttext[-6:-5] == ' ':             # 15кг.
            massa = float(ttext[-5:-3].strip().replace(',', '.'))
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','elif3','price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-2:] == 'кг' and ttext[-3:-2] == ' ' and ttext[-5:-4] == ' ':                                     # 3 кг
            massa = float(ttext[-4:-3].strip().replace(',', '.'))
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','elif4','price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-2:] == 'кг' and ttext[-3:-2] == ' ' and ttext[-7:-6] == ' ' and ttext[-12:-10] != 'шт':         # 1,5 кг
            massa = float(ttext[-6:-2].strip().replace(',', '.'))
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','elif5','price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-2:] == 'кг' and ttext[-3:-2] != ' ' and ttext[-7:-6] == ' ':                                     # 0.75кг
            massa = float(ttext[-6:-2].strip().replace(',', '.'))
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','elif6','price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-2:] == 'кг' and ttext[-3:-2] != ' ' and ttext[-6:-5] == ' ':                                     # 0.7кг
            massa = float(ttext[-5:-2].strip().replace(',', '.'))
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','elif7','price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-2:-1] == ' ' and ttext[-1:] == 'г' and ttext[-11:-5] != 'шт по ':                                    # 750 г
            massa = float(ttext[-5:-2].strip().replace(',', '.')) / 1000
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','elif8','price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-2:-1] == ' ' and ttext[-1:] == 'г'and ttext[-11:-5] != 'шт по ':                                       # 7500 г
            massa = float(ttext[-6:-2].strip().replace(',', '.')) / 1000
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','elif9','price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-2:] == 'кг' and ttext[-5:-4] == ' 'and ttext[-11:-5] != 'шт по ':                                    # 10кг
            massa = float(ttext[-4:-2])
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','elif10', 'price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-5:-4] == ' ' and ttext[-1:] == 'г' and ttext[-11:-5] != 'шт по ':                                         # 750г
            massa = float(ttext[-4:-1].strip().replace(',', '.')) / 1000
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','elif11', 'price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-6:-5] == ' ' and ttext[-2:] == 'г.'and ttext[-11:-5] != 'шт по ':                                       # 750г.
            massa = float(ttext[-5:-2].strip().replace(',', '.')) / 1000
            price_kg = round((float(price) - float(discont)) / massa)
            print('title massa','elif12', 'price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-7:-6] == ' ' and ttext[-2:] == 'г.' and ttext[-3:-2] == ' 'and ttext[-11:-5] != 'шт по ':           # 750 г.
            massa = float(ttext[-6:-3].strip().replace(',', '.')) / 1000
            price_kg = round((float(price) - float(discont)) / massa)
            print('title massa','elif13', 'price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-6:-5] == ' ' and ttext[-1:] == 'г' and ttext[-5:-3] != ' ' and ttext[-11:-5] != 'шт по ':               # 7500г
            massa = float(ttext[-5:-1].strip().replace(',', '.')) / 1000
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','elif14','price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-4:-3] == ' ' and ttext[-1:] == 'г'and ttext[-11:-5] != 'шт по ':                                        # 75г
            massa = float(ttext[-3:-1].strip().replace(',', '.')) / 1000
            price_kg = round((float(price) - float(discont)) / massa)
            #res_dict[price_kg] = 'руб/кг' + ttext + ' ' + price.strip() + ' руб, бонусы ' + discont + ' ' 
            print('title massa','elif15','price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-7:-6] == ' ' and ttext[-2:] == 'гр'and ttext[-11:-5] != 'шт по ':                                       # 200 гр
            massa = float(ttext[-6:-3].strip().replace(',', '.')) / 1000
            price_kg = round((float(price) - float(discont)) / massa)
            print('title massa','elif16','price_kg', price_kg, 'ttext', ttext, 'price',price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-6:-5] == ' ' and ttext[-2:] == 'гр' and ttext[-11:-5] != 'шт по 'and ttext[-3:-2] != ' ':  # 200гр
            massa = float(ttext[-6:-2].strip().replace(',', '.')) / 1000
            price_kg = round((float(price) - float(discont)) / massa)
            print('title massa', 'elif17', 'price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-2:]=='шт' and ttext[-8:-5]=='кг,' and ttext[-13:-12]==' ':                                  #'2,5 кг, 2 шт'
            massa = int(ttext[-4:-3])*float(ttext[-12:-9].replace(',','.'))
            price_kg=round((float(price) - float(discont)) / massa)
            print('title massa','elif18', 'price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-2:] == 'шт' and ttext[-8:-5] == 'кг,' and ttext[-12:-11] == ' ':                                 # '25 кг, 2 шт'
            massa = int(ttext[-4:-3]) * float(ttext[-11:-9])
            price_kg = round((float(price) - float(discont)) / massa)
            print('title massa','elif19', 'price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-2:] == 'кг' and ttext[-12:-5] == ' шт по ' and ttext[-14:-13] == ' ':                        # '2 шт по 15 кг'
            massa = int(ttext[-13:-12]) * float(ttext[-5:-3])
            price_kg = round((float(price) - float(discont)) / massa)
            print('title massa','elif20', 'price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-2:] == 'кг' and ttext[-12:-10] == 'шт' and ttext[-14:-13] == ' ':                           # '2 шт по 1,5 кг'
            massa = int(ttext[-14:-13]) * float(ttext[-6:-3].replace(',','.'))
            price_kg = round((float(price) - float(discont)) / massa)
            print('title massa','elif21', 'price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-1:] == 'г' and ttext[-11:-5] == 'шт по ' and ttext[-14:-13] == ' ':                          # '12шт по 600 г'
            massa = int(ttext[-13:-11]) * float(ttext[-5:-2].replace(',', '.')/1000)
            price_kg = round((float(price) - float(discont)) / massa)
            print('title massa', 'elif22','price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont
        elif ttext[-3:] == 'кг)' and ttext[-4:-3] == ' ':  # '(12 кг)'
            massa = float(ttext[-6:-4].replace(',', '.') / 1000)
            price_kg = round((float(price) - float(discont)) / massa)
            print('title massa','elif23', 'price_kg', price_kg, 'ttext', ttext, 'price', price, 'discont', discont)
            return price_kg, ttext, price, discont



        else:  # если условия не выполняются, т.е. для штучных товаров
            list_else.append(ttext)
            print('list_else',list_else)

            return price, ttext, discont
    except:
        print("error title_massa", ttext+ '\n',traceback.format_exc(), str(sys.exc_info()))

if __name__ == '__main__':
    title_m(ttext='Сухой натуральный полнорационный корм BOWL WOW с индейкой и яблоком для взрослых кошек 400 г.',price='1000',discont='200')

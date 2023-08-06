from model import Model
from carteira import get_list
import pandas as pd

final_list = []
carteira = get_list('US')

for i in carteira:
    try:
        model = Model(i)

        final_balance, trade_history = model.analyze_strategy()
        formatted_balance = '{:,.2f}'.format(final_balance)

        print(i)
        print("Initial Balance: 100,000.00")
        print("Final Balance:", formatted_balance) 
        print('::::::::::::::::::::::::::::::::::::')
        print('::::::::::::::::::::::::::::::::::::')

        final_list.append((i, 100000, final_balance, ((final_balance/100000)*100)-100))
    
    except Exception as e:
        print(str(i) + " ::: " + str(e))
        pass

final_list = pd.DataFrame(final_list)
final_list.to_excel('model.xlsx')


    # for trade in trade_history:
    #     print(trade)
        
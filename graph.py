import matplotlib.pyplot as plt

from sql_queries import connect_to_DB, disconnect_from_DB, execute_query


def draw_graph():
    connection = connect_to_DB()

    fig = plt.figure(figsize=(9, 6))
    gold_ax = fig.add_subplot(2, 2, 1)
    silver_ax = fig.add_subplot(2, 2, 2)
    platinum_ax = fig.add_subplot(2, 2, 3)
    palladium_ax = fig.add_subplot(2, 2, 4)

    gold_data = execute_query(connection, query="SELECT price_to_buy, price_to_sell FROM precious_metals WHERE name = 'Золото'", return_info=True)
    silver_data = execute_query(connection, query="SELECT price_to_buy, price_to_sell FROM precious_metals WHERE name = 'Серебро'", return_info=True)
    platinum_data = execute_query(connection, query="SELECT price_to_buy, price_to_sell FROM precious_metals WHERE name = 'Платина'", return_info=True)
    palladium_data = execute_query(connection, query="SELECT price_to_buy, price_to_sell FROM precious_metals WHERE name = 'Палладий'", return_info=True)
    print(gold_data)
    print(silver_data)
    print(platinum_data)
    print(palladium_data)
    
    gold_ax.plot()

    fig.show()
    input()

draw_graph()
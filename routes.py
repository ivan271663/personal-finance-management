from flask import render_template, request, redirect, url_for
from datetime import datetime
import matplotlib.pyplot as plt
import os
from database import get_db_connection

CHART_DIR = os.path.join('static', 'charts')
os.makedirs(CHART_DIR, exist_ok=True)

def setup_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/transactions', methods=['GET', 'POST'])
    def transactions():
        conn = get_db_connection()
        transactions = conn.execute('SELECT * FROM transactions ORDER BY date DESC').fetchall()
        conn.close()

        if request.method == 'POST':
            amount = float(request.form['amount'])
            category = request.form['category']
            transaction_type = request.form['type']
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            conn = get_db_connection()
            conn.execute(
                'INSERT INTO transactions (amount, category, type, date) VALUES (?, ?, ?, ?)',
                (amount, category, transaction_type, date)
            )
            conn.commit()
            conn.close()


        return render_template('transactions.html', transactions=transactions)

    @app.route('/statistics')
    def statistics():
        current_month = datetime.now().month
        current_year = datetime.now().year

        conn = get_db_connection()
        query = '''
            SELECT category, SUM(amount) as total
            FROM transactions
            WHERE type = 'expense'
              AND strftime('%Y', date) = ?
              AND strftime('%m', date) = ?
            GROUP BY category
        '''
        expenses = conn.execute(query, (str(current_year), f'{current_month:02d}')).fetchall()
        conn.close()



        # Преобразуем результаты в список словарей для Jinja2
        expenses_list = [{'category': row['category'], 'amount': row['total']} for row in expenses]

        # Создаём диаграмму
        categories = [row['category'] for row in expenses_list]
        amounts = [row['amount'] for row in expenses_list]

        chart_path = os.path.join(CHART_DIR, 'expenses_chart.png')

        if categories and amounts:  # Проверяем, есть ли данные для диаграммы
            plt.figure(figsize=(8, 8))
            plt.pie(amounts, labels=categories, autopct='%1.1f%%')
            plt.title(f'Расходы за {current_month}.{current_year}')
            plt.savefig(chart_path)
            plt.close()
        else:
            # Создаём заглушку, если данных нет
            plt.figure(figsize=(8, 8))
            plt.text(0.5, 0.5, 'Нет данных за текущий месяц',
                       ha='center', va='center', fontsize=14)
            plt.axis('off')  # Убираем оси
            plt.savefig(chart_path)
            plt.close()



        current_month = datetime.now().month
        current_year = datetime.now().year

        conn1 = get_db_connection()
        query1 = '''
                    SELECT category, SUM(amount) as total
                    FROM transactions
                    WHERE type = 'income'
                      AND strftime('%Y', date) = ?
                      AND strftime('%m', date) = ?
                    GROUP BY category
                '''
        incomes = conn1.execute(query1, (str(current_year), f'{current_month:02d}')).fetchall()
        conn1.close()



        # Преобразуем результаты в список словарей для Jinja2
        incomes_list = [{'category': row['category'], 'amount': row['total']} for row in incomes]

        # Создаём диаграмму
        categories1 = [row['category'] for row in incomes_list]
        amounts1 = [row['amount'] for row in incomes_list]

        chart_path1 = os.path.join(CHART_DIR, 'incomes_chart.png')

        if categories and amounts:  # Проверяем, есть ли данные для диаграммы
            plt.figure(figsize=(8, 8))
            plt.pie(amounts1, labels=categories1, autopct='%1.1f%%')
            plt.title(f'доходы за {current_month}.{current_year}')
            plt.savefig(chart_path1)
            plt.close()
        else:
            # Создаём заглушку, если данных нет
            plt.figure(figsize=(8, 8))
            plt.text(0.5, 0.5, 'Нет данных за текущий месяц',
                     ha='center', va='center', fontsize=14)
            plt.axis('off')  # Убираем оси
            plt.savefig(chart_path1)
            plt.close()

        return render_template('statistics.html', chart_url=chart_path, chart_url1 =chart_path1, expenses=expenses_list, incomes=incomes_list)

from flask import Flask, render_template, request, redirect, url_for, flash
from dbfunctions import *

app = Flask(__name__)
app.secret_key = "!@#@!#!"

@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    return response

@app.route('/')
def index():
    books = get_all_books()
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book_route():
    isbn = request.form['isbn']
    title = request.form['title']
    author = request.form['author']
    copyright_year = request.form['copyright']
    edition = request.form['edition']
    price = float(request.form['price'])
    qty = int(request.form['qty'])
    total = price * qty

    if get_book_by_isbn(isbn):
        flash("ISBN already exists!", "danger")
        return redirect(url_for('index'))

    add_book(isbn, title, author, copyright_year, edition, price, qty, total)
    flash("Book added successfully!")
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book_route(id):
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        copyright_year = request.form['copyright']
        edition = request.form['edition']
        price = float(request.form['price'])
        qty = int(request.form['qty'])
        total = price * qty

        existing_book = get_book_by_isbn(isbn)
        if existing_book and existing_book['id'] != id:
            flash("ISBN already exists!", "danger")
            return redirect(url_for('edit_book_route', id=id))

        update_book(id, isbn, title, author, copyright_year, edition, price, qty, total)
        flash("Book updated successfully!")
        return redirect(url_for('index'))
    
    book = get_book_by_id(id)
    return render_template('edit.html', book=book)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_book_route(id):
    delete_book(id)
    flash("Book deleted successfully!")
    return redirect(url_for('index'))

@app.route('/confirm_delete/<int:id>', methods=['GET', 'POST'])
def confirm_delete(id):
    book = get_book_by_id(id)

    if request.method == 'POST':
        delete_book(id)
        flash("Book deleted successfully!")
        return redirect(url_for('index'))

    return render_template('confirm_delete.html', book=book)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

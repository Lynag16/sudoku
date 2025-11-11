from flask import Flask, render_template, request, redirect, url_for, session
import random, copy
from sudoku import generate_full_board, make_puzzle, solve

app = Flask(__name__)
app.secret_key = "sudoku_secret_key"

@app.route("/")
def index():
    if "puzzle" not in session:
        full = generate_full_board()
        puzzle = make_puzzle(full)
        session["solution"] = full
        session["puzzle"] = puzzle
    else:
        puzzle = session["puzzle"]
    return render_template("index.html", board=puzzle)

@app.route("/move", methods=["POST"])
def move():
    r = int(request.form["row"])
    c = int(request.form["col"])
    val = request.form.get("val")
    puzzle = session.get("puzzle")
    solution = session.get("solution")

    if val and val.isdigit():
        val = int(val)
        if solution[r][c] == val:
            puzzle[r][c] = val
        else:
            puzzle[r][c] = 0  
    session["puzzle"] = puzzle
    return redirect(url_for("index"))

@app.route("/solve")
def show_solution():
    session["puzzle"] = session["solution"]
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    full = generate_full_board()
    puzzle = make_puzzle(full)
    session["solution"] = full
    session["puzzle"] = puzzle
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

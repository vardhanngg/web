from flask import Flask, render_template, request

app = Flask(__name__)

# Function to print the matrix in a readable format
def printmatrix(m):
    l = len(m)
    matrix_str = ""
    for i in range(l):
        matrix_str += " ".join(map(str, m[i])) + "\n"
    return matrix_str

# Function to perform Gaussian elimination and calculate the determinant
def det(m, swaps):
    l = len(m)
    product = 1
    for i in range(l):
        product = product * m[i][i]
    product = product * ((-1) ** swaps)
    return product

# Function to perform Gaussian elimination
def gaus(m):
    l = len(m)
    e = 1
    x = []
    y = []  # dup for swapping if e = 0
    c = 0
    swap = 0
    for i in range(0, l):
        e = m[i][i]
        r = i + 1
        while e == 0:
            if c >= l:
                break
            c = c + 1
            while r < l:
                if m[r][i] != 0:
                    m[i], m[r] = m[r], m[i]
                    swap = r
                    e = m[i][i]
                r = r + 1
        for v in range(i, l - 1):
            x = []
            x.extend(m[i])
            for j in range(0, l):
                if e == 0:
                    break
                x[j] = x[j] / e  # converting to 1
            for k in range(l, 0, -1):
                e2 = m[v + 1][i]
                x[l - k] = x[l - k] * e2  # multiplying by 1st element of next row
            for k in range(0, l):
                m[v + 1][k] = m[v + 1][k] - x[k]  # subtraction
    return m, swap

# Function to calculate the rank of the matrix
def rank(m):
    l = len(m)
    rank = 0
    for i in range(l):
        count = 0
        for j in range(l):
            if m[i][j] != 0:
                count = count + 1
                break
        if count > 0:
            rank = rank + 1
    return rank

# Function to handle form submission and render results
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    determinant = None
    matrix_rank = None
    error_message = None
    matrix_display = None  # To hold formatted matrix
    if request.method == "POST":
        try:
            n = int(request.form["size"])  # Get matrix size
            # Get the matrix elements from the user (split by spaces)
            rows = [request.form[f"row{i+1}"].split() for i in range(n)]
            
            # Convert each row to integers
            rows = [[int(x) for x in row] for row in rows]
            
            # Perform Gaussian elimination and calculate determinant
            gau, swap = gaus(rows)
            determinant = det(gau, swap)
            matrix_rank = rank(gau)  # Calculate the rank
            result = gau
            matrix_display = printmatrix(gau)  # Use printmatrix to format the matrix output
        except Exception as e:
            error_message = str(e)  # Capture any errors that happen during the process

    return render_template(
        "index.html", 
        result=result, 
        determinant=determinant, 
        matrix_rank=matrix_rank, 
        error_message=error_message,
        matrix_display=matrix_display  # Pass formatted matrix to the HTML template
    )

if __name__ == "__main__":
    app.run(debug=True)

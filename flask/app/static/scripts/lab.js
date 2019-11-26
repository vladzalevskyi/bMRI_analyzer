function assignment_1() {
    alert("Sorry for the following questions, they are in the seek of completing assugnment. Besides it was probably you who came up with them. Answer honestly, pleaase :)")
    var marry_with = prompt("Ho do you want to marry to?", "yourself")
    var children_num = prompt("How many children do you expect to have", "15")

    alert("Well, my 'prediction' is  that you'll marry " + marry_with + " and you'll have " + children_num + " children. Thank you for playing")
}

function assignment_2() {
    var rows_num = prompt("Enter number of rows in triangle:", "10")
    var pascal_triangle = []
    for (var row = 0; row <= rows_num; row++) {
        var current_row = []
        current_row.push(1)
        for (var col = 1; col < row; col++) {
            current_row.push(pascal_triangle[row - 1][col - 1] + pascal_triangle[row - 1][col])
        }
        if (row >= 1) {
            current_row.push(1)
        }

        pascal_triangle.push(current_row)
    }

    prety_triangle = ""
    for (row of pascal_triangle) {
        for (var i = 0; i < rows_num - pascal_triangle.indexOf(row); i++) {
            prety_triangle += "\t\t"
        }
        for (col of row) {
            prety_triangle += col + "\t\t"
        }
        prety_triangle += "\n"
    }

    alert(prety_triangle)
}

function assignment_3() {
    var result = ""
    var exit = false

    for (var i = 50; i > 0; i--) {
        if (i == 1) {
            result += i + "bottle of beer on the wall\n" + i + " bottle of beer! \nTake one down, pass it around\n\n"
        } else {
            result += i + "bottles of beer on the wall\n" + i + " bottles of beer! \nTake one down, pass it around\n\n"
        }
        exit = confirm(result)
        if (!exit) {
            break
        }
    }
    result = result + "None has left :c"
    if (!exit) { confirm(result) }

}

function assignment_4() {
    var arr = [
        { value: 100, type: 'USD' },
        { value: 215, type: 'EUR' },
        { value: 7, type: 'EUR' },
        { value: 99, type: 'USD' },
        { value: 354, type: 'USD' },
        { value: 12, type: 'EUR' },
        { value: 77, type: 'USD' },
    ];


    var usd_100 = 0
    var euro_doubled = []

    for (curr of arr) {
        if ((curr.type == "USD") && (curr.value < 100)) {
            usd_100 += curr.value
        } else if (curr.type == "EUR") {
            euro_doubled.push({ value: curr.value * 2, type: curr.type })
        }
    }

    alert(usd_100)
    for (curr of euro_doubled) {
        alert(curr.type + " - " + curr.value)
    }
}

function start_game() {
    var play_next = true
    alert("Welcome to the 4th lab work assignment. Press Ok and choose the number of game you'd lie to play. To exit");
    //check for valid data and make a condition to exit from the main loop
    while (true) {
        var game_num = prompt("Choose game number:\n1)The psychic\n2)Pascal's triangle\n3)How many bottles on the wall\n4)How many money do you own\n\n(*to exit type anything except 1,2,3,4)", '')
        if ((game_num == "1") && (play_next == true)) {
            assignment_1()
            play_next = confirm("Wanna play more?")
        } else if ((game_num == "2") && (play_next == true)) {
            assignment_2()
            play_next = confirm("Wanna play more?")
        } else if ((game_num == "3") && (play_next == true)) {
            assignment_3()
            play_next = confirm("Wanna play more?")
        } else if ((game_num == "4") && (play_next == true)) {
            assignment_4()
            play_next = confirm("Wanna play more?")
        } else {
            break
        }
        if (play_next == false) {
            break
        }
    }

}
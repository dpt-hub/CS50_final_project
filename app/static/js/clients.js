// Sorting Table when clicking the column headers
let sortData = () => {
    // Select table in javascript
    let table = document.querySelector("#clientTable")
    // Select the column header row
    let columnRow = table.rows[0]
    for(let i = 1; i < columnRow.childElementCount; i++)
    {
        let sortingDirection = "ascending"
        console.log(table.rows.length)
        columnRow.children[i].addEventListener("click", () => {
            // Do the algorithm until all data is sorted
            
            let stillSorting = true;
            while(stillSorting)
            {
                stillSorting = false;
                for(let j = 1; j < table.rows.length - 1; j++)
                {
                    // Select a row of data
                    let rowOne = table.rows[j]
                    // Select the row after it
                    let rowTwo = table.rows[j + 1]
                    // Check if the first row of data's cell corresponding column header clicked is bigger than the second row's data cell
                    if (rowOne.children[i].innerText.toLowerCase() > rowTwo.children[i].innerText.toLowerCase() && sortingDirection == "ascending")
                    {
                        rowOne.parentNode.insertBefore(rowTwo, rowOne)
                        stillSorting = true;
                    }
                    else if (rowOne.children[i].innerText.toLowerCase() < rowTwo.children[i].innerText.toLowerCase() && sortingDirection == "descending")
                    {
                        rowOne.parentNode.insertBefore(rowTwo, rowOne)
                        stillSorting = true;
                    }
                }
            }
            for (let k = 1; k < columnRow.childElementCount; k++)
            {
                const arrow = document.querySelector(`#arrow${k}`)
                if (k === i && sortingDirection == "ascending")
                {
                    arrow.className = 'active-asc-arrow'
                }
                else if (k === i && sortingDirection == "descending")
                {
                    arrow.className = 'active-dsc-arrow'
                }
                else 
                {
                    arrow.className = 'inactive-arrow'
                }
            }
            if (sortingDirection == "ascending") 
            {
                
                sortingDirection = "descending"
            }
            else 
            {
                sortingDirection = "ascending"
            }
        })
    }
}

sortData();



let createClient = document.querySelector('#createClient')

createClient.addEventListener("click", () => {
    createClient.remove();
    let table = document.getElementById("clientTable");
    
    // Create a Form element that surrounds the table - method "POST"

    // Insert a new row and it's respective cells

    // Submit button to the form

    // Input type text - required
    
    let newRow = table.insertRow();
    let newForm = newRow.appendChild(document.createElement("FORM"))
    let confirmCell = newForm.insertCell(0)
    confirmCell.appendChild(document.createElement("INPUT"))
    let nameCell = newRow.insertCell(1)
    let typeCell = newRow.insertCell(2)
    let latCell = newRow.insertCell(3)
    let lonCell = newRow.insertCell(4)
}
)
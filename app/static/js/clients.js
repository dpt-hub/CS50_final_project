let sortData = () => {
    let table = document.querySelector("#clientTable")
    let columnRow = table.rows[0]
    for(let i = 1; i < columnRow.childElementCount; i++)
    {
        let sortingDirection = "ascending"
        columnRow.children[i].addEventListener("click", () => {
            
            let stillSorting = true;
            while(stillSorting)
            {
                stillSorting = false;
                for(let j = 1; j < table.rows.length - 1; j++)
                {
                    let rowOne = table.rows[j]
                    let rowTwo = table.rows[j + 1]
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

let selectAll = () => {
    let checkHeader = document.querySelector('#master');
    checkHeader.addEventListener("click", () => {
        
        clientChecks = document.querySelectorAll('.client-checkbox')
        if(checkHeader.checked) 
        {
            changeStatus(true, clientChecks)
        }
        else
        {
            changeStatus(false, clientChecks)
        }
    })
}

let changeStatus = (bool, Nodelist) => {
    for(let i = 0; i < Nodelist.length; i++) {
        Nodelist[i].checked = bool
    }
}

selectAll();

let addClient = () => {
    let createClient = document.querySelector('#createClient')

    createClient.addEventListener("click", () => {
        createClient.remove();
        let table = document.getElementById("clientTable");
        let newRow = table.insertRow();
        
        for(let i = 0; i < table.rows[0].childElementCount; i++)
        {
            if (i == 0) 
            {
                const submitButton = document.createElement("button");
                submitButton.className = "btn btn-success btn-sm"
                submitButton.type = "submit"
                submitButton.innerText = "✓"
                newCell = newRow.insertCell(i)
                newCell.appendChild(submitButton)
            }
            else
            {
                const newInput = document.createElement("input");
                newInput.className = ""
                newInput.placeholder = `Client's ${table.rows[0].children[i].innerText.toLowerCase()}`
                newInput.type = "text"
                newInput.setAttribute ('required', true)
                newInput.name = `${table.rows[0].children[i].innerText.toLowerCase()}`
                newCell = newRow.insertCell(i)
                newCell.appendChild(newInput);
            }
        }
    })
}

addClient();



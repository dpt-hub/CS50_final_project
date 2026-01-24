
(async function() {
    
    let data = {};
    let response = await fetch('fetch/visits');
    let visits = await response.json();
    let monthLabel = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for (let visit of visits)
    {
        tempObj = {};
        
        // Extract the year and month
        let year = new Date(visit["date"]).getFullYear();
        let month = monthLabel[new Date(visit["date"]).getMonth()];
        let dataExists = true;
        // Year doesn't exist?
        if (!data[year])
        {
            data[year] = {};
            dataExists = false;
        }
        // Month doens't exist?
        if (!data[year][month])
        {
            data[year][month] = {}
            dataExists = false;
        }
        
        if (dataExists)
        {
            data[year][month]["revenue"] += visit["order_value"];
            data[year][month]["visit_count"] += 1;
        }
        else
        {
            data[year][month]["revenue"] = visit["order_value"];
            data[year][month]["visit_count"] = 1;
        }
    }
    console.log(Object.keys(data))
    let select = document.querySelector('#year')
    let current_year = new Date().getFullYear()
    for (year of Object.keys(data))
    {
        if (year == current_year)
        {
            let option = document.createElement("option")
            option.innerText = year
            option.setAttribute('selected', true)
            select.appendChild(option)
        }
        else
        {
            let option = document.createElement("option")
            option.innerText = year
            select.appendChild(option)
        }
    }

    let revenue = []
    let visitCount = []

    for(let i = 0; i < monthLabel.length; i++)
    {
        try 
        {
            let obj = data[current_year][monthLabel[i]];
            revenue.push(obj["revenue"])
            visitCount.push(obj["visit_count"])
        } 
        catch {
            revenue.push(0)
            visitCount.push(0)
        }  
    }    

    revChart = new Chart(
        document.getElementById('revenue'),
        {
            type: 'bar',
            data: {
                labels: monthLabel,
                datasets: [
                    {
                    label: 'Revenue by month',
                    data: revenue,
                    borderColor: '#6afc27',
                    backgroundColor: '#6afc27b7',
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        ticks: {
                            callback: function(value) {
                                return '$ ' + value;
                            }
                        }
                    }
                }
            }
        }   
    );

    visChart = new Chart(
        document.getElementById('visits'),
        {
            type: 'bar',
            data: {
                labels: monthLabel,
                datasets: [
                    {
                    label: 'Visits by month',
                    data: visitCount,
                    borderColor: '#fd7e14',
                    backgroundColor: '#fc8727b7',
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        ticks: {
                            beginAtZero: true,
                            stepSize: 1
                        }
                    }
                }
            }
        }   
    );

    select.addEventListener("change", () => {
        let revenue = []
        let visitCount = []

        for(let i = 0; i < monthLabel.length; i++)
        {
            try 
            { 
                let obj = data[select.value][monthLabel[i]];
                revenue.push(obj["revenue"])
                visitCount.push(obj["visit_count"])
            } 
            catch {
                revenue.push(0)
                visitCount.push(0)
            }  
        }
        revChart.data.datasets[0].data = revenue;
        revChart.update();
        visChart.data.datasets[0].data = visitCount;
        visChart.update();
    })
})();



let sortData = () => {
    let table = document.querySelector("#visitTable")
    if (table)
    {
        let columnRow = table.rows[0]
        for(let i = 1; i < columnRow.childElementCount - 1; i++)
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
                for (let k = 1; k < columnRow.childElementCount - 1; k++)
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
    
}

sortData();

let checkboxLogic = () => {
    let mainCheckbox = document.querySelector('#master');
    if (mainCheckbox)
    {
        let allClientCheckbox = document.querySelectorAll('.visit-checkbox')
        let deleteClientBut = document.querySelector('#deleteVisitButton')
        let counter = 0;

        for (singleClientCheckbox of allClientCheckbox)
        {
            singleClientCheckbox.addEventListener("input", () => {
                counter = 0
                for (singleClientCheckbox of allClientCheckbox)
                {
                    if(singleClientCheckbox.checked)
                    {
                        counter++
                    }
                }
                if (counter == allClientCheckbox.length)
                {
                    mainCheckbox.checked = true
                }
                else 
                {
                    mainCheckbox.checked = false
                }
                changeDelButStatus(counter, deleteClientBut)
            })
        }

        mainCheckbox.addEventListener("click", () => {
        
        if(mainCheckbox.checked) 
        {
            changeStatus(true, allClientCheckbox)
            counter = allClientCheckbox.length
        }
        else
        {
            changeStatus(false, allClientCheckbox)
            counter = 0
        }
        changeDelButStatus(counter, deleteClientBut)
        })
    }
}
checkboxLogic();

let changeStatus = (bool, Nodelist) => {
    for(let i = 0; i < Nodelist.length; i++) {
        Nodelist[i].checked = bool
    }
}

let changeDelButStatus = (counter, button) => {
    if (counter == 0)
    {
        button.setAttribute('disabled', true)
    }
    else
    {
        button.removeAttribute('disabled')
    }
}

let confirmDeletion = () => {
    let deleteButton = document.querySelector('#confirmDeletionButton')
    if (deleteButton)
    {
        let deleteInput = document.querySelector('#confirmDeletion')
        deleteInput.addEventListener("input", () => {
        if (deleteInput.value == "DELETE")
        {
            deleteButton.removeAttribute('disabled')
        }
        else if (!deleteButton.hasAttribute('disabled'))
        {
            deleteButton.setAttribute('disabled', true)
        }
        })
    }
}

confirmDeletion();

let defaultDate = () => {
    const today = new Date();
    const yyyy = today.getFullYear();
    let mm = today.getMonth() + 1;
    let dd = today.getDate();

    if (dd < 10) dd = '0' + dd;
    if (mm < 10) mm = '0' + mm;

    const formattedToday = yyyy + '-' + mm + '-' + dd;
    const dateInput = document.querySelector('#date');
    dateInput.setAttribute('value', formattedToday)
    dateInput.setAttribute('max', formattedToday)
}

defaultDate();
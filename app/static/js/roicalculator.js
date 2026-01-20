let investmentCalculator = () => {
    
    // Grab relevant variables from features.html
    // Input variables
    let salespeopleInput = document.querySelector('#salespeopleInput');
    let aovInput = document.querySelector('#aovInput');
    // Output variables
    let salespeopleOutput = document.querySelector('#salespeopleOutput');
    let aovOutput = document.querySelector('#aovOutput');
    let gasSavingsOutput = document.querySelector('#gasSavings');
    let newRevenueOutput = document.querySelector('#newRevenue');
    let savedTimeOutput = document.querySelector('#timeSaved');

    // Set default values
    salespeopleOutput.textContent = salespeopleInput.value;
    gasSavingsOutput.textContent =  `$${salespeopleInput.value * 35}`;
    savedTimeOutput.textContent = `${salespeopleInput.value * 22} h`
    newRevenueOutput.textContent = `$${salespeopleInput.value * 1.5 * aovInput.value}`

    // Implementing changes into output values
    salespeopleInput.addEventListener('input', () => {
        salespeopleOutput.textContent = `${salespeopleInput.value}`;
        gasSavingsOutput.textContent =  `$${salespeopleInput.value * 35}`;
        savedTimeOutput.textContent = `${salespeopleInput.value * 22} h`;
        newRevenueOutput.textContent = `$${salespeopleInput.value * 1.5 * aovInput.value}`;
    });

    aovOutput.textContent = `$${aovInput.value}`;
    aovInput.addEventListener('input', () => {
        aovOutput.textContent = `$${aovInput.value}`;
        newRevenueOutput.textContent = `$${salespeopleInput.value * 1.5 * aovInput.value}`;
    });
}

investmentCalculator();
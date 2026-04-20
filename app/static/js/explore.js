const ctx = document.getElementById('scatterChart').getContext('2d');

let mode = 2; // 0 = Female, 1 = Male, 2 = Both

const data = {
    datasets: [
        {
            label: 'Female',
            data: femaleData,
            borderColor: 'red',
            backgroundColor: 'rgba(255,0,0,0.5)',
        },
        {
            label: 'Male',
            data: maleData,
            borderColor: 'orange',
            backgroundColor: 'rgba(255,165,0,0.5)',
        }
    ]
};

const config = {
    type: 'scatter',
    data: data,
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'BMI vs Weight by Gender'
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const point = context.raw;
                        return "Workout: " + point.label + " | Weight: " + point.x + ", BMI: " + point.y;
                    }
                }
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Weight'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'BMI'
                }
            }
        }
    }
};

const chart = new Chart(ctx, config);

const button = document.getElementById("toggleBtn");

button.addEventListener("click", function () {

    if (mode === 0) {
        // Female → Male
        chart.data.datasets[0].data = [];
        chart.data.datasets[1].data = maleData;
        mode = 1;
        button.innerText = "Show Both";

    } else if (mode === 1) {
        // Male → Both
        chart.data.datasets[0].data = femaleData;
        chart.data.datasets[1].data = maleData;
        mode = 2;
        button.innerText = "Show Female";

    } else {
        // Both → Female
        chart.data.datasets[0].data = femaleData;
        chart.data.datasets[1].data = [];
        mode = 0;
        button.innerText = "Show Male";
    }

    chart.update();
});
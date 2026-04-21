const ctx = document.getElementById('scatterChart').getContext('2d');

let mode = 2; // 0 = Female, 1 = Male, 2 = Both to Toggle Stuff

console.log("Male:", maleData);
console.log("Female:", femaleData);

const femaleLine = getLineOfBestFit(femaleData);
const maleLine = getLineOfBestFit(maleData);

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
        },
        {
            label: 'Female Best Fit',
            data: femaleLine,
            type: 'line',
            borderColor: 'darkred',
            borderWidth: 2,
            fill: false,
            pointRadius: 0
        },
        {
            label: 'Male Best Fit',
            data: maleLine,
            type: 'line',
            borderColor: 'darkorange',
            borderWidth: 2,
            fill: false,
            pointRadius: 0
        }
    ]
};

function getLineOfBestFit(data) {
    const n = data.length;

    if (n === 0) return [];

    let sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;

    data.forEach(p => {
        sumX += p.x;
        sumY += p.y;
        sumXY += p.x * p.y;
        sumX2 += p.x * p.x;
    });

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    // Get min and max x values to draw the line
    const xValues = data.map(p => p.x);
    const minX = Math.min(...xValues);
    const maxX = Math.max(...xValues);

    return [
        { x: minX, y: slope * minX + intercept },
        { x: maxX, y: slope * maxX + intercept }
    ];
}

const config = {
    type: 'scatter',
    data: data,
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Weight vs Age, Sorted by Gender'
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const point = context.raw;
                        return "Workout: " + point.label + " | Age: " + point.x + ", Weight: " + point.y;
                    }
                }
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Age'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Weight'
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
        chart.setDatasetVisibility(0, false);
        chart.setDatasetVisibility(2, false);

        chart.setDatasetVisibility(1, true);
        chart.setDatasetVisibility(3, true);

        mode = 1;
        button.innerText = "Show Both";

    } else if (mode === 1) {
        // Male → Both
        chart.setDatasetVisibility(0, true);
        chart.setDatasetVisibility(1, true);
        chart.setDatasetVisibility(2, true);
        chart.setDatasetVisibility(3, true);

        mode = 2;
        button.innerText = "Show Female";

    } else {
        // Both → Female
        chart.setDatasetVisibility(0, true);
        chart.setDatasetVisibility(2, true);

        chart.setDatasetVisibility(1, false);
        chart.setDatasetVisibility(3, false);

        mode = 0;
        button.innerText = "Show Male";
    }

    chart.update();
});
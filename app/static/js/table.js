import Chart from 'chart.js/auto'

(async function() {
  const data = {
  labels: [
    'Caloric Value',
    'Fat',
    'Saturated Fats',
    'Monounsaturated Fats',
    'Polynsaturated Fats',
    'Carbohydrates',
    'Sugars'
  ],
  datasets: [{
    label: 'My First Dataset',
    data: [65, 59, 90, 81, 56, 55, 40],
    fill: true,
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
    borderColor: 'rgb(255, 99, 132)',
    pointBackgroundColor: 'rgb(255, 99, 132)',
    pointBorderColor: '#fff',
    pointHoverBackgroundColor: '#fff',
    pointHoverBorderColor: 'rgb(255, 99, 132)'
  }]
};

  new Chart(
    document.getElementById('chart'),
    {
      type: 'radar',
      data: data,
      options: {
        elements: {
          line: {
            borderWidth: 3
          }
        }
      },
    };
  );
})();

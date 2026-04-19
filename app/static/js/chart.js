const data = {
    labels: ['Fat', 'Sugar', 'Protein', 'Fiber', 'Cholesterol'],
    datasets: [
      {
        label: 'Dataset 1',
        data: breakdown,
        backgroundColor: ['red', 'orange', 'yellow', 'green', 'blue']
      }
    ]
  };
  
  const config = {
      type: 'pie',
      data: data,
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Dietary Breakdown'
          }
        }
      },
  };
  
  const chrt = document.getElementById("foodNut");
  
  new Chart(chrt, config);
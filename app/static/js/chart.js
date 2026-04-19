

const data2 = {
    labels: ['Fat', 'Carbohydrates', 'Protein'],
    datasets: [
      {
        label: 'Dataset 2',
        data: [20, 55, 25],
        backgroundColor: ['red', 'orange', 'yellow']
      }
    ]
  };
  
  const config2 = {
      type: 'pie',
      data: data2,
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Healthy Calorie Distribution Estimate'
          }
        }
      },
  };
  
  const chrt2 = document.getElementById("good");
  
  new Chart(chrt2, config2);





const data = {
    labels: ['Fat','Cholesterol', 'Sugar', 'Fiber', 'Protein'],
    datasets: [
      {
        label: 'Dataset 1',
        data: breakdown,
        backgroundColor: ['red', '#C41E3A', 'orange', '#CC5500', 'yellow']
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
            text: 'Your Dietary Breakdown Today'
          }
        }
      },
  };
  
  const chrt = document.getElementById("foodNut");
  
  new Chart(chrt, config);


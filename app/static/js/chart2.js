const nmes = xcer.map(ex => ex.name)


const bubba = xcer.map((ex, i) => ({
    x: i,
    y: ex.reps,
    r: ex.cals
  }));

const data = {
    datasets: [
      {
        label: "Your exercises",
        data: bubba,
        backgroundColor: "rgba(50, 170, 120, 0.7)"
      }
    ]
};


const config = {
    type: 'bubble',
    data: data,
    options: {
      scales: {
        x: {
          ticks: {
            callback: function(value) {
              return nmes[value];
            }
          },
          title: {
            display: false,
            text: "Exercise Comparisons"
          }
        },
        y: {
          title: {
            display: true,
            text: "reps/min"
          }
        }
      }
    }
  };

new Chart(document.getElementById("exes"), config);
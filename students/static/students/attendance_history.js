var temp_present_dates = present_dates.sort((a, b) => a - b);
var temp_absent_dates = absent_dates.sort((a, b) => a - b);

window.onload = function() {
  displayDates();
}

function selectMonth(selectedDates, dateStr, instance) {
  const value = dateStr;
  const [month, year] = value.split("-").map(item => parseInt(item));
  if(value == '') {
    temp_present_dates = present_dates;
    temp_absent_dates = absent_dates;
  } else {
    temp_present_dates = present_dates.filter(date => date.getMonth() + 1 == month && date.getFullYear() == year);
    temp_absent_dates = absent_dates.filter(date => date.getMonth() + 1 == month && date.getFullYear() == year);
  }
  displayDates();
}

function displayDates() {
  document.querySelector('#present_dates_container').innerHTML = "";
  document.querySelector('#absent_dates_container').innerHTML = "";
  temp_present_dates.forEach(date => {
    const date_template = document.createElement("div");
    date_template.className = ("col-4 border d-flex justify-content-center align-items-center p-2");
    date_template.innerText = date.toLocaleDateString('en-GB');

    document.querySelector('#present_dates_container').appendChild(date_template);
  });

  temp_absent_dates.forEach(date => {
    const date_template = document.createElement("div");
    date_template.className = ("col-4 border d-flex justify-content-center align-items-center p-2");
    date_template.innerText = date.toLocaleDateString('en-GB');

    document.querySelector('#absent_dates_container').appendChild(date_template);
  });
}
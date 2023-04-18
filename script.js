const url = 'http://192.168.4.1/parameters'
const form = document.querySelector('form');
const powerbtns = document.querySelectorAll('input[type="radio"][name="power"]');
const heatbtns = document.querySelectorAll('input[type="radio"][name="heat"]');
const otherbtns = Array.prototype.slice.call(document.querySelectorAll('input'), 2);
const offbtns = document.querySelectorAll('input[value="off"]');
const temperature_input = document.getElementById('temperature_input');
const temperature_placeholder = document.getElementById('temperature_placeholder');
function showAlert(message, type) {
  var alert = document.getElementById("alert");
  var alertMessage = document.getElementById("alert-message");
  alertMessage.innerHTML = message;
  alert.classList.add("alert-" + type);
  alert.classList.add("show");
  setTimeout(function() {
    alert.classList.remove("show");
    alert.classList.remove("alert-" + type)
  }, 5000);
}
function getCheckedRadioValue(name) {
  const selectedRadio = document.querySelector(`input[name="${name}"]:checked`);
  if (selectedRadio) {
    return selectedRadio.value;
  }
  return null;
}
function getParametersFromRadioButtons() {
  const parameters = {
    shoulder: '',
    heat: '',
    thighs: '',
    power: '',
    arms: '',
    lumber: '',
    temperature: temperature_input.value
  };
  for (const key in parameters) {
    if (key === "temperature") {
      continue;
    }
    const radioButtons = document.getElementsByName(key);
    for (const radioButton of radioButtons) {
      if (radioButton.checked) {
        parameters[key] = radioButton.value;
        break;
      }
    }
  }
  return parameters;
}
async function makeRequest(url, method = 'GET', data = null, headers = {}) {
  try {
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...headers
      },
      body: data && JSON.stringify(data)
    });
    const responseData = await response.json();
    return responseData;
  } catch (error) {
    console.error(error);
  }
}
async function setParameters(){
  try{
    const parameters = await makeRequest(url);
    const { temperature, heat, power, ...massagers } = parameters;
    for (const key in massagers) {
      const radioButtons = document.getElementsByName(key);
      for (const radioButton of radioButtons) {
        if (radioButton.value === massagers[key]) {
          radioButton.checked = true;
        }
      }
    }
    temperature_placeholder.innerText = temperature;
    temperature_input.value = temperature;
    if (power === 'off')  {
      powerbtns[0].checked = true;
    } else {
      powerbtns[1].checked = true;
    }
    if (heat === 'off')  {
      heatbtns[0].checked = true;
    } else {
      heatbtns[1].checked = true;
    }
    if (powerbtns[0].checked) {
      for (let i = 0; i < otherbtns.length; i++) {
        otherbtns[i].disabled = true;
      }
    }
  }
  catch (error){
    console.error(error);
  }
}
setParameters();
temperature_input.addEventListener('input', e => temperature_placeholder.innerText = e.target.value);
powerbtns.forEach(function (powerbtn) {
powerbtn.addEventListener('click', function () {
  if (this.value === 'off') {
    for (let i = 0; i < otherbtns.length; i++) {
      otherbtns[i].disabled = true;
    }
    offbtns.forEach(btn => btn.checked = true);
  } else if (this.value === 'on') {
    for (let i = 0; i < otherbtns.length; i++) {
      if (otherbtns[i].type !== 'range')
        otherbtns[i].disabled = false;
    }
  }
});
});
heatbtns.forEach(function (heatbtn) {
heatbtn.addEventListener('click', function () {
  if (this.value === 'off') {
    temperature_input.disabled = true;
  } else if (this.value === 'on') {
    temperature_input.disabled = false;
  }
});
});
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const parameters = getParametersFromRadioButtons();
  try {
    const response = await makeRequest(url, 'PUT', parameters);
    showAlert(response.msg, "success");
  } catch (error) {
    console.error(error);
    showAlert("There was an error. Retry or Restart the device", "danger");
  }
});
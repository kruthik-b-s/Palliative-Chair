const powerbtns = document.querySelectorAll('input[type="radio"][name="power"]');
const heatbtns = document.querySelectorAll('input[type="radio"][name="heat"]');
const otherbtns = Array.prototype.slice.call(document.querySelectorAll('input'), 2);
const offbtns = document.querySelectorAll('input[value="off"]');
const temperature_input = document.getElementById('temperature_input');
const temperature_placeholder = document.getElementById('temperature_placeholder');
temperature_placeholder.innerText = temperature_input.value;
temperature_input.addEventListener('input', e => temperature_placeholder.innerText = e.target.value);
if (powerbtns[0].checked) {
for (let i = 0; i < otherbtns.length; i++) {
  otherbtns[i].disabled = true;
}
}
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
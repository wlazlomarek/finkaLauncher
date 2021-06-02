function startUp() {
    testing();
    eel.check_network_adapter();
}
window.onload = startUp;

window.setInterval(function(){
    eel.check_network_adapter();
  }, 300 * 1000);

function running() {
    Swal.fire({
        html: 'Uruchamiam...',
        background: '#232331',
        timer: 2200,
        onBeforeOpen: () => {
            Swal.showLoading()
            timerInterval = setInterval(() => {
                Swal.getContent().querySelector('b')
                .textContent = Swal.getTimerLeft()
        }, 100)
      },
      onClose: () => {
        clearInterval(timerInterval)
      }
    })
}

function testing() {
    Swal.fire({
        html: 'Sprawdzam połączenie...',
        background: '#232331',
        timer: 4000,
        onBeforeOpen: () => {
            Swal.showLoading()
            timerInterval = setInterval(() => {
                Swal.getContent().querySelector('b')
                .textContent = Swal.getTimerLeft()
        }, 100)
      },
      onClose: () => {
        clearInterval(timerInterval)
      }
    })
}


eel.expose(network_adapter);
function network_adapter() {
    document.getElementById('ic-dot').style.background = 'red';
    document.getElementById('ss-dot').style.background = 'red';
    Swal.fire({
        type: 'error',
        title: 'Oops...',
        text: 'Nie jesteś podłączona do żadnej sieci WiFi lub kabel sieciowy został odłączony!',
        background: '#232331',
        confirmButtonColor: '#f27474',
        // buttonsStyling: false,
      })
}

eel.expose(change_color_red_ss_js);
function change_color_red_ss_js() {
    document.getElementById('ss-dot').style.background = 'red';
    Swal.fire({
        type: 'error',
        title: 'Oops...',
        text: 'Sprawdź czy serwer jest podłączony do prądu i sieci!',
        background: '#232331',
        confirmButtonColor: '#f27474',
        // buttonsStyling: false,
      })
}

eel.expose(change_color_red_ic_js);
function change_color_red_ic_js() {
    document.getElementById('ic-dot').style.background = 'red';
    Swal.fire({
        type: 'error',
        title: 'Oops...',
        text: 'Brak dostępu do internetu! Sprawdź połączenie internetowe.',
        background: '#232331',
        confirmButtonColor: '#f27474',
        // buttonsStyling: false,
      })
}

eel.expose(change_color_red_id_red_ss_one_not);
function change_color_red_id_red_ss_one_not() {
    document.getElementById('ic-dot').style.background = 'red';
    document.getElementById('ss-dot').style.background = 'red';
    Swal.fire({
        type: 'error',
        title: 'Oops...',
        text: 'Sprawdź połączenie internetowe oraz to czy serwer jest podłączony do prądu i sieci!',
        background: '#232331',
        confirmButtonColor: '#f27474',
      })
}

eel.expose(change_color_red_ic_green_ss_js_quite_not);
function change_color_red_ic_green_ss_js_quite_not() {
    document.getElementById('ic-dot').style.background = 'red';
    document.getElementById('ss-dot').style.background = 'greenyellow';
}

eel.expose(change_color_green_ic_js);
function change_color_green_ic_js() {
    document.getElementById('ic-dot').style.background = 'greenyellow';
}

eel.expose(change_color_green_ss_js);
function change_color_green_ss_js() {
    document.getElementById('ss-dot').style.background = 'greenyellow';
}

function startFinkaFK() {
    running();
    eel.finkaFK();
}

function startFinkaPLACE() {
    running();
    eel.finkaPLACE();
}

function startFinkaSTW() {
    running();
    eel.finkaSTW();
}

function startFinkaKPR() {
    running();
    eel.finkaKPR();
}

function showLog() {
    eel.showLog();
}


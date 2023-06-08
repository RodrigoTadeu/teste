var checkbox = document.querySelector('#checkbox')
var container = document.querySelector('.container')

var address = document.querySelector('#address')
var broadcast = document.querySelector('#broadcast')
var netmask = document.querySelector('#netmask')
var gateway = document.querySelector('#gateway')
var dns = document.querySelector('#dns')

var formIp = document.querySelector('#formIp')

function isChecked() {
	if(container.style.display === 'block') {
		container.style.display = 'none';
	} else {
		container.style.display = 'block';
	}
}
if (formIp) {

formIp.addEventListener('submit', (event) => {
    event.preventDefault();

    const enderecoAddress = address.value;
    const enderecoBroadcast = broadcast.value;
    const enderecoNetmask = netmask.value;
    const enderecoGateway = gateway.value;
    const enderecoDns = dns.value;

    if (!validarEnderecoIp(enderecoAddress) || !validarEnderecoIp(enderecoBroadcast) || !validarEnderecoIp(enderecoNetmask) || !validarEnderecoIp(enderecoGateway) || !validarEnderecoIp(enderecoDns)) {
      alert("Informação inválida")
      return;
    } else {
      formIp.submit();
    }
  });
}

function validarEnderecoIp(enderecoIp) {
    const partes = enderecoIp.split('.');

    if (partes.length !== 4) {
      return false;
    }

    for (let i = 0; i < partes.length; i++) {
      const parte = parseInt(partes[i]);

      if (isNaN(parte) || parte < 0 || parte > 255) {
        return false;
      }
    }

    return true;
  }

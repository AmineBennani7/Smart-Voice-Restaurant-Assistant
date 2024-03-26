export const phoneNumberPattern = /^\d{9}$/;

export const validateEmail = (email) => {
  const re = /\S+@\S+\.\S+/;
  return re.test(email);
};

export const validateFormData = (formData) => {
  if (!formData || typeof formData !== 'object') {
    console.error('formData is not valid');
    return false;
  }

  const { fullname, lastname, username, email, password, phone } = formData;

  if (!fullname || !fullname.trim()) {
    alert('Por favor ingresa tu nombre');
    return false;
  }
  if (!lastname || !lastname.trim()) {
    alert('Por favor ingresa tu apellido');
    return false;
  }
  if (!username || !username.trim()) {
    alert('Por favor ingresa un nombre de usuario');
    return false;
  }
  if (!email || !email.trim()) {
    alert('Por favor ingresa tu correo electrónico');
    return false;
  }
  if (!validateEmail(email.trim())) {
    alert('Por favor ingresa un correo electrónico válido');
    return false;
  }
  if (!password || !password.trim()) {
    alert('Por favor ingresa una contraseña');
    return false;
  }
  if (password.length < 8) {
    alert('La contraseña debe tener al menos 8 caracteres');
    return false;
  }
  if (!phone || !phone.trim()) {
    alert('Por favor ingresa tu número de teléfono');
    return false;
  }
  if (!phoneNumberPattern.test(phone.trim())) {
    alert('Por favor ingresa un número de teléfono válido (9 dígitos sin espacios ni guiones)');
    return false;
  }
  return true;
};
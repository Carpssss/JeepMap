document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const emailInput = form.querySelector('input[name="username"]');
  const passwordInput = form.querySelector('input[name="password"]');
  const loginBtn = form.querySelector('button[type="submit"]');
  const errorDiv = document.getElementById("client-error");

  function validate() {
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();
    const isValid = email && password;
    loginBtn.disabled = !isValid;
    if (isValid) {
      errorDiv.textContent = "";
      loginBtn.style.backgroundColor = "";
      loginBtn.style.cursor = "pointer";
    } else {
      loginBtn.style.backgroundColor = "#936A1A";
      loginBtn.style.cursor = "not-allowed";
    }
  }

  emailInput.addEventListener("input", validate);
  passwordInput.addEventListener("input", validate);

  form.addEventListener("submit", function (e) {
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();
    if (!email || !password) {
      e.preventDefault();
      errorDiv.textContent = "Both email and password are required.";
    }
  });

  // Initial state
  validate();
});

const passwordInput = document.getElementById("password-input");
const toggleBtn = document.getElementById("toggle-password");
const eyeIcon = document.getElementById("eye-icon");
let visible = false;

toggleBtn.addEventListener("click", function () {
  visible = !visible;
  passwordInput.type = visible ? "text" : "password";
  eyeIcon.src = visible
    ? toggleBtn.dataset.openeye
    : toggleBtn.dataset.closedeye;
  eyeIcon.alt = visible ? "Hide password" : "Show password";
});

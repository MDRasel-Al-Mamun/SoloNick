const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector('.usernameFeedBackArea');
const emailField = document.querySelector('#emailField');
const emailFeedBackArea = document.querySelector('.emailFeedBackArea');


usernameField.addEventListener('keyup', (e) => {
  const usernameVal = e.target.value;
  usernameField.classList.remove('has-error');
  feedBackArea.style.display = 'none';
  if (usernameVal.length > 0) {
    fetch('/authentication/validate_username', {
      body: JSON.stringify({ username: usernameVal }),
      method: 'POST',
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.username_error) {
          usernameField.classList.add('has-error');
          feedBackArea.style.display = 'block';
          feedBackArea.innerHTML = `<p style="text-align:left;color:#dc3545";>${data.username_error}</p>`;
        }
      });
  }
});


emailField.addEventListener('keyup', (e) => {
  const emailVal = e.target.value;
  emailField.classList.remove('has-error');
  emailFeedBackArea.style.display = 'none';
  if (emailVal.length > 0) {
    fetch('/authentication/validate_email', {
      body: JSON.stringify({ email: emailVal }),
      method: 'POST',
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_error) {
          emailField.classList.add('has-error');
          emailFeedBackArea.style.display = 'block';
          emailFeedBackArea.innerHTML = `<p style="text-align:left;color:#dc3545";>${data.email_error}</p>`;
        }
      });
  }
});
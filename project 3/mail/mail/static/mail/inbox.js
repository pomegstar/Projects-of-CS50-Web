document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});


function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function send_email(event) {
  event.preventDefault();
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      load_mailbox('sent');
  });
}


function load_mailbox(mailbox) {
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view').style.display = 'none';
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      emails.forEach(semail => {
        const element = document.createElement('div');
        element.innerHTML = `
        <h5>${semail.sender}</h5>
        <h6>${semail.subject}</h6>
        <p>${semail.timestamp}</p>
        `;
        element.className = semail.read ? "read" : "unread";

        element.addEventListener('click', function() {
            console.log('This element has been clicked!');
            view_email(semail.id, mailbox)
        });
        document.querySelector('#emails-view').append(element);
      });
  });

}


function view_email(id, mailbox) {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#view').style.display = 'block';


    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
    fetch(`/emails/${id}`)
            .then(response => response.json())
            .then(email => {
                const e_view = document.querySelector('#view');
                if (mailbox !== 'sent') {
                      if (!email.archived) {
                        e_view.innerHTML = `
                        <h6><strong>From:</strong> ${email.sender}</h6>
                        <h6><strong>To:</strong> ${email.recipients}</h6>
                        <h6><strong>Subject:</strong> ${email.subject}</h6>
                        <h6><strong>Timestamp:</strong> ${email.timestamp}</h6>
                        <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
                        <button class="btn btn-sm btn-outline-primary" id="arch">Archive</button>
                        <hr>
                        <pre>${email.body}</pre>
                        `;
                        document.querySelector('#reply').addEventListener('click', () => reply(id));
                        document.querySelector('#arch').addEventListener('click', () => archive_email(id));
                    }
                    else {
                        e_view.innerHTML = `
                        <h6><strong>From:</strong> ${email.sender}</h6>
                        <h6><strong>To:</strong> ${email.recipients}</h6>
                        <h6><strong>Subject:</strong> ${email.subject}</h6>
                        <h6><strong>Timestamp:</strong> ${email.timestamp}</h6>
                        <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
                        <button class="btn btn-sm btn-outline-primary" id="unarch">Unarchive</button>
                        <hr>
                        <pre>${email.body}</pre>
                        `;
                        document.querySelector('#reply').addEventListener('click', () => reply(id));
                        document.querySelector('#unarch').addEventListener('click', () => unarchive_email(id));
                    }

                }
                else {
                  e_view.innerHTML = `
                  <h6><strong>From:</strong> ${email.sender}</h6>
                  <h6><strong>To:</strong> ${email.recipients}</h6>
                  <h6><strong>Subject:</strong> ${email.subject}</h6>
                  <h6><strong>Timestamp:</strong> ${email.timestamp}</h6>
                  <hr>
                  <pre>${email.body}</pre>
                  `;
                }
            });
}


function archive_email(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: true
    })
  })
  load_mailbox('inbox');
}


function unarchive_email(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  load_mailbox('inbox');
}


function reply(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#view').style.display = 'none';

  fetch(`/emails/${id}`)
            .then(response => response.json())
            .then(email => {
                document.querySelector('#compose-recipients').value = email.sender;
                let subject = email.subject;
                if (!subject.startsWith("Re:")) {
                  subject = `Re: ${email.subject}`
                }
                document.querySelector('#compose-subject').value = subject;

                document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: \n${email.body}\n\n`;

            });
}

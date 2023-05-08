const addFBtns = document.querySelectorAll('.add-f-btn');
addFBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    let groupName = "this group"
    const friendName = prompt(`Enter the name of your friend to add to ${groupName}:`);
    if (friendName) {
      const form = btn.parentNode;
      const input = form.querySelector('.form-text');
      input.value = friendName;
      console.log("sf")
      input.name = "name"
      form.submit();
    }
  });
});

const addGroupBtn = document.querySelector('#addGroupBtn');
const addGroupForm = document.querySelector('#addGroupForm');
addGroupBtn.addEventListener('click', () => {
  addGroupForm.style.display = 'block';
  const groupsList = document.querySelector('#groupsList');
  const addButtonLi = groupsList.querySelector('.add-form').parentNode;
  groupsList.removeChild(addButtonLi);
});

const addForms = document.querySelectorAll('.add-form');
addForms.forEach(form => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const input = form.querySelector('input[type=text]');
    const formData = new FormData(form);
    fetch(form.action, {
      method: 'POST',
      body: formData
    })
      .then(response => response.text())
      .then(html => {
        const listItem = input.parentNode;
        const list = listItem.parentNode;
        const newListItem = document.createElement('li');
        newListItem.innerHTML = html.trim();
        list.insertBefore(newListItem, listItem.nextSibling);
        input.value = '';
      })
      .catch(error => console.error(error))
      .finally(() => {
        const groupsList = document.querySelector('#groupsList');
        const addButtonLi = groupsList.querySelector('.add-form').parentNode;
        groupsList.appendChild(addButtonLi);
      });
  });
});

const addFriendBtn = document.querySelector('#addFriendBtn');
        const addFriendForm = document.querySelector('#addFriendForm');
        addFriendBtn.addEventListener('click', () => {
          addFriendForm.style.display = 'block';
          const friendsList = document.querySelector('#friendsList');
          const addButtonLi = friendsList.querySelector('.add-form').parentNode;
          groupsList.removeChild(addButtonLi);
        });

        const addForms1 = document.querySelectorAll('.add-form');
        addForms1.forEach(form => {
          form.addEventListener('submit', (event) => {
            event.preventDefault();
            const input = form.querySelector('input[type=text]');
            const formData = new FormData(form);
            fetch(form.action, {
              method: 'POST',
              body: formData
            })
              .then(response => response.text())
              .then(html => {
                const listItem = input.parentNode;
                const list = listItem.parentNode;
                const newListItem = document.createElement('li');
                newListItem.innerHTML = html.trim();
                list.insertBefore(newListItem, listItem.nextSibling);
                input.value = '';
              })
              .catch(error => console.error(error))
              .finally(() => {
                const friendsList = document.querySelector('#friendsList');
                const addButtonLi = friendsList.querySelector('.add-form').parentNode;
                friendsList.appendChild(addButtonLi);
              });
          });
        });

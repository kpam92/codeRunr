document.addEventListener('DOMContentLoaded', () => {
  let myCodeMirror = CodeMirror(document.getElementById('editor'), {
    mode: "javascript",
    lineNumbers: true,
    autoCloseBrackets: true
  });
  window.myCodeMirror = myCodeMirror;
  let windowHeight = window.innerHeight - 65;
  let editor = document.getElementById('editor');
  let output = document.getElementById('output');
  if (editor) {
    editor.style.height = `${windowHeight}px`;
    output.style.height = `${windowHeight}px`;
    let ulHeight = windowHeight - 156;
    document.getElementById('menu').children[2].style.height = `${ulHeight}px`;
    let runButton = document.getElementById('run');
    let saveButton = document.getElementById('save');
    let newButton = document.getElementById('new');
    runButton.addEventListener('click', () => run());
    saveButton.addEventListener('click', () => save());
    newButton.addEventListener('click', () => newDoc());
  }
});


function run() {
  let code = myCodeMirror.getValue();
  let value = eval(code);
  let output = document.getElementById('output');
  output.children[0].innerHTML = value;
}

function save() {
  let title = document.getElementById('code-name-input').value
  if (window.openDoc) {
    let value = myCodeMirror.getValue();
    $.ajax({
      type: 'PATCH',
      url: '/editCode',
      data: {
        'value': value,
        'id': window.openDoc,
        'title': title
      },
    });
  } else {
    let value = myCodeMirror.getValue();
    $.ajax({
      type: 'POST',
      url: '/addCode',
      data: {
        'value': value,
        'title': title
      },
    });
  }
}

function newDoc () {
  window.openDoc = null;
  myCodeMirror.setValue('');
}


function guestSignOn() {
  document.getElementById('login-username').value = 'guest';
  document.getElementById('login-password').value = 'password';
  document.getElementById('login-submit').click();
}


function receiveCode(id) {
  $.ajax({
    type: 'GET',
    url: '/getCode',
    data: {
      'id': id
    },
    success: (code) => {
      [title, code] = code.split('/~=^md');
      myCodeMirror.setValue(code)
      document.getElementById('code-name-input').value = title
      window.openDoc = id
    }
  });
}

function renameCode(id) {
  $.ajax({
    type: 'GET'
  })
}

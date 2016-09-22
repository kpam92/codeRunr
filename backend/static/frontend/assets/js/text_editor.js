document.addEventListener('DOMContentLoaded', () => {
  let myCodeMirror = CodeMirror(document.getElementById('editor'), {
    mode: "javascript",
    lineNumbers: true,
    autoCloseBrackets: true
  });
  window.myCodeMirror = myCodeMirror;
  let windowHeight = window.innerHeight - 20;
  let editor = document.getElementById('editor')
  let output = document.getElementById('output')
  if (editor) {
    editor.style.height = `${windowHeight}px`;
    output.style.height = `${windowHeight}px`;
    let runButton = document.getElementById('run');
    let saveButton = document.getElementById('save');
    let saveTitle = document.getElementById('saveTitle')
    let newButton = document.getElementById('new');
    document.getElementById('code-name').addEventListener('click', () => {
      showTitleInput();
    })
    runButton.addEventListener('click', () => run())
    saveButton.addEventListener('click', () => save())
    saveTitle.addEventListener('click', (e) => titleSave(e))
    newButton.addEventListener('click', () => newDoc())
  }
});


function run() {
  let code = myCodeMirror.getValue();
  let value = eval(code);
  let output = document.getElementById('output');
  output.children[0].innerHTML = value;
}

function showTitleInput() {
  dcument.getElementById('code-name-form').style.display = 'block';
}

function save() {
  if (window.openDoc) {
    let value = myCodeMirror.getValue();
    $.ajax({
      type: 'PATCH',
      url: '/editCode',
      data: {
        'value': value,
        'id': window.openDoc
      },
    });
  } else {
    let value = myCodeMirror.getValue();
    $.ajax({
      type: 'POST',
      url: '/addCode',
      data: {
        'value': value
      },
    });
  }
}

function titleSave(e) {
  document.getElementById('code-name-editor').style.display = 'block';
  value = document.getElementById('code-name-input').value
  $.ajax({
    type: 'PATCH',
    url: '/editTitle',
    data: {
      'title': value,
      'id': window.openDoc
    }
  });
};

function newDoc () {
  window.openDoc = null;
  myCodeMirror.setValue('');
}


function receiveCode(id) {
  $.ajax({
    type: 'GET',
    url: '/getCode',
    data: {id},
    success: (code) => {
      [title, code] = code.split('/~=^md');
      myCodeMirror.setValue(code)
      document.getElementById('code-name').innerHTML = title;
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

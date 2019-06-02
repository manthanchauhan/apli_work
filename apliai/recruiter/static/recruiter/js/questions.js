if ( window.history.replaceState ) {

    window.history.replaceState( null, null, window.location.href );
  
  }

const fills = document.querySelectorAll('.fill');
const empties = document.querySelectorAll('.empty');
for (const fill of fills) {
    // Fill listeners
    fill.addEventListener('dragstart', dragStart);
    fill.addEventListener('dragend', dragEnd);
}
// Loop through empty boxes and add listeners
for (const empty of empties) {
    empty.addEventListener('dragover', dragOver);
    empty.addEventListener('dragenter', dragEnter);
    empty.addEventListener('dragleave', dragLeave);
    empty.addEventListener('drop', dragDrop);
}

// Drag Functions

function dragStart() {
    // this.className += ' hold';
    console.log('dragstart');
    event.dataTransfer.setData("Text", event.target.id);

    // setTimeout(() => (this.className = 'invisible'), 0);
}

function dragEnd() {
    console.log('dragend');

    //  this.className = 'fill';

}

function dragOver(e) {
    console.log('dragover');

    e.preventDefault();
}

function dragEnter(e) {
    console.log('dragenter');

    e.preventDefault();
    //this.className += ' hovered';
}

function dragLeave() {
    console.log('dragleave');

    // this.className = 'empty';
}

function dragDrop(event,el) {
    console.log('dragdrop', event,el);
    var data = event.dataTransfer.getData("Text");
    console.log(data)
    // this.className = 'empty';
    sourcenode = document.getElementById(data);
    appendnode = sourcenode.cloneNode(true);
    appendnode.setAttribute('id', 'q' + data);
    this.appendChild(appendnode);

}
$("#sortable").sortable();
$("#sortable").disableSelection();
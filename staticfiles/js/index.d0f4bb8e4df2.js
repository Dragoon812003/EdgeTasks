// Add Tasks Hide and Show

const addToDo = document.getElementById("add-todo")
const addToDoButton = document.getElementById("add-todo-button")
const addTaskCancel = document.getElementById("add-task-cancel")
const addTaskTitle = document.getElementById("add-task-title")

addToDoButton.addEventListener('click', function() {
    addToDo.classList.remove("hidden")
    addToDoButton.classList.add("hidden")
})

addTaskCancel.addEventListener('click', function () {
    addToDo.classList.add("hidden")
    addToDoButton.classList.remove("hidden")
})

//Priority Select Option
const prioritySelect = document.getElementById("priority-select")
prioritySelect.addEventListener('change', (e)=> {
    optionTarget = document.getElementById(toString(prioritySelect.value))
    prioritySelect.classList.remove("priority-4")
    prioritySelect.classList.remove("priority-3")
    prioritySelect.classList.remove("priority-2")
    prioritySelect.classList.remove("priority-1")
    prioritySelect.classList.add(prioritySelect.value)
})

